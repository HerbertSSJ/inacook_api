from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class rol(models.Model):
    nombre=models.CharField(max_length=45, unique=True)

    def __str(self):
        return self.nombre
    
class usuario (models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    rol=models.ForeignKey(rol, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.user.username

class unidadmedicion(models.Model):
    nombre=models.CharField(max_length=45)
    abreviatura=models.CharField(max_length=10)

    def __str__(self):
        return f"{self.nombre} ({self.abreviatura})"

class ingrediente(models.Model):
    nombre=models.CharField(max_length=80)
    calidad=models.CharField(max_length=45)
    costo_unitario=models.DecimalField()
    unidad_medicion=models.ForeignKey(unidadmedicion, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.nombre
    
    class receta(models.Model):
        nombre=models.CharField(max_length=100)
        categoria=models.CharField(max_length=45)
        aporte_calorico=models.IntegerField(null=True, blank=True)
        tiempo_preparacion=models.IntegerField(null=True, blank=True)
        usuario=models.ForeignKey(usuario, null=True, on_delete=models.SET_NULL)

        def __str__(self):
            return self.nombre
        
class receta_ingrediente(models.Model):
    receta=models.ForeignKey(receta, on_delete=models.CASCADE)
    ingrediente=models.ForeignKey(ingrediente, on_delete=models.CASCADE)
    cantidad=models.FloatField()

    def __str(self):
        return f"{self.cantidad} de {self.ingrediente.nombre}"
    
    class comprobante(models.Model):
        receta=models.ForeignKey(receta, null=True, on_delete=models.SET_NULL)
        factor_multiplicacion=models.IntegerField(default=1)
        iva=models.IntegerField(default=19)
        precio_bruto=models.IntegerField(default=0)
        fecha=models.DateField(null=True, blank=True)

        def __str__(self):
            return f"comprobante #{self.id}"
        
        class historial(models.Model):
            receta=models.ForeignKey(receta, on_delete=models.CASCADE)
            usuario=models.ForeignKey(usuario, null=True, on_delete=models.SET_NULL)
            fecha_entrega=models.DateField(null=True, blank=True)
            fecha_modificacion=models.DateTimeField(auto_now=True)
            cambio_realizado=models.TextField(null=True, blank=True)

            def __str__(self):
                return f"historial {self.id}"