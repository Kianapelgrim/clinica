from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages
from .forms import *
from django.forms import inlineformset_factory
from django.utils import timezone
from django.views import View
from django.db.models import Max
from django.forms import modelformset_factory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.success(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request, 'Username OR password does not exit')

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
    # Create Surcursales object with form data
    surcursal  = Surcursales.objects.create(
        nombre=nombre,
        direccion=direccion,
        correoElectronico=correoElectronico,
        telefono=telefono,
    )

    # Add a success message
    messages.success(request, '¡Sucursal registrado!')

    return redirect('/tablas')
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
        return redirect('/tablas')

    return render(request, 'your_template.html', {'surcursales': surcursales})

@login_required(login_url="/login")
def eliminarSurcursal(request, id):
    surcursales = Surcursales.objects.get(id=id)
    surcursales.delete()

    messages.success(request, '¡Surcursal eliminado!')

    return redirect('/tablas')
@login_required(login_url="/login")
def tablaproveedores(request):
    # Get all proveedores
    proveedores_list = Proveedores.objects.all()

    # Search functionality
    search_query = request.GET.get('q')
    if search_query:
        proveedores_list = proveedores_list.filter(nombre__icontains=search_query)

    # Pagination
    paginator = Paginator(proveedores_list, 10)  # Show 10 proveedores per page
    page_number = request.GET.get('page')
    try:
        proveedores = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        proveedores = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        proveedores = paginator.page(paginator.num_pages)

    return render(request, 'base/tablaProveedores.html', {"proveedores": proveedores})

@login_required(login_url="/login")
def agregarproveedores(request):
    return render(request, 'base/agregarProveedores.html')

@login_required(login_url="/login")
def registrarproveedores(request):
    if request.method == 'POST':
        nombre = request.POST['txtNombre']
        direccion = request.POST['txtDireccion']
        correoElectronico = request.POST['txtCorreoElectronico']
        telefono = request.POST['txtTelefono']
        personaEncargada = request.POST['txtPersonaEncargada']


        # Create Proveedores object with form data
        proveedor = Proveedores.objects.create(
            nombre=nombre,
            direccion=direccion,
            correoElectronico=correoElectronico,
            telefono=telefono,
            personaEncargada = personaEncargada

        )

        # Add a success message
        messages.success(request, '¡Proveedor registrado!')

        return redirect('/tablaProveedores')
    else:
        # Handle GET requests or other cases
        # You can return a response for other request methods or handle them accordingly
        return redirect('/tablaProveedores')  # Redirect to home page or render a specific template
 
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
        personaEncargada = request.POST['txtPersonaEncargada']


        # Update Surcursales object fields
        proveedores.nombre = nombre
        proveedores.direccion = direccion
        proveedores.correoElectronico = correoElectronico
        proveedores.telefono = telefono
        proveedores.personaEncargada = personaEncargada
        # Save the updated object
        proveedores.save()

        # Add a success message
        messages.success(request, '¡Proveedor actualizado!')

        # Redirect to a relevant URL
        return redirect('/tablaProveedores')

    return render(request, 'your_template.html', {'proveedores': proveedores})



@login_required(login_url="/login")
def tablapreciohmedicamento(request):
    preciohmedicamento = PrecioHMedicamento.objects.all()
    return render(request, 'base/tablapreciohmedicamento.html', {"preciohmedicamento": preciohmedicamento})
@login_required(login_url="/login")
def tablamedicamentos(request):
    medicamentos_list = Medicamentos.objects.all()
    
    # Search functionality
    search_query = request.GET.get('q')
    if search_query:
        medicamentos_list = medicamentos_list.filter(nombre__icontains=search_query)
    
    # Pagination
    paginator = Paginator(medicamentos_list, 10)  # Show 10 items per page
    page = request.GET.get('page')
    try:
        medicamentos = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        medicamentos = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        medicamentos = paginator.page(paginator.num_pages)
    
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
            return redirect('/tablamedicamentos')  # Redirect to a success page
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
            return redirect('/tablamedicamentos')  # Redirect to a success page
    else:
        medicamentos_form = MedicamentosForm()
        preciohmedicamentos_form = PrecioHMedicamentoForm()
    return render(request, 'base/agregarmedicamentos.html', {'medicamentos_form': medicamentos_form, 'preciohmedicamentos_form': preciohmedicamentos_form})



@login_required(login_url="/login")
def eliminarmedicamentos(request, id):
    medicamentos = Medicamentos.objects.get(id=id)
    medicamentos.delete()

    messages.success(request, '¡Medicamentos eliminado!')

    return redirect('/tablamedicamentos')




@login_required(login_url="/login")
def tablaecmedicamentos(request):
    ecmedicamentos = ECMedicamentos.objects.all()
    return render(request, 'base/tablaecmedicamentos.html',{"ecmedicamentos":ecmedicamentos})
@login_required(login_url="/login")
def agregarecmedicamentos(request):
    if request.method == 'POST':
        form = ECMedicamentosForm(request.POST)
        if form.is_valid():
            messages.success(request, '¡Estado Compra Medicamento agregado!')#
            
            form.save()  # Save the form data to the database
            return redirect('/tablaecmedicamentos') 
    else:
        form = ECMedicamentosForm()
    context = {'form': form}
    return render(request, 'base/agregarecmedicamentos.html', context)
 
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
        return redirect('/tablaecmedicamentos')

    render(request, 'your_template.html', {'ecmedicamentos': ecmedicamentos})

@login_required(login_url="/login")
def eliminarecmedicamentos(request, id):
    ecmedicamentos = ECMedicamentos.objects.get(id=id)
    ecmedicamentos.delete()

    messages.success(request, '¡Estado de compra de medicamentos eliminado!')

    return redirect('/tablaecmedicamentos')


def tablaInventarioMedicamento(request):
    inventarioMedicamento_list = InventarioMedicamento.objects.all()
    
    # Search functionality
    search_query = request.GET.get('q')
    if search_query:
        inventarioMedicamento_list = inventarioMedicamento_list.filter(medicamento__nombre__icontains=search_query)
    
    # Pagination
    paginator = Paginator(inventarioMedicamento_list, 10)  # Show 10 items per page
    page = request.GET.get('page')
    try:
        inventarioMedicamento = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        inventarioMedicamento = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        inventarioMedicamento = paginator.page(paginator.num_pages)
    
    return render(request, 'base/tablaInventarioMedicamento.html', {"inventarioMedicamento": inventarioMedicamento})

@login_required(login_url="/login")
def tablalotemedicamento(request):
    lotemedicamento_list = LoteMedicamento.objects.all()
    
    # Search functionality
    search_query = request.GET.get('q')
    if search_query:
        lotemedicamento_list = lotemedicamento_list.filter(medicamento__nombre__icontains=search_query)
    
    # Pagination
    paginator = Paginator(lotemedicamento_list, 10)  # Show 10 items per page
    page = request.GET.get('page')
    try:
        lotemedicamento = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        lotemedicamento = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        lotemedicamento = paginator.page(paginator.num_pages)
    
    return render(request, 'base/tablalotemedicamento.html', {"lotemedicamento": lotemedicamento})  

def tablacompra(request):
    compras = CompraMedicamento.objects.all()
    search_query = request.GET.get('q')

    # Filter the data based on the search query
    if search_query:
        compras = compras.filter(
            proveedor__nombre__icontains=search_query
        )

    # Pagination
    paginator = Paginator(compras, 10)  # Show 10 items per page
    page_number = request.GET.get('page')
    try:
        compras = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        compras = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        compras = paginator.page(paginator.num_pages)

    # Render the template with the paginated data
    return render(request, 'base/tablacompra.html', {'compras': compras})

@login_required(login_url="/login")
def compraMedicamento(request):
    LoteCompraFormSet = inlineformset_factory(CompraMedicamento, LoteMedicamento, 
                                                  form=LoteForm, extra=2, can_delete=True)
    if request.method == 'POST':
        form = CompraMedicamentoForm(request.POST)
        formset = LoteCompraFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            medicamento = form.save()  # Use a different variable name for the form instance
            formset.instance = medicamento  # Assign the instance to each form in the formset
            formset.save()  # Save the DetallePrescripciones instances, now associated with prescripcion
            messages.success(request, 'Compra guardada con éxito!')
            return redirect('/tablacompra')  # Replace '/' with the URL you want to redirect to
    else:
        form = CompraMedicamentoForm()
        formset = LoteCompraFormSet()

    context = {'form': form, 'formset': formset}


    return render(request, 'base/compraMedicamento.html', context)

@login_required(login_url="/login")
def editarcompramedicamento(request, compra_id):

    
    compra = get_object_or_404(CompraMedicamento, id=compra_id)

    if compra.estadoCompra.id == 9:
        messages.success(request, 'Esta compra ha sido cancelada y no puede modificarse.')
        return redirect('/tablacompra')

    if compra.estadoCompra.id == 8:
        messages.success(request, 'Esta compra ha sido aprobada y no puede modificarse.')
        return redirect('/tablacompra')  # Redirect to a different page, e.g., dashboard
    
    LoteCompraFormSet = inlineformset_factory(CompraMedicamento, LoteMedicamento,
                                              form=LoteForm, extra=0, can_delete=True)

    if request.method == 'POST':
        form = EditCompraMedicamentoForm(request.POST, instance=compra)
        formset = LoteCompraFormSet(request.POST, instance=compra)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Compra actualizada con éxito!')
            return redirect('/tablacompra')
    else:
        form = EditCompraMedicamentoForm(instance=compra)
        formset = LoteCompraFormSet(instance=compra)

    context = {'form': form, 'formset': formset, 'compra_id': compra_id}

    if compra.estadoCompra.nombre == "Aprobado":
                # Get all lote_med for the specific compraMedicamento
                lotes = LoteMedicamento.objects.filter(compra=compra)

                # Iterate over each loteMedicamento
                for lote in lotes:
                    # Get the related medicamento
                    medicamento = lote.medicamento

                    # Get or create the related InventarioMedicamento
                    inventario, created = InventarioMedicamento.objects.get_or_create(medicamento=medicamento)
                    
                    # Update stock and lote in InventarioMedicamento
                    inventario.stock += lote.cantidad
                    inventario.save()

    return render(request, 'base/editarcompramedicamento.html', context)



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
            return redirect('/tablametodospago') 
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
            return redirect('/tipodocumento') 
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
            return redirect('/tablacargos') 
    else:
        form = CargosForm()
    context = {'form': form}
    return render(request, 'base/agregarcargo.html', context)

@login_required(login_url="/login")
def editarcargo(request,pk):
    cargo = Cargos.objects.get(pk=pk)
    if request.method == 'POST':
        form = CargosForm(request.POST,instance=cargo)
        if form.is_valid():
            messages.success(request, '¡Cargo agregado!')#
            
            form.save()  # Save the form data to the database
            return redirect('/tablacargos') 
    else:
        form = CargosForm(instance=cargo)
    context = {'form': form}
    return render(request, 'base/agregarcargo.html', context)


@login_required(login_url="/login")
def tablaempleados(request):
    empleados = Empleados.objects.all()
    search_query = request.GET.get('q')

    # Filter the data based on the search query
    if search_query:
        empleados = empleados.filter(
            nombre__icontains=search_query
        )

    # Paginate the data
    paginator = Paginator(empleados, 10)  # Show 10 empleados per page
    page_number = request.GET.get('page')
    try:
        empleados = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        empleados = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        empleados = paginator.page(paginator.num_pages)

    # Render the template with the paginated and filtered data
    return render(request, 'base/tablaempleados.html', {"empleados": empleados, "search_query": search_query})

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
            return redirect('/tablaempleados')  # Redirect to a success page
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
            return redirect('/tablaempleados')  # Redirect to a success page
    else:
        empleado_form = EmpleadosForm(instance=empleados)
        documento_form = DocumentoForm(instance=documentos)
    return render(request, 'base/editarempleados.html', {'empleado_form': empleado_form, 'documento_form': documento_form})
   

@login_required(login_url="/login")
def eliminarempleados(request, pk):
    empleados = Empleados.objects.get(pk=pk)
    empleados.delete()

    messages.success(request, '¡Empleado eliminado!')

    return redirect('/tablaempleados')

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
            return redirect('/tablatiposalas') 
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
            return redirect('/tablatiposalas') 
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
            return redirect('/tablasalas') 
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
            return redirect('/tablasalas') 
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
    # Get all patients
    pacientes_list = Pacientes.objects.all()

    # Search functionality
    search_query = request.GET.get('q')
    if search_query:
        pacientes_list = pacientes_list.filter(nombre__icontains=search_query)

    # Pagination
    paginator = Paginator(pacientes_list, 10)  # Show 10 patients per page
    page_number = request.GET.get('page')
    try:
        pacientes = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        pacientes = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        pacientes = paginator.page(paginator.num_pages)

    return render(request, 'base/tablapacientes.html', {"pacientes": pacientes})

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
            return redirect('/tablapacientes')  # Redirect to a success page
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
            return redirect('/tablapacientes')  # Redirect to a success page
    else:
        pacientes_form = PacientesForm(instance=pacientes)
        documento_form = DocumentoForm(instance=documentos)
    return render(request, 'base/editarpaciente.html', {'pacientes_form': pacientes_form, 'documento_form': documento_form})

def tablacitas(request):
    citas = Citas.objects.all()
    search_query = request.GET.get('q')

    # Filter the data based on the search query
    if search_query:
        citas = citas.filter(
            paciente__nombre__icontains=search_query
        )

    # Paginate the data
    paginator = Paginator(citas, 10)  # Show 10 citas per page
    page_number = request.GET.get('page')
    try:
        citas = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        citas = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        citas = paginator.page(paginator.num_pages)

    # Render the template with the paginated and filtered data
    return render(request, 'base/tablacitas.html', {"citas": citas, "search_query": search_query})

@login_required(login_url="/login")
def agregarcita(request):
    if request.method == 'POST':
        form = CitasForm(request.POST)
        if form.is_valid():
            messages.success(request, '¡Cita agregada!')#
            
            form.save()  # Save the form data to the database
            return redirect('/tablacitas') 
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
            return redirect('/tablacitas') 
    else:
        form = CitasForm(instance=cita)
    context = {'form': form}
    return render(request, 'base/agregarcita.html', context)

@login_required(login_url="/login")
def eliminarcita(request, id):
    try:
        cita = Citas.objects.get(id=id)
        # Use timezone.now() instead of datetime.datetime.now() to get a timezone-aware current time
        if cita.fecha > timezone.now():
            cita.delete()
            messages.success(request, '¡Cita eliminada!')
        else:
            messages.success(request, 'No se puede eliminar la cita porque la fecha ya ha pasado.')
    except Citas.DoesNotExist:
        messages.success(request, 'La cita no existe.')

    return redirect('/tablacitas')



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
            return redirect('/tablaprescripciones')  # Replace '/' with the URL you want to redirect to
    else:
        form = PrescripcionesForm()
        formset = DetallePrescripcionesFormSet()

    context = {'form': form, 'formset': formset}
    return render(request, 'base/agregarprescripcion.html', context)

@login_required(login_url="/login")
def editarmedicamento(request, medicamento_id):
    medicamento = get_object_or_404(Medicamentos, id=medicamento_id)

    if request.method == 'POST':
        medicamentos_form = MedicamentosForm(request.POST, instance=medicamento)
        if medicamentos_form.is_valid():
            medicamentos_form.save()
            messages.success(request, '¡Medicamento actualizado!')
            return redirect('/tablaprescripciones')  # Redirect to a success page
    else:
        medicamentos_form = MedicamentosForm(instance=medicamento)

    return render(request, 'base/editarmedicamento.html', {'form': medicamentos_form})

@login_required(login_url="/login")
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
            return redirect('/tablamedicamentos')  # Redirect to a success page
    else:
        preciomedicamento_form = PrecioHMedicamentoForm(instance=finalprecio)

    return render(request, 'base/editarpreciomedicamento.html', {'form': preciomedicamento_form})

@login_required(login_url="/login")
def tablaordenesmedicas(request):
    ordenesmedicas_list = OrdenesMedicas.objects.all()
    
    # Search functionality
    search_query = request.GET.get('q')
    if search_query:
        ordenesmedicas_list = ordenesmedicas_list.filter(cita__paciente__nombre__icontains=search_query)  # Replace field_to_search with the field you want to search
    
    # Pagination
    paginator = Paginator(ordenesmedicas_list, 10)  # Show 10 items per page
    page = request.GET.get('page')
    try:
        ordenesmedicas = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        ordenesmedicas = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        ordenesmedicas = paginator.page(paginator.num_pages)
    
    context = {
        'ordenesmedicas': ordenesmedicas,
    }
    return render(request, 'base/tablaordenesmedicas.html', context)

@login_required(login_url="/login")
def agregarordenmedica(request):
    if request.method == 'POST':
        form = OrdenesMedicasForm(request.POST)
        if form.is_valid():
            messages.success(request, '¡Orden Medica agregada!')#
            
            form.save()  # Save the form data to the database
            return redirect('/tablaordenesmedicas') 
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
            return redirect('/tablaordenesmedicas') 
    else:
        form = OrdenesMedicasForm(instance=ordenesmedicas)
    context = {'form': form}
    return render(request, 'base/agregarordenmedica.html', context)

@login_required(login_url="/login")
def tablahistorialclinico(request):
    historialclinico = HistorialClinico.objects.all()

    # Handling search functionality
    search_query = request.GET.get('q')
    if search_query:
        historialclinico = historialclinico.filter(nombre__icontains=search_query)

    # Pagination
    paginator = Paginator(historialclinico, 10)  # Show 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'base/tablahistorialclinico.html', {"page_obj": page_obj})


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
def tablamedicamentosprescripcion(request, pk):
    prescripcion = get_object_or_404(Prescripciones, pk=pk)
    # Adjust the query to filter through 'cita' which has a 'paciente' field
    detallePrescripciones = DetallePrescripciones.objects.filter(prescripcion=prescripcion)

    return render(request, 'base/tablamedicamentosprescripcion.html', {'prescripcion': prescripcion, 'detallePrescripciones': detallePrescripciones})

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
            return redirect('/tablaquejas') 
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
            return redirect('/tablaparametros') 
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
            # Save the form
            form.save()
            
            messages.success(request, '¡Parámetros actualizados!')
            return redirect('/tablaparametros')
    else:
        # Populate the form with the existing instance data
        form = ParametrosEditForm(instance=parametros)
    
    # Exclude 'surcursal' from the form fields
    if 'surcursal' in form.fields:
        form.fields.pop('surcursal')
    
    context = {'form': form}
    return render(request, 'base/editarparametros.html', context)

@login_required(login_url="/login")
def factura(request, pk):
    cita = get_object_or_404(Citas, pk=pk)
    parametros = Parametros.objects.filter(surcursal=cita.surcursal).first()  # Assumes only one matching Parametros

    if parametros.next_invoice_number == parametros.rangoAutorizadoFinal:
        messages.success(request, 'Se ha llegado al rangoAutorizadoFinal.')
        return redirect('/tablafacturas')
    # Retrieve the specific Cita based on primary key
    

    

    if Factura.objects.filter(id=cita).exists():
        messages.success(request, 'Factura ya creada.')
        return redirect('/tablafacturas')
    

    
    
    isv = get_object_or_404(ISV, pk=1)
    

    if request.method == 'POST':
        
        form = FacturaForm(request.POST)
        if form.is_valid():
            subtotal=0 
    # Retrieve all Prescripciones linked to this specific Cita
            prescripciones = Prescripciones.objects.filter(cita=cita)
            # Fetch the Parametros associated with the Surcursal of the Cita
            

            for prescripcion in prescripciones:

                detalles_prescripciones = DetallePrescripciones.objects.filter(prescripcion=prescripcion)
                for detalle in detalles_prescripciones:
                    inventario_medicamento = InventarioMedicamento.objects.filter(medicamento=detalle.medicamento).first()
                    lotes = LoteMedicamento.objects.filter(medicamento=detalle.medicamento).order_by('fechaVencimiento')
                    cantidad= detalle.cantidad
                    if inventario_medicamento.stock - detalle.cantidad < 0:
                        subtotal += 0
                        messages.warning(request, f"{detalle.medicamento.nombre} no tiene stock suficiente.")
                    else:


                        subtotal = subtotal + (detalle.medicamento.precio*cantidad)
                    
                        inventario_medicamento.stock -= detalle.cantidad
                        inventario_medicamento.save()
                        new_detalle_factura = DetalleFactura(
                            cita=cita,
                            detallePrescripcion=detalle
                        )
                        new_detalle_factura.save()
                        


                        for lote in lotes:
                            if cantidad < lote.cantidad:
                                lote.cantidad -= cantidad
                                lote.save()
                                break
                            else:
                                cantidad -= lote.cantidad
                                lote.cantidad=0
                                lote.save()
                            

                        
                        
                
            subtotal= subtotal + cita.tipocita.precio

            total= subtotal*isv.impuesto
            total= total+subtotal 
            
        

                # Increment the invoice number in Parametros for the next use
            parametros.next_invoice_number += 1
            parametros.save()
            rtn = form.cleaned_data['rtn']
            descuento = form.cleaned_data['descuento']
            metodoPago = form.cleaned_data['metodoPago']
            new_factura = Factura(
                id= cita,
                numero=str(parametros.next_invoice_number),
                parametros=parametros,
                surcursal=parametros.surcursal,
                paciente=cita.paciente,
                isv= isv,
                subtotal= subtotal,
                total = total,
                rtn=rtn,
                descuento= descuento,
                metodoPago= metodoPago
            )
            new_factura.save()
            return redirect('/tablafacturas') 

            
    else:
        form = FacturaForm()

    # Prepare the context with the collected data
    context = {'form': form}

    # Render the response with the collected data in the factura.html template
    return render(request, 'base/factura.html', context)


@login_required(login_url="/login")
def tablatipocitas(request):
    tipocita = TipoCitas.objects.all()
    return render(request, 'base/tablatipocitas.html',{"tipocita":tipocita})

@login_required(login_url="/login")
def agregartipocita(request):
    
    if request.method == 'POST':
        form = TipoCitasForm(request.POST)
        if form.is_valid():
            messages.success(request, '¡Tipo de Cita agregado!')#
            
            form.save()  # Save the form data to the database
            return redirect('/tablatipocitas') 
    else:
        form = TipoCitasForm()
    context = {'form': form}
    return render(request, 'base/agregartipocita.html', context)

@login_required(login_url="/login")
def editartipocita(request,pk):
    tipocita = get_object_or_404(TipoCitas, pk=pk)
    if request.method == 'POST':
        form = TipoCitasForm(request.POST, instance=tipocita)
        if form.is_valid():
            messages.success(request, '¡Tipo de Cita agregado!')#
            
            form.save()  # Save the form data to the database
            return redirect('/tablatipocitas') 
    else:
        form = TipoCitasForm(instance=tipocita)
    context = {'form': form}
    return render(request, 'base/editartipocita.html', context)
@login_required(login_url="/login")

def tablaisv(request):
    isv = ISV.objects.all()
    return render(request, 'base/tablaisv.html',{"isv":isv})

@login_required(login_url="/login")
def isv(request,pk):
    isv = ISV.objects.get(pk=pk)
    if request.method == 'POST':
        form = ISVForm(request.POST,instance=isv)
        if form.is_valid():
            messages.success(request, '¡ISV actualizado!')#
            
            form.save()  # Save the form data to the database
            return redirect('/tablaisv') 
    else:
        form = ISVForm(instance=isv)
    context = {'form': form}
    return render(request, 'base/isv.html', context)


@login_required(login_url="/login")
def tablafacturas(request):
    facturas_list = Factura.objects.all()

    # Get the search query from the request
    search_query = request.GET.get('q')

    # If there's a search query, filter the facturas based on it
    if search_query:
        facturas_list = facturas_list.filter(paciente__nombre__icontains=search_query)

    # Paginate the filtered facturas list
    paginator = Paginator(facturas_list, 10)  # Show 10 facturas per page
    page_number = request.GET.get('page')

    try:
        facturas = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        facturas = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        facturas = paginator.page(paginator.num_pages)

    return render(request, 'base/tablafacturas.html', {"facturas": facturas})

@login_required(login_url="/login")
def facturas(request,pk):
    factura = Factura.objects.get(pk=pk)
    cita = Citas.objects.get(pk=pk)
    detalleFactura = DetalleFactura.objects.filter(cita=cita)
   
    context = {
        'factura': factura,
        'cita': cita,
        'detalleFactura': detalleFactura,
        
        }


    return render(request, 'base/facturas.html',context)
