# stock/models.py

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

#CRUD
class Proveedores(models.Model):
    id_prov = models.AutoField(primary_key=True)
    nombre_prov = models.CharField(max_length=100, verbose_name="nombre del proveedor", null=False, blank=True)
    cuit_prov = models.CharField(max_length=100 ,verbose_name="cuit del proveedor",null=True, blank=True)
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
    cuit_cli=models.CharField(max_length=100 ,verbose_name="cuit-dni del cliente", null=False)
    direcc_cli=models.CharField(max_length=100, verbose_name="Direccion del cliente", null=True, blank=True)
    tel_cli=models.CharField(max_length=50, verbose_name="Telefono del cliente", null=True, blank=True) 

    def __str__(self):
        return self.nombre_cli
    
class Empleados(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='empleado', null=True, blank=True)
    id_emplead = models.AutoField(primary_key=True)
    nombre_emplead = models.CharField(max_length=100, verbose_name="Nombre del empleado", null=False)
    apellido_emplead = models.CharField(max_length=100, verbose_name="Apellido del empleado", null=False)
    dni_emplead = models.CharField(max_length=100, verbose_name="DNI del empleado", null=False)
    direcc_emplead = models.CharField(max_length=100, verbose_name="Dirección del empleado", null=True, blank=True)
    tel_emplead = models.CharField(max_length=50, verbose_name="Teléfono del empleado", null=True, blank=True)
    correo_emplead = models.EmailField(max_length=100, verbose_name="Email del empleado", null=True, blank=True)
    sueldo_emplead = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Sueldo del empleado", null=True, blank=True)
    fecha_inicio = models.DateField(verbose_name="Fecha de inicio", null=False)
    fecha_fin = models.DateField(verbose_name="Fecha de finalización", null=True, blank=True)

    def delete(self, *args, **kwargs):
        # Si el empleado tiene un usuario asociado, eliminarlo también
        if self.user:
            self.user.delete()
        super().delete(*args, **kwargs)
        
    def __str__(self):
        return f"{self.nombre_emplead} {self.apellido_emplead}"

class AuditoriaEmpleado(models.Model):
    empleado = models.ForeignKey(Empleados, on_delete=models.CASCADE)
    nombre_empleado = models.CharField(max_length=255)
    proceso = models.CharField(max_length=255)
    fecha_hora = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.nombre_empleado} - {self.proceso} - {self.fecha_hora}"
    
class Productos(models.Model):
    id_prod= models.AutoField(primary_key=True)
    id_prov=models.ForeignKey(Proveedores, on_delete=models.SET_NULL, null=True, blank=True, related_name="productos")
    nombre_prod=models.CharField(max_length=100, verbose_name="Nombre del Articulo", null=False)
    precio_costo=models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio de costo", null=True, blank=True)
    precio_prod=models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio", null=False)
    stock_min=models.IntegerField(null=True, blank=True)
    stock_max=models.IntegerField(null=True, blank=True)
    stock_actual=models.IntegerField(null=True,blank=True)
    punto_reposicion=models.IntegerField(null=True,blank=True)

    def __str__(self):
        return self.nombre_prod

#CAJA
class ArqueoCaja(models.Model):
    id_caja = models.AutoField(primary_key=True) 
    # Identificador único de cada arqueo de caja, generado automáticamente.

    id_emplead = models.ForeignKey('Empleados', on_delete=models.SET_NULL, null=True, related_name="cajas") 
    # Relación con el modelo de empleados, indica qué empleado realizó el arqueo.
    # Si se elimina el empleado, el campo queda como NULL.

    fecha_hs_apertura = models.DateTimeField(verbose_name="Fecha y hora de apertura", null=False) 
    # Fecha y hora de apertura de la caja.

    fecha_hs_cierre = models.DateTimeField(verbose_name="Fecha y hora de cierre", null=True, blank=True) 
    # Fecha y hora de cierre de la caja (opcional).

    monto_inicial = models.DecimalField(max_digits=10, decimal_places=2) 
    # Monto inicial con el que se abre la caja.

    monto_final = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) 
    # Monto final calculado al cerrar la caja.

    total_ingreso = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ingreso total del día", null=True, blank=True) 
    # Suma total de todos los ingresos relacionados con esta caja.

    total_egreso = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Gastos del día", null=True, blank=True) 
    # Suma total de todos los egresos relacionados con esta caja.

    cerrado = models.BooleanField(default=False) 
    # Indica si la caja está cerrada o no.

    @classmethod
    def get_arqueo_abierto(cls, empleado):
        return cls.objects.filter(id_emplead=empleado, cerrado=False).order_by('-fecha_hs_apertura').first()
    # Método de clase que retorna la última caja abierta de un empleado.

    def save(self, *args, **kwargs):
        # Sobrescribe el método save para incluir cálculos automáticos.
        if not self.pk:
            super().save(*args, **kwargs)  # Guarda el objeto si es nuevo.

        if not kwargs.pop('skip_calculation', False):
            self.calcular_montos()  # Calcula montos solo si no se pasa el flag 'skip_calculation'.

        super().save(*args, **kwargs)  # Llama al método save original.

    def calcular_montos(self):
        """Calcula los totales de ingreso y egreso y actualiza el monto final."""
        self.total_ingreso = sum(ingreso.monto for ingreso in self.ingresos.all())
        self.total_egreso = sum(egreso.monto for egreso in self.egresos.all())
        self.monto_final = self.monto_inicial + self.total_ingreso - self.total_egreso
        self.save(skip_calculation=True)  # Guarda el resultado omitiendo recálculo.

    def cerrar_caja(self):
        """Cierra la caja calculando el balance final y marcándola como cerrada."""
        self.total_ingreso = sum(ingreso.monto for ingreso in self.ingresos.all())
        self.total_egreso = sum(egreso.monto for egreso in self.egresos.all())
        self.monto_final = self.monto_inicial + self.total_ingreso - self.total_egreso
        self.cerrado = True
        self.fecha_hs_cierre = timezone.now()  # Marca la fecha y hora de cierre.
        self.save()

    def __str__(self):
        return f"Caja: {self.id_emplead} ID {self.id_caja} "
    # Representación en texto que muestra el ID del empleado y la caja.

class Ingreso(models.Model):
    id_ingreso = models.AutoField(primary_key=True) 
    # Identificador único del ingreso.

    id_caja = models.ForeignKey(ArqueoCaja, on_delete=models.CASCADE, related_name='ingresos') 
    # Relación con la caja a la que pertenece el ingreso.

    descripcion = models.CharField(max_length=255) 
    # Descripción breve del ingreso.

    monto = models.DecimalField(max_digits=10, decimal_places=2) 
    # Monto del ingreso.

    fecha_ingreso = models.DateTimeField(auto_now_add=True) 
    # Fecha y hora del ingreso (automáticamente asignado al momento de creación).

    tipo = models.CharField(max_length=50, choices=[('manual', 'Manual'), ('venta', 'Venta')]) 
    # Tipo de ingreso, ya sea por venta o ingreso manual.

    def __str__(self):
        return f"Ingreso {self.id_ingreso} - {self.descripcion}"
    # Representación en texto que muestra el ID y la descripción del ingreso.

class Egreso(models.Model):
    id_egreso = models.AutoField(primary_key=True) 
    # Identificador único del egreso.

    id_caja = models.ForeignKey(ArqueoCaja, on_delete=models.CASCADE, related_name='egresos') 
    # Relación con la caja que realiza el egreso.

    descripcion = models.CharField(max_length=255) 
    # Descripción breve del egreso.

    monto = models.DecimalField(max_digits=10, decimal_places=2) 
    # Monto del egreso.

    fecha_egreso = models.DateTimeField(auto_now_add=True) 
    # Fecha y hora del egreso, asignado automáticamente.

    tipo = models.CharField(max_length=50, choices=[('manual', 'Manual'), ('compra', 'Compra')]) 
    # Tipo de egreso, ya sea por compra o manual.

    def __str__(self):
        return f"Egreso {self.id_egreso} - {self.descripcion}"
    # Representación en texto que muestra el ID y la descripción del egreso.

class Movimiento(models.Model):
    caja = models.ForeignKey(ArqueoCaja, on_delete=models.CASCADE, related_name='movimientos') 
    # Relación con la caja asociada al movimiento.

    fecha = models.DateTimeField(auto_now_add=True) 
    # Fecha y hora del movimiento.

    monto = models.DecimalField(max_digits=10, decimal_places=2) 
    # Monto involucrado en el movimiento.

    tipo = models.CharField(max_length=50) 
    # Tipo de movimiento (por ejemplo, ingreso o egreso).

    descripcion = models.CharField(max_length=255, null=True, blank=True) 
    # Descripción opcional del movimiento.

    def __str__(self):
        return f"Movimiento en caja {self.caja.id_caja}: {self.tipo} por {self.monto}"
    # Representación en texto que muestra el movimiento, tipo y monto.

#COMPRA
class Compras(models.Model):
    id_compra=models.AutoField(primary_key=True)
    id_prov=models.ForeignKey(Proveedores, on_delete=models.SET_NULL, null=True, blank=True, related_name="compras")
    id_caja=models.ForeignKey(ArqueoCaja, on_delete=models.SET_NULL, null=True, related_name="compras")
    fecha_compra=models.DateField(verbose_name="Fecha de compra", null=False)
    total_compra=models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total de la compra", null=False)
    descrip_compra=models.CharField(max_length=150, verbose_name="Agregue un comentario", null=True, blank=True)

    def __str__(self):
        return f"Compra: {self.id_compra}"
    
class det_compras(models.Model):
    id_det_compra=models.AutoField(primary_key=True)
    id_compra=models.ForeignKey(Compras, on_delete=models.SET_NULL, null=True, blank=True, related_name="det_compras")
    id_prod=models.ForeignKey(Productos, on_delete=models.SET_NULL, null=True, blank=True, related_name="det_compras")
    cant_comprada=models.IntegerField(verbose_name="Cantidad unitaria", null=False)
    precio_unitario=models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio", null=False)
    subtotal_compra=models.DecimalField(max_digits=10, decimal_places=2, null=False)
    
    def __str__(self):
        return f"det_venta: {self.id_det_compra}"

#VENTA
class Ventas(models.Model):
    id_venta=models.AutoField(primary_key=True)
    id_caja=models.ForeignKey(ArqueoCaja, on_delete=models.SET_NULL, null=True, related_name="ventas")
    id_cli=models.ForeignKey(Clientes, on_delete=models.SET_NULL, null=True,blank=True, related_name="ventas")
    fecha_hs=models.DateTimeField(null=False)
    total_venta=models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total de la venta",null=False)

    def __str__(self):
        return f"Venta: {self.id_venta}"

class det_ventas(models.Model):
    id_det_venta=models.AutoField(primary_key=True)
    id_prod=models.ForeignKey(Productos, on_delete=models.SET_NULL,null= True, blank=True, related_name="det_ventas" )
    id_venta=models.ForeignKey(Ventas, on_delete=models.SET_NULL, null=True, blank=True, related_name="det_ventas")
    precio_prod=models.DecimalField(max_digits=10, decimal_places=2,null=False, verbose_name="Precio")
    subtotal_venta=models.DecimalField(max_digits=10, decimal_places=2, null=False, verbose_name="Subtotal")
    cant_vendida=models.IntegerField(null=False, verbose_name="Cantidad")

    def __str__(self):
        return f"det_venta: {self.id_det_venta}"
    



