



from .models import  PedidoDetalle
from .forms import PedidoForm



def registrar_pedido(request):
    if request.method == 'POST':
        pedido_form = PedidoForm(request.POST)
        productos = request.POST.getlist('productos[]')
        cantidades = request.POST.getlist('cantidades[]')
        costos = request.POST.getlist('costos_unitarios[]')  # Corregido para coincidir con el HTML

        if pedido_form.is_valid() and productos and cantidades and costos:  # Verificar que también lleguen los costos
            pedido = pedido_form.save()
            total_pedido = 0  # Inicializar total del pedido

            for producto_id, cantidad, costo in zip(productos, cantidades, costos):
                producto = Producto.objects.get(id=producto_id)
                cantidad = int(cantidad)
                costo = float(costo)
                # Crear detalles del pedido
                PedidoDetalle.objects.create(
                    pedido=pedido,
                    producto=producto,
                    cantidad=cantidad,
                    costo_unitario=costo
                )
                total_pedido += cantidad * costo  # Sumar subtotales al total

            pedido.total = total_pedido  # Guardar total en el pedido
            pedido.save()

            return redirect('listar_pedidos')
    else:
        pedido_form = PedidoForm()

    productos = Producto.objects.all()
    proveedores = Proveedor.objects.all()
    context = {
        'pedido_form': pedido_form,
        'productos': productos,
        'proveedores': proveedores,
    }
    return render(request, 'pedidos/registrar_pedido.html', context)


def actualizar_estado_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    if request.method == 'POST':
        estado = request.POST.get('estado')
        if estado:
            pedido.estado = estado
            pedido.save()
            if estado == 'recibido':
                for detalle in PedidoDetalle.objects.filter(pedido=pedido):
                    detalle.actualizar_stock()
        return redirect('listar_pedidos')
    return render(request, 'pedidos/actualizar_estado_pedido.html', {'pedido': pedido})


def listar_pedidos(request):
    query_id = request.GET.get('id')
    query_proveedor = request.GET.get('proveedor')
    query_fecha = request.GET.get('fecha')
    query_estado = request.GET.get('estado')
    query_producto = request.GET.get('producto')

    pedidos = Pedido.objects.all()

    if query_id:
        pedidos = pedidos.filter(id=query_id)

    if query_proveedor:
        pedidos = pedidos.filter(proveedor_id=query_proveedor)

    if query_fecha:
        pedidos = pedidos.filter(fecha_pedido=query_fecha)

    if query_estado:
        pedidos = pedidos.filter(estado=query_estado)

    if query_producto:
        pedidos = pedidos.filter(pedidodetalle__producto_id=query_producto).distinct()

    return render(request, 'pedidos/listar_pedidos.html', {'pedidos': pedidos, 'proveedores': Proveedor.objects.all(), 'productos': Producto.objects.all()})
from django.shortcuts import render, redirect
from .forms import ProveedorForm

def registrar_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_proveedores')  # Redirige a la vista de proveedores listados
    else:
        form = ProveedorForm()
    return render(request, 'pedidos/registrar_proveedor.html', {'form': form})
from django.shortcuts import render
from .models import Proveedor

def listar_proveedores(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'pedidos/listar_proveedores.html', {'proveedores': proveedores})
from django.http import JsonResponse
from .models import Producto, Proveedor

def filtro_opciones(request):
    filtro = request.GET.get('filtro')
    opciones_html = ''

    if filtro == 'producto':
        productos = Producto.objects.all()
        opciones_html = '<select name="producto">'
        for producto in productos:
            opciones_html += f'<option value="{producto.id}">{producto.nombre}</option>'
        opciones_html += '</select>'
    elif filtro == 'proveedor':
        proveedores = Proveedor.objects.all()
        opciones_html = '<select name="proveedor">'
        for proveedor in proveedores:
            opciones_html += f'<option value="{proveedor.id}">{proveedor.nombre}</option>'
        opciones_html += '</select>'
    elif filtro == 'fecha':
        opciones_html = '<input type="date" name="fecha">'
    elif filtro == 'estado':
        opciones_html = '''<select name="estado">
                            <option value="pedido">Pedido</option>
                            <option value="en camino">En camino</option>
                            <option value="recibido">Recibido</option>
                          </select>'''

    return JsonResponse({'opciones_html': opciones_html})
from django.shortcuts import render, get_object_or_404
from .models import Pedido
def detalles_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    return render(request, 'pedidos/detalles_pedido.html', {'pedido': pedido})


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages


def eliminar_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, id=proveedor_id)

    if request.method == 'POST':
        proveedor.delete()
        messages.success(request, f'El proveedor {proveedor.nombre} ha sido eliminado correctamente.')
        return redirect('listar_proveedores')

    return render(request, 'pedidos/eliminar_proveedor_confirmacion.html', {'proveedor': proveedor})
