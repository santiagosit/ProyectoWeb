from django import forms
from .models import Pedido, PedidoDetalle

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['proveedor', 'estado']

class PedidoDetalleForm(forms.ModelForm):
    class Meta:
        model = PedidoDetalle
        fields = ['producto', 'cantidad', 'costo_unitario']

from django import forms
from .models import Proveedor

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'direccion', 'telefono', 'email']
