# Generated by Django 5.1.1 on 2024-10-02 22:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_inventario', '0001_initial'),
        ('app_ventas', '0007_producto_remove_venta_total_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ventadetalle',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_inventario.producto'),
        ),
        migrations.AddField(
            model_name='venta',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.DeleteModel(
            name='Producto',
        ),
    ]
