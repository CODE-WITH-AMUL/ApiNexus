from django.urls import path
from .views import *
from api.views import *

urlpatterns = [
    path('home/', home, name='home'),
    path('', index, name='index'),
    path('document/', document, name='document')
]
