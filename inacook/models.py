from django.db import models
from django.contrib.auth.models import User

class Rol(models.Model):
    nombre=models.CharField(max_length=45, unique=True)

    def __str__(self):
        return self.nombre
    
class Usuario (models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    rol=models.ForeignKey(Rol, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.user.username

class UnidadMedicion(models.Model):
    nombre=models.CharField(max_length=45)
    abreviatura=models.CharField(max_length=10)

    def __str__(self):
        return f"{self.nombre} ({self.abreviatura})"

class Ingrediente(models.Model):
    nombre=models.CharField(max_length=80)
    calidad=models.CharField(max_length=45)
    costo_unitario=models.IntegerField()
    unidad_medicion=models.ForeignKey(UnidadMedicion, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.nombre
    
class Receta(models.Model):
    nombre=models.CharField(max_length=100)
    categoria=models.CharField(max_length=45)
    aporte_calorico=models.IntegerField(null=True, blank=True)
    tiempo_preparacion=models.IntegerField(null=True, blank=True)
    usuario=models.ForeignKey(Usuario, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
        
class Receta_Ingrediente(models.Model):
    receta=models.ForeignKey(Receta, on_delete=models.CASCADE)
    ingrediente=models.ForeignKey(Ingrediente, on_delete=models.CASCADE)
    cantidad=models.FloatField()

    def __str__(self):
        return f"{self.cantidad} de {self.ingrediente.nombre}"
    
class Comprobante(models.Model):
    receta=models.ForeignKey(Receta, null=True, on_delete=models.CASCADE)
    factor_multiplicacion=models.IntegerField(default=1)
    iva=models.IntegerField(default=19)
    precio_bruto=models.IntegerField(default=0)
    fecha=models.DateField(null=True, blank=True)

    def __str__(self):
        return f"comprobante #{self.id}"
        
class Historial(models.Model):
    receta=models.ForeignKey(Receta, on_delete=models.CASCADE)
    usuario=models.ForeignKey(Usuario, null=True, on_delete=models.SET_NULL)
    fecha_entrega=models.DateField(null=True, blank=True)
    fecha_modificacion=models.DateTimeField(auto_now=True)
    cambio_realizado=models.TextField(null=True, blank=True)

    def __str__(self):
        return f"historial {self.id}"