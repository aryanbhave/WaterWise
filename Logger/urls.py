from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='logger-home'),
    path('about/', views.about, name='logger-about'),
    path('logging/', views.logging, name='logging'),
    path('data/', views.data, name='data')
]