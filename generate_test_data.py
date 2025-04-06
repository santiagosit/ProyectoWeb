import os
import sys
import django
import random
from datetime import datetime, timedelta
from decimal import Decimal

# Configurar entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ProyectoWeb.settings')
django.setup()

# Importar modelos después de configurar Django
from django.contrib.auth.models import User
from app_usuarios.models import Profile
from app_inventario.models import Producto
from app_pedidos.models import Proveedor, Pedido, PedidoDetalle
from app_ventas.models import Venta, VentaDetalle
from app_eventos.models import Cliente, Evento
from app_finanzas.models import Ingreso, Egreso
from app_predicciones.models import PrediccionVenta, EstadisticaVenta
from app_reportes.models import EstadisticaVenta as ReporteEstadisticaVenta
from django.db import transaction

# Función para limpiar la base de datos
def clean_database():
    print("Limpiando base de datos...")
    # Eliminar datos en orden inverso a las dependencias
    Ingreso.objects.all().delete()
    Egreso.objects.all().delete()
    PrediccionVenta.objects.all().delete()
    EstadisticaVenta.objects.all().delete()
    ReporteEstadisticaVenta.objects.all().delete()
    VentaDetalle.objects.all().delete()
    Venta.objects.all().delete()
    PedidoDetalle.objects.all().delete()
    Pedido.objects.all().delete()
    Evento.objects.all().delete()
    Cliente.objects.all().delete()
    Proveedor.objects.all().delete()
    Producto.objects.all().delete()
    # No eliminamos usuarios para mantener el superusuario
    print("Base de datos limpiada correctamente.")

# Función para crear usuarios de prueba
def create_test_users(num_users=5):
    print(f"Creando {num_users} usuarios de prueba...")
    users = []
    roles = ['Administrador', 'Empleado']
    
    for i in range(num_users):
        username = f"usuario{i+1}"
        email = f"usuario{i+1}@example.com"
        
        # Verificar si el usuario ya existe
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(
                username=username,
                email=email,
                password="password123",
                first_name=f"Nombre{i+1}",
                last_name=f"Apellido{i+1}"
            )
            
            # Crear perfil para el usuario
            profile = Profile.objects.create(
                user=user,
                nombre_completo=f"Nombre{i+1} Apellido{i+1}",
                telefono=f"9{random.randint(10000000, 99999999)}",
                direccion=f"Calle {i+1}, Ciudad",
                fecha_contratacion=datetime.now().date() - timedelta(days=random.randint(30, 365)),
                rol=roles[i % len(roles)]
            )
            users.append(user)
    
    print(f"Se crearon {len(users)} usuarios de prueba.")
    return users

# Función para crear proveedores de prueba
def create_test_providers(num_providers=5):
    print(f"Creando {num_providers} proveedores de prueba...")
    providers = []
    
    for i in range(num_providers):
        provider = Proveedor.objects.create(
            nombre=f"Proveedor {i+1}",
            telefono=f"9{random.randint(10000000, 99999999)}",
            email=f"proveedor{i+1}@example.com",
            direccion=f"Dirección Proveedor {i+1}, Ciudad"
        )
        providers.append(provider)
    
    print(f"Se crearon {len(providers)} proveedores de prueba.")
    return providers

# Función para crear productos de prueba
def create_test_products(num_products=10):
    print(f"Creando {num_products} productos de prueba...")
    products = []
    
    for i in range(num_products):
        price = Decimal(str(random.uniform(5.0, 100.0))).quantize(Decimal('0.01'))
        stock = random.randint(5, 50)
        min_stock = random.randint(3, 10)
        
        product = Producto.objects.create(
            nombre=f"Producto {i+1}",
            descripcion=f"Descripción del producto {i+1}",
            precio=price,
            cantidad_stock=stock,
            stock_minimo=min_stock
        )
        products.append(product)
    
    print(f"Se crearon {len(products)} productos de prueba.")
    return products

# Función para crear clientes de prueba
def create_test_clients(num_clients=8):
    print(f"Creando {num_clients} clientes de prueba...")
    clients = []
    
    for i in range(num_clients):
        client = Cliente.objects.create(
            nombre=f"Cliente {i+1}",
            telefono=f"9{random.randint(10000000, 99999999)}",
            email=f"cliente{i+1}@example.com",
            direccion=f"Dirección Cliente {i+1}, Ciudad"
        )
        clients.append(client)
    
    print(f"Se crearon {len(clients)} clientes de prueba.")
    return clients

# Función para crear pedidos de prueba
def create_test_orders(providers, products, num_orders=6):
    print(f"Creando {num_orders} pedidos de prueba...")
    orders = []
    estados = ['pedido', 'en camino', 'recibido']
    
    for i in range(num_orders):
        # Fecha del pedido (últimos 30 días)
        fecha_pedido = datetime.now().date() - timedelta(days=random.randint(0, 30))
        
        # Crear pedido
        order = Pedido.objects.create(
            proveedor=random.choice(providers),
            fecha_pedido=fecha_pedido,
            estado=random.choice(estados)
        )
        
        # Crear detalles del pedido (entre 1 y 3 productos por pedido)
        num_details = random.randint(1, 3)
        selected_products = random.sample(products, num_details)
        
        for product in selected_products:
            cantidad = random.randint(5, 20)
            costo_unitario = Decimal(str(random.uniform(3.0, float(product.precio) * 0.7))).quantize(Decimal('0.01'))
            
            PedidoDetalle.objects.create(
                pedido=order,
                producto=product,
                cantidad=cantidad,
                costo_unitario=costo_unitario
            )
            
            # Si el pedido está recibido, actualizar el stock
            if order.estado == 'recibido':
                product.cantidad_stock += cantidad
                product.save()
        
        # Crear egreso para el pedido
        if order.estado in ['en camino', 'recibido']:
            Egreso.objects.create(
                tipo='pedido',
                pedido=order,
                monto=order.calcular_total(),
                descripcion=f"Pago por pedido #{order.id}",
                categoria='Pedido'
            )
        
        orders.append(order)
    
    print(f"Se crearon {len(orders)} pedidos de prueba.")
    return orders

# Función para crear ventas de prueba
def create_test_sales(users, products, num_sales=15):
    print(f"Creando {num_sales} ventas de prueba...")
    sales = []
    estados = ['completada', 'completada', 'completada', 'pendiente', 'cancelada']  # Más probabilidad de completadas
    
    # Obtener perfiles de usuarios
    profiles = [user.profile for user in users if hasattr(user, 'profile')]
    
    if not profiles:
        print("No hay perfiles de usuario disponibles para crear ventas.")
        return []
    
    for i in range(num_sales):
        # Fecha de la venta (últimos 60 días)
        fecha_creacion = datetime.now() - timedelta(days=random.randint(0, 60), 
                                                  hours=random.randint(0, 23),
                                                  minutes=random.randint(0, 59))
        
        # Seleccionar empleado y creador
        empleado = random.choice(profiles)
        creador = random.choice(profiles)
        
        # Estado de la venta
        estado = random.choice(estados)
        
        # Crear venta
        sale = Venta.objects.create(
            empleado=empleado,
            creado_por=creador,
            modificado_por=creador,
            fecha_creacion=fecha_creacion,
            fecha_modificacion=fecha_creacion,
            estado=estado,
            observaciones=f"Venta de prueba #{i+1}"
        )
        
        # Crear detalles de la venta (entre 1 y 4 productos por venta)
        num_details = random.randint(1, 4)
        available_products = [p for p in products if p.cantidad_stock > 0]
        
        if not available_products:
            print("No hay productos con stock disponible.")
            sale.delete()
            continue
        
        selected_products = random.sample(available_products, min(num_details, len(available_products)))
        
        for product in selected_products:
            max_cantidad = min(product.cantidad_stock, 5)  # Máximo 5 unidades o lo que haya en stock
            if max_cantidad <= 0:
                continue
                
            cantidad = random.randint(1, max_cantidad)
            precio_unitario = product.precio
            precio_total = precio_unitario * Decimal(str(cantidad))
            
            # Solo reducir stock si la venta está completada
            if estado == 'completada':
                try:
                    VentaDetalle.objects.create(
                        venta=sale,
                        producto=product,
                        cantidad=cantidad,
                        precio_unitario=precio_unitario,
                        precio_total=precio_total
                    )
                except ValueError:
                    # Si hay error de stock insuficiente, continuar con el siguiente producto
                    continue
            else:
                # Para ventas pendientes o canceladas no reducimos stock
                VentaDetalle.objects.create(
                    venta=sale,
                    producto=product,
                    cantidad=cantidad,
                    precio_unitario=precio_unitario,
                    precio_total=precio_total
                )
        
        # Si no se agregaron detalles, eliminar la venta
        if not sale.detalles.exists():
            sale.delete()
            continue
            
        # Actualizar total de la venta
        sale.actualizar_total()
        
        # Si la venta está completada, crear ingreso
        if estado == 'completada':
            sale.completar_venta()
        
        sales.append(sale)
    
    print(f"Se crearon {len(sales)} ventas de prueba.")
    return sales

# Función para crear eventos de prueba
def create_test_events(clients, num_events=10):
    print(f"Creando {num_events} eventos de prueba...")
    events = []
    estados = ['Pendiente', 'Confirmado', 'Cancelado']
    
    for i in range(num_events):
        # Fecha del evento (próximos 90 días)
        fecha_evento = datetime.now() + timedelta(days=random.randint(1, 90), 
                                                hours=random.randint(0, 23),
                                                minutes=random.randint(0, 59))
        
        event = Evento.objects.create(
            cliente=random.choice(clients),
            descripcion=f"Descripción del evento {i+1}",
            fecha_evento=fecha_evento,
            estado=random.choice(estados)
        )
        events.append(event)
    
    print(f"Se crearon {len(events)} eventos de prueba.")
    return events

# Función para crear predicciones de venta
def create_test_predictions(products, num_predictions=8):
    print(f"Creando {num_predictions} predicciones de venta de prueba...")
    predictions = []
    tendencias = ['alta', 'media', 'baja', 'riesgo']
    
    for i in range(num_predictions):
        # Fechas de análisis (últimos 30-90 días)
        fecha_fin = datetime.now().date() - timedelta(days=random.randint(1, 10))
        fecha_inicio = fecha_fin - timedelta(days=random.randint(30, 90))
        
        # Seleccionar producto aleatorio
        producto = random.choice(products)
        
        # Valores aleatorios para la predicción
        ventas_promedio = Decimal(str(random.uniform(1.0, 20.0))).quantize(Decimal('0.01'))
        tendencia = random.choice(tendencias)
        confianza = Decimal(str(random.uniform(0.3, 0.95))).quantize(Decimal('0.01'))
        cantidad_sugerida = random.randint(5, 30)
        
        prediction = PrediccionVenta.objects.create(
            producto=producto,
            fecha_prediccion=datetime.now() - timedelta(days=random.randint(0, 15)),
            fecha_inicio_analisis=fecha_inicio,
            fecha_fin_analisis=fecha_fin,
            ventas_promedio=ventas_promedio,
            tendencia=tendencia,
            confianza_prediccion=confianza,
            cantidad_sugerida=cantidad_sugerida,
            observaciones=f"Predicción de prueba para {producto.nombre}"
        )
        predictions.append(prediction)
    
    print(f"Se crearon {len(predictions)} predicciones de venta de prueba.")
    return predictions

# Función para crear estadísticas de venta
def create_test_statistics(products, num_days=30):
    print(f"Creando estadísticas de venta para los últimos {num_days} días...")
    statistics = []
    
    for product in products:
        for day in range(num_days):
            fecha = datetime.now().date() - timedelta(days=day)
            
            # Valores aleatorios para las estadísticas
            cantidad_vendida = random.randint(0, 10)
            ingreso_total = Decimal(str(cantidad_vendida)) * product.precio
            rotacion = Decimal(str(random.uniform(0.0, 1.0))).quantize(Decimal('0.01'))
            dias_sin_venta = 0 if cantidad_vendida > 0 else random.randint(1, 5)
            
            # Crear estadística en app_predicciones
            stat = EstadisticaVenta.objects.create(
                producto=product,
                fecha=fecha,
                cantidad_vendida=cantidad_vendida,
                ingreso_total=ingreso_total,
                rotacion_inventario=rotacion,
                dias_sin_venta=dias_sin_venta
            )
            
            # Crear estadística en app_reportes (mismos datos)
            report_stat = ReporteEstadisticaVenta.objects.create(
                producto=product,
                fecha=fecha,
                cantidad_vendida=cantidad_vendida,
                ingreso_total=ingreso_total,
                rotacion_inventario=rotacion,
                dias_sin_venta=dias_sin_venta
            )
            
            statistics.append(stat)
    
    print(f"Se crearon {len(statistics)} estadísticas de venta de prueba.")
    return statistics

# Función principal para generar todos los datos de prueba
@transaction.atomic
def generate_all_test_data():
    print("Iniciando generación de datos de prueba...")
    
    # Limpiar base de datos
    clean_database()
    
    # Crear datos de prueba en orden de dependencia
    users = create_test_users(5)
    providers = create_test_providers(5)
    products = create_test_products(10)
    clients = create_test_clients(8)
    orders = create_test_orders(providers, products, 6)
    sales = create_test_sales(users, products, 15)
    events = create_test_events(clients, 10)
    predictions = create_test_predictions(products, 8)
    statistics = create_test_statistics(products, 30)
    
    print("\nGeneración de datos de prueba completada con éxito.")
    print("\nResumen:")
    print(f"- Usuarios: {len(users)}")
    print(f"- Proveedores: {len(providers)}")
    print(f"- Productos: {len(products)}")
    print(f"- Clientes: {len(clients)}")
    print(f"- Pedidos: {len(orders)}")
    print(f"- Ventas: {len(sales)}")
    print(f"- Eventos: {len(events)}")
    print(f"- Predicciones: {len(predictions)}")
    print(f"- Estadísticas: {len(statistics)}")

# Ejecutar el script si se llama directamente
if __name__ == "__main__":
    generate_all_test_data()