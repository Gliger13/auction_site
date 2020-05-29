from django.urls import path

from lots import views

urlpatterns = [
    path('create/', views.create),
    path('page/', views.page)
]
