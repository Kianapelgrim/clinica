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
    path('eliminarProveedores/<int:id>/', views.eliminarproveedores, name='eliminarProveedores'),

    path('tablamedicamentos', views.tablamedicamentos, name='tablamedicamentos'),
    path('agregarmedicamentos/', views.agregarmedicamentos, name='agregarmedicamentos'),
    path('registrarmedicamentos/', views.registrarmedicamentos, name='registrarmedicamentos'),
    path('editarmedicamentos/<int:id>/', views.editarmedicamentos, name='editarmedicamentos'),
    path('edicionmedicamentos/<int:id>/', views.edicionmedicamentos, name='edicionmedicamentos'),
    path('eliminarmedicamentos/<int:id>/', views.eliminarmedicamentos, name='eliminarmedicamentos'),


    path('tablaecmedicamentos', views.tablaecmedicamentos, name='tablaecmedicamentos'),
    path('agregarecmedicamentos/', views.agregarecmedicamentos, name='agregarecmedicamentos'),
    path('registrarecmedicamentos/', views.registrarecmedicamentos, name='registrarecmedicamentos'),
    path('editarecmedicamentos/<int:id>/', views.editarecmedicamentos, name='editarecmedicamentos'),
    path('edicionecmedicamentos/<int:id>/', views.edicionecmedicamentos, name='edicionecmedicamentos'),
    path('eliminarecmedicamentos/<int:id>/', views.eliminarecmedicamentos, name='eliminarecmedicamentos'),


    path('tablapreciohmedicamento', views.tablapreciohmedicamento, name='tablapreciohmedicamento'),
    path('agregarpreciohmedicamento/', views.agregarpreciohmedicamento, name='agregarpreciohmedicamento'),
    path('eliminarpreciohmedicamento/<int:id>/', views.eliminarpreciohmedicamento, name='eliminarpreciohmedicamento'),


    path('tablaInventarioMedicamento', views.tablaInventarioMedicamento, name='tablaInventarioMedicamento'),


    path('tablalotemedicamento', views.tablalotemedicamento, name='tablalotemedicamento'),

    path('tablacompra', views.tablacompra, name='tablacompra'),

    path('compraMedicamento', views.compraMedicamento, name='compraMedicamento'),

    path('editarcompramedicamento/<int:pk>/', views.editarcompramedicamento, name='editarcompramedicamento'),

    path('tablametodospago', views.tablametodospago, name='tablametodospago'),

    path('agregarmetodospago', views.agregarmetodospago, name='agregarmetodospago'),

    path('tablatipodocumento', views.tablatipodocumento, name='tablatipodocumento'),

    path('agregartipodocumento', views.agregartipodocumento, name='agregartipodocumento'),
]   
