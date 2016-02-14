# -*- encoding: utf-8 -*-
from django.contrib import admin

# Register your models here.
from .models import Usuarios, Permisos, Roles

admin.site.register(Usuarios)
admin.site.register(Permisos)
admin.site.register(Roles)