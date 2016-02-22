from django.test import TestCase
from django.contrib.auth.models import User
from .models import Usuarios, Permisos, Roles, Permisos_Roles, Roles_Usuarios
# Create your tests here.

class UsuarioTestCase(TestCase):
    
    def Registro(self):
        user = User.objects.create(username="sujeto_prueba",password="sujeto.123", 
                                   email="sujeto_prueba@mail.com", first_name="Sujeto", last_name="Prueba")
        usuario = Usuarios.objects.create(user=user, direccion="Av. Falsa 123", )