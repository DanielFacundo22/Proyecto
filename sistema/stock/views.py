from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def apertura_caja(request):
    return render(request, "apertura_caja.html")
def inicio(request):
    return render (request, "inicio.html")
def mostrar(request):
    return render(request, "articulos/mostrar.html")
def mostrar_clientes(request):
    return render(request, "mostrar_clientes.html")
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
