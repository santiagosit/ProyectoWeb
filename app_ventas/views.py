# Django imports
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

# Local imports
from app_usuarios.utils import is_employee_or_above, is_admin_or_superuser
from app_inventario.models import Producto
from .models import Venta, VentaDetalle
from .forms import VentaForm

# Helper functions
def actualizar_producto_en_sesion(request, producto_id, cantidad, producto):
    """Actualiza la cantidad de un producto en la sesión."""
    productos_venta = request.session['productos_venta']
    producto_existente = next(
        (p for p in productos_venta if p['producto_id'] == producto_id), 
        None
    )

    if producto_existente:
        nueva_cantidad_total = int(producto_existente['cantidad']) + cantidad
        if nueva_cantidad_total > producto.cantidad_stock:
            messages.error(
                request,
                f'La cantidad total para "{producto.nombre}" no puede ser mayor '
                f'al stock disponible ({producto.cantidad_stock}).'
            )
            return False
        producto_existente['cantidad'] = nueva_cantidad_total
        producto_existente['subtotal'] = str(
            float(producto_existente['precio_unitario']) * nueva_cantidad_total
        )
    else:
        if cantidad > producto.cantidad_stock:
            messages.error(
                request,
                f'La cantidad para "{producto.nombre}" no puede ser mayor '
                f'al stock disponible ({producto.cantidad_stock}).'
            )
            return False
        detalle = {
            'producto_id': producto.id,
            'producto_nombre': producto.nombre,
            'cantidad': cantidad,
            'precio_unitario': str(producto.precio),
            'subtotal': str(producto.precio * cantidad)
        }
        request.session['productos_venta'].append(detalle)
    
    request.session.modified = True
    return True

def procesar_venta(request, venta_form):
    """Procesa y guarda una venta con sus detalles."""
    if venta_form.is_valid() and len(request.session['productos_venta']) > 0:
        venta = venta_form.save(commit=False)
        total_venta = 0
        venta.save()

        for detalle in request.session['productos_venta']:
            producto = Producto.objects.get(id=detalle['producto_id'])
            cantidad = int(detalle['cantidad'])
            precio_unitario = float(detalle['precio_unitario'])

            producto.cantidad_stock -= cantidad
            producto.save()

            VentaDetalle.objects.create(
                venta=venta,
                producto=producto,
                cantidad=cantidad,
                precio_unitario=precio_unitario
            )
            total_venta += cantidad * precio_unitario

        venta.total = total_venta
        venta.save()

        request.session['productos_venta'] = []
        messages.success(request, 'Venta registrada exitosamente.')
        return True
    
    messages.error(request, 'Debe añadir al menos un producto para confirmar la venta.')
    return False

# View functions
@login_required
@user_passes_test(is_employee_or_above)
def registrar_venta(request):
    """Vista para registrar una nueva venta."""
    productos = Producto.objects.all()

    # Inicializa una lista en la sesión para almacenar los productos temporalmente
    if 'productos_venta' not in request.session:
        request.session['productos_venta'] = []

    if request.method == 'POST':
        if 'agregar_producto' in request.POST:
            producto_id = int(request.POST.get('producto'))
            cantidad = int(request.POST.get('cantidad'))
            producto = Producto.objects.get(id=producto_id)
            actualizar_producto_en_sesion(request, producto_id, cantidad, producto)

        elif 'eliminar_producto' in request.POST:
            indice_producto = int(request.POST.get('eliminar_producto'))
            productos_venta = request.session['productos_venta']

            if 0 <= indice_producto < len(productos_venta):
                del productos_venta[indice_producto]
                request.session.modified = True
                messages.success(request, 'Producto eliminado correctamente.')

        elif 'confirmar_venta' in request.POST:
            venta_form = VentaForm(request.POST)
            if procesar_venta(request, venta_form):
                return redirect('listar_productos')

    # Calcular el total de la venta
    total_venta = sum(
        float(detalle['subtotal']) 
        for detalle in request.session['productos_venta']
    )

    context = {
        'productos': productos,
        'productos_venta': request.session['productos_venta'],
        'total_venta': total_venta,
        'venta_form': VentaForm(),
    }
    
    return render(request, 'ventas/registrar_venta.html', context)
