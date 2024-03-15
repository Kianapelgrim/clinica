from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import messages


def home(request):
    return render(request, 'base/index.html')
def login(request):
    return render(request, 'base/login.html')
def tables(request):
    surcursales = Surcursales.objects.all()
    return render(request, 'base/tables.html',{"surcursales":surcursales})
def agregarsurcursal(request):
    return render(request, 'base/agregarSurcursal.html')
def registrarSurcursal(request):
    nombre = request.POST['txtNombre']
    direccion = request.POST['txtDireccion']
    correoElectronico = request.POST['txtCorreoElectronico']
    telefono = request.POST['txtTelefono']

    # Create Surcursales object with form data
    surcursal  = Surcursales.objects.create(
        nombre=nombre,
        direccion=direccion,
        correoElectronico=correoElectronico,
        telefono=telefono
    )

    # Add a success message
    messages.success(request, '¡Sucursal registrado!')

    return redirect('/')

def editarSurcursal(request, id):
    surcursales = Surcursales.objects.get(id=id)
    return render(request, "base/editarSurcursal.html", {"surcursales": surcursales})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Surcursales

def edicionSurcursal(request, id):
    # Retrieve the Surcursales object using the ID from the URL
    surcursales = get_object_or_404(Surcursales, id=id)

    if request.method == 'POST':
        # Extract form data
        nombre = request.POST['txtNombre']
        direccion = request.POST['txtDireccion']
        correoElectronico = request.POST['txtCorreoElectronico']
        telefono = request.POST['txtTelefono']

        # Update Surcursales object fields
        surcursales.nombre = nombre
        surcursales.direccion = direccion
        surcursales.correoElectronico = correoElectronico
        surcursales.telefono = telefono
        
        # Save the updated object
        surcursales.save()

        # Add a success message
        messages.success(request, '¡Surcursal actualizado!')

        # Redirect to a relevant URL
        return redirect('/')

    return render(request, 'your_template.html', {'surcursales': surcursales})


def eliminarSurcursal(request, id):
    surcursales = Surcursales.objects.get(id=id)
    surcursales.delete()

    messages.success(request, '¡Surcursal eliminado!')

    return redirect('/')

def tablaproveedores(request):
    proveedores = Proveedores.objects.all()
    return render(request, 'base/tablaProveedores.html',{"proveedores":proveedores})

def agregarproveedores(request):
    return render(request, 'base/agregarProveedores.html')

from .models import Proveedores
from django.shortcuts import redirect
from django.contrib import messages

def registrarproveedores(request):
    if request.method == 'POST':
        nombre = request.POST['txtNombre']
        direccion = request.POST['txtDireccion']
        correoElectronico = request.POST['txtCorreoElectronico']
        telefono = request.POST['txtTelefono']

        # Create Proveedores object with form data
        proveedor = Proveedores.objects.create(
            nombre=nombre,
            direccion=direccion,
            correoElectronico=correoElectronico,
            telefono=telefono
        )

        # Add a success message
        messages.success(request, '¡Proveedor registrado!')

        return redirect('/')
    else:
        # Handle GET requests or other cases
        # You can return a response for other request methods or handle them accordingly
        return redirect('/')  # Redirect to home page or render a specific template
 

def editarproveedores(request, id):
    proveedores = Proveedores.objects.get(id=id)
    return render(request, "base/editarProveedores.html", {"proveedores": proveedores})


def edicionproveedores(request, id):
    # Retrieve the Surcursales object using the ID from the URL
    proveedores = get_object_or_404(Proveedores, id=id)

    if request.method == 'POST':
        # Extract form data
        nombre = request.POST['txtNombre']
        direccion = request.POST['txtDireccion']
        correoElectronico = request.POST['txtCorreoElectronico']
        telefono = request.POST['txtTelefono']

        # Update Surcursales object fields
        proveedores.nombre = nombre
        proveedores.direccion = direccion
        proveedores.correoElectronico = correoElectronico
        proveedores.telefono = telefono
        
        # Save the updated object
        proveedores.save()

        # Add a success message
        messages.success(request, '¡Proveedor actualizado!')

        # Redirect to a relevant URL
        return redirect('/')

    return render(request, 'your_template.html', {'proveedores': proveedores})


def eliminarproveedores(request, id):
    proveedores = Proveedores.objects.get(id=id)
    proveedores.delete()

    messages.success(request, '¡Proveedor eliminado!')

    return redirect('/')




def tablamedicamentos(request):
    medicamentos = Medicamentos.objects.all()
    return render(request, 'base/tablamedicamentos.html',{"medicamentos":medicamentos})

def agregarmedicamentos(request):
    return render(request, 'base/agregarmedicamentos.html')

from .models import Medicamentos
from django.shortcuts import redirect
from django.contrib import messages

def registrarmedicamentos(request):
    if request.method == 'POST':
        nombre = request.POST['txtNombre']
        ingredientes = request.POST['txtIngredientes']
        precio = request.POST['txtPrecio']

        # Create Proveedores object with form data
        medicamentos = Medicamentos.objects.create(
            nombre=nombre,
            ingredientes = ingredientes,
            precio= precio,
        )

        # Add a success message
        messages.success(request, '¡Medicamento registrado!')

        return redirect('/')
    else:
        # Handle GET requests or other cases
        # You can return a response for other request methods or handle them accordingly
        return redirect('/')  # Redirect to home page or render a specific template
 

def editarmedicamentos(request, id):
    medicamentos= Medicamentos.objects.get(id=id)
    return render(request, "base/editarmedicamentos.html", {"medicamentos": medicamentos})


def edicionmedicamentos(request, id):
    # Retrieve the Surcursales object using the ID from the URL
    medicamentos = get_object_or_404(Medicamentos, id=id)

    if request.method == 'POST':
        # Extract form data
        nombre = request.POST['txtNombre']
        ingredientes = request.POST['txtIngredientes']
        precio = request.POST['txtPrecio']
        

        # Update Surcursales object fields
        medicamentos.nombre = nombre
        medicamentos.ingredientes = ingredientes
        medicamentos.precio = precio
    
        
        # Save the updated object
        medicamentos.save()

        # Add a success message
        messages.success(request, '¡Medicamentos actualizado!')

        # Redirect to a relevant URL
        return redirect('/')

    render(request, 'your_template.html', {'medicamentos': medicamentos})


def eliminarmedicamentos(request, id):
    medicamentos = Medicamentos.objects.get(id=id)
    medicamentos.delete()

    messages.success(request, '¡Medicamentos eliminado!')

    return redirect('/')





def tablaecmedicamentos(request):
    ecmedicamentos = ECMedicamentos.objects.all()
    return render(request, 'base/tablaecmedicamentos.html',{"ecmedicamentos":ecmedicamentos})

def agregarecmedicamentos(request):
    return render(request, 'base/agregarecmedicamentos.html')

from .models import ECMedicamentos
from django.shortcuts import redirect
from django.contrib import messages

def registrarecmedicamentos(request):
    if request.method == 'POST':
        nombre = request.POST['txtNombre']

        # Create Proveedores object with form data
        ecmedicamentos = ECMedicamentos.objects.create(
            nombre=nombre,
        )

        # Add a success message
        messages.success(request, '¡Estado de compra de Medicamento registrado!')

        return redirect('/')
    else:
        # Handle GET requests or other cases
        # You can return a response for other request methods or handle them accordingly
        return redirect('/')  # Redirect to home page or render a specific template
 

def editarecmedicamentos(request, id):
    ecmedicamentos= ECMedicamentos.objects.get(id=id)
    return render(request, "base/editarecmedicamentos.html", {"ecmedicamentos": ecmedicamentos})


def edicionecmedicamentos(request, id):
    # Retrieve the Surcursales object using the ID from the URL
    ecmedicamentos = get_object_or_404(ECMedicamentos, id=id)

    if request.method == 'POST':
        # Extract form data
        nombre = request.POST['txtNombre']
       

        # Update Surcursales object fields
        ecmedicamentos.nombre = nombre
        
    
        
        # Save the updated object
        ecmedicamentos.save()

        # Add a success message
        messages.success(request, '¡Estado de compra de medicamento actualizado!')

        # Redirect to a relevant URL
        return redirect('/')

    render(request, 'your_template.html', {'ecmedicamentos': ecmedicamentos})


def eliminarecmedicamentos(request, id):
    ecmedicamentos = ECMedicamentos.objects.get(id=id)
    ecmedicamentos.delete()

    messages.success(request, '¡Estado de compra de medicamentos eliminado!')

    return redirect('/')