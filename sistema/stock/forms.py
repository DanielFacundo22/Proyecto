from django import forms
from .models import *

class ProveedoresForm(forms.ModelForm):
    class Meta:
        model = Proveedores
        fields = "__all__"

class ClientesForm(forms.ModelForm):
    class Meta:
        model = Clientes
        fields="__all__"

class EmpleadosForm(forms.ModelForm):
    class Meta:
        model = Empleados
        fields="__all__"

class ProductosForm(forms.ModelForm):
    class Meta:
        model = Productos
        fields="__all__"

