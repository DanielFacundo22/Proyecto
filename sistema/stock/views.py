from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Proveedor
from .models import Clientes
from .models import Empleados
from .forms import ProveedorForm 
# Create your views here.
    
def procesar_login(request):    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('apertura_caja')  # Redirige a la página de inicio
        else:
            messages.error(request, "Usuario o contraseña incorrecta")  
    return render(request, "procesar_login.html")


@login_required
def apertura_caja(request):
    return render(request, "apertura_caja.html")
@login_required
def inicio(request):
    return render (request, "inicio.html")

##CRUD Articulos
def mostrar_articulos(request):
    return render(request, "articulos/mostrar.html")
def editar_articulos(request):
    return render(request, "articulos/editar.html")
def crear_articulos(request):
    return render(request, "articulos/crear.html")
##CRUD Clientes
def mostrar_clientes(request):
    cliente=Clientes.objects.all()
    return render(request, "clientes/mostrar.html",{"clientes":cliente})
def editar_clientes(request):
    return render(request, "clientes/editar.html")
def crear_clientes(request):
    return render(request,"clientes/crear.html")
##CRUD Empleados
def mostrar_empleados(request):
    empleado=Empleados.objects.all()
    return render(request,"empleados/mostrar.html",{"empleados":empleado})
def editar_empleados(request):
    pass
def crear_empleados(request):
    return render(request, "proveedores/crear.html")
##CRUD Proveedores
def mostrar_proveedores(request):
    proveedor= Proveedor.objects.all()
    return render(request, "proveedores/mostrar.html",{"proveedores": proveedor})
def editar_proveedores(request):
    return render(request, "proveedores/editar.html")
def crear_proveedores(request):
    formulario = ProveedorForm(request.POST or None)
    if formulario.is_valid ():
     formulario.save()
     return redirect("mostrar_proveedores")
    return render(request, "proveedores/crear.html", {"formulario": formulario})

