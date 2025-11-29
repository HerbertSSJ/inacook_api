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

