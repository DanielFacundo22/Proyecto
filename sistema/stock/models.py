# stock/models.py

from django.db import models

from django.db import models

class Proveedor(models.Model):
    id_prov = models.AutoField(primary_key=True)
    nombre_prov = models.CharField(max_length=100, verbose_name="nombre del proveedor", null=False)
    cuit_prov = models.IntegerField(verbose_name="cuit del proveedor",null=True, blank=True)
    tipo_prov = models.CharField(max_length=100,verbose_name="tipo de proveedor", null=True, blank=True)
    direcc_prov = models.CharField(max_length=100,verbose_name="direccion del proveedor", null=False)
    tel_prov = models.CharField(max_length=50,verbose_name="telefono del proveedor", null=True, blank=True)
    correo_prov = models.EmailField(max_length=100,verbose_name="email del proveedor", null=True, blank=True)

    def __str__(self):
        return self.nombre_prov
    
class Clientes(models.Model):
    id_cli=models.AutoField(primary_key=True)
    nombre_cli=models.CharField(max_length=100, verbose_name="Nombre del cliente",null=False)
    apellido_cli=models.CharField(max_length=100, verbose_name="Apellido del cliente", null=False)
    cuit_cli=models.IntegerField(verbose_name="cuit-dni del cliente", null=False)
    direcc_cli=models.CharField(max_length=100, verbose_name="Direccion del cliente", null=True, blank=True)
    tel_cli=models.CharField(max_length=50, verbose_name="Telefono del cliente", null=True, blank=True) 

    def __str__(self):
        return self.nombre_cli
    

class Empleados(models.Model):
    id_emplead=models.AutoField(primary_key=True)
    nombre_emplead=models.CharField(max_length=100, verbose_name="Nombre del empelado", null=False)
    apellido_emplead=models.CharField(max_length=100, verbose_name="Apellido del empleado",null=False)
    dni_emplead=models.IntegerField(verbose_name="DNI del empleado", null=False)
    direcc_emplead=models.CharField(max_length=100, verbose_name="Direccion del empleado", null=True, blank=True)
    tel_emplead=models.CharField(max_length=50, verbose_name="Telefono del empleado", null=True, blank=True)
    correo_emplead=models.CharField(max_length=100, verbose_name="Email del empleado", null=True, blank=True)
    sueldo_emplead=models.DecimalField(max_digits=10,decimal_places=2, verbose_name="Sueldo del empleado", null=True, blank=True)
    fecha_inicio=models.DateField(verbose_name="Fecha de inicio", null=False)
    fecha_fin=models.DateField(verbose_name="Fecha de finalizacion", null=True, blank=True)

    def __str__(self):
        return self.nombre_emplead
    
class Articulos(models.Model):
    pass
