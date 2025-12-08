from django.contrib import admin
from django.urls import path
from inacook.views import (
    ListaIngredientes, 
    DetalleIngrediente, 
    ListaReceta, 
    DetalleReceta,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('ingredientes/', ListaIngredientes.as_view()),
    path('ingredientes/<int:id>/', DetalleIngrediente.as_view()),
    path('recetas/', ListaReceta.as_view()),
    path('recetas/<int:id>/', DetalleReceta.as_view()),
]
