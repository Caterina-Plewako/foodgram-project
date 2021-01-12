from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CreationForm
from django.contrib.auth import login


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('index')
    template_name = 'registration/signup.html'

