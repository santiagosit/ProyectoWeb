from django import forms
from .models import Ingreso, Egreso

class IngresoForm(forms.ModelForm):
    class Meta:
        model = Ingreso
        fields = ['venta', 'monto', 'descripcion']
        widgets = {
            'venta': forms.Select(attrs={'class': 'form-control'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

# app_finanzas/forms.py
class EgresoForm(forms.ModelForm):
    class Meta:
        model = Egreso
        fields = ['tipo', 'pedido', 'monto', 'descripcion', 'categoria']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'pedido': forms.Select(attrs={'class': 'form-control'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'categoria': forms.TextInput(attrs={'class': 'form-control'}),
        }
