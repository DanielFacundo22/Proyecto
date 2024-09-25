from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import logout
from .models import *
from .forms import *
from django.db.models import Q
    
def procesar_login(request):    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('inicio')  # Redirige a la página de inicio
        else:
            messages.error(request, "Usuario o contraseña incorrecta")  
    return render(request, "procesar_login.html")


@login_required
def apertura_caja(request):
    return render(request, "apertura_caja.html")

def cierre_caja(request):
    return render(request, "cierre_caja.html")

@login_required
def inicio(request):
    producto=Productos.objects.all()
    return render (request, "inicio.html",{"productos":producto})


##CRUD Articulos
def mostrar_articulos(request):
    query = request.GET.get('q')  # Obtener el término de búsqueda
    if query:
        # Filtrar los productos por nombre o código usando el término de búsqueda
        productos = Productos.objects.filter(Q(nombre_prod__icontains=query) | Q(id_prod__icontains=query))
    else:
        # Mostrar todos los productos si no hay búsqueda
        productos = Productos.objects.all()

    return render(request, "articulos/mostrar.html", {"productos": productos})
def editar_articulos(request,id_prod):
    producto=Productos.objects.get(id_prod=id_prod)
    formulario = ProductosForm(request.POST or None, request.FILES or None, instance=producto)
    return render(request, "articulos/editar.html", {"formulario": formulario})
def crear_articulos(request):
    formulario = ProductosForm(request.POST or None)
    if formulario.is_valid():
     formulario.save()
     return redirect("mostrar_articulos")
    return render(request, "articulos/crear.html", {"formulario": formulario})
##Borrar_Articulos
def eliminar_productos(request,id_prod):
    producto = Productos.objects.get(id_prod=id_prod)
    producto.delete()
    return redirect("mostrar_articulos")
##CRUD Clientes
def mostrar_clientes(request):
    cliente=Clientes.objects.all()
    return render(request, "clientes/mostrar.html",{"clientes":cliente})
def editar_clientes(request,id_cli):
    cliente=Clientes.objects.get(id_cli=id_cli)
    formulario=ClientesForm(request.POST or None, request.FILES or None, instance=cliente)
    return render(request, "clientes/editar.html", {"formulario": formulario})
def crear_clientes(request):
    formulario = ClientesForm(request.POST or None)
    if formulario.is_valid():
        formulario.save()
        return redirect("mostrar_clientes")
    return render(request,"clientes/crear.html",{"formulario": formulario})
##Borrar_clientes
def eliminar_clientes(request, id_cli):
    cliente = Clientes.objects.get(id_cli=id_cli)
    cliente.delete()
    return redirect("mostrar_clientes")


##CRUD Empleados
def mostrar_empleados(request):
    empleado=Empleados.objects.all()
    return render(request,"empleados/mostrar.html",{"empleados":empleado})
def editar_empleados(request,id_emplead):
    empleado = Empleados.objects.get(id_emplead=id_emplead)
    formulario = EmpleadosForm(request.POST or None, request.FILES or None,instance=empleado)
    return render(request, "empleados/editar.html",{"formulario":formulario})
def crear_empleados(request):
    formulario = EmpleadosForm(request.POST or None)
    if formulario.is_valid():
        formulario.save()
        return redirect("mostrar_empleados")
    return render(request, "empleados/crear.html",{"formulario": formulario})
##Borrar_empleados
def eliminar_empleados(request, id_emplead):
    empleado = Empleados.objects.get(id_emplead=id_emplead)
    empleado.delete()
    return redirect("mostrar_empleados")

##CRUD Proveedores
def mostrar_proveedores(request):
    proveedor= Proveedores.objects.all()
    return render(request, "proveedores/mostrar.html",{"proveedores": proveedor})
def editar_proveedores(request,id_prov):
    proveedor = Proveedores.objects.get(id_prov=id_prov)
    formulario = ProveedoresForm(request.POST or None, request.FILES or None, instance=proveedor)
    return render(request, "proveedores/editar.html", {"formulario": formulario})
def crear_proveedores(request):
    formulario = ProveedoresForm(request.POST or None)
    if formulario.is_valid ():
     formulario.save()
     return redirect("mostrar_proveedores")
    return render(request, "proveedores/crear.html", {"formulario": formulario})

##Borrar_proveedores
def eliminar_proveedores(request,id_prov):
    proveedor = Proveedores.objects.get(id_prov=id_prov)
    proveedor.delete()
    return redirect("mostrar_proveedores")

##Compras
def mostrar_compras(request):
    return render(request,"compras/lista_compras.html")

##Ventas
def mostrar_ventas(request):
    producto = Productos.objects.all()
    empleado = Empleados.objects.all()
    cliente = Clientes.objects.all()

    context={
        "empleados":empleado,
        "clientes": cliente,
        "productos": producto

    }
    return render(request, "ventas/lista_ventas.html",context)

