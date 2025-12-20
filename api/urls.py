from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('', views.home, name='home'),
    path('api/<slug:slug>/', views.APIDetailView.as_view(), name='detail'),
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('tags/', views.TagListView.as_view(), name='tags'),
    path('category/<slug:slug>/', views.home, name='category'),
    path('tag/<slug:slug>/', views.home, name='tag'),
]