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


