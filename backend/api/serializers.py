from rest_framework import serializers
from .models import *
from django.http import JsonResponse

def validate_length(value, min_len, field_name):
    if len(value) < min_len:
        raise serializers.ValidationError(f"{field_name} debe tener al menos {min_len} caracteres")
    return value

def validate_numeric(value, field_name):
    if not value.isdigit():
        raise serializers.ValidationError(f"{field_name} solo puede contener números")
    return value

def validate_no_numbers(value, field_name):
    if any(c.isdigit() for c in value):
        raise serializers.ValidationError(f"{field_name} no puede contener números")
    return value

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'
    
    def validate_nombre(self, value):
        value = validate_length(value, 3, "Nombre")
        validate_no_numbers(value, "Nombre")
        return value.strip().title()
    
    def validate_telefono(self, value):
        value = validate_numeric(value, "Teléfono")
        return validate_length(value, 9, "Teléfono")

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

    def validate_nombre(self, value):
        value = validate_length(value, 3, "Nombre")
        validate_no_numbers(value, "Nombre")
        return value

    def validate_descripcion(self, value):
        return validate_length(value, 10, "Descripción")

    def validate_precio(self, value):
        if value <= 0:
            raise serializers.ValidationError("El precio debe ser mayor a cero")
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("El stock no puede ser negativo")
        return value

class DetallePedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetallePedido
        fields = '__all__'
    
    def validate_cantidad(self, value):
        if value < 1:
            raise serializers.ValidationError("La cantidad mínima es 1")
        return value
    
    def validate_precio_unitario(self, value):
        if value <= 0:
            raise serializers.ValidationError("El precio unitario debe ser mayor a cero")
        return value

class PedidoSerializer(serializers.ModelSerializer):
    detalles = DetallePedidoSerializer(many=True, read_only=True)

    class Meta:
        model = Pedido
        fields = '__all__'

class EmpleadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleado
        fields = '__all__'
    
    def validate_cargo(self, value):
        value = validate_length(value, 3, "Cargo")
        validate_no_numbers(value, "Cargo")
        return value

class MetodoPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetodoPago
        fields = '__all__'
    
    def validate_tipo(self, value):
        return validate_length(value, 3, "Tipo de pago")

def api_root(request):
    return JsonResponse({
        "message": "Bienvenido a la API",
        "endpoints": {
            "clientes": "/api/clientes/",
            "productos": "/api/productos/",
            "empleados": "/api/empleados/",
            "metodos-pago": "/api/metodos-pago/",
            "pedidos": "/api/pedidos/"
        }
    })