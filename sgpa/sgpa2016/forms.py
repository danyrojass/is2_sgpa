# -*- encoding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
import string
from .models import Roles


TIPOS = ( 
    ( 'cl', 'Cliente' ),
    ( 'ur', 'Usuario Regular'),
)
    
class RegistroUserForm(forms.Form):
    id = 0
    username = forms.CharField(min_length=5)
    email = forms.EmailField()
    password = forms.CharField(min_length=10)
    password2 = forms.CharField(min_length=10)
    telefono = forms.CharField(required=False, max_length=15)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    direccion = forms.CharField(required=False, max_length=45)
    tipo = forms.ChoiceField(choices=TIPOS)
    observacion = forms.CharField(required=False, max_length=50)

    def clean_username(self):
        """Comprueba que no exista un username igual en la db"""
        username = self.cleaned_data['username']
        if User.objects.filter(username=username):
            raise forms.ValidationError('Nombre de usuario ya registrado.')
        return username
    
    def clean_password2(self):
        """Comprueba que password y password2 sean iguales."""
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        # Setup Our Lists of Characters and Numbers
        characters = list(string.letters)
        numbers = [str(i) for i in range(10)]
        special_characters = list(string.punctuation)
        
        # Assume False until Proven Otherwise
        numCheck = False
        charCheck = False
        spcecialcharCheck = False

        # Loop until we Match        
        for char in password: 
            if not charCheck:
                if char in characters:
                    charCheck = True
            if not numCheck:
                if char in numbers:
                    numCheck = True
            if not spcecialcharCheck:
                if char in special_characters:
                    spcecialcharCheck = True
            if (numCheck and charCheck) and spcecialcharCheck:
                break
        
        if (not numCheck or not charCheck) or not spcecialcharCheck:
            raise forms.ValidationError('Su contraseña debe incluir al menos un número y un caracter no alfanumérico.')

        if password != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return password2
    
class EditarUserForm(forms.Form):
    def clean_password2(self):
        """Comprueba que password y password2 sean iguales."""
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        # Setup Our Lists of Characters and Numbers
        characters = list(string.letters)
        numbers = [str(i) for i in range(10)]
        special_characters = list(string.punctuation)
        
        # Assume False until Proven Otherwise
        numCheck = False
        charCheck = False
        spcecialcharCheck = False

        # Loop until we Match        
        for char in password: 
            if not charCheck:
                if char in characters:
                    charCheck = True
            if not numCheck:
                if char in numbers:
                    numCheck = True
            if not spcecialcharCheck:
                if char in special_characters:
                    spcecialcharCheck = True
            if (numCheck and charCheck) and spcecialcharCheck:
                break
        
        if (not numCheck or not charCheck) or not spcecialcharCheck:
            raise forms.ValidationError('Su contraseña debe incluir al menos un número y un caracter no alfanumérico.')

        if password != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return password2
    
    email = forms.EmailField()
    password = forms.CharField(min_length=10)
    password2 = forms.CharField(min_length=10)
    telefono = forms.CharField(required=False, max_length=15)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    direccion = forms.CharField(required=False, max_length=45)
    observacion = forms.CharField(required=False, max_length=50)

class ModificarContrasenaForm(forms.Form):
    actual_password = forms.CharField(min_length=10)
    password = forms.CharField(min_length=10)
    password2 = forms.CharField(min_length=10)
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        return super(ModificarContrasenaForm, self).__init__(*args, **kwargs)
    
    def clean_password_actual(self):
        """Comprueba que no exista un nombre igual en la db"""
        actual_password = self.cleaned_data['actual_password']
        if not self.user.check_password(actual_password):
            raise forms.ValidationError('La contraseña no coincide con la actual.')
        return actual_password
    
    def clean_password2(self):
        """Comprueba que password y password2 sean iguales."""
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        # Setup Our Lists of Characters and Numbers
        characters = list(string.letters)
        numbers = [str(i) for i in range(10)]
        special_characters = list(string.punctuation)
        
        # Assume False until Proven Otherwise
        numCheck = False
        charCheck = False
        spcecialcharCheck = False

        # Loop until we Match        
        for char in password: 
            if not charCheck:
                if char in characters:
                    charCheck = True
            if not numCheck:
                if char in numbers:
                    numCheck = True
            if not spcecialcharCheck:
                if char in special_characters:
                    spcecialcharCheck = True
            if (numCheck and charCheck) and spcecialcharCheck:
                break
        
        if (not numCheck or not charCheck) or not spcecialcharCheck:
            raise forms.ValidationError('Su contraseña debe incluir al menos un número y un caracter no alfanumérico.')

        if password != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return password2
    

class BuscarUserForm(forms.Form):
    id = forms.IntegerField(required=False)
    username = forms.CharField(required=False)
    email = forms.CharField(required=False)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    
class CrearRolForm(forms.Form):
    nombre = forms.CharField(max_length=50)
    tipo = forms.BooleanField(required=False)
    estado = forms.BooleanField(required=False)
    observacion = forms.CharField(max_length=50, required=False)
    
    def clean_nombre(self):
        """Comprueba que no exista un nombre igual en la db"""
        nombre = self.cleaned_data['nombre']
        if Roles.objects.filter(nombre=nombre):
            raise forms.ValidationError('Nombre de rol ya registrado.')
        return nombre
    
class BuscarRolForm(forms.Form):
    nombre = forms.CharField(required=False)
    tipo = forms.BooleanField(required=False)
    observacion = forms.CharField(required=False)
    
class EditarRolForm(forms.Form):
    nombre = forms.CharField(max_length=50)
    tipo = forms.BooleanField(required=False)
    observacion = forms.CharField(max_length=50, required=False)
    
    def __init__(self, *args, **kwargs):
        self.rol_id = kwargs.pop('rol_id')
        return super(EditarRolForm, self).__init__(*args, **kwargs)
        
    def clean_nombre(self):
        """Comprueba que no exista un nombre igual en la db"""
        nombre = self.cleaned_data['nombre']
        
        if Roles.objects.filter(nombre=nombre).exclude(id=self.rol_id):
            raise forms.ValidationError('Nombre de rol ya registrado.')
        return nombre

class AsignarRolForm(forms.Form):
    rol_id = forms.IntegerField()
    proyecto_id = forms.IntegerField()
    