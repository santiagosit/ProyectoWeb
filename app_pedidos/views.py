# Django imports
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse

# Local imports
from app_usuarios.utils import is_admin_or_superuser, is_employee_or_above
from .models import PedidoDetalle, Pedido, Producto, Proveedor
from .forms import PedidoForm, ProveedorForm

# Protected views - Employee level access
@login_required
@user_passes_test(is_employee_or_above)
def listar_pedidos(request):
    pedidos = Pedido.objects.all()
    
    # Aplicar filtros si existen
    filters = {
        'id': request.GET.get('id'),
        'proveedor_id': request.GET.get('proveedor'),
        'fecha_pedido': request.GET.get('fecha'),
        'estado': request.GET.get('estado'),
    }
    
    # Aplicar cada filtro si tiene valor
    for key, value in filters.items():
        if value:
            pedidos = pedidos.filter(**{key: value})
    
    # Filtro especial para productos
    if query_producto := request.GET.get('producto'):
        pedidos = pedidos.filter(
            pedidodetalle__producto_id=query_producto
        ).distinct()

    context = {
        'pedidos': pedidos,
        'proveedores': Proveedor.objects.all(),
        'productos': Producto.objects.all()
    }
    return render(request, 'pedidos/listar_pedidos.html', context)


def listar_proveedores(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'pedidos/listar_proveedores.html', 
                 {'proveedores': proveedores})


# Protected views - Admin level access
@login_required
@user_passes_test(is_admin_or_superuser)
def registrar_pedido(request):
    if request.method == 'POST':
        pedido_form = PedidoForm(request.POST)
        productos = request.POST.getlist('productos[]')
        cantidades = request.POST.getlist('cantidades[]')
        costos = request.POST.getlist('costos_unitarios[]')

        if pedido_form.is_valid() and productos and cantidades and costos:
            pedido = pedido_form.save()
            total_pedido = 0

            for producto_id, cantidad, costo in zip(productos, cantidades, costos):
                producto = Producto.objects.get(id=producto_id)
                cantidad = int(cantidad)
                costo = float(costo)
                
                PedidoDetalle.objects.create(
                    pedido=pedido,
                    producto=producto,
                    cantidad=cantidad,
                    costo_unitario=costo
                )
                total_pedido += cantidad * costo

            pedido.total = total_pedido
            pedido.save()
            return redirect('listar_pedidos')
    else:
        pedido_form = PedidoForm()

    context = {
        'pedido_form': pedido_form,
        'productos': Producto.objects.all(),
        'proveedores': Proveedor.objects.all(),
    }
    return render(request, 'pedidos/registrar_pedido.html', context)


@login_required
@user_passes_test(is_admin_or_superuser)
def registrar_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_proveedores')
    else:
        form = ProveedorForm()
    return render(request, 'pedidos/registrar_proveedor.html', {'form': form})


@login_required
@user_passes_test(is_admin_or_superuser)
def actualizar_estado_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    if request.method == 'POST':
        if estado := request.POST.get('estado'):
            pedido.estado = estado
            pedido.save()
            if estado == 'recibido':
                for detalle in PedidoDetalle.objects.filter(pedido=pedido):
                    detalle.actualizar_stock()
        return redirect('listar_pedidos')
    return render(request, 'pedidos/actualizar_estado_pedido.html', 
                 {'pedido': pedido})


@login_required
@user_passes_test(is_admin_or_superuser)
def eliminar_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, id=proveedor_id)
    if request.method == 'POST':
        proveedor.delete()
        messages.success(
            request, 
            f'El proveedor {proveedor.nombre} ha sido eliminado correctamente.'
        )
        return redirect('listar_proveedores')
    return render(request, 'pedidos/eliminar_proveedor_confirmacion.html', 
                 {'proveedor': proveedor})


# Utility views
def detalles_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    return render(request, 'pedidos/detalles_pedido.html', {'pedido': pedido})


def filtro_opciones(request):
    filtro = request.GET.get('filtro')
    opciones_html = ''

    opciones_map = {
        'producto': (Producto, 'nombre'),
        'proveedor': (Proveedor, 'nombre'),
        'fecha': None,
        'estado': [
            ('pedido', 'Pedido'),
            ('en camino', 'En camino'),
            ('recibido', 'Recibido')
        ]
    }

    if filtro in ['producto', 'proveedor']:
        model, field = opciones_map[filtro]
        items = model.objects.all()
        opciones_html = f'<select name="{filtro}">'
        opciones_html += ''.join(
            f'<option value="{item.id}">{getattr(item, field)}</option>'
            for item in items
        )
        opciones_html += '</select>'
    elif filtro == 'fecha':
        opciones_html = '<input type="date" name="fecha">'
    elif filtro == 'estado':
        opciones_html = '<select name="estado">'
        opciones_html += ''.join(
            f'<option value="{value}">{label}</option>'
            for value, label in opciones_map['estado']
        )
        opciones_html += '</select>'

    return JsonResponse({'opciones_html': opciones_html})
