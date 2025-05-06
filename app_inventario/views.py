# Django imports
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import ProtectedError
from django.db.models.deletion import ProtectedError

# Local imports
from .models import Producto
from .forms import ProductoForm
from app_usuarios.utils import is_admin_or_superuser, is_employee_or_above

# Helper functions
def get_productos_bajo_stock():
    productos = Producto.objects.all()
    return [producto for producto in productos if producto.stock_bajo()]


# Public views
def home(request):
    productos_bajo_stock = get_productos_bajo_stock()
    return render(request, 'home.html', {
        'productos_bajo_stock': productos_bajo_stock,
        'num_notificaciones': len(productos_bajo_stock)
    })


def notificaciones(request):
    productos_bajo_stock = get_productos_bajo_stock()
    return {
        'productos_bajo_stock': productos_bajo_stock,
        'num_notificaciones': len(productos_bajo_stock),
    }


# Protected views - Employee level access
@login_required
@user_passes_test(is_employee_or_above)
def listar_productos(request):
    productos = Producto.objects.all()

    # Filtros GET
    nombre = request.GET.get('nombre', '').strip()
    descripcion = request.GET.get('descripcion', '').strip()
    precio_min = request.GET.get('precio_min', '').strip()
    precio_max = request.GET.get('precio_max', '').strip()
    stock_min = request.GET.get('stock_min', '').strip()
    stock_max = request.GET.get('stock_max', '').strip()
    stockmin_min = request.GET.get('stockmin_min', '').strip()
    stockmin_max = request.GET.get('stockmin_max', '').strip()

    if nombre:
        productos = productos.filter(nombre__icontains=nombre)
    if descripcion:
        productos = productos.filter(descripcion__icontains=descripcion)
    if precio_min:
        productos = productos.filter(precio__gte=precio_min)
    if precio_max:
        productos = productos.filter(precio__lte=precio_max)
    if stock_min:
        productos = productos.filter(cantidad_stock__gte=stock_min)
    if stock_max:
        productos = productos.filter(cantidad_stock__lte=stock_max)
    if stockmin_min:
        productos = productos.filter(stock_minimo__gte=stockmin_min)
    if stockmin_max:
        productos = productos.filter(stock_minimo__lte=stockmin_max)

    productos_bajo_stock = get_productos_bajo_stock()
    context = {
        'productos': productos,
        'productos_bajo_stock': productos_bajo_stock,
        'num_notificaciones': len(productos_bajo_stock),
        'filtros': {
            'nombre': nombre,
            'descripcion': descripcion,
            'precio_min': precio_min,
            'precio_max': precio_max,
            'stock_min': stock_min,
            'stock_max': stock_max,
            'stockmin_min': stockmin_min,
            'stockmin_max': stockmin_max,
        }
    }
    return render(request, 'inventarios/listar_productos.html', context)


# Protected views - Admin level access
@login_required
@user_passes_test(is_admin_or_superuser)
def registrar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            if Producto.objects.filter(nombre=nombre).exists():
                messages.error(request, 'El producto ya existe.')
                return redirect('registrar_producto')
            form.save()
            messages.success(request, 'Producto añadido exitosamente.')
            return redirect('listar_productos')
    else:
        form = ProductoForm()

    productos_bajo_stock = get_productos_bajo_stock()
    return render(request, 'inventarios/registrar_producto.html', {
        'form': form,
        'productos_bajo_stock': productos_bajo_stock,
        'num_notificaciones': len(productos_bajo_stock)
    })


@login_required
@user_passes_test(is_admin_or_superuser)
def modificar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto modificado exitosamente.')
            return redirect('listar_productos')
    else:
        form = ProductoForm(instance=producto)

    productos_bajo_stock = get_productos_bajo_stock()
    return render(request, 'inventarios/modificar_producto.html', {
        'form': form,
        'producto': producto,
        'productos_bajo_stock': productos_bajo_stock,
        'num_notificaciones': len(productos_bajo_stock)
    })


@login_required
@user_passes_test(is_admin_or_superuser)
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    frase_desafio = f'Eliminar "{producto.nombre}"'
    
    if request.method == 'POST':
        frase_confirmacion = request.POST.get('frase_confirmacion', '').strip()
        if frase_confirmacion == frase_desafio:
            try:
                producto.delete()
                messages.success(request, 'Producto eliminado exitosamente.')
                return redirect('listar_productos')
            except ProtectedError:
                messages.error(request, 'No se puede eliminar: el producto tiene ventas, pedidos u otros registros asociados.')
                return redirect('listar_productos')
        else:
            messages.error(request, f'Debes escribir exactamente la frase: {frase_desafio}')
    
    # Verificar si tiene relaciones para mostrar advertencia anticipada
    tiene_relaciones = False
    if producto.ventadetalle_set.exists() or producto.pedidodetalle_set.exists() or \
       producto.ventas_reportes.exists():
        tiene_relaciones = True
    
    productos_bajo_stock = get_productos_bajo_stock()
    return render(request, 'inventarios/eliminar_producto.html', {
        'producto': producto,
        'tiene_relaciones': tiene_relaciones,
        'productos_bajo_stock': productos_bajo_stock,
        'num_notificaciones': len(productos_bajo_stock)
    })
