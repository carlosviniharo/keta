from django.urls import path

from tickets.views import *

urlpatterns = [
    path('create_tickets/', JproblemasCreateView.as_view(), name='create_ticket'),
]

#     path('canlesrecepciones/', JcanalesrecepcionesListView.as_view(), name='canales_recepcion'),
#     path('classestarjetas/', JclasestarjetasListView.as_view(), name='clases_tarjetas'),
#     path('tiposproductos/', JtiposproductosListView.as_view(), name='tipos_productos'),
#     path('conceptos/', JconceptosListView.as_view(), name='conceptos'),
#     path('marcastarjetas/', JmarcastarjetasListView.as_view(), name='marcas_tarjetas'),
#     path('prioridades/', JprioridadesListView.as_view(), name='prioridades'),
#     path('tipostarjetas/', JtipostarjetasListView.as_view(), name='tipos_tarjetas'),
#     path('tarjetas/',  JtarjetasListView.as_view(), name='tarjetas'),
#     path('tiposcomentarios/', JtiposcomentariosListView.as_view(),name='tipos_comentarios'),
#     path('tickettipos/', JtickettiposListView.as_view(), name='tipos_tickets'),
#