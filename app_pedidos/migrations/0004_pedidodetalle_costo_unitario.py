# Generated by Django 5.1.1 on 2024-10-11 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_pedidos', '0003_alter_pedidodetalle_pedido'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedidodetalle',
            name='costo_unitario',
            field=models.DecimalField(decimal_places=2, default='0', max_digits=10),
            preserve_default=False,
        ),
    ]
