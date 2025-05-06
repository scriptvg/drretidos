from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # Tus rutas existentes de API
    path('', include('api.urls')),      # Ruta raíz alternativa
]