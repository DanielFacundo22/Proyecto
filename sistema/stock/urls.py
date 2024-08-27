from django.urls import path
from . import views

urlpatterns = [
    path("", views.login, name="login"),
    path("apertura_caja", views.apertura_caja, name="apertura_caja"),
    path("inicio", views.inicio, name="inicio"),
    path("mostrar",views.mostrar, name="mostrar"),
    path("mostrar_clientes", views.mostrar_clientes, name="mostrar_clientes")
]