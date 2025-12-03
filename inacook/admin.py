from django.contrib import admin
from .models import rol, usuario, unidadmedicion, ingrediente, receta, receta_ingrediente, comprobante, historial

# Register your models here.
admin.site.register(rol)
admin.site.register(usuario)
admin.site.register(unidadmedicion)
admin.site.register(ingrediente)
admin.site.register(receta)
admin.site.register(receta_ingrediente)
admin.site.register(comprobante)
admin.site.register(historial)