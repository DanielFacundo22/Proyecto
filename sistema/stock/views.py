from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import logout
from .forms import EmpleadosForm
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from twilio.rest import Client
from .models import *
from .forms import *

# Create your views here.
    
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
    producto=Productos.objects.all()
    return render(request, "articulos/mostrar.html",{"productos":producto})

@permission_required('stock.view_articulo')
def editar_articulos(request,id_prod):
    producto = Productos.objects.get(id_prod=id_prod)
    formulario = ProductosForm(request.POST or None, request.FILES or None, instance=producto)

    if request.method == 'POST':
        if formulario.is_valid():  # Verifica si el formulario es válido
            formulario.save()  # Guarda los cambios en el modelo
            messages.success(request, "Artículo editado exitosamente.")  # Mensaje de éxito
            return redirect('mostrar_articulos')  # Redirige a la lista de artículos (ajusta el nombre según tu URL)

    return render(request, "articulos/editar.html", {"formulario": formulario})

def crear_articulos(request):
    formulario = ProductosForm(request.POST or None)
    if request.method == 'POST':  # Asegúrate de que el método sea POST
        if formulario.is_valid():
            formulario.save()
            return redirect("mostrar_articulos")
    return render(request, "articulos/crear.html", {"formulario": formulario})


@permission_required('stock.view_articulo')
def eliminar_productos(request,id_prod):
    producto = Productos.objects.get(id_prod=id_prod)
    producto.delete()
    return redirect("mostrar_articulos")
##CRUD Clientes
def mostrar_clientes(request):
    cliente=Clientes.objects.all()
    return render(request, "clientes/mostrar.html",{"clientes":cliente})

@permission_required('stock.view_cliente')
def editar_clientes(request, id_cli):
    cliente = Clientes.objects.get(id_cli=id_cli)
    formulario = ClientesForm(request.POST or None, request.FILES or None, instance=cliente)
    
    if request.method == 'POST':
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Cliente editado exitosamente.")
            return redirect('mostrar_clientes')  # Redirige a la lista de clientes o donde desees

    return render(request, "clientes/editar.html", {"formulario": formulario})


@permission_required('stock.view_cliente')
def crear_clientes(request):
    formulario = ClientesForm(request.POST or None)
    if formulario.is_valid():
        formulario.save()
        return redirect("mostrar_clientes")
    return render(request,"clientes/crear.html",{"formulario": formulario})
##Borrar_clientes
@permission_required('stock.view_cliente')
def eliminar_clientes(request, id_cli):
    cliente = Clientes.objects.get(id_cli=id_cli)
    cliente.delete()
    return redirect("mostrar_clientes")


##CRUD Empleados
def mostrar_empleados(request):
    empleado=Empleados.objects.all()
    return render(request,"empleados/mostrar.html",{"empleados":empleado})

@permission_required('stock.view_empleado')
def editar_empleados(request, id_emplead):
    empleado = get_object_or_404(Empleados, id_emplead=id_emplead)
    user = empleado.user  # Asegúrate de que la relación entre empleado y usuario esté bien definida
    formulario = EmpleadosForm(request.POST or None, request.FILES or None, instance=empleado)

    if request.method == 'POST':
        if formulario.is_valid():
            username = formulario.cleaned_data.get('username')
            
            # Verifica si el username ya existe en otro usuario
            if User.objects.filter(username=username).exclude(id=user.id).exists():
                formulario.add_error('username', 'Este nombre de usuario ya está en uso por otro empleado.')
            else:
                formulario.save()
                messages.success(request, "Empleado actualizado con éxito.")
                return redirect('mostrar_empleados')  # Redirige a la lista de empleados

    return render(request, "empleados/editar.html", {"formulario": formulario})


##aqui va el toquen de autenticacion y el numero de wpp

@permission_required('stock.view_empleado')
def crear_empleados(request):
    formulario = EmpleadosForm(request.POST or None)
    if formulario.is_valid():
        empleado = formulario.save(commit=False)
        if empleado.user:
            user = empleado.user
            password = get_random_string(length=12)
            user.set_password(password)
            user.save()

            telefono_empleado = request.POST.get('tel_emplead')  # Asegúrate de que este campo esté en el formulario
            
            if telefono_empleado:
                client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
                try:
                    # Enviar mensaje por WhatsApp
                    message = client.messages.create(
                        body=f"Hola {user.username}, tu contraseña generada es: {password}",
                        from_=TWILIO_WHATSAPP_NUMBER,
                        to=f'whatsapp:+{telefono_empleado}'  # Asegúrate de que el número de teléfono esté en formato internacional
                    )
                    messages.success(request, f"La contraseña generada para el usuario {user.username} ha sido enviada por WhatsApp.")
                except Exception as e:
                    messages.error(request, f"Ocurrió un error al enviar el mensaje: {str(e)}")
            else:
                messages.error(request, "No se proporcionó un número de teléfono válido.")

        empleado.save()
        return redirect("mostrar_empleados")
    
    return render(request, "empleados/crear.html", {"formulario": formulario})

@permission_required('stock.view_empleado')
def eliminar_empleados(request, id_emplead):
    empleado = Empleados.objects.get(id_emplead=id_emplead)
    empleado.delete()
    messages.success(request, "Empleado y usuario eliminados correctamente.")
    return redirect("mostrar_empleados")

##CRUD Proveedores
def mostrar_proveedores(request):
    proveedor= Proveedores.objects.all()
    return render(request, "proveedores/mostrar.html",{"proveedores": proveedor})

@permission_required('stock.view_empleado')
def editar_proveedores(request, id_prov):
    # Obtener el proveedor o devolver un 404 si no existe
    proveedor = get_object_or_404(Proveedores, id_prov=id_prov)
    
    # Crear un formulario con los datos existentes del proveedor
    formulario = ProveedoresForm(request.POST or None, request.FILES or None, instance=proveedor)
    
    # Si el formulario es válido, guardamos los cambios
    if formulario.is_valid():
        formulario.save()  # Guardar los cambios en la base de datos
        messages.success(request, 'Proveedor actualizado correctamente.')
        return redirect('mostrar_proveedores')  # Redirigir a la lista de proveedores o la página que elijas
    
    # Renderizamos la página de edición si es GET o el formulario no es válido
    return render(request, "proveedores/editar.html", {"formulario": formulario})

@permission_required('stock.view_empleado')
def crear_proveedores(request):
    formulario = ProveedoresForm(request.POST or None)
    if formulario.is_valid ():
     formulario.save()
     return redirect("mostrar_proveedores")
    return render(request, "proveedores/crear.html", {"formulario": formulario})

@permission_required('stock.view_empleado')
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


