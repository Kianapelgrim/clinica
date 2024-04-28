from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('login', views.loginPage , name= "login"),
    path('', views.home , name= "home"),
  

    path('tablas', views.tables , name= "tablas"),
    path('agregarsurcursal/', views.agregarsurcursal, name='agregarsurcursal'),
    path('registrarSurcursal/', views.registrarSurcursal, name='registrarSurcursal'),
    path('editarSurcursal/<int:id>/', views.editarSurcursal, name='editarSurcursal'),
    path('edicionSurcursal/<int:id>/', views.edicionSurcursal, name='edicionSurcursal'),
    path('eliminarSurcursal/<int:id>/', views.eliminarSurcursal, name='eliminarsurcursal'),

    path('tablaProveedores', views.tablaproveedores, name='tablaProveedores'),
    path('agregarproveedores/', views.agregarproveedores, name='agregarproveedores'),
    path('registrarproveedores/', views.registrarproveedores, name='registrarproveedores'),
    path('editarProveedores/<int:id>/', views.editarproveedores, name='editarproveedores'),
    path('edicionProveedores/<int:id>/', views.edicionproveedores, name='edicionProveedores'),

    path('tablamedicamentos', views.tablamedicamentos, name='tablamedicamentos'),
    path('agregarmedicamentos/', views.agregarmedicamentos, name='agregarmedicamentos'),
    path('editarmedicamento/<int:medicamento_id>/', views.editarmedicamento, name='editarmedicamento'),
    path('editarpreciomedicamento/<int:pk>/', views.editarpreciomedicamento, name='editarpreciomedicamento'),
    path('eliminarmedicamentos/<int:id>/', views.eliminarmedicamentos, name='eliminarmedicamentos'),


    path('tablaecmedicamentos', views.tablaecmedicamentos, name='tablaecmedicamentos'),
    path('agregarecmedicamentos/', views.agregarecmedicamentos, name='agregarecmedicamentos'),
    path('editarecmedicamentos/<int:id>/', views.editarecmedicamentos, name='editarecmedicamentos'),
    path('edicionecmedicamentos/<int:id>/', views.edicionecmedicamentos, name='edicionecmedicamentos'),
    path('eliminarecmedicamentos/<int:id>/', views.eliminarecmedicamentos, name='eliminarecmedicamentos'),


    path('tablapreciohmedicamento', views.tablapreciohmedicamento, name='tablapreciohmedicamento'),


    path('tablaInventarioMedicamento', views.tablaInventarioMedicamento, name='tablaInventarioMedicamento'),


    path('tablalotemedicamento', views.tablalotemedicamento, name='tablalotemedicamento'),

    path('tablacompra', views.tablacompra, name='tablacompra'),

    path('compraMedicamento', views.compraMedicamento, name='compraMedicamento'),

    path('editarcompramedicamento/<int:compra_id>/', views.editarcompramedicamento, name='editarcompramedicamento'),

    path('tablametodospago', views.tablametodospago, name='tablametodospago'),

    path('agregarmetodospago', views.agregarmetodospago, name='agregarmetodospago'),

    path('tablatipodocumento', views.tablatipodocumento, name='tablatipodocumento'),

    path('agregartipodocumento', views.agregartipodocumento, name='agregartipodocumento'),

    path('tablacargos', views.tablacargos, name='tablacargos'),

    path('agregarcargo/', views.agregarcargo, name='agregarcargo'),

    path('editarcargo/<int:pk>/', views.editarcargo, name='editarcargo'),

    path('tabladocumento', views.tabladocumento, name='tabladocumento'),

    path('tablaempleados', views.tablaempleados, name='tablaempleados'),

    path('agregarempleados/', views.agregarempleados, name='agregarempleados'),

    path('editarempleados/<int:pk>/', views.editarempleados, name='editarempleados'),

    path('eliminarempleados/<int:pk>/', views.eliminarempleados, name='eliminarempleados'),

    path('tablatiposalas/', views.tablatiposalas, name='tablatiposalas'),

    path('tablasalas/', views.tablasalas, name='tablasalas'),

    path('agregartiposala/', views.agregartiposala, name='agregartiposala'),

    path('agregarsala/', views.agregarsala, name='tagregarsala'),

    path('editartiposala/<int:pk>/', views.editartiposala, name='editartiposala'),

    path('editarsala/<int:pk>/', views.editarsala, name='editarsala'),

    path('tablapacientes', views.tablapacientes, name='tablapacientes'),

    path('agregarpaciente/', views.agregarpaciente, name='agregarpaciente'),

    path('editarpaciente/<int:pk>/', views.editarpaciente, name='editarpaciente'),

    path('tablatipocitas/', views.tablatipocitas, name='tablatipocitas'),

    path('agregartipocita/', views.agregartipocita, name='agregartipocita'),

    path('tablacitas', views.tablacitas, name='tablacitas'),

    path('agregarcita/', views.agregarcita, name='agregarcita'),

    path('editarcita/<int:pk>/', views.editarcita, name='editarcita'),

    path('eliminarcita/<int:id>/', views.eliminarcita, name='eliminarcita'),

    path('tablaprescripciones', views.tablaprescripciones, name='tablaprescripciones'),

    path('agregarprescripcion/', views.agregarprescripcion, name='agregarprescripcion'),
   
    path('tablaordenesmedicas', views.tablaordenesmedicas, name='tablaordenesmedicas'),

    path('agregarordenmedica/', views.agregarordenmedica, name='agregarordenmedica'),

    path('editarordenmedica/<int:pk>/', views.editarordenmedica, name='editarordenmedica'),

    path('tablahistorialclinico', views.tablahistorialclinico, name='tablahistorialclinico'),

    path('tablacitapaciente/<int:pk>/', views.tablacitapaciente, name='tablacitapaciente'),

    path('tablaprescripcionespaciente/<int:pk>/', views.tablaprescripcionespaciente, name='tablaprescripcionespaciente'),

    path('tablaordenesmedicaspaciente/<int:pk>/', views.tablaordenesmedicaspaciente, name='tablaordenesmedicaspaciente'),

    path('tablaquejas/', views.tablaquejas, name='tablaquejas'),

    path('agregarqueja/', views.agregarqueja, name='agregarqueja'),

    path('factura/<int:pk>/', views.factura, name='factura'),

    path('tablaparametros/', views.tablaparametros, name='tablaparametros'),

    path('agregarparametros/', views.agregarparametros, name='agregarparametros'),

    path('tablaisv/', views.tablaisv, name='tablaisv'),

    path('isv/<int:pk>/', views.isv, name='isv'),

    path('editarparametros/<int:pk>/', views.editarparametros, name='editarparametros'),

    path('tablamedicamentosprescripcion/<int:pk>/', views.tablamedicamentosprescripcion, name='tablamedicamentosprescripcion'),

    path('tablafacturas/', views.tablafacturas, name='tablafacturas'),

    path('facturas/<int:pk>/', views.facturas, name='facturas'),

]   
