# -*- encoding: utf-8 -*-
from django.db import models
from django.conf import settings

class Permisos(models.Model):
    nombre = models.CharField(max_length=50, default="")
    nivel = models.IntegerField()
    estado = models.BooleanField(default=False)
    def __unicode__(self):
        return u"%s" % self.nombre

    def __str__(self):
        return self.nombre
    
class Roles(models.Model):
    nombre = models.CharField(max_length=50, default="")
    tipo = models.BooleanField(default=False) #True: Roles de Sistema. False: Roles de Usuario.
    estado = models.BooleanField(default=False)
    observacion = models.CharField(max_length=50, default="")
    permisos = models.ManyToManyField(Permisos, through='Permisos_Roles')

    def __str__(self):
        return self.nombre
    
class Usuarios(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    telefono = models.CharField(max_length=15, default="")
    direccion = models.CharField(max_length=45, default="")
    tipo = models.CharField(max_length=2, default="")
    observacion = models.CharField(max_length=50, default="")
    roles = models.ManyToManyField(Roles, through='Roles_Usuarios')
    
    def __str__(self):
        return self.user.username

class Permisos_Roles(models.Model):
    permisos = models.ForeignKey(Permisos)
    roles = models.ForeignKey(Roles)
    
class Roles_Usuarios(models.Model):
    roles = models.ForeignKey(Roles)
    usuario = models.ForeignKey(Usuarios)
    
    def __str__(self):
        return self.roles

class Proyectos(models.Model):
    nombre_largo = models.CharField(max_length=15, default="")
    nombre_corto = models.CharField(max_length=15, default="")
    tipo = models.BooleanField(default=False) #True: Proyecto. False: Servicio.
    descripcion = models.CharField(max_length=15, default="")
    fecha_inicio = models.DateField()
    fecha_fin_estimado = models.DateField()
    fecha_fin_real = models.DateField()
    observaciones = models.CharField(max_length=15, default="")
    estado = models.IntegerField(default=4) #1: Pendiente. 2: Anulado. 3: Activo. 4: Finalizado.
    
    def __str__(self):
        return self.nombre