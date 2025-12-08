from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import (Ingrediente, Receta, Comprobante, Historial)
from .serializers import (
    IngredienteSerializer, 
    RecetaSerializer, 
    ComprobanteSerializer, 
    HistorialSerializer
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

# recetas crear y listar
class ListaReceta(APIView):

    def get(self, request):
        recetas = Receta.objects.all()
        serializer = RecetaSerializer(recetas, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RecetaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# recetas detalle, actualizar y eliminar
class DetalleReceta(APIView):

    def get_object(self, id):
        try:
            return Receta.objects.get(id=id)
        except Receta.DoesNotExist:
            return None

    def get(self, request, id):
        receta=self.get_object(id)
        if not receta:
            return Response({"error": "Receta no encontrada"}, status=404)

        serializer=RecetaSerializer(receta)
        return Response(serializer.data)

    def put(self, request, id):
        receta=self.get_object(id)
        if not receta:
            return Response({"error": "Receta no encontrada"}, status=404)

        serializer=RecetaSerializer(receta, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    def delete(self, request, id):
        receta=self.get_object(id)
        if not receta:
            return Response({"error": "Receta no encontrada"}, status=404)

        receta.delete()
        return Response({"mensaje": "Receta eliminada"}, status=204)

