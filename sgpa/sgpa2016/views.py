# -*- encoding: utf-8 -*-

from django.shortcuts import get_object_or_404, render, render_to_response
from django.contrib.auth.models import User

from .forms import RegistroUserForm, EditarUserForm, BuscarUserForm, CrearRolForm, BuscarRolForm, EditarRolForm, ModificarContrasenaForm, AsignarRolForm, CrearProyectoForm, DefinirProyectoForm, BuscarProyectoForm, EditarProyectoForm
from .models import Usuarios, Permisos, Roles, Permisos_Roles, Roles_Usuarios, Proyectos, Usuarios_Proyectos

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

from django.http import HttpResponseRedirect
from django.template import RequestContext
from datetime import datetime
from django.contrib.auth.hashers import make_password


"""Ingreso al sistema."""
def inicio(request):    
    if request.user.is_anonymous():
        return HttpResponseRedirect('/ingresar')
    else:
        return HttpResponseRedirect('/index')

def ingresar(request):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    request.session['last_activity'] = str(now)
    
    if not request.user.is_anonymous():
        return HttpResponseRedirect('/index')
    if request.method == 'POST':
        formulario = AuthenticationForm(request.POST)
        if formulario.is_valid:
            usuario = request.POST['username']
            clave = request.POST['password']
            acceso = authenticate(username=usuario, password=clave)
            if acceso is not None:
                if acceso.is_active:
                    login(request, acceso)

                    return HttpResponseRedirect('/index')
                else:
                    return render_to_response('noactivo.html', context_instance=RequestContext(request))
            else:
                return render_to_response('nousuario.html', context_instance=RequestContext(request))
    else:
        formulario = AuthenticationForm()
    return render_to_response('login.html',{'formulario':formulario}, context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def cerrar(request):
    logout(request)
    return HttpResponseRedirect('/ingresar')

@login_required(login_url='/ingresar')
def index(request):
    comprobar(request)
    if(request.user.is_anonymous()):
        return HttpResponseRedirect('/ingresar')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    request.session['last_activity'] = str(now)
    
    usuario = request.user
    staff= request.user.is_staff
    
    saludo= saludo_dia()
        
    if staff:
        return render_to_response('inicio_admin.html', {'usuario':usuario, 'saludo':saludo}, context_instance=RequestContext(request))    
    else:
        return render_to_response('inicio_usuario.html', {'usuario':usuario, 'saludo':saludo}, context_instance=RequestContext(request))   

def creditos(request):
    comprobar(request)
    if(request.user.is_anonymous()):
        return HttpResponseRedirect('/ingresar')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    request.session['last_activity'] = str(now)
        
    usuario = request.user
    saludo = saludo_dia()
    return render_to_response('creditos.html', {'usuario':usuario, 'saludo':saludo}, context_instance=RequestContext(request))    
     
"""Administración de Usuarios"""
@login_required(login_url='/ingresar')
def registrar_usuarios(request):
    aid = 1
    comprobar(request)
    if(request.user.is_anonymous()):
        return HttpResponseRedirect('/ingresar')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    request.session['last_activity'] = str(now)
        
    usuario = request.user
    saludo = saludo_dia()
        
    if request.method == 'POST':
        form = RegistroUserForm(request.POST, request.FILES)
    
        if form.is_valid():
            cleaned_data = form.cleaned_data
            username = cleaned_data.get('username')
            password = cleaned_data.get('password')
            email = cleaned_data.get('email')
            first_name = cleaned_data.get('first_name')
            last_name = cleaned_data.get('last_name')
            telefono = cleaned_data.get('telefono')
            direccion = cleaned_data.get('direccion')
            tipo = cleaned_data.get('tipo')
            observacion = cleaned_data.get('observacion')
    
            user_model = User.objects.create_user(username=username, password=password)
            user_model.email = email
            user_model.first_name = first_name
            user_model.last_name = last_name
            user_model.is_active = True
            user_model.save()
                
            user_profile = Usuarios()
            user_profile.user = user_model
            user_profile.id = user_model.id
            user_profile.telefono = telefono
            user_profile.direccion = direccion
            user_profile.tipo = tipo
            user_profile.observacion = observacion
            
            user_profile.save()
            return render_to_response('usuarios/gracias.html', {'usuario':usuario, 'saludo':saludo, 'um':user_model, 'up':user_profile, 'aid':aid}, context_instance=RequestContext(request))   
    else:
        form = RegistroUserForm()
    
    return render(request, 'usuarios/registro.html', {'usuario':usuario, 'saludo':saludo, 'form': form})

@login_required(login_url='/ingresar')
def index_usuarios(request):
    comprobar(request)
    if(request.user.is_anonymous()):
        return HttpResponseRedirect('/ingresar')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    request.session['last_activity'] = str(now)
    
    usuario = request.user
    saludo = saludo_dia()
    
    usuarios = User.objects.filter(is_active=True).order_by('id')
    filas= usuarios.count() - 1
    
    if request.method == 'POST':
        results = User.objects.filter(is_active=True)
        form = BuscarUserForm(request.POST)
        
        if form.is_valid():
            uid = request.POST.get('id', None)
            if uid:
                if uid != usuario.id:
                    results = results.filter(id__iexact=uid)
                else:
                    results = None
                    
            uusername = request.POST.get('username', None)
            if uusername:
                if uusername != usuario.username:
                    results = results.filter(username__contains=uusername)
                else:
                    results = None
                    
            uemail = request.POST.get('email', None)
            if uemail:
                if uemail != usuario.email:
                    results = results.filter(email__contains=uemail)
                else:
                    results = None
                    
            first_name = request.POST.get('first_name', None)
            if first_name:
                if first_name != usuario.first_name:
                    results = results.filter(first_name__contains=first_name)
                else:
                    results = None
                    
            last_name = request.POST.get('last_name', None)
            if last_name:
                if last_name != usuario.last_name:
                    results = results.filter(last_name__contains=last_name)
                else:
                    results = None
                    
            if not uid and not uusername and not uemail and not first_name and not last_name:
                results = None
            
            if results:
                results.order_by('id')
            return render_to_response('usuarios/results.html', {'usuario':usuario, 'saludo':saludo, 'results':results}, context_instance=RequestContext(request))
    else:
        form = BuscarUserForm()
    
    return render(request, 'usuarios/index.html', {'usuario':usuario, 'saludo':saludo, 'usuarios':usuarios, 'filas':filas})

@login_required(login_url='/ingresar')
def editar_usuarios(request, user_id):
    aid = 2
    comprobar(request)
    if(request.user.is_anonymous()):
        return HttpResponseRedirect('/ingresar')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    request.session['last_activity'] = str(now)
    
    usuario = request.user
    saludo = saludo_dia()
    
    user_model = get_object_or_404(User, pk=user_id)
    user_profile = get_object_or_404(Usuarios, id=user_id)

    if request.method == 'POST':
        form = EditarUserForm(request.POST, request.FILES)
        if form.is_valid():
            user_model.password =  make_password(form.cleaned_data['password'])
            user_model.email = form.cleaned_data['email']
            user_model.first_name = form.cleaned_data['first_name']
            user_model.last_name = form.cleaned_data['last_name']  
            activo = form.cleaned_dat['estado']
            if activo:
                user_model.is_active = activo
            user_model.save()
            
            user_profile.telefono = form.cleaned_data['telefono']
            user_profile.direccion = form.cleaned_data['direccion']
            user_profile.observacion = form.cleaned_data['observacion']
            user_profile.save()

            return render_to_response('usuarios/gracias.html', {'usuario':usuario, 'saludo':saludo, 'aid':aid, 'um':user_model, 'up':user_profile}, context_instance=RequestContext(request))
    else:
        form = EditarUserForm()
    return render(request, 'usuarios/editar.html', {'form': form, 'usuario':usuario, 'saludo':saludo, 'um':user_model, 'up':user_profile})

@login_required(login_url='/ingresar')
def modificar_contrasena(request):
    aid = 4
    comprobar(request)
    if(request.user.is_anonymous()):
        return HttpResponseRedirect('/ingresar')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    request.session['last_activity'] = str(now)
    
    usuario = request.user
    user = User.objects.filter(id=usuario.id)
    saludo = saludo_dia()
    
    if request.method == 'POST':
        form = ModificarContrasenaForm(request.POST, user=user)
        if form.is_valid():
            usuario.password =  make_password(form.cleaned_data['password'])   
            usuario.save()

            return render_to_response('usuarios/gracias.html', {'aid':aid, 'usuario':usuario, 'saludo':saludo}, context_instance=RequestContext(request))
    else:
        form = ModificarContrasenaForm(user=user)
    return render(request, 'usuarios/modificar_contrasena.html', {'form': form, 'usuario':usuario, 'saludo':saludo})

@login_required(login_url='/ingresar')
def eliminar_usuarios(request, user_id):
    comprobar(request)
    if(request.user.is_anonymous()):
        return HttpResponseRedirect('/ingresar')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    request.session['last_activity'] = str(now)
    
    usuario = request.user
    saludo = saludo_dia()
    
    user = get_object_or_404(User, pk=user_id)
    
    return render_to_response('usuarios/eliminar.html', {'usuario':usuario, 'saludo':saludo, 'user':user})

@login_required(login_url='/ingresar')
def delete_usuarios(request, user_id):
    aid = 3
    usuario = request.user
    saludo = saludo_dia()
       
    user_model = get_object_or_404(User, pk=user_id)
    user_profile = get_object_or_404(Usuarios, id=user_id)
    
    user_model.is_active = False
    user_model.save()    
    return render_to_response('usuarios/gracias.html', {'usuario':usuario, 'saludo':saludo, 'um':user_model, 'up':user_profile, 'aid':aid}, context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def ver_usuarios(request, user_id):
    comprobar(request)
    if(request.user.is_anonymous()):
        return HttpResponseRedirect('/ingresar')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    request.session['last_activity'] = str(now)
    
    usuario = request.user
    saludo = saludo_dia()
    
    user_model = get_object_or_404(User, pk=user_id)
    user_profile = get_object_or_404(Usuarios, id=user_id)
    
    return render_to_response('usuarios/ver.html', {'usuario':usuario, 'saludo':saludo, 'um':user_model, 'up':user_profile})

def asignar_roles_usuarios_proyecto(request, user_id):
    aid = 5
    comprobar(request)
    if(request.user.is_anonymous()):
        return HttpResponseRedirect('/ingresar')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    request.session['last_activity'] = str(now)
    
    usuario = request.user
    saludo = saludo_dia()
    
    user_profile = get_object_or_404(Usuarios, id=user_id)
    user_model = get_object_or_404(User, id=user_id)
    roles = Roles.objects.filter(estado=True)
    proyectos = Proyectos.objects.all()

    if request.method == 'POST':
        form = AsignarRolForm(request.POST)
        if form.is_valid():
            rol_id = request.POST.get('rol_id', None)
            proyecto_id = request.POST.get('proyecto_id', None)
            
            rol = get_object_or_404(Roles, id=rol_id) 
            ru = Roles_Usuarios(usuario=user_profile, roles=rol)
            ru.save()

            proyecto = get_object_or_404(Proyectos, id=proyecto_id)
            up = Usuarios_Proyectos(proyecto=proyecto, usuarios=user_profile)
            up.save()
            
            return render_to_response('usuarios/gracias.html', {'aid':aid, 'usuario':usuario, 'saludo':saludo, 'um':user_model, 'p':proyecto, 'r':rol}, context_instance=RequestContext(request))
    else:
        form = AsignarRolForm()
    return render(request, 'usuarios/asignar.html', {'form': form, 'roles':roles, 'proyectos':proyectos, 'usuario':usuario, 'saludo':saludo, 'um':user_model, 'up':user_profile})


"""Administración de Roles"""
def index_roles(request):
    comprobar(request)
    if(request.user.is_anonymous()):
        return HttpResponseRedirect('/ingresar')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    request.session['last_activity'] = str(now)
    
    usuario = request.user
    saludo = saludo_dia()
    
    roles = Roles.objects.filter(estado=True).order_by('id')
    filas= roles.count()
    
    if request.method == 'POST':
        results = Roles.objects.all()
        form = BuscarRolForm(request.POST)
        
        if form.is_valid():
            rid = request.POST.get('id', None)
            if rid:
                results = results.filter(id=rid)
            
            rnombre = request.POST.get('nombre', None)
            if rnombre:
                results = results.filter(nombre__contains=rnombre)
            
            robservacion = request.POST.get('observacion', None)
            if robservacion:
                results = results.filter(observacion__contains=robservacion)
                    
            if not rid and not rnombre and not robservacion:
                results = None
            
            if results:
                results.order_by('id')
            return render_to_response('roles/results.html', {'usuario':usuario, 'saludo':saludo, 'results':results}, context_instance=RequestContext(request))
    else:
        form = BuscarRolForm()
    
    return render(request, 'roles/index.html', {'usuario':usuario, 'saludo':saludo, 'roles':roles, 'filas':filas})

def crear_roles(request):
    aid = 1
    comprobar(request)
    if(request.user.is_anonymous()):
        return HttpResponseRedirect('/ingresar')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    request.session['last_activity'] = str(now)
    
    usuario = request.user
    saludo = saludo_dia()
    
    permisos1 = Permisos.objects.all().filter(nivel=1)
    permisos2 = Permisos.objects.all().filter(nivel=2)
    permisos3 = Permisos.objects.all().filter(nivel=3)
    permisos = map(None, permisos1, permisos2, permisos3)
        
    if request.method == 'POST':
        form = CrearRolForm(request.POST, request.FILES)
    
        if form.is_valid():
            cleaned_data = form.cleaned_data
            nombre = cleaned_data.get('nombre')
            tipo = cleaned_data.get('tipo')
            observacion = cleaned_data.get('observacion')
    
            rol = Roles()
            rol.nombre = nombre
            rol.tipo = tipo
            rol.observacion = observacion
            rol.estado = True
            rol.save()
            
            rol_id = rol.id
            lista_permisos = request.POST.getlist(u'permisos')
            
            asignar_permisos_rol(request, rol_id, lista_permisos)
            pr1 = rol.permisos.all().filter(nivel=1)
            pr2 = rol.permisos.all().filter(nivel=2)
            pr3 = rol.permisos.all().filter(nivel=3)
            pr = map(None, pr1, pr2, pr3)
            
            return render_to_response('roles/gracias.html', {'aid':aid, 'usuario':usuario, 'saludo':saludo, 'pr':pr, 'rol':rol}, context_instance=RequestContext(request))

    else:
        form = CrearRolForm()
    
    return render(request, 'roles/crear.html', {'usuario':usuario, 'saludo':saludo, 'form': form, 'permisos':permisos})

def asignar_permisos_rol(request, rol_id, lista_permisos):    
    rol = get_object_or_404(Roles, id=rol_id)
    
    for p in lista_permisos:
        
        permiso = Permisos.objects.get(pk=p)   
        pr = Permisos_Roles(permisos=permiso, roles=rol)
        pr.save()
       
    return pr

def editar_roles(request, rol_id):
    aid = 2
    comprobar(request)
    if(request.user.is_anonymous()):
        return HttpResponseRedirect('/ingresar')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    request.session['last_activity'] = str(now)
    
    usuario = request.user
    saludo = saludo_dia()
    
    permisos1 = Permisos.objects.all().filter(nivel=1)
    permisos2 = Permisos.objects.all().filter(nivel=2)
    permisos3 = Permisos.objects.all().filter(nivel=3)
    permisos = map(None, permisos1, permisos2, permisos3)
    
    rol = get_object_or_404(Roles, id=rol_id)
    p1 = rol.permisos.all().filter(nivel=1)
    p2 = rol.permisos.all().filter(nivel=2)
    p3 = rol.permisos.all().filter(nivel=3)
    lista = map(None, p1, p2, p3)

    if request.method == 'POST':
        form = EditarRolForm(request.POST, rol_id=rol_id)
        if form.is_valid():
            rol.nombre = form.cleaned_data['nombre']
            rol.tipo = form.cleaned_data['tipo']
            rol.observacion = form.cleaned_data['observacion']
            rol.save()
            
            rol_id = rol.id
            lista_permisos = request.POST.getlist(u'permisos')
            
            editar_permisos_rol(request, rol_id, lista_permisos)
            pr1 = rol.permisos.all().filter(nivel=1)
            pr2 = rol.permisos.all().filter(nivel=2)
            pr3 = rol.permisos.all().filter(nivel=3)
            pr = map(None, pr1, pr2, pr3)
            
            return render_to_response('roles/gracias.html', {'aid':aid, 'usuario':usuario, 'saludo':saludo, 'pr':pr, 'rol':rol}, context_instance=RequestContext(request))
    else:
        form = EditarRolForm(rol_id=rol_id)
    return render(request, 'roles/editar.html', {'form': form, 'usuario':usuario, 'saludo':saludo, 'rol':rol, 'lista':lista, 'permisos':permisos})

def editar_permisos_rol(request, rol_id, lista_permisos):
    
    rol = get_object_or_404(Roles, id=rol_id)
    rp = rol.permisos.all() 
    existe = False
    
    for pe in rp:
        for p in lista_permisos:
            if pe.id == p:
                existe = True
        if existe == False:
            permiso = get_object_or_404(Permisos, id=pe.id)
            roles = get_object_or_404(Roles, id=rol_id)
            permisosRoles = Permisos_Roles.objects.get(permisos=permiso, roles=roles)
            permisosRoles.delete()
        existe = False
            
    for p in lista_permisos:
        for pe in rp:
            if p != pe.id:         
                permiso = Permisos.objects.get(pk=p)   
                per = Permisos_Roles(permisos=permiso, roles=rol)
                per.save()
                break
       
    return per

def ver_roles(request, rol_id):
    comprobar(request)
    if(request.user.is_anonymous()):
        return HttpResponseRedirect('/ingresar')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    request.session['last_activity'] = str(now)
    
    usuario = request.user
    saludo = saludo_dia()
    
    rol = get_object_or_404(Roles, id=rol_id)
    permisos1 = rol.permisos.all().filter(nivel=1)
    permisos2 = rol.permisos.all().filter(nivel=2)
    permisos3 = rol.permisos.all().filter(nivel=3)
    pr = map(None, permisos1, permisos2, permisos3)
    
    return render_to_response('roles/ver.html', {'usuario':usuario, 'saludo':saludo, 'rol':rol, 'pr':pr})

def eliminar_roles(request, rol_id):
    comprobar(request)
    if(request.user.is_anonymous()):
        return HttpResponseRedirect('/ingresar')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    request.session['last_activity'] = str(now)
    
    usuario = request.user
    saludo = saludo_dia()
    
    rol = get_object_or_404(Roles, id=rol_id)
    
    return render_to_response('roles/eliminar.html', {'usuario':usuario, 'saludo':saludo, 'rol':rol})
 
def delete_roles(request, rol_id):
    aid = 3
    comprobar(request)
    if(request.user.is_anonymous()):
        return HttpResponseRedirect('/ingresar')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    request.session['last_activity'] = str(now)
    
    usuario = request.user
    saludo = saludo_dia()
    
    rol = get_object_or_404(Roles, id=rol_id)
    pr = rol.permisos.all()
    rol.estado = False
    rol.save()
    
    return render_to_response('roles/gracias.html', {'aid':aid, 'usuario':usuario, 'saludo':saludo, 'rol':rol, 'pr':pr})  
    
def crear_permisos():
    nombres = ['Administración de Usuarios', 'Administración de Proyectos/Servicios', 'Definición de Proyectos/Servicios',
               'Asignación de Usuarios', 'Administración de Roles y Permisos', 'Creación de US', 
               'Asignación de Roles', 'Modificación de US - Valores de Negocios', 'Modificación de US - Valor Técnico', 
               'Modificación de US - Size', 'Modificación de US - Prioridad', 'Eliminación de US', 
               'Administración de Sprints', 'Administración de Flujos', 'Consultar lista de Usuarios', 
               'Consultar lista de Proyectos/Servicios', 'Modificación de US - Notas', 
               'Modificación de US - Archivos adjuntos', 'Modificación de US - Descripción', 
               'Consultar estado de Actividades', 'Consultar Recursos Disponibles', 
               'Consultar Historial del Proyecto/Servicio', 'Generar Burn Down Chart', 'Generar listado de US']
    niveles = [0, 0, 1,
               1, 1, 1, 
               1, 1, 1,
               1, 1, 1,
               1, 1, 1,
               1, 2,
               2, 2,
               2, 2,
               3, 3, 3]
    c = 0
    for n in nombres:
        agregar_permisos(n, niveles[c])
        c = c + 1 
           
def agregar_permisos(nombre, nivel):
    permisos = Permisos()
    permisos.nombre = nombre
    permisos.nivel = nivel
    permisos.estado = True
    permisos.save()

def administrador():
    user = User.objects.get(pk=1)
    usuario = Usuarios(user=user)
    rol = Roles(nombre="Administrador", tipo=True, estado=True, observacion="Administrador del Sistema.")
    permisos = Permisos.objects.all()
    
    for p in permisos:  
        pr = Permisos_Roles(permisos=p, roles=rol)
        pr.save()
    ru = Roles_Usuarios(usuario=usuario, roles=rol)
    ru.save()
    
    
"""Administración de Proyectos"""
def crear_proyectos(request):
    aid = 1
    comprobar(request)
    if(request.user.is_anonymous()):
        return HttpResponseRedirect('/ingresar')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    request.session['last_activity'] = str(now)
    
    usuario = request.user
    saludo = saludo_dia()
    
    if request.method == 'POST':
        form = CrearProyectoForm(request.POST, request.FILES)
    
        if form.is_valid():
            cleaned_data = form.cleaned_data
            nombre_largo = cleaned_data.get('nombre_largo')
    
            proyecto = Proyectos()
            proyecto.nombre_largo = nombre_largo
            proyecto.estado = 1
            proyecto.save()
            
            return render_to_response('proyectos/gracias.html', {'aid':aid, 'usuario':usuario, 'saludo':saludo, 'proyecto':proyecto}, context_instance=RequestContext(request))

    else:
        form = CrearProyectoForm()
    
    return render(request, 'proyectos/crear.html', {'usuario':usuario, 'saludo':saludo, 'form': form})

def definir_proyectos(request, proyecto_id):
    aid = 2
    comprobar(request)
    if(request.user.is_anonymous()):
        return HttpResponseRedirect('/ingresar')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    request.session['last_activity'] = str(now)
    
    usuario = request.user
    saludo = saludo_dia()
    
    proyecto = get_object_or_404(Proyectos, id=proyecto_id)
    
    if request.method == 'POST':
        form = DefinirProyectoForm(request.POST, request.FILES)
    
        if form.is_valid():
            cleaned_data = form.cleaned_data
            nombre_corto = cleaned_data.get('nombre_corto')
            tipo = cleaned_data.get('tipo')
            descripcion = cleaned_data.get('descripcion')
            fecha_inicio = cleaned_data.get('fecha_inicio')
            fecha_fin_estimado = cleaned_data.get('fecha_fin_estimado')
            observaciones = cleaned_data.get('observaciones')
    
            proyecto.nombre_corto = nombre_corto
            proyecto.tipo = tipo
            proyecto.descripcion = descripcion
            proyecto.fecha_inicio = fecha_inicio
            proyecto.fecha_fin_estimado = fecha_fin_estimado
            proyecto.observaciones = observaciones
            proyecto.estado = 1
            proyecto.save()
            
            return render_to_response('proyectos/gracias.html', {'aid':aid, 'usuario':usuario, 'saludo':saludo, 'proyecto':proyecto}, context_instance=RequestContext(request))

    else:
        form = DefinirProyectoForm()
    
    return render(request, 'proyectos/definir.html', {'usuario':usuario, 'saludo':saludo, 'form': form})

def editar_proyectos(request, proyecto_id):
    aid = 3
    comprobar(request)
    if(request.user.is_anonymous()):
        return HttpResponseRedirect('/ingresar')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    request.session['last_activity'] = str(now)
    
    usuario = request.user
    saludo = saludo_dia()
    
    proyecto = get_object_or_404(Proyectos, id=proyecto_id)
    
    if request.method == 'POST':
        form = EditarProyectoForm(request.POST, request.FILES)
    
        if form.is_valid():
            cleaned_data = form.cleaned_data
            nombre_corto = cleaned_data.get('nombre_corto')
            tipo = cleaned_data.get('tipo')
            descripcion = cleaned_data.get('descripcion')
            fecha_inicio = cleaned_data.get('fecha_inicio')
            fecha_fin_estimado = cleaned_data.get('fecha_fin_estimado')
            observaciones = cleaned_data.get('observaciones')
    
            proyecto.nombre_corto = nombre_corto
            proyecto.tipo = tipo
            proyecto.descripcion = descripcion
            proyecto.fecha_inicio = fecha_inicio
            proyecto.fecha_fin_estimado = fecha_fin_estimado
            proyecto.observaciones = observaciones
            proyecto.save()
            
            return render_to_response('proyectos/gracias.html', {'aid':aid, 'usuario':usuario, 'saludo':saludo, 'proyecto':proyecto}, context_instance=RequestContext(request))

    else:
        form = EditarProyectoForm()
    
    return render(request, 'proyectos/editar.html', {'usuario':usuario, 'saludo':saludo, 'form': form, 'proyecto':proyecto})

def ver_proyectos(request, proyecto_id):
    aid = 3
    comprobar(request)
    if(request.user.is_anonymous()):
        return HttpResponseRedirect('/ingresar')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    request.session['last_activity'] = str(now)
    
    usuario = request.user
    saludo = saludo_dia()
    
    proyecto = get_object_or_404(Proyectos, id=proyecto_id)
    
    return render(request, 'proyectos/ver.html', {'usuario':usuario, 'saludo':saludo, 'proyecto':proyecto})


def index_proyectos(request):
    comprobar(request)
    if(request.user.is_anonymous()):
        return HttpResponseRedirect('/ingresar')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    request.session['last_activity'] = str(now)
    
    usuario = request.user
    saludo = saludo_dia()
    
    proyectos = Proyectos.objects.all().order_by('id')
    filas= proyectos.count()
    
    if request.method == 'POST':
        results = Proyectos.objects.all()
        form = BuscarProyectoForm(request.POST)
        
        if form.is_valid():
            pid = request.POST.get('id', None)
            if pid:
                results = results.filter(id=pid)
            
            pnombre_largo = request.POST.get('nombre_largo', None)
            if pnombre_largo:
                results = results.filter(nombre_largo__contains=pnombre_largo)
            
            pnombre_corto = request.POST.get('nombre_corto', None)
            if pnombre_corto:
                results = results.filter(nombre_corto__contains=pnombre_corto)
            
            pdescripcion = request.POST.get('descripcion', None)
            if pdescripcion:
                results = results.filter(descripcion_contains=pdescripcion)
                    
            if not pid and not pnombre_corto and not pnombre_largo and not pdescripcion:
                results = None
            
            if results:
                results.order_by('id')
            return render_to_response('proyectos/results.html', {'usuario':usuario, 'saludo':saludo, 'results':results}, context_instance=RequestContext(request))
    else:
        form = BuscarProyectoForm()
    
    return render(request, 'proyectos/index.html', {'usuario':usuario, 'saludo':saludo, 'proyectos':proyectos, 'filas':filas})
    
"""Funciones de saludo y comprobación de última actividad."""
def saludo_dia():
    hora = datetime.now().hour
    if hora >= 0 and hora < 6:
        saludo= "Buenas madrugadas"
    elif hora > 5 and hora < 12:
        saludo= "Buenos dias"
    elif hora >= 12 and hora <= 13:
        saludo= "Buena siesta"
    elif hora > 13 and hora <= 18:
        saludo= "Buenas tardes"
    elif hora >= 19 and hora <= 23:
        saludo= "Buenas noches"
        
    return saludo

def comprobar(request):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    now_object = datetime.strptime(now, '%Y-%m-%d %H:%M:%S')

    last_activity = request.session['last_activity']
    date_object = datetime.strptime(last_activity, '%Y-%m-%d %H:%M:%S')

    restaminutos = ((now_object - date_object).seconds)/60 
    
    if restaminutos >= 10:
        logout(request)
        return HttpResponseRedirect('/ingresar')