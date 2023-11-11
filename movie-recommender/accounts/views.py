from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.views import View
from django.urls import reverse_lazy
from accounts.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
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
            return redirect('movies')
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
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')  # Redirect to login page after successful registration

    def get(self, request):
        #to avoid the rendering the default form
        return render(request, self.template_name)

    def post(self, request, *args,**kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            user = authenticate(request, email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            return redirect('movies')
        else:
            return render(request, self.template_name, {'form': form.errors})


class UserUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserUpdateForm
    template_name = 'accounts/profile.html'
    model = User
    
    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.object.pk})  # Redirect to user's profile page after successful update

    def get_object(self, queryset=None):
        print(self.request.user.id)
        return self.model.objects.get(id=self.request.user.id)
    
        obj = super().get_object(queryset=queryset)
        if not obj.id == self.request.user.id:  # Ensure users can only update their own profile
            raise PermissionDenied()
        return obj


def profile(request):
    return HttpResponse(f"Hi {request.user.name} 👋")