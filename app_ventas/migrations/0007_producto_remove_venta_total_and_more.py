# Generated by Django 5.1.1 on 2024-10-02 21:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_ventas', '0006_alter_ventadetalle_producto_delete_producto'),
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cantidad_stock', models.IntegerField()),
                ('stock_minimo', models.IntegerField(default=3)),
            ],
        ),
        migrations.RemoveField(
            model_name='venta',
            name='total',
        ),
        migrations.AlterField(
            model_name='ventadetalle',
            name='cantidad',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='ventadetalle',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_ventas.producto'),
        ),
    ]
