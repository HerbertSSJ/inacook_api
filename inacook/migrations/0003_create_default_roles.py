from django.db import migrations


def create_default_roles(apps, schema_editor):
    Rol = apps.get_model('inacook', 'Rol')
    for nombre in ['estudiante', 'profesor']:
        Rol.objects.get_or_create(nombre=nombre)


def noop(apps, schema_editor):
    
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('inacook', '0002_receta_ingrediente_peso_and_more'),
    ]

    operations = [
        migrations.RunPython(create_default_roles, noop),
    ]
