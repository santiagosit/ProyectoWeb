from django import forms
from .models import Venta, VentaDetalle
from  app_inventario.models import Producto

VentaDetalleFormSet = forms.inlineformset_factory(
    Venta, VentaDetalle, fields=['producto', 'cantidad', 'precio_unitario'], extra=1, can_delete=True
)


class VentaForm(forms.ModelForm):
    fecha = forms.DateTimeField(
        label="Fecha de la venta",
        input_formats=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"],
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    class Meta:
        model = Venta
        fields = ['fecha', 'observaciones']
