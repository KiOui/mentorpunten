import base64
import hashlib

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView


class IndexView(TemplateView):
    """Index view."""

    template_name = "mentorpunten/index.html"

    def get(self, request, **kwargs):
        """GET request for IndexView."""
        return render(request, self.template_name)
