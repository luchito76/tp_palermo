from django.urls import path, include
from .views import ClienteList

urlpatterns = [    
    path('v1/clientes/',ClienteList.as_view(),name='cliente_list')
]