from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('register/', views.register_request, name='register'),
    path('account/', views.accountView, name='accountView'),
]
