from rest_framework import serializers
from .models import Cliente, Pedido, Producto, DetallePedido

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'
    
    def validate_nombre(self, value):
        if any(c.isdigit() for c in value):
            raise serializers.ValidationError("El nombre no puede contener números")
        return value.strip().title()
    
    def validate_telefono(self, value):
        if len(value) < 9:
            raise serializers.ValidationError("Teléfono debe tener al menos 9 dígitos")
        return value

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'
    
    def validate_precio(self, value):
        if value <= 0:
            raise serializers.ValidationError("El precio debe ser mayor a cero")
        return round(value, 2)
    
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

class PedidoSerializer(serializers.ModelSerializer):
    detalles = DetallePedidoSerializer(many=True, read_only=True)

    class Meta:
        model = Pedido
        fields = '__all__'
    
    def validate_fecha_pedido(self, value):
        from django.utils import timezone
        if value > timezone.now():
            raise serializers.ValidationError("Fecha no puede ser futura")
        return value
    
    def validate(self, data):
        if data.get('fecha_entrega') and data.get('fecha_pedido'):
            if data['fecha_entrega'] < data['fecha_pedido']:
                raise serializers.ValidationError("Fecha de entrega no puede ser anterior al pedido")
        return data