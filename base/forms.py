
from datetime import date
import datetime
from django import forms
from django.forms import DateTimeInput, EmailInput, ModelForm, DateInput, TextInput
from django.forms.models import inlineformset_factory, modelformset_factory
from .models import *
import pytz

class ECMedicamentosForm(ModelForm):
    class Meta:
        model = ECMedicamentos
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

        # Check for uniqueness of nombre
        if TipoSalas.objects.filter(nombre__iexact=nombre).exists():
            raise forms.ValidationError("Una sala con este nombre ya existe.")
        return nombre


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

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio is not None and precio <= 0:
            raise forms.ValidationError("El precio no puede ser menor que 0.")
        return precio    


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

    def __init__(self, *args, **kwargs):
        super(CompraMedicamentoForm, self).__init__(*args, **kwargs)
        estado_choices = self.fields['estadoCompra'].choices
        # Assuming 'Aprobado' is one of the options and you know its value, e.g., 'aprobado'
        filtered_choices = [choice for choice in estado_choices if choice[0] not in (8, 9)]
        self.fields['estadoCompra'].choices = filtered_choices

    def clean_precioTotal(self):
        precio_total = self.cleaned_data.get('precioTotal')
        if precio_total is not None and precio_total <= 0:
            raise forms.ValidationError("El precio total no puede ser menor que 0.")
        return precio_total

class EditCompraMedicamentoForm(forms.ModelForm):
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

    def clean(self):
        cleaned_data = super().clean()
        estado_compra = cleaned_data.get('estadoCompra')
        fecha_recibido = cleaned_data.get('fechaRecibido')
        fecha_despacho = cleaned_data.get('fechaDespacho')

        if estado_compra and estado_compra.id == 8:
            if not fecha_recibido:
                self.add_error('fechaRecibido', 'La fecha de recibido es obligatoria.')
            if not fecha_despacho:
                self.add_error('fechaDespacho', 'La fecha de despacho es obligatoria.')

        return cleaned_data

    def clean_precioTotal(self):
            precio_total = self.cleaned_data.get('precioTotal')
            if precio_total is not None and precio_total <= 0:
                raise forms.ValidationError("El precio total no puede ser menor que 0.")
            return precio_total


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
            }),
             'compra': forms.Select(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
            }),
            'cantidad': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
            })
        
        }

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad is not None and cantidad < 1:
            raise forms.ValidationError("La cantidad no puede ser menor que 1.")
        return cantidad
    
    def clean_fechaVencimiento(self):
        fecha_vencimiento = self.cleaned_data.get('fechaVencimiento')
        if fecha_vencimiento <= timezone.now().date():
            raise forms.ValidationError("La fecha de vencimiento debe ser posterior a hoy.")
        return fecha_vencimiento


         

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
        nombre = self.cleaned_data.get('nombre')
        if not nombre.replace(" ", "").isalpha():  # Allows spaces within the name but checks the rest for alphabetic characters
            raise forms.ValidationError("El nombre solo puede contener letras.")
        if nombre.isspace() or len(nombre) < 3:
            raise forms.ValidationError("El nombre debe tener al menos 3 caracteres y no puede estar vacío.")

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
        if not nombre.replace(" ", "").isalpha():  # Allows spaces within the name but checks the rest for alphabetic characters
            raise forms.ValidationError("El nombre solo puede contener letras.")
        if nombre.isspace() or len(nombre) < 3:
            raise forms.ValidationError("El nombre debe tener al menos 3 caracteres y no puede estar vacío.")
    
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

    def clean(self):
        cleaned_data = super().clean()
        tipodocumento = cleaned_data.get('tipodocumento')
        informacion = cleaned_data.get('informacion')

        if tipodocumento == 1: 
            if not (informacion.isdigit() and len(informacion) == 13):
                raise ValidationError({
                    'informacion': "Para el tipo de documento Identidad, la información debe tener exactamente 13 dígitos."
                })

        return cleaned_data


class EmpleadosForm(forms.ModelForm):
    class Meta:
        model = Empleados
        fields = ['nombre','fechaNacimiento','telefono','correoElectronico','direccion','cargo','estado']
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
            'estado': forms.Select(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
                'placeholder': 'Nombre',
            })
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
        instance = self.instance
        if Empleados.objects.filter(telefono=telefono).exclude(id=instance.id).exists():
            raise ValidationError("Este teléfono ya está registrado.")
        if not telefono.isdigit():
            raise ValidationError("El teléfono debe contener solo dígitos.")
        if len(telefono) != 8:
            raise ValidationError("El teléfono debe tener exactamente 8 dígitos.")
        if telefono[0] not in ['2', '3', '8', '9']:
            raise ValidationError("El teléfono debe comenzar con 22, 3, 8, o 9.")
        return telefono

    def clean_correoElectronico(self):
        correoElectronico = self.cleaned_data.get('correoElectronico')
        instance = self.instance
        if Empleados.objects.filter(correoElectronico=correoElectronico).exclude(id=instance.id).exists():
            raise ValidationError("Este correo electrónico ya está registrado.")
        pattern = r"[^@]+@[^@]+\.[^@]+"
        if not re.match(pattern, correoElectronico):
            raise ValidationError("Correo electrónico inválido.")
        pattern1 = r"[^@]+@[^@]+\.[a-zA-Z]{1,3}$"  # New pattern to match maximum of 3 letters after the .
        if not re.match(pattern1, correoElectronico):
            raise ValidationError("Correo electrónico inválido.")
        parts = correoElectronico.split('@')[1].split('.')
        if len(parts[0]) < 2 or len(parts[1]) < 2:
            raise ValidationError("El correo electrónico debe tener al menos 2 caracteres después del @ y al menos 2 caracteres después del punto.")
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

        # Check for uniqueness of nombre
        if TipoSalas.objects.filter(nombre__iexact=nombre).exists():
            raise forms.ValidationError("Una sala con este nombre ya existe.")
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
        
        if Salas.objects.filter(nombre=nombre).exists():
            raise ValidationError("Una sala con este nombre ya existe.")
        
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
        instance = self.instance
        if Pacientes.objects.filter(telefono=telefono).exclude(id=instance.id).exists():
            raise ValidationError("Este teléfono ya está registrado.")
        if not telefono.isdigit():
            raise ValidationError("El teléfono debe contener solo dígitos.")
        if len(telefono) != 8:
            raise ValidationError("El teléfono debe tener exactamente 8 dígitos.")
        if telefono[0] not in ['2', '3', '8', '9']:
            raise ValidationError("El teléfono debe comenzar con 22, 3, 8, o 9.")
        return telefono

    def clean_correoElectronico(self):
        correoElectronico = self.cleaned_data.get('correoElectronico')
        instance = self.instance
        if Pacientes.objects.filter(correoElectronico=correoElectronico).exclude(id=instance.id).exists():
            raise ValidationError("Este correo electrónico ya está registrado.")
        pattern = r"[^@]+@[^@]+\.[^@]+"
        if not re.match(pattern, correoElectronico):
            raise ValidationError("Correo electrónico inválido.")
        pattern1 = r"[^@]+@[^@]+\.[a-zA-Z]{1,3}$"  # New pattern to match maximum of 3 letters after the .
        if not re.match(pattern1, correoElectronico):
            raise ValidationError("Correo electrónico inválido.")
        parts = correoElectronico.split('@')[1].split('.')
        if len(parts[0]) < 2 or len(parts[1]) < 2:
            raise ValidationError("El correo electrónico debe tener al menos 2 caracteres después del @ y al menos 2 caracteres después del punto.")
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
            'tipocita': forms.Select(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
            })
        }

    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        tz = pytz.timezone('America/Costa_Rica')
        now = timezone.now().astimezone(tz)
        if fecha.date() == now.date() and fecha.hour <= now.hour:

            raise ValidationError(f"La cita para hoy debe ser al menos una hora después de la hora actual ({now.hour}:00).")
        if fecha.minute != 0 or fecha.second != 0:
            raise ValidationError("La cita debe ser programada a la hora en punto.")
        if not (7 <= fecha.hour < 17):
            raise ValidationError("La cita debe ser entre las 7:00 AM y las 5:00 PM.")
        return fecha

    def __init__(self, *args, **kwargs):
        super(CitasForm, self).__init__(*args, **kwargs)
        # Adjust the queryset for the 'medico' field to include only employees with cargo_id = 4 and estado = 'Activo'
        self.fields['medico'].queryset = Empleados.objects.filter(cargo=4, estado='A')

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
            'cantidad': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
            })
        
        }

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad is not None and cantidad < 1:
            raise forms.ValidationError("La cantidad no puede ser menor que 1.")
        return cantidad
    
        
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
            'cita': forms.Select(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
            }),
        }
    def clean_indicaciones(self):
        indicaciones = self.cleaned_data.get('indicaciones')
        if indicaciones:
            if len(indicaciones) < 3:
                self.add_error('indicaciones', "La indicaciones debe tener al menos 3 caracteres.")
            if indicaciones.isspace():
                self.add_error('indicaciones', "La indicaciones no puede contener solo espacios.")
            if indicaciones.isdigit():
                self.add_error('indicaciones', "La indicaciones no puede contener solo números.")
        return indicaciones
    
    

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


class   TipoCitasForm(forms.ModelForm):
    class Meta:
        model =  TipoCitas
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
            })
        }
    def clean_precio(self):
            precio = self.cleaned_data.get('precio')
            if precio is not None and precio <= 0:
                raise forms.ValidationError("El precio total no puede ser menor que 0.")
            return precio
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not nombre.replace(" ", "").isalpha():  # Allows spaces within the name but checks the rest for alphabetic characters
            raise forms.ValidationError("El nombre solo puede contener letras.")
        if nombre.isspace() or len(nombre) < 3:
            raise forms.ValidationError("El nombre debe tener al menos 3 caracteres y no puede estar vacío.")

        # Check for uniqueness of nombre
        if TipoSalas.objects.filter(nombre__iexact=nombre).exists():
            raise forms.ValidationError("Una sala con este nombre ya existe.")
        return nombre
        


class   QuejasYSugerenciasForm(forms.ModelForm):
    class Meta:
        model =  QuejasYSugerencias
        fields = '__all__'
        widgets = {
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
                'rows': 4,  # Adjust the number of rows as needed
            }),
            'fecha': forms.DateInput(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
                'type': 'date',
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
            }),
        }

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
            })
        }
    def clean(self):
        cleaned_data = super().clean()
        surcursal = cleaned_data.get("surcursal")
        if Parametros.objects.filter(surcursal=surcursal).exists():
            raise forms.ValidationError("Ya existe parametro con esa surcursal.")
        return cleaned_data
    
    def clean_cai(self):
        cai = self.cleaned_data.get('cai')
        if not cai.isalnum() or len(cai) != 32:
            raise forms.ValidationError("El CAI debe tener exactamente 32 caracteres alfanuméricos.")
        return cai

    def clean_rtn(self):
        rtn = self.cleaned_data.get('rtn')
        if not rtn.isdigit() or len(rtn) != 13:
            raise forms.ValidationError("El RTN debe tener exactamente 13 dígitos.")
        return rtn

    def clean_razonSocial(self):
        return self.validate_company_name(self.cleaned_data.get('razonSocial'))

    def clean_nombreEmpresa(self):
        return self.validate_company_name(self.cleaned_data.get('nombreEmpresa'))

    def validate_company_name(self, name):
        if not name:
            raise forms.ValidationError("Este campo es obligatorio.")
        if any(char.isdigit() for char in name):
            raise forms.ValidationError("El nombre no debe contener números.")
        return name

    def clean_rangoAutorizadoInicial(self):
        inicial = self.cleaned_data.get('rangoAutorizadoInicial')
        if inicial <= 0:
            raise forms.ValidationError("El rango autorizado inicial debe ser mayor que 0.")
        return inicial

    def clean_rangoAutorizadoFinal(self):
        final = self.cleaned_data.get('rangoAutorizadoFinal')
        inicial = self.cleaned_data.get('rangoAutorizadoInicial')
        if final <= 0:
            raise forms.ValidationError("El rango autorizado final debe ser mayor que 0.")
        if final <= inicial:
            raise forms.ValidationError("El rango autorizado final debe ser mayor que el inicial.")
        return final

    def clean_fechaLimiteEmision(self):
        fecha = self.cleaned_data.get('fechaLimiteEmision')
        if fecha <= timezone.now().date():
            raise forms.ValidationError("La fecha límite de emisión debe ser posterior a hoy.")
        return fecha
    
    def clean_correoElectronico(self):
        correoElectronico = self.cleaned_data.get('correoElectronico')
        instance = self.instance
        if Pacientes.objects.filter(correoElectronico=correoElectronico).exclude(id=instance.id).exists():
            raise ValidationError("Este correo electrónico ya está registrado.")
        pattern = r"[^@]+@[^@]+\.[^@]+"
        if not re.match(pattern, correoElectronico):
            raise ValidationError("Correo electrónico inválido.")
        pattern1 = r"[^@]+@[^@]+\.[a-zA-Z]{1,3}$"  # New pattern to match maximum of 3 letters after the .
        if not re.match(pattern1, correoElectronico):
            raise ValidationError("Correo electrónico inválido.")
        parts = correoElectronico.split('@')[1].split('.')
        if len(parts[0]) < 2 or len(parts[1]) < 2:
            raise ValidationError("El correo electrónico debe tener al menos 2 caracteres después del @ y al menos 2 caracteres después del punto.")
        return correoElectronico


    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        instance = self.instance
        if Pacientes.objects.filter(telefono=telefono).exclude(id=instance.id).exists():
            raise ValidationError("Este teléfono ya está registrado.")
        if not telefono.isdigit():
            raise ValidationError("El teléfono debe contener solo dígitos.")
        if len(telefono) != 8:
            raise ValidationError("El teléfono debe tener exactamente 8 dígitos.")
        if telefono[0] not in ['2', '3', '8', '9']:
            raise ValidationError("El teléfono debe comenzar con 22, 3, 8, o 9.")
        return telefono

    

class ParametrosEditForm(forms.ModelForm):
    class Meta:
        model = Parametros
        fields = ['cai', 'rtn','razonSocial', 'nombreEmpresa','rangoAutorizadoInicial', 'rangoAutorizadoFinal','fechaLimiteEmision', 'correoElectronico','telefono']
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
            })
        }

    def clean(self):
        cleaned_data = super().clean()
        instance = self.instance
        surcursal = cleaned_data.get('surcursal')
        if instance and surcursal:
            if instance.surcursal != surcursal:
                self.add_error('surcursal', "You cannot change the surcursal.")
        return cleaned_data
    
    def clean_cai(self):
        cai = self.cleaned_data.get('cai')
        if not cai.isalnum() or len(cai) != 32:
            raise forms.ValidationError("El CAI debe tener exactamente 32 caracteres alfanuméricos.")
        return cai

    def clean_rtn(self):
        rtn = self.cleaned_data.get('rtn')
        if not rtn.isdigit() or len(rtn) != 13:
            raise forms.ValidationError("El RTN debe tener exactamente 13 dígitos.")
        return rtn

    def clean_razonSocial(self):
        return self.validate_company_name(self.cleaned_data.get('razonSocial'))

    def clean_nombreEmpresa(self):
        return self.validate_company_name(self.cleaned_data.get('nombreEmpresa'))

    def validate_company_name(self, name):
        if not name:
            raise forms.ValidationError("Este campo es obligatorio.")
        if any(char.isdigit() for char in name):
            raise forms.ValidationError("El nombre no debe contener números.")
        return name

    def clean_rangoAutorizadoInicial(self):
        inicial = self.cleaned_data.get('rangoAutorizadoInicial')
        if inicial <= 0:
            raise forms.ValidationError("El rango autorizado inicial debe ser mayor que 0.")
        return inicial

    def clean_rangoAutorizadoFinal(self):
        final = self.cleaned_data.get('rangoAutorizadoFinal')
        inicial = self.cleaned_data.get('rangoAutorizadoInicial')
        if final <= 0:
            raise forms.ValidationError("El rango autorizado final debe ser mayor que 0.")
        if final <= inicial:
            raise forms.ValidationError("El rango autorizado final debe ser mayor que el inicial.")
        return final

    def clean_fechaLimiteEmision(self):
        fecha = self.cleaned_data.get('fechaLimiteEmision')
        if fecha <= timezone.now().date():
            raise forms.ValidationError("La fecha límite de emisión debe ser posterior a hoy.")
        return fecha
    
    def clean_correoElectronico(self):
        correoElectronico = self.cleaned_data.get('correoElectronico')
        instance = self.instance
        if Pacientes.objects.filter(correoElectronico=correoElectronico).exclude(id=instance.id).exists():
            raise ValidationError("Este correo electrónico ya está registrado.")
        pattern = r"[^@]+@[^@]+\.[^@]+"
        if not re.match(pattern, correoElectronico):
            raise ValidationError("Correo electrónico inválido.")
        pattern1 = r"[^@]+@[^@]+\.[a-zA-Z]{1,3}$"  # New pattern to match maximum of 3 letters after the .
        if not re.match(pattern1, correoElectronico):
            raise ValidationError("Correo electrónico inválido.")
        parts = correoElectronico.split('@')[1].split('.')
        if len(parts[0]) < 2 or len(parts[1]) < 2:
            raise ValidationError("El correo electrónico debe tener al menos 2 caracteres después del @ y al menos 2 caracteres después del punto.")
        return correoElectronico


    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        instance = self.instance
        if Pacientes.objects.filter(telefono=telefono).exclude(id=instance.id).exists():
            raise ValidationError("Este teléfono ya está registrado.")
        if not telefono.isdigit():
            raise ValidationError("El teléfono debe contener solo dígitos.")
        if len(telefono) != 8:
            raise ValidationError("El teléfono debe tener exactamente 8 dígitos.")
        if telefono[0] not in ['2', '3', '8', '9']:
            raise ValidationError("El teléfono debe comenzar con 22, 3, 8, o 9.")
        return telefono

class   ISVForm(forms.ModelForm):
    class Meta:
        model =  ISV
        fields = '__all__'
        widgets = {
            'impuesto': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'impuesto'
            }),
        }
        

    def clean_impuesto(self):
        impuesto = self.cleaned_data.get('impuesto')
        if impuesto is not None and impuesto <= 0:
            raise forms.ValidationError("El impuesto no puede ser menor que 0.")
        return impuesto


class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields =  ['descuento', 'rtn','metodoPago']
        widgets = {
                'rtn': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
                'placeholder': 'RTN',
            }),
                'descuento': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Precio'
            }),
                'metodoPago': forms.Select(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px;',
            })
            
            }
        
    def clean_rtn(self):
        rtn = self.cleaned_data.get('rtn')
        if rtn and (not rtn.isdigit() or len(rtn) != 13):
            raise forms.ValidationError("El RTN debe tener exactamente 13 dígitos.")
        return rtn

    def clean_descuento(self):
        descuento = self.cleaned_data.get('descuento')
        if descuento is not None and descuento < 0:
            raise forms.ValidationError("El descuento no puede ser menor que 0.")
        if descuento > 1:
            raise forms.ValidationError("El descuento no puede ser mayor a 1.")
        return descuento 
    