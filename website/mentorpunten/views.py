from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.views.generic import TemplateView


class IndexView(TemplateView):
    """Index view."""

    template_name = "mentorpunten/index.html"

    def get(self, request, **kwargs):
        """GET request for IndexView."""
        return render(request, self.template_name)


class LogoutView(TemplateView):
    """Logout View."""

    def post(self, request, **kwargs):
        """POST request for Logout view."""
        logout(request)
        return redirect("/")
