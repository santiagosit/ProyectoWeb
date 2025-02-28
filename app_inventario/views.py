from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Producto
from .forms import ProductoForm


def listar_productos(request):
    productos = Producto.objects.all()
    productos_bajo_stock = [producto for producto in productos if producto.stock_bajo()]
    return render(request, 'inventarios/listar_productos.html', {
        'productos': productos,
        'productos_bajo_stock': productos_bajo_stock,
        'num_notificaciones': len(productos_bajo_stock)
    })


def registrar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            if Producto.objects.filter(nombre=nombre).exists():
                messages.error(request, 'El producto ya existe.')
                return redirect('registrar_producto')
            else:
                form.save()
                messages.success(request, 'Producto añadido exitosamente.')
                return redirect('listar_productos')
    else:
        form = ProductoForm()

    productos_bajo_stock = [producto for producto in Producto.objects.all() if producto.stock_bajo()]
    return render(request, 'inventarios/registrar_producto.html', {
        'form': form,
        'productos_bajo_stock': productos_bajo_stock,
        'num_notificaciones': len(productos_bajo_stock)
    })


def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado exitosamente.')
        return redirect('listar_productos')

    productos_bajo_stock = [producto for producto in Producto.objects.all() if producto.stock_bajo()]
    return render(request, 'inventarios/eliminar_producto.html', {
        'producto': producto,
        'productos_bajo_stock': productos_bajo_stock,
        'num_notificaciones': len(productos_bajo_stock)
    })


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

    productos_bajo_stock = [producto for producto in Producto.objects.all() if producto.stock_bajo()]
    return render(request, 'inventarios/modificar_producto.html', {
        'form': form,
        'producto': producto,
        'productos_bajo_stock': productos_bajo_stock,
        'num_notificaciones': len(productos_bajo_stock)
    })


def home(request):
    productos = Producto.objects.all()
    productos_bajo_stock = [producto for producto in productos if producto.stock_bajo()]
    return render(request, 'home.html', {
        'productos_bajo_stock': productos_bajo_stock,
        'num_notificaciones': len(productos_bajo_stock)
    })
def notificaciones(request):
    productos_bajo_stock = [producto for producto in Producto.objects.all() if producto.stock_bajo()]
    num_notificaciones = len(productos_bajo_stock)
    return {
        'productos_bajo_stock': productos_bajo_stock,
        'num_notificaciones': num_notificaciones,
    }
