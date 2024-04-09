from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages
from .forms import *
from django.forms import inlineformset_factory

def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exit')

    context = {}
    return render(request, 'base/login.html', context)

@login_required(login_url="/login")
def home(request):
    return render(request, 'base/index.html')
@login_required(login_url="/login")
def tables(request): 
    surcursales = Surcursales.objects.all()
    return render(request, 'base/tables.html',{"surcursales":surcursales})
@login_required(login_url="/login")
def agregarsurcursal(request):
    return render(request, 'base/agregarSurcursal.html')
@login_required(login_url="/login")
def registrarSurcursal(request):
    nombre = request.POST['txtNombre']
    direccion = request.POST['txtDireccion']
    correoElectronico = request.POST['txtCorreoElectronico']
    telefono = request.POST['txtTelefono']
    personaEncargada= request.POST['txtPersonaEncargada']
    # Create Surcursales object with form data
    surcursal  = Surcursales.objects.create(
        nombre=nombre,
        direccion=direccion,
        correoElectronico=correoElectronico,
        telefono=telefono,
        personaEncargada=personaEncargada
    )

    # Add a success message
    messages.success(request, '¡Sucursal registrado!')

    return redirect('/')
@login_required(login_url="/login")
def editarSurcursal(request, id):
    surcursales = Surcursales.objects.get(id=id)
    return render(request, "base/editarSurcursal.html", {"surcursales": surcursales})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Surcursales
@login_required(login_url="/login")
def edicionSurcursal(request, id):
    # Retrieve the Surcursales object using the ID from the URL
    surcursales = get_object_or_404(Surcursales, id=id)

    if request.method == 'POST':
        # Extract form data
        nombre = request.POST['txtNombre']
        direccion = request.POST['txtDireccion']
        correoElectronico = request.POST['txtCorreoElectronico']
        telefono = request.POST['txtTelefono']
        personaEncargada = request.POST['txtPersonaEncargada']

        # Update Surcursales object fields
        surcursales.nombre = nombre
        surcursales.direccion = direccion
        surcursales.correoElectronico = correoElectronico
        surcursales.telefono = telefono
        surcursales.personaEncargada = personaEncargada
        
        # Save the updated object
        surcursales.save()

        # Add a success message
        messages.success(request, '¡Surcursal actualizado!')

        # Redirect to a relevant URL
        return redirect('/')

    return render(request, 'your_template.html', {'surcursales': surcursales})

@login_required(login_url="/login")
def eliminarSurcursal(request, id):
    surcursales = Surcursales.objects.get(id=id)
    surcursales.delete()

    messages.success(request, '¡Surcursal eliminado!')

    return redirect('/')
@login_required(login_url="/login")
def tablaproveedores(request):
    proveedores = Proveedores.objects.all()
    return render(request, 'base/tablaProveedores.html',{"proveedores":proveedores})
@login_required(login_url="/login")
def agregarproveedores(request):
    return render(request, 'base/agregarProveedores.html')

from .models import Proveedores
from django.shortcuts import redirect
from django.contrib import messages
@login_required(login_url="/login")
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
 
@login_required(login_url="/login")
def editarproveedores(request, id):
    proveedores = Proveedores.objects.get(id=id)
    return render(request, "base/editarProveedores.html", {"proveedores": proveedores})

@login_required(login_url="/login")
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

@login_required(login_url="/login")
def eliminarproveedores(request, id):
    proveedores = Proveedores.objects.get(id=id)
    proveedores.delete()

    messages.success(request, '¡Proveedor eliminado!')

    return redirect('/')



@login_required(login_url="/login")
def tablamedicamentos(request):
    medicamentos = Medicamentos.objects.all()
    return render(request, 'base/tablamedicamentos.html',{"medicamentos":medicamentos})
@login_required(login_url="/login")
def agregarmedicamentos(request):
    return render(request, 'base/agregarmedicamentos.html')

from .models import Medicamentos
from django.shortcuts import redirect
from django.contrib import messages
@login_required(login_url="/login")
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
 
@login_required(login_url="/login")
def editarmedicamentos(request, id):
    medicamentos= Medicamentos.objects.get(id=id)
    return render(request, "base/editarmedicamentos.html", {"medicamentos": medicamentos})

@login_required(login_url="/login")
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

@login_required(login_url="/login")
def eliminarmedicamentos(request, id):
    medicamentos = Medicamentos.objects.get(id=id)
    medicamentos.delete()

    messages.success(request, '¡Medicamentos eliminado!')

    return redirect('/')




@login_required(login_url="/login")
def tablaecmedicamentos(request):
    ecmedicamentos = ECMedicamentos.objects.all()
    return render(request, 'base/tablaecmedicamentos.html',{"ecmedicamentos":ecmedicamentos})
@login_required(login_url="/login")
def agregarecmedicamentos(request):
    medicamentos = Medicamentos.objects.all()
    surcursales = Surcursales.objects.all()
    return render(request, 'base/agregarecmedicamentos.html', {'medicamentos': medicamentos, 'surcursales': surcursales})


@login_required(login_url="/login")
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
 
@login_required(login_url="/login")
def editarecmedicamentos(request, id):
    ecmedicamentos= ECMedicamentos.objects.get(id=id)
    return render(request, "base/editarecmedicamentos.html", {"ecmedicamentos": ecmedicamentos})

@login_required(login_url="/login")
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

@login_required(login_url="/login")
def eliminarecmedicamentos(request, id):
    ecmedicamentos = ECMedicamentos.objects.get(id=id)
    ecmedicamentos.delete()

    messages.success(request, '¡Estado de compra de medicamentos eliminado!')

    return redirect('/')





@login_required(login_url="/login")
def tablapreciohmedicamento(request):
    preciohmedicamento = PrecioHMedicamento.objects.all()
    return render(request, 'base/tablapreciohmedicamento.html', {"preciohmedicamento": preciohmedicamento})
@login_required(login_url="/login")
def agregarpreciohmedicamento(request):
    if request.method == 'POST':
        form = PrecioHMedicamentoForm(request.POST)
        if form.is_valid():
            messages.success(request, '¡Estado de compra de medicamentos eliminado!')#
            form.save()  # Save the form data to the database
    
    else:
        form = PrecioHMedicamentoForm()
    context = {'form': form}
    return render(request, 'base/agregarpreciohmedicamento.html', context)



@login_required(login_url="/login")
def eliminarpreciohmedicamento(request, id):
    preciohmedicamento = get_object_or_404(PrecioHMedicamento, id=id)
    preciohmedicamento.delete()

    messages.success(request, '¡Precio histórico de medicamento eliminado!')

    return redirect('/')

@login_required(login_url="/login")
def tablaInventarioMedicamento(request):
    inventarioMedicamento = InventarioMedicamento.objects.all()
    return render(request, 'base/tablaInventarioMedicamento.html', {"inventarioMedicamento": inventarioMedicamento})

@login_required(login_url="/login")
def tablalotemedicamento(request):
    lotemedicamento = LoteMedicamento.objects.all()
    return render(request, 'base/tablalotemedicamento.html', {"lotemedicamento": lotemedicamento})

@login_required(login_url="/login")
def tablacompra(request):
    compra = CompraMedicamento.objects.all()
    return render(request, 'base/tablacompra.html', {"compra": compra})

@login_required(login_url="/login")
def compraMedicamento(request):
    DetallePedidoFormSet = inlineformset_factory(CompraMedicamento, DetallePedido, 
                                                  form=DetallePedidoForm, extra=2, can_delete=True)
    if request.method == 'POST':
        form = CompraMedicamentoForm(request.POST)
        formset = DetallePedidoFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            compraMedicamento = form.save()  # Save the CompraMedicamento instance first
            formset.instance = compraMedicamento  # Assign the instance to each form in the formset
            formset.save()  # Save the DetallePedido instances, now associated with compraMedicamento
            messages.success(request, 'Compra de medicamento guardada con éxito!')
            return redirect('/')  # Replace '/' with the URL you want to redirect to
    else:
        form = CompraMedicamentoForm()
        formset = DetallePedidoFormSet()

    context = {'form': form, 'formset': formset}
    return render(request, 'base/compraMedicamento.html', context)

@login_required(login_url="/login")
def editarcompramedicamento(request, pk):
    compra_medicamento = CompraMedicamento.objects.get(pk=pk)
    if request.method == 'POST':
        form = CompraMedicamentoForm(request.POST, instance=compra_medicamento)
        formset = DetallePedidoFormSet(request.POST, instance=compra_medicamento)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Compra de medicamento editar con éxito!')
            return redirect('/')  # Redirect to a success URL
    else:
        form = CompraMedicamentoForm(instance=compra_medicamento)
        formset = DetallePedidoFormSet(instance=compra_medicamento)
    return render(request, 'base/editarcompramedicamento.html', {'form': form, 'formset': formset})

@login_required(login_url="/login")
def tablametodospago(request): 
    metodospago = MetodosPago.objects.all()
    return render(request, 'base/tablametodospago.html',{"metodospago":metodospago })

@login_required(login_url="/login")
def agregarmetodospago(request):
    if request.method == 'POST':
        form = MetodosPagoForm(request.POST)
        if form.is_valid():
            messages.success(request, '¡Metodo de pago agregado!')#
            
            form.save()  # Save the form data to the database
            return redirect('/') 
    else:
        form = MetodosPagoForm()
    context = {'form': form}
    return render(request, 'base/agregarmetodospago.html', context)

@login_required(login_url="/login")
def tablatipodocumento(request): 
    tipodocumento = TipoDocumento.objects.all()
    return render(request, 'base/tablatipodocumento.html',{"tipodocumento":tipodocumento })

@login_required(login_url="/login")
def agregartipodocumento(request):
    if request.method == 'POST':
        form = TipoDocumentoForm(request.POST)
        if form.is_valid():
            messages.success(request, '¡Tipo Documento agregado!')#
            
            form.save()  # Save the form data to the database
            return redirect('/') 
    else:
        form = TipoDocumentoForm()
    context = {'form': form}
    return render(request, 'base/agregartipodocumento.html', context)
