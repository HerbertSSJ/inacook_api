from django.apps import AppConfig


class InacookConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inacook'

    def ready(self):
        # Crear roles y un admin por defecto después de migraciones
        from django.db.models.signals import post_migrate

        def create_defaults(sender, **kwargs):
            from django.contrib.auth import get_user_model
            from django.conf import settings
            from django.db import IntegrityError
            try:
                Rol = self.get_model('Rol')
            except Exception:
                # Si el modelo no existe aún (por ejemplo en ciertos comandos), salir
                return

            # Crear roles necesarios
            for nombre in ('admin', 'profesor', 'estudiante'):
                try:
                    Rol.objects.get_or_create(nombre=nombre)
                except Exception:
                    pass

            
            User = get_user_model()
            admin_username = getattr(settings, 'DEFAULT_ADMIN_USERNAME', 'admin')
            admin_email = getattr(settings, 'DEFAULT_ADMIN_EMAIL', 'admin@example.com')
            admin_password = getattr(settings, 'DEFAULT_ADMIN_PASSWORD', None)
            if admin_password:
                try:
                    if not User.objects.filter(username=admin_username).exists():
                        User.objects.create_superuser(username=admin_username, email=admin_email, password=admin_password)
                except IntegrityError:
                    pass

        post_migrate.connect(create_defaults, sender=self)
