from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inacook', '0002_receta_ingrediente_peso_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingrediente',
            name='usuario',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inacook.usuario'),
        ),
    ]
