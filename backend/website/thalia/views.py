import base64
import hashlib

from django.contrib.auth import get_user_model, login
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from django.utils.http import urlencode
from django.views.generic import TemplateView
from django.conf import settings
from oauthlib.oauth2 import WebApplicationClient
from requests_oauthlib import OAuth2Session

from thalia.models import AuthenticationRequest, ThaliaUser


User = get_user_model()


class LoginView(TemplateView):
    """Login View."""

    def get(self, request, **kwargs):
        """GET request for Login view."""
        if request.user.is_authenticated:
            return redirect("/")

        authentication_request = AuthenticationRequest.objects.create()

        client = WebApplicationClient(client_id=settings.THALIA_API_OAUTH_CLIENT_ID)

        code_verifier = authentication_request.challenge
        code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
        code_challenge = base64.urlsafe_b64encode(code_challenge).decode("utf-8")
        code_challenge = code_challenge.replace("=", "")

        authorization_url = client.prepare_request_uri(
            f"{settings.THALIA_API_BASE_URI}{settings.THALIA_API_AUTHORIZATION_ENDPOINT}",
            redirect_uri=settings.THALIA_API_OAUTH_REDIRECT_URI
            + "?"
            + urlencode({"next": request.GET.get("next")}),
            code_challenge=code_challenge,
            code_challenge_method="S256",
            state=authentication_request.state,
            scope=["profile:read"],
        )
        response = HttpResponseRedirect(authorization_url)
        response.set_cookie("state", authentication_request.state, max_age=300)
        return response


class CallbackView(TemplateView):
    """Callback for OAuth login view."""

    def get(self, request, **kwargs):
        """GET request."""
        code = request.GET.get("code", None)
        state_in_request = request.GET.get("state", None)
        state_in_cookie = request.COOKIES.get("state")
        if state_in_request != state_in_cookie:
            return HttpResponse(status=400)
        else:
            state = state_in_request

        try:
            authentication_request = AuthenticationRequest.objects.get(state=state)
        except AuthenticationRequest.DoesNotExist:
            return HttpResponse(status=404)

        client = WebApplicationClient(client_id=settings.THALIA_API_OAUTH_CLIENT_ID)

        oauth = OAuth2Session(
            client=client,
            redirect_uri=settings.THALIA_API_OAUTH_REDIRECT_URI
            + "?"
            + urlencode({"next": request.GET.get("next")}),
            scope=["profile:read"],
        )

        oauth.fetch_token(
            token_url=f"{settings.THALIA_API_BASE_URI}{settings.THALIA_API_ACCESS_TOKEN_ENDPOINT}",
            code=code,
            client_id=settings.THALIA_API_OAUTH_CLIENT_ID,
            client_secret=settings.THALIA_API_OAUTH_CLIENT_SECRET,
            code_verifier=authentication_request.challenge,
        )

        response = oauth.get(
            f"{settings.THALIA_API_BASE_URI}{settings.THALIA_API_MEMBERS_URL}"
        )
        if response.status_code != 200:
            return HttpResponse(status=500)

        member_data = response.json()
        thalia_identifier = member_data["pk"]
        thalia_display_name = member_data["profile"]["display_name"]
        photo = (
            member_data["profile"]["photo"]["medium"]
            if "photo" in member_data["profile"].keys()
            and "medium" in member_data["profile"]["photo"].keys()
            else None
        )

        try:
            thalia_user = ThaliaUser.objects.get(thalia_id=thalia_identifier)
        except ThaliaUser.DoesNotExist:
            user = User.objects.create_user(
                str(thalia_identifier), full_name=thalia_display_name
            )
            thalia_user = ThaliaUser.objects.create(
                thalia_id=thalia_identifier,
                user=user,
            )

        if thalia_user.user.profile_image != photo:
            thalia_user.user.profile_image = photo
            thalia_user.user.save()

        login(request, thalia_user.user)
        next_query = request.GET.get("next", None)
        if next_query is not None:
            return redirect(next_query)
        else:
            return redirect("/")
