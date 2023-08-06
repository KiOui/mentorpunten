from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import TemplateView


class LogoutView(TemplateView):
    """Logout View."""

    template_name = "users/logout.html"

    def get(self, request, **kwargs):
        """GET request."""
        next_url = request.GET.get("next", "/")
        if not request.user.is_authenticated:
            return redirect(next_url)

        back_url = request.GET.get("back", "/")
        next_url = request.GET.get("next", "/")
        return render(request, self.template_name, {"next": next_url, "back": back_url})

    def post(self, request, **kwargs):
        """POST request."""
        next_url = request.POST.get("next", "/")
        if not request.user.is_authenticated:
            return redirect(next_url)

        submit_value = request.POST.get("submit", None)
        if submit_value == 'Yes':
            logout(request)

        next_url = request.POST.get("next", "/")
        return redirect(next_url)
