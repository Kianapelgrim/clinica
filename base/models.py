from datetime import timezone
import re
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import phonenumbers
from django.utils import timezone
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver



class Surcursales(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    direccion = models.TextField()
    correoElectronico = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
    personaEncargada= models.CharField(max_length = 255, null = True)

    def clean(self):
        super().clean()
        try:
        # Parse the phone number using phonenumbers
         parsed_number = phonenumbers.parse(self.telefono, None)
        # Check if the number is vali2
        # d
         if not phonenumbers.is_possible_number(parsed_number):
            raise ValidationError('Invalid phone number format.')
        except phonenumbers.phonenumberutil.NumberParseException:
         raise ValidationError('Invalid phone number format.')
    def __str__(self):
        return self.nombre
    
class Proveedores(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    direccion = models.TextField()
    correoElectronico = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
    personaEncargada= models.CharField(max_length = 255, null = True)

    def clean(self):
        super().clean()
        try:
        # Parse the phone number using phonenumbers
         parsed_number = phonenumbers.parse(self.telefono, None)
        # Check if the number is valid
         if not phonenumbers.is_possible_number(parsed_number):
            raise ValidationError('Invalid phone number format.')
        except phonenumbers.phonenumberutil.NumberParseException:
         raise ValidationError('Invalid phone number format.')
    def __str__(self):
        return self.nombre
    


class Medicamentos(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, blank=False,unique=True)
    ingredientes = models.CharField(max_length=255)
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=False)


    def __str__(self):
        return self.nombre
    
class PrecioHMedicamento(models.Model): 
    id = models.AutoField(primary_key=True)
    fechaInicio = models.DateField(auto_now_add=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    Medicamentos = models.ForeignKey(Medicamentos, on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return f"{self.Medicamentos.nombre} - {self.surcursal.nombre} ({self.fechaInicio})"
   
class LoteMedicamento(models.Model):
    id = models.AutoField(primary_key=True)
    # Correctly set 'null=True' and specify the model
    fechaVencimiento = models.DateField(null=True)
    medicamento = models.ForeignKey('Medicamentos', on_delete=models.CASCADE,null=True)



    def __str__(self):
        return f"{self.medicamento.nombre} - {self.id}"


class ECMedicamentos(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(unique= True, max_length=255, blank=False)
    def __str__(self):
        return self.nombre
    

class InventarioMedicamento(models.Model):
    id = models.AutoField(primary_key=True)
    stock = models.IntegerField()
    # Specify the model for ForeignKey and correct 'null' capitalization
    medicamento = models.ForeignKey('Medicamentos', on_delete=models.CASCADE,null=True)
    lote = models.ForeignKey(LoteMedicamento, on_delete=models.SET_NULL,null=True)


    
    def __str__(self):
        return f"{self.medicamento.nombre} - {self.stock}"
    




class CompraMedicamento(models.Model):
    id = models.AutoField(primary_key=True)
    proveedor = models.ForeignKey('Proveedores', on_delete=models.SET_NULL, null=True)
    precioTotal = models.DecimalField(max_digits=10, decimal_places=2)
    fechaPedido = models.DateField()
    fechaRecibido = models.DateField(null=True, blank=True)
    estadoCompra = models.ForeignKey('ECMedicamentos', on_delete=models.SET_NULL, null=True)
    fechaDespacho = models.DateField(null=True, blank=True)
    numeroFactura = models.CharField(max_length=255)

    # Your existing fields...

    def clean(self):
        # Call the clean method of the superclass
        super().clean()

        # Validation: Preciototal shouldn't be more than 10000000000
        if self.precioTotal is not None and self.precioTotal > 10000000000:
            raise ValidationError({'precioTotal': 'Precio total no puede ser mayor a 10000000000.'})
        
        # Validation: fechapedido shouldn't be after today's date
        if self.fechaPedido is not None and self.fechaPedido > timezone.now().date():
            raise ValidationError({'fechaPedido': 'La fecha de pedido no puede ser posterior a la fecha actual.'})
        
        # Validation: fechaDespacho shouldn't be after today's date and before fechapedido's date
        if self.fechaDespacho:
            if self.fechaDespacho > timezone.now().date() or (self.fechaPedido and self.fechaDespacho < self.fechaPedido):
                raise ValidationError({'fechaDespacho': 'La fecha de despacho debe estar entre la fecha de pedido y la fecha actual.'})

        # Validation: fechaRecibido shouldn't be after today's date, before fechapedido's date, and before fechaDespacho
        if self.fechaRecibido and self.fechaDespacho and self.fechaRecibido < self.fechaDespacho:
            raise ValidationError({'fechaRecibido': 'La fecha de recibido debe ser igual o mayor a la fecha de despacho.'})

        # Validation: Numero factura should have exactly 16 digits
        if len(str(self.numeroFactura)) != 16:
            raise ValidationError({'numeroFactura': 'El número de factura debe tener exactamente 16 dígitos.'})
    
    def __str__(self):
        return f"{self.medicamento.nombre} - {self.id}"
    
class DetallePedido(models.Model):
    id = models.AutoField(primary_key=True)
    compraMedicamentoId = models.ForeignKey('CompraMedicamento', on_delete=models.CASCADE)
    lote = models.ForeignKey('LoteMedicamento', on_delete = models.SET_NULL, null = True)
    cantidad = models.IntegerField()

def __str__(self):
        return f"{self.medicamento.nombre} - {self.id}"

class MetodosPago(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return f"{self.nombre}"

class TipoDocumento(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, blank=False)
    def __str__(self):
        return f"{self.nombre}"

class Documento(models.Model):
    id = models.AutoField(primary_key=True)
    tipodocumento = models.ForeignKey('TipoDocumento',on_delete = models.SET_NULL, null = True)
    informacion = models.CharField(max_length=255, blank=False)
    def __str__(self):
        return f"{self.tipodocumento.nombre}"

class Cargos(models.Model):
    id = models.AutoField(primary_key=True)
    nombre= models.CharField(max_length=255, blank=False)
    descripcion = models.CharField(max_length=255, blank=False)
    def __str__(self):
        return self.nombre

class Empleados(models.Model):
    id = models.AutoField(primary_key=True)
    nombre= models.CharField(max_length=255, blank=False)
    fechaNacimiento = models.DateField()
    telefono = models.CharField(max_length=20)
    correoElectronico = models.EmailField(unique=True)
    direccion= models.CharField(max_length=255, blank=False)
    documento=models.ForeignKey('Documento',on_delete = models.SET_NULL, null = True)
    cargo=models.ForeignKey('Cargos',on_delete = models.SET_NULL, null = True) 



    def __str__(self):
        return f"{self.nombre}"

class TipoSalas(models.Model):
    id = models.AutoField(primary_key=True)
    nombre= models.CharField(max_length=255, blank=False)

    def __str__(self):
        return f"{self.nombre}"

class Salas(models.Model):
    id = models.AutoField(primary_key=True)
    nombre= models.CharField(max_length=255, blank=False)
    tipoSalas=models.ForeignKey('TipoSalas',on_delete = models.SET_NULL, null = True)
    surcursal=models.ForeignKey('Surcursales',on_delete = models.SET_NULL, null = True)

    def __str__(self):
        return f"{self.nombre}"
    
class Pacientes(models.Model):
    GENDER_CHOICES = [
        ('F', 'Femenino'),
        ('M', 'Masculino'),
    ]

    id = models.AutoField(primary_key=True)
    nombre= models.CharField(max_length=255, blank=False)
    fechaDeNacimiento = models.DateField(null=True)
    telefono = models.CharField(max_length=20)
    correoElectronico = models.EmailField(unique=True)
    direccion= models.CharField(max_length=255, blank=False)
    documento=models.ForeignKey('Documento',on_delete = models.SET_NULL, null = True)
    genero = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Genero")

    def __str__(self):
        return self.nombre
    
class Citas(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.DateTimeField()
    descripcion = models.TextField(blank=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    paciente=models.ForeignKey('Pacientes',on_delete = models.SET_NULL, null = True)
    medico=models.ForeignKey('Empleados',on_delete = models.SET_NULL, null = True)
    sala=models.ForeignKey('Salas',on_delete = models.SET_NULL, null = True)
    surcursal=models.ForeignKey('Surcursales',on_delete = models.SET_NULL, null = True)
    
    def __str__(self):
        return self.paciente.nombre

class Prescripciones(models.Model):
    id = models.AutoField(primary_key=True)
    indicaciones = models.TextField(blank=True)
    fecha = models.DateField(auto_now_add=True)
    cita=models.ForeignKey('Citas',on_delete = models.SET_NULL, null = True)
    
    def __str__(self):
        return self.cita.paciente.nombre

class DetallePrescripciones(models.Model):
    id = models.AutoField(primary_key=True)
    medicamento=models.ForeignKey('Medicamentos',on_delete = models.SET_NULL, null = True)
    prescripcion=models.ForeignKey('Prescripciones',on_delete = models.SET_NULL, null = True)
    
    def __str__(self):
        return self.cita.paciente.nombre

class OrdenesMedicas(models.Model):
    id = models.AutoField(primary_key=True)
    indicaciones = models.TextField(blank=True)
    fecha = models.DateField(auto_now_add=True)
    cita=models.ForeignKey('Citas',on_delete = models.SET_NULL, null = True)
    
    def __str__(self):
        return self.cita.paciente.nombre
    
class HistorialClinico(models.Model):
    id = models.ForeignKey('Pacientes',primary_key=True, on_delete= models.CASCADE,unique=True)
    creado = models.DateField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return self.paciente.nombre
    

class Parametros(models.Model):
    id = models.AutoField(primary_key=True)
    surcursal= models.ForeignKey('Surcursales', on_delete= models.SET_NULL, null= True)
    cai = models.CharField(max_length=30)
    rtn = models.CharField(max_length=30)
    razonSocial = models.CharField(max_length=30)
    nombreEmpresa = models.CharField(max_length=30)
    rangoAutorizadoInicial = models.IntegerField()
    rangoAutorizadoFinal = models.IntegerField()
    fechaLimiteEmision = models.DateField()
    correoElectronico = models.EmailField()
    telefono = models.CharField(max_length=20)
    def __str__(self):
        return f"{self.id} - {self.surcursal.nombre}"


class Factura(models.Model):
    id = models.AutoField(primary_key=True)
    numero= models.CharField(max_length=200, null=True)
    surcursal= models.ForeignKey('Surcursales', on_delete= models.SET_NULL, null= True)
    paciente= models.ForeignKey('Pacientes', on_delete= models.SET_NULL, null= True)
    fecha = models.DateField()
    isv = models.DecimalField(max_digits=12, decimal_places=2, null=False, blank=False)
    metodoPago= models.ForeignKey('MetodosPago', on_delete= models.SET_NULL, null= True)
    parametros= models.ForeignKey('Parametros', on_delete= models.SET_NULL, null= True)
    descuento= models.DecimalField(max_digits=12, decimal_places=2, null=False, blank=False)
    total= models.DecimalField(max_digits=12, decimal_places=2, null=False, blank=False)
 
    def __str__(self):
        return f"{self.paciente.nombre} - {self.fecha}"

from django.db import models

class QuejasYSugerencias(models.Model):
    TIPOS = (
        ('Queja', 'Queja'),
        ('Sugerencia', 'Sugerencia'),
    )
    tipo = models.CharField(max_length=20, choices=TIPOS)
    descripcion = models.TextField()
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo} - {self.fecha}"



@receiver(post_save, sender=Pacientes)
def create_historial_clinico(sender, instance, created, **kwargs):
    if created:
        HistorialClinico.objects.create(id=instance)

@receiver(post_save, sender=Medicamentos)
def create_inventario_medicamento(sender, instance, created, **kwargs):
    if created:
        InventarioMedicamento.objects.create(medicamento=instance, stock=0)

@receiver(post_save, sender=CompraMedicamento)
def update_stock(sender, instance, created, **kwargs):
    # Check if the instance is created or updated and if the estadoCompra is "Aprobado"
    if not created and instance.estadoCompra == 'Aprobado':
        # Get all detallePedido related to the CompraMedicamento instance
        detalles = DetallePedido.objects.filter(compraMedicamentoId=instance)
        # Update the stock in InventarioMedicamento for each detallePedido
        for detalle in detalles:
            inventario = InventarioMedicamento.objects.get(medicamento=detalle.medicamento)
            inventario.stock += detalle.cantidad
            inventario.save()