from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Email used as username
        user = authenticate(
            request,
            username=email,
            password=password
        )

        if user is not None:
            auth_login(request, user)
            return redirect("/home/")
        else:
            messages.error(request, "Invalid email or password")
            return redirect("/login/")

    return render(request, "accounts/login.html")


def register(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confrom_password")

        # Validation
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("/register/")

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already exists")
            return redirect("/register/")

        if len(password) < 6:
            messages.error(request, "Password must be at least 6 characters long")
            return redirect("/register/")

        # Create user
        user = User.objects.create_user(
            username=email,   # IMPORTANT
            email=email,
            password=password
        )

        auth_login(request, user)
        return redirect("/home/")

    return render(request, "accounts/register.html")


def logout_view(request):
    auth_logout(request)
    return redirect("/login/")


def forgotpass(request):
    return render(request, "accounts/forgotpassword.html")