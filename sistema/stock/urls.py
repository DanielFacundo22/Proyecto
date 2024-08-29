from django.urls import path
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    path("apertura_caja", views.apertura_caja, name="apertura_caja"),
    path("mostrar",views.mostrar, name="mostrar"),
    path("mostrar_clientes", views.mostrar_clientes, name="mostrar_clientes"),
    path('apertura_caja/', views.apertura_caja, name='apertura_caja'),
    path('inicio/', views.inicio, name='inicio'),
    path('mostrar/', views.mostrar, name='mostrar'),
    path('mostrar_clientes/', views.mostrar_clientes, name='mostrar_clientes'),
    path('login/', views.procesar_login, name='login'),
    path('apertura_caja/', views.apertura_caja, name='apertura_caja'),
    path('', RedirectView.as_view(url='procesar_login/', permanent=True)),
    path('procesar_login/', views.procesar_login, name='procesar_login'),
]