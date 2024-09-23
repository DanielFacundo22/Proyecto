# Generated by Django 5.1 on 2024-09-08 18:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0007_productos_proveedores_delete_proveedor_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cajas',
            fields=[
                ('id_caja', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_hs_apertura', models.DateTimeField(verbose_name='Fecha y hora de apertura')),
                ('fecha_hs_cierre', models.DateTimeField(verbose_name='Fecha y hora de cierre')),
                ('saldo_caja', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Saldo')),
                ('monto_inicial', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Monto inicial')),
                ('total_ingreso', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Ingreso total del dia')),
                ('total_egreso', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Gastos del dia')),
                ('abierto_caja', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Compras',
            fields=[
                ('id_compra', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_compra', models.DateField(verbose_name='Fecha de compra')),
                ('total_compra', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Total de la compra')),
                ('descrip_compra', models.CharField(blank=True, max_length=150, null=True, verbose_name='Agregue un comentario')),
            ],
        ),
        migrations.CreateModel(
            name='det_compras',
            fields=[
                ('id_det_compra', models.AutoField(primary_key=True, serialize=False)),
                ('cant_comprada', models.IntegerField(verbose_name='Cantidad unitaria')),
                ('precio_unitario', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Precio')),
                ('subtotal_compra', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='det_ventas',
            fields=[
                ('id_det_venta', models.AutoField(primary_key=True, serialize=False)),
                ('precio_prod', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Precio')),
                ('subtotal_venta', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Subtotal')),
                ('cant_vendida', models.IntegerField(verbose_name='Cantidad')),
                ('id_prod', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='det_ventas', to='stock.productos')),
            ],
        ),
        migrations.CreateModel(
            name='Ventas',
            fields=[
                ('id_venta', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_hs', models.DateTimeField()),
                ('total_venta', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Total de la venta')),
            ],
        ),
        migrations.DeleteModel(
            name='Articulos',
        ),
        migrations.AlterField(
            model_name='clientes',
            name='cuit_cli',
            field=models.CharField(max_length=100, verbose_name='cuit-dni del cliente'),
        ),
        migrations.AlterField(
            model_name='empleados',
            name='dni_emplead',
            field=models.CharField(max_length=100, verbose_name='DNI del empleado'),
        ),
        migrations.AlterField(
            model_name='proveedores',
            name='cuit_prov',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='cuit del proveedor'),
        ),
        migrations.AddField(
            model_name='cajas',
            name='id_emplead',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cajas', to='stock.empleados'),
        ),
        migrations.AddField(
            model_name='compras',
            name='id_caja',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='compras', to='stock.cajas'),
        ),
        migrations.AddField(
            model_name='compras',
            name='id_prov',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='compras', to='stock.proveedores'),
        ),
        migrations.AddField(
            model_name='det_compras',
            name='id_compra',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='det_compras', to='stock.compras'),
        ),
        migrations.AddField(
            model_name='det_compras',
            name='id_prod',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='det_compras', to='stock.productos'),
        ),
        migrations.AddField(
            model_name='ventas',
            name='id_caja',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ventas', to='stock.cajas'),
        ),
        migrations.AddField(
            model_name='ventas',
            name='id_cliente',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ventas', to='stock.clientes'),
        ),
        migrations.AddField(
            model_name='det_ventas',
            name='id_venta',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='det_ventas', to='stock.ventas'),
        ),
    ]