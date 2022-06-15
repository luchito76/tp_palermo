from django.urls import path

from .views import MarcaView, MarcaNew, MarcaEdit, marca_inactivar  
    

urlpatterns = [
    path('marcas/',MarcaView.as_view(), name="marca_list"),
    path('marcas/new',MarcaNew.as_view(), name="marca_new"),
    path('marcas/edit/<int:pk>',MarcaEdit.as_view(), name="marca_edit"),
    path('marcas/inactivar/<int:id>',marca_inactivar, name="marca_inactivar")   
]