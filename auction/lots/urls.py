from django.urls import path

from lots import views

urlpatterns = [
    path('create/', views.create),
    path('page/<int:num>', views.page),
    path('lot/<int:lot_id>', views.lot),
]
