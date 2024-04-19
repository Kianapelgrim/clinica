from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages
from .forms import *
from django.forms import inlineformset_factory
from django.views import View
from django.db.models import Max
from django.forms import modelformset_factory

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
def tablapreciohmedicamento(request):
    preciohmedicamento = PrecioHMedicamento.objects.all()
    return render(request, 'base/tablapreciohmedicamento.html', {"preciohmedicamento": preciohmedicamento})

def tablamedicamentos(request):
    medicamentos = Medicamentos.objects.all()
    
    context = {
        'medicamentos': medicamentos,
    }
    return render(request, 'base/tablamedicamentos.html', context)

@login_required(login_url="/login")
def agregarmedicamentos(request):
    return render(request, 'base/agregarmedicamentos.html')

@login_required(login_url="/login")
def agregarmedicamentos(request):
    if request.method == 'POST':
        medicamentos_form = MedicamentosForm(request.POST)
        preciohmedicamentos_form = PrecioHMedicamentoForm(request.POST)
        if medicamentos_form.is_valid() and preciohmedicamentos_form.is_valid():
            medicamento = medicamentos_form.save(commit=False)  # Don't save yet
            medicamento.save()  # Save the medicamento instance to get an ID
            
            preciohmedicamento = preciohmedicamentos_form.save(commit=False)  # Don't save yet
            preciohmedicamento.Medicamentos = medicamento  # Associate with medicamento
            preciohmedicamento.save()  # Save preciohmedicamento
            
            medicamento.precio = preciohmedicamento.precio  # Set medicamento precio
            medicamento.save()  # Save medicamento with updated precio
            
            messages.success(request, '¡Medicamento agregado!')
            return redirect('/')  # Redirect to a success page
    else:
        medicamentos_form = MedicamentosForm()
        preciohmedicamentos_form = PrecioHMedicamentoForm()
    return render(request, 'base/agregarmedicamentos.html', {'medicamentos_form': medicamentos_form, 'preciohmedicamentos_form': preciohmedicamentos_form})

@login_required(login_url="/login")
def editarmedicamentos(request, id):
    if request.method == 'POST':
        medicamentos_form = MedicamentosForm(request.POST)
        preciohmedicamentos_form = PrecioHMedicamentoForm(request.POST)
        if medicamentos_form.is_valid() and preciohmedicamentos_form.is_valid():
            medicamentos = medicamentos_form.save()
            preciohmedicamentos = preciohmedicamentos_form.save(commit=False)
            preciohmedicamentos.save()
            medicamentos.precio = preciohmedicamentos  # Associate the document with the employee
            medicamentos.save()
            messages.success(request, '¡Medicamento agregado!')
            return redirect('/')  # Redirect to a success page
    else:
        medicamentos_form = MedicamentosForm()
        preciohmedicamentos_form = PrecioHMedicamentoForm()
    return render(request, 'base/agregarmedicamentos.html', {'medicamentos_form': medicamentos_form, 'preciohmedicamentos_form': preciohmedicamentos_form})



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
    if request.method == 'POST':
        compra_form = CompraMedicamentoForm(request.POST)
        detalle_formset = DetallePedidoFormSet(request.POST)
        lote_form = LoteForm(request.POST)

        if compra_form.is_valid() and detalle_formset.is_valid() and lote_form.is_valid():
            compra = compra_form.save()
            lote = lote_form.save()

            for detalle_form in detalle_formset:
                detalle = detalle_form.save(commit=False)
                detalle.compraMedicamentoId = compra
                detalle.lote = lote
                detalle.save()

            return redirect('/')  # Redirect as necessary
    else:
        compra_form = CompraMedicamentoForm()
        detalle_formset = DetallePedidoFormSet()
        lote_form = LoteForm()

    return render(request, 'base/compraMedicamento.html', {
        'compra_form': compra_form,
        'detalle_formset': detalle_formset,
        'lote_form': lote_form
    })

def editarcompramedicamento(request, compra_id):
    compra = get_object_or_404(CompraMedicamento, id=compra_id)
    if request.method == 'POST':
        compra_form = CompraMedicamentoForm(request.POST, instance=compra)
        if compra_form.is_valid():
            compra = compra_form.save()

            # Check if estadoCompra is 3
            if compra.estadoCompra.nombre == "Aprobado":
                # Get all detalle_pedidos for the specific compraMedicamento
                detalle_pedidos = DetallePedido.objects.filter(compraMedicamentoId=compra)
                
                # Iterate over each detallePedido
                for detalle_pedido in detalle_pedidos:
                    # Get the related loteMedicamento
                    lote = detalle_pedido.lote
                    # Get the related medicamento
                    medicamento = lote.medicamento
                    
                    # Get or create the related InventarioMedicamento
                    inventarios = InventarioMedicamento.objects.filter(medicamento=medicamento)
                    
                    # Iterate over filtered InventarioMedicamento instances
                    for inventario in inventarios:
                        # Update stock and lote in InventarioMedicamento
                        inventario.stock += detalle_pedido.cantidad
                        inventario.save()
            return redirect('/')  # Adjust the redirect as necessary
    else:
        compra_form = CompraMedicamentoForm(instance=compra)

    return render(request, 'base/editarcompramedicamento.html', {
        'compra_form': compra_form,
    })

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


@login_required(login_url="/login")
def tablacargos(request):
    cargos = Cargos.objects.all()
    return render(request, 'base/tablacargos.html',{"cargos":cargos})

@login_required(login_url="/login")
def agregarcargo(request):
    if request.method == 'POST':
        form = CargosForm(request.POST)
        if form.is_valid():
            messages.success(request, '¡Cargo agregado!')#
            
            form.save()  # Save the form data to the database
            return redirect('/') 
    else:
        form = CargosForm()
    context = {'form': form}
    return render(request, 'base/agregarcargo.html', context)


@login_required(login_url="/login")
def tablaempleados(request):
    empleados = Empleados.objects.all()
    return render(request, 'base/tablaempleados.html',{"empleados":empleados})

@login_required(login_url="/login")
def agregarempleados(request):
    if request.method == 'POST':
        empleado_form = EmpleadosForm(request.POST)
        documento_form = DocumentoForm(request.POST)
        if empleado_form.is_valid() and documento_form.is_valid():
            empleado = empleado_form.save()
            documento = documento_form.save(commit=False)
            documento.save()
            empleado.documento = documento  # Associate the document with the employee
            empleado.save()
            messages.success(request, '¡Empleado agregado!')#
            return redirect('/')  # Redirect to a success page
    else:
        empleado_form = EmpleadosForm()
        documento_form = DocumentoForm()
    return render(request, 'base/agregarempleados.html', {'empleado_form': empleado_form, 'documento_form': documento_form})

@login_required(login_url="/login")
def editarempleados(request, pk):
    empleados = Empleados.objects.get(pk=pk)
    documentos =Documento.objects.get(pk=pk)
    if request.method == 'POST':
        empleado_form = EmpleadosForm(request.POST,instance=empleados)
        documento_form = DocumentoForm(request.POST,instance=documentos)
        if empleado_form.is_valid() and documento_form.is_valid():
            empleado = empleado_form.save()
            documento = documento_form.save(commit=False)
            documento.save()
            empleado.documento = documento  # Associate the document with the employee
            empleado.save()
            messages.success(request, '¡Empleado agregado!')#
            return redirect('/')  # Redirect to a success page
    else:
        empleado_form = EmpleadosForm(instance=empleados)
        documento_form = DocumentoForm(instance=documentos)
    return render(request, 'base/editarempleados.html', {'empleado_form': empleado_form, 'documento_form': documento_form})
   
@login_required(login_url="/login")
def tablatiposalas(request):
    tiposalas = TipoSalas.objects.all()
    return render(request, 'base/tablatiposalas.html',{"tiposalas":tiposalas})

@login_required(login_url="/login")
def agregartiposala(request):
    if request.method == 'POST':
        form = TipoSalasForm(request.POST)
        if form.is_valid():
            messages.success(request, '¡Tipo Sala agregado!')#
            
            form.save()  # Save the form data to the database
            return redirect('/') 
    else:
        form = TipoSalasForm()
    context = {'form': form}
    return render(request, 'base/agregartiposala.html', context)

@login_required(login_url="/login")
def editartiposala(request, pk):
    tiposala= TipoSalas.objects.get(pk=pk)
    if request.method == 'POST':
        form = TipoSalasForm(request.POST,instance=tiposala)
        if form.is_valid():
            messages.success(request, '¡Tipo Sala actualizado!')#
            
            form.save()  # Save the form data to the database
            return redirect('/') 
    else:
        form = TipoSalasForm(instance=tiposala)
    context = {'form': form}
    return render(request, 'base/editartiposala.html', context)

@login_required(login_url="/login")
def tablasalas(request):
    salas = Salas.objects.all()
    return render(request, 'base/tablasalas.html',{"salas":salas})

@login_required(login_url="/login")
def agregarsala(request):
    if request.method == 'POST':
        form = SalasForm(request.POST)
        if form.is_valid():
            messages.success(request, '¡Sala agregado!')#
            
            form.save()  # Save the form data to the database
            return redirect('/') 
    else:
        form = SalasForm()
    context = {'form': form}
    return render(request, 'base/agregarsala.html', context)

@login_required(login_url="/login")
def editarsala(request, pk):
    sala = Salas.objects.get(pk=pk)
    if request.method == 'POST':

        form = SalasForm(request.POST,instance=sala)
        if form.is_valid():
            messages.success(request, '¡Sala actualizado!')#
            
            form.save()  # Save the form data to the database
            return redirect('/') 
    else:
        form = SalasForm(instance=sala)
    context = {'form': form}
    return render(request, 'base/agregarsala.html', context)

@login_required(login_url="/login")
def tabladocumento(request):
    documento = Documento.objects.all()
    return render(request, 'base/tabladocumento.html',{"documento":documento})

@login_required(login_url="/login")
def tablapacientes(request):
    pacientes = Pacientes.objects.all()
    return render(request, 'base/tablapacientes.html',{"pacientes":pacientes})

@login_required(login_url="/login")
def agregarpaciente(request):
    if request.method == 'POST':
        pacientes_form = PacientesForm(request.POST)
        documento_form = DocumentoForm(request.POST)
        if pacientes_form.is_valid() and documento_form.is_valid():
            pacientes = pacientes_form.save()
            documento = documento_form.save(commit=False)
            documento.save()
            pacientes.documento = documento  # Associate the document with the employee
            pacientes.save()
            messages.success(request, '¡Paciente agregado!')#
            return redirect('/')  # Redirect to a success page
    else:
        pacientes_form = PacientesForm()
        documento_form = DocumentoForm()
    return render(request, 'base/agregarpaciente.html', {'pacientes_form': pacientes_form, 'documento_form': documento_form})

@login_required(login_url="/login")
def editarpaciente(request, pk):
    pacientes = Pacientes.objects.get(pk=pk)
    documentos =Documento.objects.get(pk=pk)
    if request.method == 'POST':
        pacientes_form = PacientesForm(request.POST,instance=pacientes)
        documento_form = DocumentoForm(request.POST,instance=documentos)
        if pacientes_form.is_valid() and documento_form.is_valid():
            epacientes = pacientes_form.save()
            documento = documento_form.save(commit=False)
            documento.save()
            pacientes.documento = documento  # Associate the document with the employee
            pacientes.save()
            messages.success(request, '¡Paciente actualizado!')#
            return redirect('/')  # Redirect to a success page
    else:
        pacientes_form = PacientesForm(instance=pacientes)
        documento_form = DocumentoForm(instance=documentos)
    return render(request, 'base/editarpaciente.html', {'pacientes_form': pacientes_form, 'documento_form': documento_form})

def tablacitas(request):
    citas = Citas.objects.all()
    return render(request, 'base/tablacitas.html',{"citas":citas})

@login_required(login_url="/login")
def agregarcita(request):
    if request.method == 'POST':
        form = CitasForm(request.POST)
        if form.is_valid():
            messages.success(request, '¡Cita agregada!')#
            
            form.save()  # Save the form data to the database
            return redirect('/') 
    else:
        form = CitasForm()
    context = {'form': form}
    return render(request, 'base/agregarcita.html', context)

@login_required(login_url="/login")
def editarcita(request, pk):
    cita = Citas.objects.get(pk=pk)
    if request.method == 'POST':

        form = CitasForm(request.POST,instance=cita)
        if form.is_valid():
            messages.success(request, '¡Cita actualizada!')#
            
            form.save()  # Save the form data to the database
            return redirect('/') 
    else:
        form = CitasForm(instance=cita)
    context = {'form': form}
    return render(request, 'base/agregarcita.html', context)


@login_required(login_url="/login")
def tablaprescripciones(request):
    prescripciones = Prescripciones.objects.all()
    return render(request, 'base/tablaprescripciones.html', {"prescripciones": prescripciones})



@login_required(login_url="/login")
def agregarprescripcion(request):
    DetallePrescripcionesFormSet = inlineformset_factory(Prescripciones, DetallePrescripciones, 
                                                  form=DetallePrescripcionesForm, extra=2, can_delete=True)
    if request.method == 'POST':
        form = PrescripcionesForm(request.POST)
        formset = DetallePrescripcionesFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            prescripcion = form.save()  # Use a different variable name for the form instance
            formset.instance = prescripcion  # Assign the instance to each form in the formset
            formset.save()  # Save the DetallePrescripciones instances, now associated with prescripcion
            messages.success(request, 'Prescripcion guardada con éxito!')
            return redirect('/')  # Replace '/' with the URL you want to redirect to
    else:
        form = PrescripcionesForm()
        formset = DetallePrescripcionesFormSet()

    context = {'form': form, 'formset': formset}
    return render(request, 'base/agregarprescripcion.html', context)


def editarmedicamento(request, medicamento_id):
    medicamento = get_object_or_404(Medicamentos, id=medicamento_id)

    if request.method == 'POST':
        medicamentos_form = MedicamentosForm(request.POST, instance=medicamento)
        if medicamentos_form.is_valid():
            medicamentos_form.save()
            messages.success(request, '¡Medicamento actualizado!')
            return redirect('/')  # Redirect to a success page
    else:
        medicamentos_form = MedicamentosForm(instance=medicamento)

    return render(request, 'base/editarmedicamento.html', {'form': medicamentos_form})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Medicamentos, PrecioHMedicamento
from .forms import PrecioHMedicamentoForm

def editarpreciomedicamento(request, pk):
    medicamento = get_object_or_404(Medicamentos, id=pk)
    finalprecio = None

    # Find the existing PrecioHMedicamento instance associated with the given Medicamentos
    preciohmedicamentos = PrecioHMedicamento.objects.filter(Medicamentos=medicamento)
    if preciohmedicamentos.exists():
        finalprecio = preciohmedicamentos.first()

    if request.method == 'POST':
        preciomedicamento_form = PrecioHMedicamentoForm(request.POST)
        if preciomedicamento_form.is_valid():
            # Save the preciohmedicamento_form to get the instance
            preciomedicamento = preciomedicamento_form.save(commit=False)
            # Associate the preciomedicamento with the medicamento
            preciomedicamento.Medicamentos = medicamento
            # Now save the preciomedicamento
            preciomedicamento.save()

            # Update the precio field of the medicamento instance
            medicamento.precio = preciomedicamento.precio
            medicamento.save()

            messages.success(request, '¡Nuevo precio del medicamento registrado y actualizado!')
            return redirect('/')  # Redirect to a success page
    else:
        preciomedicamento_form = PrecioHMedicamentoForm(instance=finalprecio)

    return render(request, 'base/editarpreciomedicamento.html', {'form': preciomedicamento_form})

@login_required(login_url="/login")
def tablaordenesmedicas(request):
    ordenesmedicas = OrdenesMedicas.objects.all()
    return render(request, 'base/tablaordenesmedicas.html',{"ordenesmedicas":ordenesmedicas})

@login_required(login_url="/login")
def agregarordenmedica(request):
    if request.method == 'POST':
        form = OrdenesMedicasForm(request.POST)
        if form.is_valid():
            messages.success(request, '¡Orden Medica agregada!')#
            
            form.save()  # Save the form data to the database
            return redirect('/') 
    else:
        form = OrdenesMedicasForm()
    context = {'form': form}
    return render(request, 'base/agregarordenmedica.html', context)

@login_required(login_url="/login")
def editarordenmedica(request, pk):
    ordenesmedicas = OrdenesMedicas.objects.get(pk=pk)
    if request.method == 'POST':

        form = OrdenesMedicasForm(request.POST,instance=ordenesmedicas)
        if form.is_valid():
            messages.success(request, '¡Orden Medica actualizada!')#
            
            form.save()  # Save the form data to the database
            return redirect('/') 
    else:
        form = OrdenesMedicasForm(instance=ordenesmedicas)
    context = {'form': form}
    return render(request, 'base/agregarordenmedica.html', context)

@login_required(login_url="/login")
def tablahistorialclinico(request):
    historialclinico = HistorialClinico.objects.all()
    return render(request, 'base/tablahistorialclinico.html',{"historialclinico":historialclinico})


@login_required(login_url="/login")
def tablacitapaciente(request,pk):
    paciente = get_object_or_404(Pacientes, pk=pk)
    citas = Citas.objects.filter(paciente=paciente)  
    return render(request, 'base/tablacitapaciente.html', {'paciente': paciente, 'citas': citas})

@login_required(login_url="/login")
def tablaprescripcionespaciente(request, pk):
    paciente = get_object_or_404(Pacientes, pk=pk)
    # Adjust the query to filter through 'cita' which has a 'paciente' field
    prescripciones = Prescripciones.objects.filter(cita__paciente=paciente)

    return render(request, 'base/tablaprescripcionespaciente.html', {'paciente': paciente, 'prescripciones': prescripciones})

@login_required(login_url="/login")
def tablaordenesmedicaspaciente(request, pk):
    paciente = get_object_or_404(Pacientes, pk=pk)
    # Adjust the query to filter through 'cita' which has a 'paciente' field
    ordenesmedicas = OrdenesMedicas.objects.filter(cita__paciente=paciente)

    return render(request, 'base/tablaordenesmedicaspaciente.html', {'paciente': paciente, 'ordenesmedicas': ordenesmedicas})

@login_required(login_url="/login")
def tablaquejas(request):
    quejas = QuejasYSugerencias.objects.all()
    return render(request, 'base/tablaquejas.html',{"quejas":quejas})

@login_required(login_url="/login")
def agregarqueja(request):
    if request.method == 'POST':
        form = QuejasYSugerenciasForm(request.POST)
        if form.is_valid():
            messages.success(request, '¡Queja/Sugerencia agregado!')#
            
            form.save()  # Save the form data to the database
            return redirect('/') 
    else:
        form = QuejasYSugerenciasForm()
    context = {'form': form}
    return render(request, 'base/agregarqueja.html', context)

@login_required(login_url="/login")
def tablaparametros(request):
    parametros = Parametros.objects.all()
    return render(request, 'base/tablaparametros.html',{"parametros":parametros})

@login_required(login_url="/login")
def agregarparametros(request):
    if request.method == 'POST':
        form = ParametrosForm(request.POST)
        if form.is_valid():
            messages.success(request, '¡Parametros agregado!')#
            
            form.save()  # Save the form data to the database
            return redirect('/') 
    else:
        form = ParametrosForm()
    context = {'form': form}
    return render(request, 'base/agregarparametros.html', context)

@login_required(login_url="/login")
def editarparametros(request, pk):
    # Retrieve the existing Parametros instance
    parametros = Parametros.objects.get(pk=pk)
    
    if request.method == 'POST':
        # Populate the form with the data from the POST request and the existing instance
        form = ParametrosEditForm(request.POST, instance=parametros)
        if form.is_valid():
            # Create a new instance with the form data
            new_parametros = form.save(commit=False)
            new_parametros.pk = None  # Set the primary key to None to create a new instance
            new_parametros.save()  # Save the new instance to the database
            
            messages.success(request, '¡Parametros agregado!')
            return redirect('/')
    else:
        # Populate the form with the existing instance data
        form = ParametrosEditForm(instance=parametros)
    
    context = {'form': form}
    return render(request, 'base/editarparametros.html', context)
