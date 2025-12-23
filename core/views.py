from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required



def index(request):
	return render(request,'index.html')



def document(request):
    return render(request,'content/document.html')



def apis(request):
    return render(request, 'api.html')