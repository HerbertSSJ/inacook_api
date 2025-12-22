from django.db import migrations, models
import django.db.models.deletion


def create_default_roles(apps, schema_editor):
    Rol = apps.get_model('inacook', 'Rol')
    for nombre in ['estudiante', 'profesor', 'admin']:
        Rol.objects.get_or_create(nombre=nombre)


def create_default_unidades(apps, schema_editor):
    UnidadMedicion = apps.get_model('inacook', 'UnidadMedicion')
    defaults = [
        ('Kilogramo', 'kg'),
        ('Gramo', 'g'),
        ('Litro', 'L'),
        ('Unidad', 'u'),
    ]
    for nombre, abre in defaults:
        UnidadMedicion.objects.get_or_create(nombre=nombre, abreviatura=abre)


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('inacook', '0001_initial'),
    ]

    operations = [
        # Receta_Ingrediente: peso y peso_total
        migrations.AddField(
            model_name='receta_ingrediente',
            name='peso',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
        migrations.AddField(
            model_name='receta_ingrediente',
            name='peso_total',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),

        # Ingrediente: usuario FK
        migrations.AddField(
            model_name='ingrediente',
            name='usuario',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inacook.usuario'),
        ),

        # Receta: seccion y asignatura
        migrations.AddField(
            model_name='receta',
            name='seccion',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='receta',
            name='asignatura',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),

        # Receta: imagen
        migrations.AddField(
            model_name='receta',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='recetas/'),
        ),

        # RunPython: seed roles and unidades
        migrations.RunPython(create_default_roles, noop),
        migrations.RunPython(create_default_unidades, noop),
    ]
