from django.shortcuts import render
from .models import Ingreso, Egreso
from django.contrib.auth.decorators import login_required

@login_required
@login_required
def listar_ingresos(request):
    ingresos = Ingreso.objects.select_related('venta').all().order_by('-fecha')

    for ingreso in ingresos:
        total = sum(detalle.subtotal() for detalle in ingreso.venta.detalles.all())
        ingreso.monto = total  # Calculamos el monto dinámicamente

    return render(request, 'finanzas/listar_ingresos.html', {'ingresos': ingresos})


@login_required
def listar_egresos(request):
    egresos_pedidos = Egreso.objects.filter(tipo='pedido').select_related('pedido').order_by('-fecha')
    egresos_personalizados = Egreso.objects.filter(tipo='personalizado').order_by('-fecha')
    return render(request, 'finanzas/listar_egresos.html', {
        'egresos_pedidos': egresos_pedidos,
        'egresos_personalizados': egresos_personalizados,
    })


@login_required
def detalle_ingreso(request, ingreso_id):
    ingreso = Ingreso.objects.get(id=ingreso_id)
    detalles = ingreso.venta.detalles.all()  # Obtener los detalles de la venta
    total = sum(detalle.subtotal() for detalle in detalles)

    context = {
        'ingreso': ingreso,
        'detalles': detalles,
        'total': total,  # Total calculado de la venta
    }
    return render(request, 'finanzas/detalle_ingreso.html', context)


from django.shortcuts import get_object_or_404


@login_required
def detalle_egreso(request, egreso_id):
    egreso = get_object_or_404(Egreso, id=egreso_id)

    # Si el egreso está asociado a un pedido, obtenemos los detalles del pedido
    if egreso.tipo == 'pedido' and egreso.pedido is not None:
        detalles = egreso.pedido.detalles()
        total = sum(detalle.subtotal() for detalle in detalles)
    else:
        detalles = None  # Los egresos personalizados no tienen detalles asociados
        total = egreso.monto  # En este caso, solo mostramos el monto del egreso personalizado

    context = {
        'egreso': egreso,
        'detalles': detalles,
        'total': total,
    }
    return render(request, 'finanzas/detalle_egreso.html', context)


# app_finanzas/views.py
from django.shortcuts import redirect
from .forms import EgresoForm

@login_required
def crear_egreso_personalizado(request):
    if request.method == 'POST':
        form = EgresoForm(request.POST)
        if form.is_valid():
            egreso = form.save(commit=False)
            if egreso.tipo == 'personalizado':
                egreso.pedido = None  # Asegura que no esté asociado a un pedido
            egreso.save()
            return redirect('listar_egresos')
    else:
        form = EgresoForm()
    return render(request, 'finanzas/crear_egreso_personalizado.html', {'form': form})
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

@login_required
def eliminar_egreso_personalizado(request, egreso_id):
    egreso = get_object_or_404(Egreso, id=egreso_id, tipo='personalizado')
    egreso.delete()
    messages.success(request, 'Egreso personalizado eliminado exitosamente.')
    return redirect('listar_egresos')
