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
from django.utils import timezone
from xhtml2pdf import pisa  
from django.template.loader import get_template
    
def procesar_login(request):    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('inicio')  
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
        if formulario.is_valid():  
            formulario.save()  
            messages.success(request, "Artículo editado exitosamente.")  
            return redirect('mostrar_articulos') 

    return render(request, "articulos/editar.html", {"formulario": formulario})

def crear_articulos(request):
    formulario = ProductosForm(request.POST or None)
    if request.method == 'POST':  # 
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
            return redirect('mostrar_clientes') 

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
    user = empleado.user 
    formulario = EmpleadosForm(request.POST or None, request.FILES or None, instance=empleado)

    if request.method == 'POST':
        if formulario.is_valid():
            username = formulario.cleaned_data.get('username')
            
           
            if User.objects.filter(username=username).exclude(id=user.id).exists():
                formulario.add_error('username', 'Este nombre de usuario ya está en uso por otro empleado.')
            else:
                formulario.save()
                messages.success(request, "Empleado actualizado con éxito.")
                return redirect('mostrar_empleados')  

    return render(request, "empleados/editar.html", {"formulario": formulario})




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
   
    proveedor = get_object_or_404(Proveedores, id_prov=id_prov)
    

    formulario = ProveedoresForm(request.POST or None, request.FILES or None, instance=proveedor)

    if formulario.is_valid():
        formulario.save()  
        messages.success(request, 'Proveedor actualizado correctamente.')
        return redirect('mostrar_proveedores')  
    
   
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



def crear_venta(request):
    producto = Productos.objects.all()
    empleado = Empleados.objects.all()
    cliente = Clientes.objects.all()

    if request.method == "POST":
        
        id_cli = request.POST.get('cliente')    
        total_venta = request.POST.get('total') 

        nueva_venta = Ventas(
            id_cli=Clientes.objects.get(id_cli=id_cli),  
            total_venta=total_venta,
            fecha_hs=timezone.now()
        )
        nueva_venta.save()

         
        productos_ids = request.POST.getlist('productos[]')
        cantidades = request.POST.getlist('cantidades[]')
        subtotales = request.POST.getlist('subtotales[]')

      
        for i in range(len(productos_ids)):
            producto = Productos.objects.get(id_prod=productos_ids[i])
            cantidad = int(cantidades[i])
            subtotal = float(subtotales[i])

           
            nuevo_detalle = det_ventas(
                id_prod=producto,
                id_venta=nueva_venta,
                precio_prod=producto.precio_prod,
                subtotal_venta=subtotal,
                cant_vendida=cantidad
            )
            nuevo_detalle.save()

        return redirect('det_venta',id_venta=nueva_venta.id_venta)

    else:
        formulario = VentasForm()

    context = {
        "empleados": empleado,
        "clientes": cliente,
        "productos": producto,
        "formulario": formulario
    }

    return render(request, "ventas/crear_venta.html", context)



def det_venta(request, id_venta):
    venta = get_object_or_404(Ventas, id_venta=id_venta)
    detalles = det_ventas.objects.filter(id_venta=venta)

    context = {
        'venta': venta,
        'detalles': detalles
    }

    return render(request, 'ventas/detalle_ventas.html', context)


def GenerarPdf(request,id_venta ):
    venta=Ventas.objects.get(id_venta=id_venta)
    detalles=det_ventas.objects.filter(id_venta=venta)

    context={
        "venta":venta,
        "detalles":detalles,
    }
    template =get_template("ventas/detalle_ventas_pdf.html")
    html=template.render(context)
    
    response=HttpResponse(content_type="aplication/pdf")
    response["content-disposition"]=f'attachment; filename="DetalleVenta_{venta.id_venta}.pdf"'

    pisa_status= pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse(f"error: {pisa_status.err}")
    return response
