# Importaciones de Django
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

# Importaciones locales
from .models import Ingreso, Egreso
from .forms import EgresoForm
from app_usuarios.utils import is_admin_or_superuser, is_employee_or_above

# Vistas de ingresos
@login_required
@user_passes_test(is_admin_or_superuser)
def listar_ingresos(request):
    """Vista para listar todos los ingresos"""
    ingresos = Ingreso.objects.select_related('venta').all().order_by('-fecha')

    for ingreso in ingresos:
        total = sum(detalle.subtotal() for detalle in ingreso.venta.detalles.all())
        ingreso.monto = total

    return render(request, 'finanzas/listar_ingresos.html', {'ingresos': ingresos})

@login_required
@user_passes_test(is_admin_or_superuser)
def detalle_ingreso(request, ingreso_id):
    """Vista para ver el detalle de un ingreso específico"""
    ingreso = Ingreso.objects.get(id=ingreso_id)
    detalles = ingreso.venta.detalles.all()
    total = sum(detalle.subtotal() for detalle in detalles)

    context = {
        'ingreso': ingreso,
        'detalles': detalles,
        'total': total,
    }
    return render(request, 'finanzas/detalle_ingreso.html', context)

# Vistas de egresos
@login_required
@user_passes_test(is_admin_or_superuser)
def listar_egresos(request):
    """Vista para listar todos los egresos"""
    egresos_pedidos = Egreso.objects.filter(tipo='pedido').select_related('pedido').order_by('-fecha')
    egresos_personalizados = Egreso.objects.filter(tipo='personalizado').order_by('-fecha')
    
    return render(request, 'finanzas/listar_egresos.html', {
        'egresos_pedidos': egresos_pedidos,
        'egresos_personalizados': egresos_personalizados,
    })

@login_required
@user_passes_test(is_admin_or_superuser)
def detalle_egreso(request, egreso_id):
    """Vista para ver el detalle de un egreso específico"""
    egreso = get_object_or_404(Egreso, id=egreso_id)

    if egreso.tipo == 'pedido' and egreso.pedido is not None:
        detalles = egreso.pedido.detalles()
        total = sum(detalle.subtotal() for detalle in detalles)
    else:
        detalles = None
        total = egreso.monto

    context = {
        'egreso': egreso,
        'detalles': detalles,
        'total': total,
    }
    return render(request, 'finanzas/detalle_egreso.html', context)

@login_required
@user_passes_test(is_admin_or_superuser)
def crear_egreso_personalizado(request):
    """Vista para crear un nuevo egreso personalizado"""
    if request.method == 'POST':
        form = EgresoForm(request.POST)
        if form.is_valid():
            egreso = form.save(commit=False)
            if egreso.tipo == 'personalizado':
                egreso.pedido = None
            egreso.save()
            return redirect('listar_egresos')
    else:
        form = EgresoForm()
    return render(request, 'finanzas/crear_egreso_personalizado.html', {'form': form})

@login_required
@user_passes_test(is_admin_or_superuser)
def eliminar_egreso_personalizado(request, egreso_id):
    """Vista para eliminar un egreso personalizado"""
    egreso = get_object_or_404(Egreso, id=egreso_id, tipo='personalizado')
    egreso.delete()
    messages.success(request, 'Egreso personalizado eliminado exitosamente.')
    return redirect('listar_egresos')
