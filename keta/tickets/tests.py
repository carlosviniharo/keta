import pdb
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse


class JproblemasViewSetTestCase(APITestCase):
    fixtures = ["tickets_test.json"]

    def setUp(self):
        self.client = APIClient()
        self.data_reclamos_generales = {
            "persona": {
                "idgenero": "http://127.0.0.1:8000/users/api/generos/1/",
                "idtipoidentificacion": "http://127.0.0.1:8000/users/api/tiposidentificaciones/1/",
                "idtipopersona": "http://127.0.0.1:8000/users/api/tipospersonas/1/",
                "identificacion": "1004140881",
                "nombre": "Carlos",
                "apellido": " Maliza",
                "emailcliente": "carlos@hotmail.es",
                "celular": "0999999999",
                "telefono": "062922066",
                "direccion": "Otavalo"
            },
            "ticket": {
                "descripcionasunto": "Example reclamo general",
                "monto": "10.00",
                "idusuario": "http://127.0.0.1:8000/users/api/usuarios/1/",
                "idtipotransaccion": "http://127.0.0.1:8000/tickets/api/tipostransacciones/1/",
                "idtipoproducto": "http://127.0.0.1:8000/tickets/api/tiposproductos/1/",
                "idtipocomentario": "http://127.0.0.1:8000/tickets/api/tiposcomentarios/1/",
                "idcanalrecepcion": "http://127.0.0.1:8000/tickets/api/canalesrecepciones/1/",
                "idtipoticket": "http://127.0.0.1:8000/tickets/api/tickettipos/3/",
                "idconcepto": "http://127.0.0.1:8000/tickets/api/conceptos/1/",
                "idprioridad": "http://127.0.0.1:8000/tickets/api/prioridades/1/",
                "idsucursal": "http://127.0.0.1:8000/users/api/sucursales/1/",
                "idusuarioproblema": "http://127.0.0.1:8000/users/api/usuarios/1/",
                "servicio": "Bad customer service"
            }
        }
        self.data_reclamos_tarjeta = {
            "persona": {
                "idgenero": "http://127.0.0.1:8000/users/api/generos/1/",
                "idtipoidentificacion": "http://127.0.0.1:8000/users/api/tiposidentificaciones/1/",
                "idtipopersona": "http://127.0.0.1:8000/users/api/tipospersonas/1/",
                "identificacion": "1111404883",
                "nombre": "Bryan",
                "apellido": " Aldas",
                "emailcliente": "bryan@hotmail.es",
                "celular": "0999999999",
                "telefono": "062922068",
                "direccion": "Atuntaqui"
            },
            "ticket": {
                "descripcionasunto": "Incorrecta cantidad de dinero en ATM",
                "monto": "1800.00",
                "idusuario": "http://127.0.0.1:8000/users/api/usuarios/1/",
                "idtipotransaccion": "http://127.0.0.1:8000/tickets/api/tipostransacciones/1/",
                "idcanalrecepcion": "http://127.0.0.1:8000/tickets/api/canalesrecepciones/1/",
                "idtipoticket": "http://127.0.0.1:8000/tickets/api/tickettipos/2/",
                "idprioridad": "http://127.0.0.1:8000/tickets/api/prioridades/1/",
                "idtipocomentario": "http://127.0.0.1:8000/tickets/api/tiposcomentarios/1/",
                "idsucursal": "http://127.0.0.1:8000/users/api/sucursales/1/"
            },
            "tarjeta": {
                "idmarcatarjeta": "http://127.0.0.1:8000/tickets/api/marcastarjetas/1/",
                "idtipotarjeta": "http://127.0.0.1:8000/tickets/api/tipostarjetas/1/",
                "idclasetarjeta": "http://127.0.0.1:8000/tickets/api/clasestarjetas/1/",
                "numerotarjeta": "1234123412341234"
            }
        }
        self.data_cobros_indebidos = {
            "persona": {
                "idgenero": "http://127.0.0.1:8000/users/api/generos/1/",
                "idtipoidentificacion": "http://127.0.0.1:8000/users/api/tiposidentificaciones/1/",
                "idtipopersona": "http://127.0.0.1:8000/users/api/tipospersonas/1/",
                "identificacion": "1004140881",
                "nombre": "Carlos",
                "apellido": " Maliza",
                "emailcliente": "carlos@hotmail.es",
                "celular": "0999999999",
                "telefono": "062922066",
                "direccion": "Otavalo"
            },
            "ticket": {
                "descripcionasunto": "Mal cobro indebido",
                "monto": "1800.00",
                "archivo": "+HilYtSEaJIZTqQaXtGyLmn82rDTp5Ex6b6CSeWbkuT2A+FqPfObQuT0R1PkiiNIRVHvDnvXfTHMySqtkgVBXdzZrgYLuRH5BBUQLT1vLF",
                "idusuario": "http://127.0.0.1:8000/users/api/usuarios/1/",
                "idtipotransaccion": "http://127.0.0.1:8000/tickets/api/tipostransacciones/1/",
                "idtipoproducto": "http://127.0.0.1:8000/tickets/api/tiposproductos/1/",
                "idtipocomentario": "http://127.0.0.1:8000/tickets/api/tiposcomentarios/1/",
                "idcanalrecepcion": "http://127.0.0.1:8000/tickets/api/canalesrecepciones/1/",
                "idtipoticket": "http://127.0.0.1:8000/tickets/api/tickettipos/1/",
                "idconcepto": "http://127.0.0.1:8000/tickets/api/conceptos/1/",
                "idprioridad": "http://127.0.0.1:8000/tickets/api/prioridades/1/",
                "idsucursal": "http://127.0.0.1:8000/users/api/sucursales/1/"
            }
        }

    def test_create_jproblemas(self):
        url = reverse("jproblemas-list")
        # pdb.set_trace()
        response_reclamo_general = self.client.post(url, self.data_reclamos_generales, format="json")
        self.assertEqual(response_reclamo_general.status_code, status.HTTP_201_CREATED)
        
        response_reclamo_tarjeta = self.client.post(url, self.data_reclamos_tarjeta, format="json")
        self.assertEqual(response_reclamo_tarjeta.status_code, status.HTTP_201_CREATED)
        
        response_cobros_indebidos = self.client.post(url, self.data_cobros_indebidos, format="json")
        self.assertEqual(response_cobros_indebidos.status_code, status.HTTP_201_CREATED)
    