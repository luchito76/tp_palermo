from django.shortcuts import render,redirect
from django.views import generic

from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from datetime import datetime
from django.contrib import messages

from django.contrib.auth import authenticate

from bases.views import SinPrivilegios

from .models import Cliente
from .forms import ClienteForm
import inv.views as inv

class ClienteView(SinPrivilegios, generic.ListView):
    model = Cliente
    template_name = "fac/cliente_list.html"
    context_object_name = "obj"
    permission_required="cmp.view_cliente"


class VistaBaseCreate(SuccessMessageMixin,SinPrivilegios, \
    generic.CreateView):
    context_object_name = 'obj'
    success_message="Registro Agregado Satisfactoriamente"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

class VistaBaseEdit(SuccessMessageMixin,SinPrivilegios, \
    generic.UpdateView):
    context_object_name = 'obj'
    success_message="Registro Actualizado Satisfactoriamente"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)


class ClienteNew(VistaBaseCreate):
    model=Cliente
    template_name="fac/cliente_form.html"
    form_class=ClienteForm
    success_url= reverse_lazy("fac:cliente_list")
    permission_required="fac.add_cliente"

    def get(self, request, *args, **kwargs):
        print("sobre escribir get")
        
        try:
            t = request.GET["t"]
        except:
            t = None

        print(t)
        
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form, 't':t})


class ClienteEdit(VistaBaseEdit):
    model=Cliente
    template_name="fac/cliente_form.html"
    form_class=ClienteForm
    success_url= reverse_lazy("fac:cliente_list")
    permission_required="fac.change_cliente"

    def get(self, request, *args, **kwargs):
        print("sobre escribir get en editar")

        print(request)
        
        try:
            t = request.GET["t"]
        except:
            t = None

        print(t)
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(object=self.object, form=form,t=t)
        print(form_class,form,context)
        return self.render_to_response(context)


@login_required(login_url="/login/")
@permission_required("fac.change_cliente",login_url="/login/")
def clienteInactivar(request,id):
    cliente = Cliente.objects.filter(pk=id).first()

    if request.method=="POST":
        if cliente:
            cliente.estado = not cliente.estado
            cliente.save()
            return HttpResponse("OK")
        return HttpResponse("FAIL")
    
    return HttpResponse("FAIL")

@login_required(login_url="/login/")
@permission_required("fac.change_cliente",login_url="/login/")
def cliente_add_modify(request,pk=None):
    template_name="fac/cliente_form.html"
    context = {}

    if request.method=="GET":
        context["t"]="fc"
        if not pk:
            form = ClienteForm()
        else:
            cliente = Cliente.objects.filter(id=pk).first()
            form = ClienteForm(instance=cliente)
            context["obj"]=cliente
        context["form"] = form
    else:
        nombres = request.POST.get("nombres")
        apellidos = request.POST.get("apellidos")
        celular = request.POST.get("celular")
        tipo = request.POST.get("tipo")
        usr = request.user

        if not pk:
            cliente = Cliente.objects.create(
                nombres=nombres,
                apellidos=apellidos,
                celular = celular,
                tipo = tipo,
                uc=usr,
            )
        else:
            cliente = Cliente.objects.filter(id=pk).first()
            cliente.nombres=nombres
            cliente.apellidos=apellidos
            cliente.celular = celular
            cliente.tipo = tipo
            cliente.um=usr.id

        cliente.save()
        if not cliente:
            return HttpResponse("No pude Guardar/Crear Cliente")
        
        id = cliente.id
        return HttpResponse(id)
    
    return render(request,template_name,context)
    