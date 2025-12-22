from django.db import migrations


def merge_admin_into_profesor(apps, schema_editor):
    Rol = apps.get_model('inacook', 'Rol')
    Usuario = apps.get_model('inacook', 'Usuario')

    # Normalize names and find target profesor role (case-insensitive)
    profesor_qs = Rol.objects.filter(nombre__iexact='profesor')
    if profesor_qs.exists():
        profesor = profesor_qs.first()
    else:
        profesor = Rol.objects.create(nombre='Profesor')

    # Find admin roles (case-insensitive)
    admin_roles = Rol.objects.filter(nombre__iexact='admin')
    if not admin_roles.exists():
        # Nothing to do
        return

    # Reassign usuarios that have admin role to profesor
    for admin in admin_roles:
        Usuario.objects.filter(rol=admin).update(rol=profesor)

    # Remove admin role entries
    admin_roles.delete()


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('inacook', '0005_add_peso_ingrediente'),
    ]

    operations = [
        migrations.RunPython(merge_admin_into_profesor, reverse_code=noop),
    ]
