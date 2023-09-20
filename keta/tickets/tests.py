from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from .models import Jproblemas
from .serializers import JproblemasSerializer


class JproblemasViewSetTestCase(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_create_jproblemas(self):
        data_reclamo_general = {
            "persona": {
                "idgenero": "http://127.0.0.1:8000/users/api/generos/1/",
                "idtipoidentificacion": "http://127.0.0.1:8000/users/api/tiposidentificaciones/1/",
                "idtipopersona": "http://127.0.0.1:8000/users/api/tipospersonas/2/",
                "identificacion": "1004140881",
                "nombre": "Carlos",
                "apellido": " Maliza",
                "emailcliente": "carlos@hotmail.es",
                "celular": "0999999999",
                "telefono": "062922066",
                "direccion": "Otavalo",
            },
            "ticket": {
                "descripcionasunto": "Mal cobro indebido",
                "monto": "100.00",
                "idusuario": "http://127.0.0.1:8000/users/api/usuarios/1/",
                "idtipotransaccion": "http://127.0.0.1:8000/tickets/api/tipostransacciones/1/",
                "idtipoproducto": "http://127.0.0.1:8000/tickets/api/tiposproductos/2/",
                "idtipocomentario": "http://127.0.0.1:8000/tickets/api/tiposcomentarios/3/",
                "idcanalrecepcion": "http://127.0.0.1:8000/tickets/api/canalesrecepciones/1/",
                "idtipoticket": "http://127.0.0.1:8000/tickets/api/tickettipos/3/",
                "idconcepto": "http://127.0.0.1:8000/tickets/api/conceptos/10/",
                "idprioridad": "http://127.0.0.1:8000/tickets/api/prioridades/1/",
                "idsucursal": "http://127.0.0.1:8000/users/api/sucursales/1/",
            },
        }
