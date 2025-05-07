from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response

class APIRoot(APIView):
    def get(self, request, format=None):
        return Response({
            "message": "Bienvenido a la API",
            "endpoints": {
                "clientes":     "http://127.0.0.1:8000/api/clientes",
                "productos":    "http://127.0.0.1:8000/api/productos/",
                "empleados":    "http://127.0.0.1:8000/api/empleados/",
                "metodos-pago": "http://127.0.0.1:8000/api/metodos-pago/",
                "pedidos":      "http://127.0.0.1:8000/api/pedidos/"
            }
        })

class ClienteListCreate(ListCreateAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class ClienteDetail(RetrieveUpdateDestroyAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class ProductoListCreate(ListCreateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class ProductoDetail(RetrieveUpdateDestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class EmpleadoListCreate(ListCreateAPIView):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer

class EmpleadoDetail(RetrieveUpdateDestroyAPIView):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer

class MetodoPagoListCreate(ListCreateAPIView):
    queryset = MetodoPago.objects.all()
    serializer_class = MetodoPagoSerializer

class MetodoPagoDetail(RetrieveUpdateDestroyAPIView):
    queryset = MetodoPago.objects.all()
    serializer_class = MetodoPagoSerializer

class PedidoListCreate(ListCreateAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

class PedidoDetail(RetrieveUpdateDestroyAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer