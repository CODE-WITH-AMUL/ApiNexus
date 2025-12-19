from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.http import JsonResponse
from django.shortcuts import redirect

User = get_user_model()


def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(
            request,
            email=email,
            password=password
        )

        if user is not None:
            auth_login(request, user)
            return redirect('/home/')
        else:
            return JsonResponse({'message': 'Invalid email or password'}, status=401)

    return render(request, 'login.html')


def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            return JsonResponse({'message': 'Email already exists'}, status=400)

        user = User.objects.create_user(
            email=email,
            password=password
        )
        return redirect('/login/')

    return render(request, 'register.html')


def logout_view(request):
    auth_logout(request)
    return redirect('/login/')


def forgotpass(request):
    return render(request, 'forgotpassword.html')
