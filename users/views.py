from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.http import HttpResponseRedirect

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import MarketUser
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

class UserListView(generic.ListView):
    model = MarketUser

class UserDetailView(generic.DetailView):
    model = MarketUser

# class UpdateUser(generic.UpdateView):
#     model = MarketUser
#     form_class = CustomUserChangeForm
#     success_url = reverse_lazy('login')
#     template_name = 'update_user.html'

def view_user_info(request):

    return render(request, 'view_user_info.html')

def update_user(request):

    user = request.user
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect(reverse('view-user'))
    else:
        form = CustomUserChangeForm(instance=user)
    context = {
        'form': form,
    }
    return render(request, 'update_user.html', context)

def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            #login(request, request.user)
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect(reverse('view-user'))
    else:
        form = PasswordChangeForm(user=request.user)

    for field in form.fields.values():
        field.help_text = None

    context = {
        'form': form,
         }

    return render(request, 'update_password.html', context)
