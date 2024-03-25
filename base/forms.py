from datetime import date
from django import forms
from django.forms import ModelForm, DateInput
from .models import MetodosPago, PrecioHMedicamento, TipoDocumento

class PrecioHMedicamentoForm(ModelForm):
    class Meta: 
        model = PrecioHMedicamento
        fields = '__all__'
        widgets = {
            'fechaInicio': DateInput(attrs={'type': 'date'}),
            'fechaFinal': DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        medicamento = cleaned_data.get('medicamento')
        precio = cleaned_data.get('precio')
        fecha_inicio = cleaned_data.get('fechaInicio')
        fecha_final = cleaned_data.get('fechaFinal')
        today = date.today()

        # Check if fechaInicio is later than today
        if fecha_inicio and fecha_inicio > today:
            raise forms.ValidationError("La fecha de inicio no puede ser posterior a hoy.")

        # Check if fechaFinal is later than today
        if fecha_final and fecha_final > today:
            raise forms.ValidationError("La fecha final no puede ser posterior a hoy.")

        # Check if the current price is the same as the last one for the medication
        if medicamento:
            last_price = PrecioHMedicamento.objects.filter(medicamento=medicamento).order_by('-fechaInicio').first()
            if last_price and last_price.precio == precio:
                raise forms.ValidationError("El precio no puede ser igual al último precio registrado para este medicamento.")

        return cleaned_data
from django import forms
from django.forms import inlineformset_factory, ModelForm
from .models import CompraMedicamento, DetallePedido, Medicamentos
from .models import CompraMedicamento, DetallePedido

class CompraMedicamentoForm(forms.ModelForm):
    class Meta:
        model = CompraMedicamento
        fields = '__all__'
        widgets = {
            'fechaPedido': forms.DateInput(attrs={'type': 'date'}),
            'fechaRecibido': forms.DateInput(attrs={'type': 'date'}),
            'fechaDespacho': forms.DateInput(attrs={'type': 'date'}),
        }

class DetallePedidoForm(forms.ModelForm):
    class Meta:
        model = DetallePedido
        fields = ['medicamento', 'cantidad']

DetallePedidoFormSet = forms.inlineformset_factory(
    CompraMedicamento,
    DetallePedido,
    form=DetallePedidoForm,
    extra=1,
    can_delete=True
)

class MetodosPagoForm(ModelForm):
    class Meta: 
        model = MetodosPago
        fields = '__all__'

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')

        # Check if the nombre is less than 3 characters
        if len(nombre) < 3:
            raise forms.ValidationError("El nombre debe tener al menos 3 caracteres.")

        # Check if the nombre contains only tabs
        if nombre.isspace():
            raise forms.ValidationError("El nombre no puede contener solo espacios.")

        # Check if the nombre contains only numbers
        if nombre.isdigit():
            raise forms.ValidationError("El nombre no puede contener solo números.")

        return nombre
    
class TipoDocumentoForm(ModelForm):
    class Meta: 
        model = TipoDocumento
        fields = '__all__'

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')

        # Check if the nombre is less than 3 characters
        if len(nombre) < 3:
            raise forms.ValidationError("El nombre debe tener al menos 3 caracteres.")

        # Check if the nombre contains only tabs
        if nombre.isspace():
            raise forms.ValidationError("El nombre no puede contener solo espacios.")

        # Check if the nombre contains only numbers
        if nombre.isdigit():
            raise forms.ValidationError("El nombre no puede contener solo números.")

        return nombre
