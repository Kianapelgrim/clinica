from django.db import models
from django.core.exceptions import ValidationError
import phonenumbers
class Surcursales(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    direccion = models.TextField()
    correoElectronico = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)

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
    
class Proveedores(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    direccion = models.TextField()
    correoElectronico = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)

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
    nombre = models.CharField(max_length=255, blank=False)
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    ingredientes = models.CharField(max_length=255)
    def __str__(self):
        return self.nombre
