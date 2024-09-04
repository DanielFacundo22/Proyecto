from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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

def apertura_caja(request):
    return render(request, "apertura_caja.html")
def inicio(request):
    return render (request, "inicio.html")
def mostrar_articulos(request):
    return render(request, "articulos/mostrar.html")
def editar_articulos(request):
    return render(request, "articulos/editar.html")
def crear_articulos(request):
    return render(request, "articulos/crear.html")
def mostrar_clientes(request):
    return render(request, "clientes/mostrar.html")
def editar_clientes(request):
    return render(request, "clientes/editar.html")
def crear_clientes(request):
    return render(request,"clientes/crear.html")
def mostrar_empleados(request):
    pass
def editar_empleados(request):
    pass
def crear_empleados(request):
    return render(request, "proveedores/crear.html")
def mostrar_proveedores(request):
    return render(request, "proveedores/mostrar.html")
def editar_proveedores(request):
    return render(request, "proveedores/editar.html")
def crear_proveedores(request):
    return render(request, "proveedores/crear.html")

