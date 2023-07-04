from django.shortcuts import render, redirect
from django.views.generic import TemplateView


class LoginView(TemplateView):
    """Login View."""

    def get(self, request, **kwargs):
        """GET Login View."""
        return redirect()