from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

@login_required
def profile_view(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})

def login_view(request):
    return render(request, 'login.html')

def signup_view(request):
    return render(request, 'signup.html')

class CustomAdminLoginView(LoginView):
    template_name = 'admin/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return '/dashboard/'  # force it, ignoring ?next

class CustomPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('password_change_done')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.request.user
        if user.must_change_password:
            user.must_change_password = False
            user.save()
        return response

