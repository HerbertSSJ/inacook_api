from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('ver-recetas/', views.ver_recetas, name='ver_recetas'),
    path('ver-ingredientes/', views.ver_ingredientes, name='ver_ingredientes'),
    path('ver-historial/', views.ver_historial, name='ver_historial'),
    path('editar-receta/<int:id>/', views.editar_receta, name='editar_receta'),
]   