from django.urls import path

from users import views

urlpatterns = [
    path('register/', views.register),
    path('logout/', views.logout_user),
    path('login/', views.login),
]
