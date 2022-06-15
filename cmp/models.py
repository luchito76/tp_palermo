from django.db import models

#Para los signals
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum

from bases.models import ClaseModelo

class Proveedor(ClaseModelo):
    descripcion=models.CharField(
        max_length=100,
        unique=True
        )
    direccion=models.CharField(
        max_length=250,
        null=True, blank=True
        )
    contacto=models.CharField(
        max_length=100
    )
    telefono=models.CharField(
        max_length=10,
        null=True, blank=True
    )
    email=models.CharField(
        max_length=250,
        null=True, blank=True
    )

    def __str__(self):
        return '{}'.format(self.descripcion)

    def save(self):
        self.descripcion = self.descripcion.upper()
        super(Proveedor, self).save()

    class Meta:
        verbose_name_plural = "Proveedores"