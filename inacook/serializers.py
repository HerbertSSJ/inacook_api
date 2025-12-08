from rest_framework import serializers
from inacook.models import (
    Rol, 
    Usuario, 
    UnidadMedicion, 
    Ingrediente, 
    Receta_Ingrediente, 
    Receta, 
    Historial, 
    Comprobante
)


class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'


class UnidadMedicionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadMedicion
        fields = '__all__'


class IngredienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingrediente
        fields = '__all__'


class RecetaIngredienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receta_Ingrediente
        fields = '__all__'

class RecetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receta
        fields = '__all__'

class ComprobanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comprobante
        fields = '__all__'

class HistorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Historial
        fields = '__all__'