
from datetime import date
import datetime
from django import forms
from django.forms import DateTimeInput, EmailInput, ModelForm, DateInput, TextInput
from django.forms.models import inlineformset_factory, modelformset_factory
from .models import *

class PrecioHMedicamentoForm(ModelForm):
    class Meta: 
        model = PrecioHMedicamento
        fields = ['precio']
        widgets = {
            'precio': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Precio'
            }),
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

class MedicamentosForm(forms.ModelForm):
    class Meta:
        model = Medicamentos
        fields = ['nombre', 'ingredientes']
        widgets = {
                    'nombre': TextInput(attrs={
                        'class': "form-control",
                        'style': 'max-width: 300px;',
                        'placeholder': 'Nombre'
                    }),

                    'ingredientes': TextInput(attrs={
                        'class': "form-control",
                        'style': 'max-width: 300px;',
                        'placeholder': 'Ingredientes'
                    }),
                }

    def clean_txtNombre(self):
        nombre = self.cleaned_data.get('txtNombre')
        if not nombre or not nombre.isalpha():
            raise ValidationError('Nombre solo puede contener letras')
        return nombre

    def clean_txtIngredientes(self):
        ingredientes = self.cleaned_data.get('txtIngredientes')
        if not ingredientes or ingredientes.isdigit() or ingredientes.isspace():
            raise ValidationError('Casilla de ingredientes no puede estar vacía y no puede contener solo números o espacios')
        return ingredientes


class CompraMedicamentoForm(forms.ModelForm):
    class Meta:
        model = CompraMedicamento
        fields = '__all__'
        widgets = {
            'fechaPedido': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'style': 'max-width: 300px;',
            }),
            'fechaRecibido': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'style': 'max-width: 300px;',
            }),
            'fechaDespacho': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'style': 'max-width: 300px;',
            }),
            'proveedor': forms.Select(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
            }),
            'precioTotal': forms.NumberInput(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
            }),
            'estadoCompra': forms.Select(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
            }),
            'numeroFactura': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
            }),
        }

class DetallePedidoForm(forms.ModelForm):
    # Assume each detail can optionally create a LoteMedicamento
    class Meta:
        model = DetallePedido
        fields = [ 'cantidad']
        widgets = {
            'cantidad': forms.Select(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
            })
        }

DetallePedidoFormSet = inlineformset_factory(
    CompraMedicamento,
    DetallePedido,
    form=DetallePedidoForm,
    extra=1,
    can_delete=True
)

class LoteForm(forms.ModelForm):
    class Meta:
        model = LoteMedicamento
        fields = '__all__'
        widgets = {
            'fechaVencimiento': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'style': 'max-width: 300px;',
            }),
            'medicamento': forms.Select(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
            })
        }


LoteFormSet = modelformset_factory(
    LoteMedicamento,
    form=LoteForm,
    extra=1,
    can_delete=True
)
         

class MetodosPagoForm(forms.ModelForm):
    class Meta: 
        model = MetodosPago
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
            })
        }

    

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre').strip()  # Using strip() to remove leading/trailing whitespace

        # Check if the nombre is less than 3 characters
        if len(nombre) < 3:
            raise forms.ValidationError("El nombre debe tener al menos 3 caracteres.")

        # Check if the nombre contains only spaces (after stripping whitespace)
        if not nombre:
            raise forms.ValidationError("El nombre no puede estar vacío.")

        # Check if the nombre contains only letters
        if not nombre.isalpha():
            raise forms.ValidationError("El nombre solo puede contener letras.")

        # Check for uniqueness of nombre
        if MetodosPago.objects.filter(nombre__iexact=nombre).exists():
            raise forms.ValidationError("El nombre ya existe. Por favor, elige otro nombre.")

        return nombre
    
class TipoDocumentoForm(ModelForm):
    class Meta: 
        model = TipoDocumento
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
            })
        }
        

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
    
  # Adjust this import based on your project structure

class CargosForm(ModelForm):
    class Meta:
        model = Cargos
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
            }),
            
            'descripcion': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
            })
        }

    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get('nombre')
        descripcion = cleaned_data.get('descripcion')

        # Validation for nombre
        if nombre:
            if len(nombre) < 3:
                self.add_error('nombre', "El nombre debe tener al menos 3 caracteres.")
            if nombre.isspace():
                self.add_error('nombre', "El nombre no puede contener solo espacios.")

            if not nombre.replace(" ", "").isalpha():  # Allows spaces within the name but checks the rest for alphabetic characters
                self.add_error('nombre', "El nombre solo puede contener letras.")
        
        # Validation for descripcion
        if descripcion:
            if len(descripcion) < 3:
                self.add_error('descripcion', "La descripcion debe tener al menos 3 caracteres.")
            if descripcion.isspace():
                self.add_error('descripcion', "La descripcion no puede contener solo espacios.")
            if descripcion.isdigit():
                self.add_error('descripcion', "La descripcion no puede contener solo números.")
        
        return cleaned_data


class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = '__all__'
        widgets = {
            'tipodocumento': forms.Select(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;'
            }),
            'informacion': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Informacion'
            }),
        }


class EmpleadosForm(forms.ModelForm):
    class Meta:
        model = Empleados
        fields = ['nombre','fechaNacimiento','telefono','correoElectronico','direccion','cargo',]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
                'placeholder': 'Nombre',
            }),
            'fechaNacimiento': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'style': 'max-width: 300px;',
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
                'placeholder': 'Teléfono',
            }),
            'correoElectronico': forms.EmailInput(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
                'placeholder': 'Correo Electrónico',
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
                'placeholder': 'Dirección',
            }),
            'cargo': forms.Select(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
            }),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not nombre.replace(" ", "").isalpha():  # Allows spaces within the name but checks the rest for alphabetic characters
            raise forms.ValidationError("El nombre solo puede contener letras.")
        if nombre.isspace() or len(nombre) < 3:
            raise forms.ValidationError("El nombre debe tener al menos 3 caracteres y no puede estar vacío.")
        return nombre

    def clean_fechaNacimiento(self):
        fechaNacimiento = self.cleaned_data.get('fechaNacimiento')
        today = date.today()
        age = today.year - fechaNacimiento.year - ((today.month, today.day) < (fechaNacimiento.month, fechaNacimiento.day))
        if age < 18 or age > 100:
            raise forms.ValidationError("El empleado debe tener 18 años o más y menos de 100 años.")
        return fechaNacimiento

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if not telefono.isdigit():
            raise forms.ValidationError("El teléfono debe contener solo dígitos.")
        if len(telefono) != 8:
            raise forms.ValidationError("El teléfono debe tener exactamente 8 dígitos.")
        if telefono[0] not in ['2', '3', '8', '9']:
            raise forms.ValidationError("El teléfono debe comenzar con 22, 3, 8, o 9.")
        return telefono

    def clean_correoElectronico(self):
        correoElectronico = self.cleaned_data.get('correoElectronico')
        pattern = r"[^@]+@[^@]+\.[^@]+"
        if not re.match(pattern, correoElectronico):
            raise forms.ValidationError("Correo electrónico inválido.")
        parts = correoElectronico.split('@')[1].split('.')
        if len(parts[0]) < 2 or len(parts[1]) < 2:
            raise forms.ValidationError("El correo electrónico debe tener al menos 2 caracteres después del @ y al menos 2 caracteres después del punto.")
        return correoElectronico

    def clean_direccion(self):
        direccion = self.cleaned_data.get('direccion')
        if len(direccion) < 6:
            raise forms.ValidationError("La dirección debe tener al menos 6 caracteres.")
        if re.match("^[0-9]|[^A-Za-z0-9 ]", direccion):
            raise forms.ValidationError("La dirección no puede tener números ni caracteres especiales al inicio.")
        return direccion

class TipoSalasForm(ModelForm):
    class Meta:
        model = TipoSalas
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
            })
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not nombre.replace(" ", "").isalpha():  # Allows spaces within the name but checks the rest for alphabetic characters
            raise forms.ValidationError("El nombre solo puede contener letras.")
        if nombre.isspace() or len(nombre) < 3:
            raise forms.ValidationError("El nombre debe tener al menos 3 caracteres y no puede estar vacío.")
        return nombre



class SalasForm(ModelForm):
    class Meta:
        model = Salas
        fields = '__all__' 
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
                'placeholder': 'Nombre',
            }),
            'tipoSalas': forms.Select(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
            }),
            'surcursal': forms.Select(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
            }),
        } 

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre.isspace() or len(nombre) < 3:
            raise forms.ValidationError("El nombre debe tener al menos 3 caracteres y no puede estar vacío.")
        return nombre
      
class PacientesForm(forms.ModelForm):
    class Meta:
        model = Pacientes

        fields = ['nombre','fechaDeNacimiento','telefono','correoElectronico','direccion','genero']
       
        widgets = {
            'nombre': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Name'
            }),
            'fechaDeNacimiento': DateInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'type': 'date'  # Ensure the input type is set to date
            }),
            'telefono': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Phone Number'
            }),
            'correoElectronico': EmailInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Email'
            }),
            'direccion': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Address'
            }),
            'genero': forms.Select(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;'
            })  
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not nombre.replace(" ", "").isalpha():  # Allows spaces within the name but checks the rest for alphabetic characters
            raise forms.ValidationError("El nombre solo puede contener letras.")
        if nombre.isspace() or len(nombre) < 3:
            raise forms.ValidationError("El nombre debe tener al menos 3 caracteres y no puede estar vacío.")
        return nombre

    def clean_fechaDeNacimiento(self):
        fechaDeNacimiento = self.cleaned_data.get('fechaDeNacimiento')
        if fechaDeNacimiento:
            if fechaDeNacimiento > datetime.date.today():
                raise forms.ValidationError("La fecha de nacimiento no puede ser en el futuro.")
        return fechaDeNacimiento

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if not telefono.isdigit():
            raise forms.ValidationError("El teléfono debe contener solo dígitos.")
        if len(telefono) != 8:
            raise forms.ValidationError("El teléfono debe tener exactamente 8 dígitos.")
        if telefono[0] not in ['2', '3', '8', '9']:
            raise forms.ValidationError("El teléfono debe comenzar con 22, 3, 8, o 9.")
        return telefono

    def clean_correoElectronico(self):
        correoElectronico = self.cleaned_data.get('correoElectronico')
        pattern = r"[^@]+@[^@]+\.[^@]+"
        if not re.match(pattern, correoElectronico):
            raise forms.ValidationError("Correo electrónico inválido.")
        parts = correoElectronico.split('@')[1].split('.')
        if len(parts[0]) < 2 or len(parts[1]) < 2:
            raise forms.ValidationError("El correo electrónico debe tener al menos 2 caracteres después del @ y al menos 2 caracteres después del punto.")
        return correoElectronico

    def clean_direccion(self):
        direccion = self.cleaned_data.get('direccion')
        if len(direccion) < 6:
            raise forms.ValidationError("La dirección debe tener al menos 6 caracteres.")
        if re.match("^[0-9]|[^A-Za-z0-9 ]", direccion):
            raise forms.ValidationError("La dirección no puede tener números ni caracteres especiales al inicio.")
        return direccion
    
class CitasForm(ModelForm):
    class Meta: 
        model = Citas
        fields = '__all__'
        widgets = {
        'fecha': DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class CitasForm(ModelForm):
    class Meta: 
        model = Citas
        fields = '__all__'
        widgets = {
            'fecha': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
                'type': 'datetime-local',  # Change input type to datetime-local
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
                'rows': 3,  # Set the number of rows for the textarea
                'placeholder': 'Descripción',
            }),
            'paciente': forms.Select(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
            }),
            'medico': forms.Select(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
            }),
            'sala': forms.Select(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
            }),
            'surcursal': forms.Select(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
            }),
        }

    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        now = datetime.datetime.now(datetime.timezone.utc)
        if fecha <= now:
            raise ValidationError("La fecha de la cita debe estar en el futuro.")
        if fecha.minute != 0 or fecha.second != 0:
            raise ValidationError("La cita debe ser programada a la hora en punto.")
        if not (7 <= fecha.hour < 17):
            raise ValidationError("La cita debe ser entre las 7:00 AM y las 5:00 PM.")
        return fecha

    def __init__(self, *args, **kwargs):
        super(CitasForm, self).__init__(*args, **kwargs)
        # Adjust the queryset for the 'medico' field to include only employees with cargo_id = 4
        self.fields['medico'].queryset = Empleados.objects.filter(cargo=4)

    def clean(self):
        cleaned_data = super().clean()
        medico = cleaned_data.get('medico')
        fecha = cleaned_data.get('fecha')

        # Check for overlapping appointments
        if medico and fecha:
            overlapping_citas = Citas.objects.filter(
                medico=medico,
                fecha__year=fecha.year,
                fecha__month=fecha.month,
                fecha__day=fecha.day,
                fecha__hour=fecha.hour
            ).exclude(id=self.instance.id if self.instance.id else None)
            if overlapping_citas.exists():
                raise ValidationError("Ya existe una cita para este médico a la misma hora.")

    def save(self, commit=True):
        instance = super().save(commit=False)
        if instance.fecha:
            instance.fecha_fin = instance.fecha + datetime.timedelta(hours=1)
        if commit:
            instance.save()
        return instance
    

class DetallePrescripcionesForm(forms.ModelForm):
    class Meta:
        model = DetallePrescripciones
        fields = '__all__'
        widgets = {
            'medicamento': forms.Select(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
            }),
            'prescripcion': forms.Select(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
            }),
        }
        
class PrescripcionesForm(forms.ModelForm):
    class Meta:
        model =  Prescripciones
        fields = '__all__'
        widgets = {
            'indicaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
                'rows': 3,  # Set the number of rows for the textarea
            }),
            'fecha': forms.DateInput(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
                'type': 'date',  # Change input type to date
            }),
            'cita': forms.Select(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        indicaciones = cleaned_data.get('indicaciones')

        # Validation for indicaciones
        if indicaciones:
            if len(indicaciones) < 3:
                self.add_error('indicaciones', "La indicaciones debe tener al menos 3 caracteres.")
            if indicaciones.isspace():
                self.add_error('indicaciones', "La indicaciones no puede contener solo espacios.")
            if indicaciones.isdigit():
                self.add_error('indicaciones', "La indicaciones no puede contener solo números.")
        
        return cleaned_data
    

class   OrdenesMedicasForm(forms.ModelForm):
    class Meta:
        model =  OrdenesMedicas
        fields = '__all__'
        widgets = {
            'indicaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
                'rows': 4,  # Adjust the number of rows as needed
            }),
            'fecha': forms.DateInput(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
                'type': 'date',
            }),
            'cita': forms.Select(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        indicaciones = cleaned_data.get('indicaciones')

        # Validation for indicaciones
        if indicaciones:
            if len(indicaciones) < 3:
                self.add_error('indicaciones', "La indicaciones debe tener al menos 3 caracteres.")
            if indicaciones.isspace():
                self.add_error('indicaciones', "La indicaciones no puede contener solo espacios.")
            if indicaciones.isdigit():
                self.add_error('indicaciones', "La indicaciones no puede contener solo números.")
        
        return cleaned_data


class   HistorialClinicoForm(forms.ModelForm):
    class Meta:
        model =  HistorialClinico
        fields = '__all__'

class   QuejasYSugerenciasForm(forms.ModelForm):
    class Meta:
        model =  QuejasYSugerencias
        fields = '__all__'

class ParametrosForm(forms.ModelForm):
    class Meta:
        model = Parametros
        fields = '__all__'
        widgets = {
            'surcursal': forms.Select(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
            }),
            'cai': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
                'placeholder': 'CAI',
            }),
            'rtn': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
                'placeholder': 'RTN',
            }),
            'razonSocial': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
                'placeholder': 'Razón Social',
            }),
            'nombreEmpresa': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
                'placeholder': 'Nombre de la Empresa',
            }),
            'rangoAutorizadoInicial': forms.NumberInput(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
                'placeholder': 'Rango Autorizado Inicial',
            }),
            'rangoAutorizadoFinal': forms.NumberInput(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
                'placeholder': 'Rango Autorizado Final',
            }),
            'fechaLimiteEmision': forms.DateInput(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
                'type': 'date',
            }),
            'correoElectronico': forms.EmailInput(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
                'placeholder': 'Correo Electrónico',
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
                'placeholder': 'Teléfono',
            }),
        }
    def clean(self):
        cleaned_data = super().clean()
        surcursal = cleaned_data.get("surcursal")
        if Parametros.objects.filter(surcursal=surcursal).exists():
            raise forms.ValidationError("Ya existe parametro con esa surcursal.")
        return cleaned_data

class ParametrosEditForm(forms.ModelForm):
    class Meta:
        model = Parametros
        fields = '__all__'
        widgets = {
            'surcursal': forms.Select(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
            }),
            'cai': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
                'placeholder': 'CAI',
            }),
            'rtn': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
                'placeholder': 'RTN',
            }),
            'razonSocial': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
                'placeholder': 'Razón Social',
            }),
            'nombreEmpresa': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
                'placeholder': 'Nombre de la Empresa',
            }),
            'rangoAutorizadoInicial': forms.NumberInput(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
                'placeholder': 'Rango Autorizado Inicial',
            }),
            'rangoAutorizadoFinal': forms.NumberInput(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
                'placeholder': 'Rango Autorizado Final',
            }),
            'fechaLimiteEmision': forms.DateInput(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
                'type': 'date',
            }),
            'correoElectronico': forms.EmailInput(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
                'placeholder': 'Correo Electrónico',
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
                'placeholder': 'Teléfono',
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        instance = self.instance
        surcursal = cleaned_data.get('surcursal')
        if instance and surcursal:
            if instance.surcursal != surcursal:
                self.add_error('surcursal', "You cannot change the surcursal.")
        return cleaned_data