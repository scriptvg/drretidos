from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    direccion = models.TextField(blank=True)

class Producto(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.IntegerField()
    
    def __str__(self):
        return f"{self.nombre} - ${self.precio}"

class Empleado(models.Model):
    nombre = models.CharField(max_length=100)
    cargo = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return f"{self.nombre} - {self.cargo}"
    
class MetodoPago(models.Model):
    tipo = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True)
    
    def __str__(self):
        return self.tipo

class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=8, decimal_places=2)
    metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.SET_NULL, null=True)
    empleado = models.ForeignKey(Empleado, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente.nombre}"

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=6, decimal_places=2)
    
    def __str__(self):
        return f"{self.producto.nombre} - {self.cantidad} unidades"