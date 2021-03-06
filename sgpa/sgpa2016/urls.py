# -*- encoding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^usuarios/registro/$', views.registrar_usuarios, name='registrar_usuarios'),
    url(r'^usuarios/index/$', views.index_usuarios, name='index_usuarios'),
    url(r'^usuarios/modificar_contrasena/$', views.modificar_contrasena, name='modificar_contrasena'),
    url(r'^usuarios/(?P<user_id>\d+)/editar/$', views.editar_usuarios, name='editar_usuarios'),
    url(r'^usuarios/(?P<user_id>\d+)/eliminar/$', views.eliminar_usuarios, name='eliminar_usuarios'),
    url(r'^usuarios/(?P<user_id>\d+)/delete/$', views.delete_usuarios, name='delete_usuarios'),
    url(r'^usuarios/(?P<user_id>\d+)/ver/$', views.ver_usuarios, name='ver_usuarios'),
    url(r'^usuarios/(?P<user_id>\d+)/asignar/$', views.asignar_roles_usuarios_proyecto, name='asignar_roles_usuarios_proyecto'),
    url(r'^roles/crear/$', views.crear_roles, name='crear_roles'),
    url(r'^roles/index/$', views.index_roles, name='index_roles'),
    url(r'^roles/(?P<rol_id>\d+)/editar/$', views.editar_roles, name='editar_roles'),
    url(r'^roles/(?P<rol_id>\d+)/ver/$', views.ver_roles, name='ver_roles'),
    url(r'^roles/(?P<rol_id>\d+)/eliminar/$', views.eliminar_roles, name='eliminar_roles'),
    url(r'^roles/(?P<rol_id>\d+)/delete/$', views.delete_roles, name='delete_roles'),
    url(r'^proyectos/crear/$', views.crear_proyectos, name='crear_proyectos'),
    url(r'^proyectos/index/$', views.index_proyectos, name='index_proyectos'),
    url(r'^proyectos/(?P<proyecto_id>\d+)/definir/$', views.definir_proyectos, name='definir_proyectos'),
    url(r'^proyectos/(?P<proyecto_id>\d+)/editar/$', views.editar_proyectos, name='editar_proyectos'),
    url(r'^proyectos/(?P<proyecto_id>\d+)/ver/$', views.ver_proyectos, name='ver_proyectos'),
]