from rest_framework import serializers
from inacook.models import rol, usuario, unidadmedicion, ingrediente, receta_ingrediente


class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = rol
        fields = '__all__'


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = usuario
        fields = '__all__'


class UnidadmedicionSerializer(serializers.ModelSerializer):
    class Meta:
        model = unidadmedicion
        fields = '__all__'


class IngredienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ingrediente
        fields = '__all__'


class RecetaIngredienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = receta_ingrediente
        fields = '__all__'
