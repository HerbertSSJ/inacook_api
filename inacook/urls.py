from django.contrib import admin
from django.urls import path
from inacook.views import (ListaIngredientes, DetalleIngrediente,ListaRoles,DetalleRol, ListaUnidadMedicion, DetalleUnidadMedicion)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('ingredientes/', ListaIngredientes.as_view()),
    path('ingredientes/<int:id>/', DetalleIngrediente.as_view()),
    path('roles/',ListaRoles.as_view()),
    path('roles/<int:id>/', DetalleRol.as_view()),
    path('unidades/', ListaUnidadMedicion.as_view()),
    path('unidades/<int:id>/', DetalleUnidadMedicion.as_view()),
]
