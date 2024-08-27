from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def login(request):
    return render(request,"login.html")
def apertura_caja(request):
    return render(request, "apertura_caja.html")
def inicio(request):
    return render (request, "inicio.html")
def mostrar(request):
    return render(request, "articulos/mostrar.html")
def mostrar_clientes(request):
    return render(request, "mostrar_clientes.html")

