from django.urls import path
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    path('apertura_caja/', views.apertura_caja, name='apertura_caja'),
    path('inicio/', views.inicio, name='inicio'),
    path('mostrar_articulos/', views.mostrar_articulos, name='mostrar'),
    path("editar_articulos", views.editar_articulos, name="editar_articulos"),
    path("crear_articulos", views.crear_articulos, name="crear_articulos"),
    path('mostrar_clientes/', views.mostrar_clientes, name='mostrar_clientes'),
    path('', RedirectView.as_view(url='procesar_login/', permanent=True)),
    path('procesar_login/', views.procesar_login, name='login'),
]