from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import (Rol, UnidadMedicion, Ingrediente, Receta, Comprobante, Historial)
from .serializers import (
    IngredienteSerializer, 
    RecetaSerializer, 
    ComprobanteSerializer, 
    HistorialSerializer,
    RolSerializer,
    UnidadMedicionSerializer
)
#Ingredientes (Lista y crea)
class ListaIngredientes(APIView):

    def get(self, request):
        ingredientes=Ingrediente.objects.all()
        serializer=IngredienteSerializer(ingredientes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer=IngredienteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DetalleIngrediente(APIView):

    def get_object(self, id):
        try:
            return Ingrediente.objects.get(id=id)
        except Ingrediente.DoesNotExist:
            return None

    def get(self, request, id):
        ingrediente=self.get_object(id)
        if not ingrediente:
            return Response({"error": "Ingrediente no encontrado"}, status=404)

        serializer=IngredienteSerializer(ingrediente)
        return Response(serializer.data)

    def put(self, request, id):
        ingrediente=self.get_object(id)
        if not ingrediente:
            return Response({"error": "Ingrediente no encontrado"}, status=404)

        serializer=IngredienteSerializer(ingrediente, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id):
        ingrediente=self.get_object(id)
        if not ingrediente:
            return Response({"error": "Ingrediente no encontrado"}, status=404)

        ingrediente.delete()
        return Response({"mensaje": "Ingrediente eliminado"}, status=204)

class ListaRoles(APIView):
    def get(self, request):
        roles = Rol.objects.all()
        serializer = RolSerializer(roles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RolSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetalleRol(APIView):
    def get_object(self, id):
        try:
            return Rol.objects.get(id=id)
        except Rol.DoesNotExist:
            return None

    def get(self, request, id):
        rol = self.get_object(id)
        if not rol:
            return Response({"error": "Rol no encontrado"}, status=404)
        serializer = RolSerializer(rol)
        return Response(serializer.data)

    def put(self, request, id):
        rol = self.get_object(id)
        if not rol:
            return Response({"error": "Rol no encontrado"}, status=404)
        serializer = RolSerializer(rol, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id):
        rol = self.get_object(id)
        if not rol:
            return Response({"error": "Rol no encontrado"}, status=404)
        rol.delete()
        return Response({"mensaje": "Rol eliminado"}, status=204)


class ListaUnidadMedicion(APIView):
    def get(self, request):
        unidades = UnidadMedicion.objects.all()
        serializer = UnidadMedicionSerializer(unidades, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UnidadMedicionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetalleUnidadMedicion(APIView):
    def get_object(self, id):
        try:
            return UnidadMedicion.objects.get(id=id)
        except UnidadMedicion.DoesNotExist:
            return None

    def get(self, request, id):
        unidad = self.get_object(id)
        if not unidad:
            return Response({"error": "Unidad no encontrada"}, status=404)
        serializer = UnidadMedicionSerializer(unidad)
        return Response(serializer.data)

    def put(self, request, id):
        unidad = self.get_object(id)
        if not unidad:
            return Response({"error": "Unidad no encontrada"}, status=404)
        serializer = UnidadMedicionSerializer(unidad, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id):
        unidad = self.get_object(id)
        if not unidad:
            return Response({"error": "Unidad no encontrada"}, status=404)
        unidad.delete()
        return Response({"mensaje": "Unidad eliminada"}, status=204)
