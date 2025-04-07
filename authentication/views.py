from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})

def login_view(request):
    return render(request, 'login.html')

def signup_view(request):
    return render(request, 'signup.html')