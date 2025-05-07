from django.urls import path
from .views import *

urlpatterns = [
    path('', APIRoot.as_view(), name='api-root'),
    
    path('clientes/', ClienteListCreate.as_view()),
    path('clientes/<int:pk>/', ClienteDetail.as_view()),
    
    path('productos/', ProductoListCreate.as_view()),
    path('productos/<int:pk>/', ProductoDetail.as_view()),
    
    path('empleados/', EmpleadoListCreate.as_view()),
    path('empleados/<int:pk>/', EmpleadoDetail.as_view()),
    
    path('metodos-pago/', MetodoPagoListCreate.as_view()),
    path('metodos-pago/<int:pk>/', MetodoPagoDetail.as_view()),
    
    path('pedidos/', PedidoListCreate.as_view()),
    path('pedidos/<int:pk>/', PedidoDetail.as_view()),
]