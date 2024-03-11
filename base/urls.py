from django.urls import path
from . import views



urlpatterns = [
    path('', views.home , name= "home"),
    path('login', views.login , name= "login"),

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

]   
