from django.contrib import admin

#Proveedores
from .models import Proveedores
admin.site.register(Proveedores)
#Clientes
from .models import Clientes
admin.site.register(Clientes)

#Empleados
from .models import Empleados
admin.site.register(Empleados)

#Productos
from .models import Productos
admin.site.register(Productos)