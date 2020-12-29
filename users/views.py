from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CreationForm
from django.http import HttpResponseRedirect
from django.contrib.auth import login


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('index')
    template_name = 'registration/signup.html'


# def sign_up(request):
#     if request.method == 'POST':
#         form = CreationForm(request.POST)
#         if user_form.is_valid():
#             new_user = form.save(commit=False)
#             new_user.set_password(form.cleaned_data['password'])
#             new_user.save()
#             return render(request, 'registration/login.html', {'new_user': new_user})
#     else:
#         form = CreationForm()
#     return render(request, 'registration/signup.html', {'form': form})
