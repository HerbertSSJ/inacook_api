from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

from .models import (
    Rol,
    UnidadMedicion,
    Ingrediente,
    Receta,
    Comprobante,
    Historial,
    Receta_Ingrediente,
    Usuario,
)

from .serializers import (
    IngredienteSerializer, 
    RecetaSerializer, 
    ComprobanteSerializer, 
    HistorialSerializer,
    RolSerializer,
    UnidadMedicionSerializer,
    RecetaIngredienteSerializer,
    UsuarioSerializer,
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
        recetas=Receta.objects.all()
        serializer=RecetaSerializer(recetas, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer=RecetaSerializer(data=request.data)
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

# Lista y crea roles
class ListaRol(APIView):

    def get(self, request):
        roles=Rol.objects.all()
        serializer=RolSerializer(roles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer=RolSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class DetalleRol(APIView):
    def get_object(self, id):
        try:
            return Rol.objects.get(id=id)
        except Rol.DoesNotExist:
            return None

    def get(self, request, id):
        rol=self.get_object(id)
        if not rol:
            return Response({"error": "Rol no encontrado"}, status=404)
        serializer=RolSerializer(rol)
        return Response(serializer.data)

    def put(self, request, id):
        rol=self.get_object(id)
        if not rol:
            return Response({"error": "Rol no encontrado"}, status=404)
        serializer=RolSerializer(rol, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id):
        rol=self.get_object(id)
        if not rol:
            return Response({"error": "Rol no encontrado"}, status=404)
        rol.delete()
        return Response({"mensaje": "Rol eliminado"}, status=204)


class ListaUnidadMedicion(APIView):
    def get(self, request):
        unidades=UnidadMedicion.objects.all()
        serializer=UnidadMedicionSerializer(unidades, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer=UnidadMedicionSerializer(data=request.data)
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
        unidad=self.get_object(id)
        if not unidad:
            return Response({"error": "Unidad no encontrada"}, status=404)
        serializer=UnidadMedicionSerializer(unidad)
        return Response(serializer.data)

    def put(self, request, id):
        unidad=self.get_object(id)
        if not unidad:
            return Response({"error": "Unidad no encontrada"}, status=404)
        serializer=UnidadMedicionSerializer(unidad, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id):
        unidad=self.get_object(id)
        if not unidad:
            return Response({"error": "Unidad no encontrada"}, status=404)
        unidad.delete()
        return Response({"mensaje": "Unidad eliminada"}, status=204)


class ListaComprobante(APIView):

    def get(self, request):
        comprobantes=Comprobante.objects.all()
        serializer=ComprobanteSerializer(comprobantes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer=ComprobanteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class DetalleComprobante(APIView):

    def get_object(self, id):
        try:
            return Comprobante.objects.get(id=id)
        except Comprobante.DoesNotExist:
            return None

    def get(self, request, id):
        comprobante=self.get_object(id)
        if not comprobante:
            return Response({"error": "Comprobante no encontrado"}, status=404)

        serializer=ComprobanteSerializer(comprobante)
        return Response(serializer.data)

    def put(self, request, id):
        comprobante=self.get_object(id)
        if not comprobante:
            return Response({"error": "Comprobante no encontrado"}, status=404)

        serializer=ComprobanteSerializer(comprobante, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    def delete(self, request, id):
        comprobante=self.get_object(id)
        if not comprobante:
            return Response({"error": "Comprobante no encontrado"}, status=404)

        comprobante.delete()
        return Response({"mensaje": "Comprobante eliminado"}, status=204)

class ListaHistorial(APIView):

    def get(self, request):
        historial=Historial.objects.all()
        serializer=HistorialSerializer(historial, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer=HistorialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class DetalleHistorial(APIView):

    def get_object(self, id):
        try:
            return Historial.objects.get(id=id)
        except Historial.DoesNotExist:
            return None

    def get(self, request, id):
        registro=self.get_object(id)
        if not registro:
            return Response({"error": "Historial no encontrado"}, status=404)

        serializer=HistorialSerializer(registro)
        return Response(serializer.data)

    def put(self, request, id):
        registro=self.get_object(id)
        if not registro:
            return Response({"error": "Historial no encontrado"}, status=404)

        serializer=HistorialSerializer(registro, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    def delete(self, request, id):
        registro=self.get_object(id)
        if not registro:
            return Response({"error": "Historial no encontrado"}, status=404)

        registro.delete()
        return Response({"mensaje": "Historial eliminado"}, status=204)

# Lista y crea usuarios
class ListaUsuario(APIView):

    def get(self, request):
        usuarios=Usuario.objects.all()
        serializer=UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data)

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")
        rol_id = request.data.get("rol")

        if not username or not password:
             return Response({"error": "Faltan datos"}, status=400)

        # 1. Crear usuario de Django (Auth User)
        try:
            if User.objects.filter(username=username).exists():
                return Response({"error": "El usuario ya existe"}, status=400)

            user = User.objects.create_user(username=username, password=password, email=email)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

        # 2. Crear perfil de Usuario
        try:
            # rol_id puede ser None, el modelo lo permite
            usuario = Usuario.objects.create(user=user, rol_id=rol_id)
            serializer = UsuarioSerializer(usuario)
            return Response(serializer.data, status=201)
        except Exception as e:
            # Si falla, borramos el user para no dejar basura? 
            # Para simpleza estudiante, lo dejamos o intentamos borrar.
            user.delete()
            return Response({"error": "Error al crear perfil: " + str(e)}, status=400)


# Obtener, editar o borrar un usuario
class DetalleUsuario(APIView):

    def get_object(self, id):
        try:
            return Usuario.objects.get(id=id)
        except Usuario.DoesNotExist:
            return None

    def get(self, request, id):
        usuario=self.get_object(id)
        if not usuario:
            return Response({"error": "Usuario no encontrado"}, status=404)
        serializer = UsuarioSerializer(usuario)
        return Response(serializer.data)

    def put(self, request, id):
        usuario=self.get_object(id)
        if not usuario:
            return Response({"error": "Usuario no encontrado"}, status=404)

        serializer=UsuarioSerializer(usuario, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    def delete(self, request, id):
        usuario=self.get_object(id)
        if not usuario:
            return Response({"error": "Usuario no encontrado"}, status=404)

        usuario.delete()
        return Response({"mensaje": "Usuario eliminado"}, status=204)

# Lista y crea relaciones receta-ingrediente
class ListaRecetaIngrediente(APIView):

    def get(self, request):
        relaciones=Receta_Ingrediente.objects.all()
        serializer=RecetaIngredienteSerializer(relaciones, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer=RecetaIngredienteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


# Obtener, editar o borrar una relación receta-ingrediente
class DetalleRecetaIngrediente(APIView):

    def get_object(self, id):
        try:
            return Receta_Ingrediente.objects.get(id=id)
        except Receta_Ingrediente.DoesNotExist:
            return None

    def get(self, request, id):
        relacion=self.get_object(id)
        if not relacion:
            return Response({"error": "Relación no encontrada"}, status=404)
        serializer=RecetaIngredienteSerializer(relacion)
        return Response(serializer.data)

    def put(self, request, id):
        relacion=self.get_object(id)
        if not relacion:
            return Response({"error": "Relación no encontrada"}, status=404)

        serializer=RecetaIngredienteSerializer(relacion, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    def delete(self, request, id):
        relacion=self.get_object(id)
        if not relacion:
            return Response({"error": "Relación no encontrada"}, status=404)

        relacion.delete()
        return Response({"mensaje": "Relación eliminada"}, status=204)

class CambiarPassword(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not user_id or not old_password or not new_password:
            return Response({"error": "Faltan datos"}, status=400)

        try:
            # Encontrar el User de Django asociado al Usuario id o directamente el User id?
            # Asumiremos que user_id es el ID del modelo Usuario de inaccok
            usuario = Usuario.objects.get(id=user_id)
            user = usuario.user
        except Usuario.DoesNotExist:
            return Response({"error": "Usuario no encontrado"}, status=404)

        if not user.check_password(old_password):
            return Response({"error": "Contraseña actual incorrecta"}, status=400)

        user.set_password(new_password)
        user.save()
        return Response({"mensaje": "Contraseña actualizada éxito"}, status=200)

