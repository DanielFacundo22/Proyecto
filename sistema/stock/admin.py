from django.contrib import admin

#Proveedores
from .models import Proveedor
admin.site.register(Proveedor)
#Clientes
from .models import Clientes
admin.site.register(Clientes)

#Empleados
from .models import Empleados
admin.site.register(Empleados)