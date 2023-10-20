from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.views import View
from django.urls import reverse_lazy
from accounts.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from accounts.forms import UserCreateForm, UserUpdateForm


from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

class Auth(View):
    def get(self, request):
        return render(request, 'accounts/login.html')
    
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('profile')
        else:
            messages.error(request, 'Invalid credentials.')
            return redirect('login')

class Logout(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'Logout successful.')
        return redirect('login')
        

class UserCreateView(CreateView):
    form_class = UserCreateForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('login')  # Redirect to login page after successful registration


class UserUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserUpdateForm
    template_name = 'accounts/user_form.html'
    
    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.object.pk})  # Redirect to user's profile page after successful update

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if not obj.id == self.request.user.id:  # Ensure users can only update their own profile
            raise PermissionDenied()
        return obj
