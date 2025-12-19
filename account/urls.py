from django.urls import path
from .views import login_view, register, logout_view, forgotpass

urlpatterns = [
path('login/', login_view, name='login'),
path('register/', register, name='register'),
path('forgot-password/', forgotpass, name='forgotpass'),

]
