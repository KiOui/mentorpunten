from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.generic import TemplateView


class LogoutView(TemplateView):
    """Logout View."""

    def post(self, request, **kwargs):
        """POST request for Logout view."""
        logout(request)
        return redirect("/")
