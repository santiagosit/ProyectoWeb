# Generated by Django 5.1.1 on 2024-10-02 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_ventas', '0002_alter_venta_fecha_alter_venta_hora_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venta',
            name='fecha',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='venta',
            name='hora',
            field=models.TimeField(auto_now_add=True),
        ),
    ]
