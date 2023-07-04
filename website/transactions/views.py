from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from transactions.models import Account
