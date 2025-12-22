
import django.db.migrations.operations.special
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models






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


def add_missing_columns(apps, schema_editor):
    conn = schema_editor.connection
    cur = conn.cursor()
    
    try:
        cur.execute("SHOW COLUMNS FROM inacook_receta LIKE 'imagen'")
        if not cur.fetchall():
            cur.execute("ALTER TABLE inacook_receta ADD COLUMN imagen varchar(255) NULL")
    except Exception:
        pass

    try:
        cur.execute("SHOW COLUMNS FROM inacook_ingrediente LIKE 'usuario_id'")
        if not cur.fetchall():
            cur.execute("ALTER TABLE inacook_ingrediente ADD COLUMN usuario_id bigint NULL")
    except Exception:
        pass


def create_roles_and_units(apps, schema_editor):
    Rol = apps.get_model('inacook', 'Rol')
    UnidadMedicion = apps.get_model('inacook', 'UnidadMedicion')
    for nombre, _ in [('Admin', ''), ('Estudiante', ''), ('Profesor', '')]:
        Rol.objects.get_or_create(nombre=nombre)
    unidades = [
        ('Kilogramo', 'kg'),
        ('Gramo', 'g'),
        ('Litro', 'L'),
        ('Unidad', 'u'),
    ]
    for nombre, ab in unidades:
        UnidadMedicion.objects.get_or_create(nombre=nombre, abreviatura=ab)


def add_seccion_asignatura(apps, schema_editor):
    conn = schema_editor.connection
    cur = conn.cursor()
    try:
        cur.execute("SHOW COLUMNS FROM inacook_receta LIKE 'seccion'")
        if not cur.fetchall():
            cur.execute("ALTER TABLE inacook_receta ADD COLUMN seccion varchar(100) NULL")
    except Exception:
        pass
    try:
        cur.execute("SHOW COLUMNS FROM inacook_receta LIKE 'asignatura'")
        if not cur.fetchall():
            cur.execute("ALTER TABLE inacook_receta ADD COLUMN asignatura varchar(100) NULL")
    except Exception:
        pass



class Migration(migrations.Migration):

    replaces = [('inacook', '0001_initial'), ('inacook', '0002_receta_ingrediente_peso_and_more'), ('inacook', '0003_fix_missing_columns'), ('inacook', '0004_add_seccion_asignatura'), ('inacook', '0005_add_peso_ingrediente')]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingrediente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=80)),
                ('calidad', models.CharField(max_length=45)),
                ('costo_unitario', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Receta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('categoria', models.CharField(max_length=45)),
                ('aporte_calorico', models.IntegerField(blank=True, null=True)),
                ('tiempo_preparacion', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=45, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='UnidadMedicion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=45)),
                ('abreviatura', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Comprobante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('factor_multiplicacion', models.IntegerField(default=1)),
                ('iva', models.IntegerField(default=19)),
                ('precio_bruto', models.IntegerField(default=0)),
                ('fecha', models.DateField(blank=True, null=True)),
                ('receta', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inacook.receta')),
            ],
        ),
        migrations.CreateModel(
            name='Receta_Ingrediente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.FloatField()),
                ('peso', models.FloatField(blank=True, default=0.0, null=True)),
                ('peso_total', models.FloatField(blank=True, default=0.0, null=True)),
                ('ingrediente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inacook.ingrediente')),
                ('receta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inacook.receta')),
            ],
        ),
        migrations.AddField(
            model_name='ingrediente',
            name='unidad_medicion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='inacook.unidadmedicion'),
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rol', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='inacook.rol')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='receta',
            name='usuario',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inacook.usuario'),
        ),
        migrations.CreateModel(
            name='Historial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_entrega', models.DateField(blank=True, null=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
                ('cambio_realizado', models.TextField(blank=True, null=True)),
                ('receta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inacook.receta')),
                ('usuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='inacook.usuario')),
            ],
        ),
        migrations.AddField(
            model_name='ingrediente',
            name='usuario',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inacook.usuario'),
        ),
        migrations.AddField(
            model_name='receta',
            name='seccion',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='receta',
            name='asignatura',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='receta',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='recetas/'),
        ),
        migrations.RunPython(
            code=create_default_roles,
            reverse_code=noop,
        ),
        migrations.RunPython(
            code=create_default_unidades,
            reverse_code=noop,
        ),
        migrations.RunPython(
            code=add_missing_columns,
            reverse_code=migrations.RunPython.noop,
        ),
        migrations.RunPython(
            code=create_roles_and_units,
            reverse_code=migrations.RunPython.noop,
        ),
        migrations.RunPython(
            code=add_seccion_asignatura,
            reverse_code=migrations.RunPython.noop,
        ),
        migrations.AddField(
            model_name='ingrediente',
            name='peso',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
    ]
