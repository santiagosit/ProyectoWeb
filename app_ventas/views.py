
from django.shortcuts import render, redirect
from django.contrib import messages
from app_inventario.models import Producto
from .models import Venta, VentaDetalle
from .forms import VentaForm

def registrar_venta(request):
    productos = Producto.objects.all()

    # Inicializa una lista en la sesión para almacenar los productos temporalmente
    if 'productos_venta' not in request.session:
        request.session['productos_venta'] = []


    if request.method == 'POST':
        if 'agregar_producto' in request.POST:
            # Proceso para añadir un producto a la lista
            producto_id = int(request.POST.get('producto'))
            cantidad = int(request.POST.get('cantidad'))
            producto = Producto.objects.get(id=producto_id)

            # Verificar si el producto ya ha sido añadido
            productos_venta = request.session['productos_venta']
            producto_existente = next((p for p in productos_venta if p['producto_id'] == producto_id), None)

            if producto_existente:
                nueva_cantidad_total = int(producto_existente['cantidad']) + cantidad
                if nueva_cantidad_total > producto.cantidad_stock:
                    messages.error(request, f'La cantidad total para "{producto.nombre}" no puede ser mayor al stock disponible ({producto.cantidad_stock}).')
                else:
                    producto_existente['cantidad'] = nueva_cantidad_total
                    producto_existente['subtotal'] = str(float(producto_existente['precio_unitario']) * nueva_cantidad_total)
                    request.session.modified = True
            else:
                if cantidad > producto.cantidad_stock:
                    messages.error(request, f'La cantidad para "{producto.nombre}" no puede ser mayor al stock disponible ({producto.cantidad_stock}).')
                else:
                    detalle = {
                        'producto_id': producto.id,
                        'producto_nombre': producto.nombre,
                        'cantidad': cantidad,
                        'precio_unitario': str(producto.precio),
                        'subtotal': str(producto.precio * cantidad)
                    }
                    request.session['productos_venta'].append(detalle)
                    request.session.modified = True

        elif 'eliminar_producto' in request.POST:
            # Proceso para eliminar un producto de la lista
            indice_producto = int(request.POST.get('eliminar_producto'))
            productos_venta = request.session['productos_venta']

            if 0 <= indice_producto < len(productos_venta):
                del productos_venta[indice_producto]
                request.session.modified = True
                messages.success(request, 'Producto eliminado correctamente.')

        elif 'confirmar_venta' in request.POST:
            venta_form = VentaForm(request.POST)
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
                return redirect('listar_productos')
            else:
                messages.error(request, 'Debe añadir al menos un producto para confirmar la venta.')

    # Calcular el total de la venta
    total_venta = sum(float(detalle['subtotal']) for detalle in request.session['productos_venta'])

    return render(request, 'ventas/registrar_venta.html', {
        'productos': productos,
        'productos_venta': request.session['productos_venta'],
        'total_venta': total_venta,  # Pasamos el total al contexto
        'venta_form': VentaForm(),
    })


