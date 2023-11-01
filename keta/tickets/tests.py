from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse

from users.tests import ExampleViewSetTestCase

from .models import (
    Jcanalesrecepciones,
    Jclasestarjetas,
    Jconceptos,
    Jmarcastarjetas,
    Jprioridades,
    Jtipostarjetas,
    Jtarjetas,
    Jtiposcomentarios, Jtickettipos, Jtipostransacciones,
)


class JproblemasViewSetTestCase(APITestCase):
    fixtures = ["tickets_test.json"]

    def setUp(self):
        self.client = APIClient()
        self.url = reverse("jproblemas-list")
        self.generic_persona = {
                "idgenero": "http://127.0.0.1:8000/users/api/generos/1/",
                "idtipoidentificacion": "http://127.0.0.1:8000/users/api/tiposidentificaciones/1/",
                "idtipopersona": "http://127.0.0.1:8000/users/api/tipospersonas/1/",
                "identificacion": "1001001001",
                "nombre": "Example",
                "apellido": "Same Person ",
                "emailcliente": "same@person.com",
                "celular": "0999999999",
                "telefono": "062922066",
                "direccion": "Otavalo"
            }
        
        self.new_persona = {
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
        }
        
        self.data_reclamos_generales = {
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
        
        self.data_reclamos_tarjeta = {
                "descripcionasunto": "Incorrecta cantidad de dinero en ATM",
                "monto": "1800.00",
                "idusuario": "http://127.0.0.1:8000/users/api/usuarios/1/",
                "idtipotransaccion": "http://127.0.0.1:8000/tickets/api/tipostransacciones/1/",
                "idcanalrecepcion": "http://127.0.0.1:8000/tickets/api/canalesrecepciones/1/",
                "idtipoticket": "http://127.0.0.1:8000/tickets/api/tickettipos/2/",
                "idprioridad": "http://127.0.0.1:8000/tickets/api/prioridades/1/",
                "idtipocomentario": "http://127.0.0.1:8000/tickets/api/tiposcomentarios/1/",
                "idsucursal": "http://127.0.0.1:8000/users/api/sucursales/1/"
            }
        self.data_reclamos_same_tarjeta = {
                "descripcionasunto": "Incorrecta cantidad de dinero en ATM",
                "monto": "180.00",
                "idusuario": "http://127.0.0.1:8000/users/api/usuarios/1/",
                "idtipotransaccion": "http://127.0.0.1:8000/tickets/api/tipostransacciones/1/",
                "idcanalrecepcion": "http://127.0.0.1:8000/tickets/api/canalesrecepciones/1/",
                "idtipoticket": "http://127.0.0.1:8000/tickets/api/tickettipos/2/",
                "idprioridad": "http://127.0.0.1:8000/tickets/api/prioridades/1/",
                "idtipocomentario": "http://127.0.0.1:8000/tickets/api/tiposcomentarios/1/",
                "idsucursal": "http://127.0.0.1:8000/users/api/sucursales/1/"
            }
        
        self.tarjeta= {
                "idmarcatarjeta": "http://127.0.0.1:8000/tickets/api/marcastarjetas/1/",
                "idtipotarjeta": "http://127.0.0.1:8000/tickets/api/tipostarjetas/1/",
                "idclasetarjeta": "http://127.0.0.1:8000/tickets/api/clasestarjetas/1/",
                "numerotarjeta": "1234123412341234"
            }
        
        self.data_cobros_indebidos = {
                "descripcionasunto": "Mal cobro indebido",
                "monto": "1800.00",
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
    
    def create_jproblemas(self, data):
        response = self.client.post(self.url, data, format="json")
        return response
    
    def test_create_reclamo_general(self):
        response = self.create_jproblemas({
            "persona": self.generic_persona,
            "ticket": self.data_reclamos_generales,
        })
        # pdb.set_trace()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_create_same_claim(self):
        self.create_jproblemas({
            "persona": self.new_persona,
            "ticket": self.data_reclamos_generales,
        })
        response_repeated = self.create_jproblemas({
            "persona": self.new_persona,
            "ticket": self.data_reclamos_generales,
        })
        self.assertEqual(response_repeated.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_new_claim_same_person(self):
        response = self.create_jproblemas({
            "persona": self.new_persona,
            "ticket": self.data_reclamos_generales,
        })
        response_new_person = self.create_jproblemas({
            "persona": self.new_persona,
            "ticket": self.data_cobros_indebidos,
        })
        self.assertEqual(response_new_person.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["persona"]["idpersona"], response_new_person.data["persona"]["idpersona"])
        self.assertTrue(response.data["nueva persona"])
        self.assertFalse(response_new_person.data["nueva persona"])

    def test_create_claim_incomplete_request(self):
        # pdb.set_trace()
        response = self.create_jproblemas({"persona": self.new_persona})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check that the response contains the expected error message
        self.assertEqual(response.data, {'non_field_errors': ['No data provided']})
        
        response_card = self.create_jproblemas({
            "persona": self.generic_persona,
            "ticket": self.data_reclamos_tarjeta,
            })
        self.assertEqual(response_card.status_code, status.HTTP_400_BAD_REQUEST)
        # Check that the response contains the expected error message
        # pdb.set_trace()
        self.assertEqual({'non_field_errors': ['No data provided']}, response.data)
        
    def test_create_reclamo_tarjeta(self):
        response = self.create_jproblemas({
            "persona": self.generic_persona,
            "ticket": self.data_reclamos_tarjeta,
            "tarjeta": self.tarjeta
        })
        response_same_persona_new_card = self.create_jproblemas({
            "persona": self.generic_persona,
            "ticket": self.data_reclamos_same_tarjeta,
            "tarjeta": self.tarjeta
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_same_persona_new_card.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data["tarjeta"]["idtarjeta"],
            response_same_persona_new_card.data["tarjeta"]["idtarjeta"]
        )
        
    def test_create_cobros_indebidos(self):
        response = self.create_jproblemas({
            "persona": self.generic_persona,
            "ticket": self.data_cobros_indebidos,
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class JcanalesrecepcionesTestCase(ExampleViewSetTestCase):
    def setUp(self):
        super().setUp()
        self.model2test = Jcanalesrecepciones
        self.model_name = self.model2test.__name__.lower()
        self.field_name = "canalrecepcion"
        self.data_field = f"descripcion{self.field_name}"
        self.model2test_data = {self.data_field: "Example string"}
        self.created_model = self.model2test.objects.create(**self.model2test_data)


class JclasestarjetasTestsCase(ExampleViewSetTestCase):
    def setUp(self):
        super().setUp()
        self.model2test = Jclasestarjetas
        self.model_name = self.model2test.__name__.lower()
        self.field_name = "clasetarjeta"
        self.data_field = f"descripcion{self.field_name}"
        self.model2test_data = {self.data_field: "Example string"}
        self.created_model = self.model2test.objects.create(**self.model2test_data)


class JtiposproductosTestsCase(ExampleViewSetTestCase):
    def setUp(self):
        super().setUp()
        self.model2test = Jconceptos
        self.model_name = self.model2test.__name__.lower()
        self.field_name = self.model_name[1:-1]
        self.data_field = f"descripcion{self.field_name}"
        self.model2test_data = {self.data_field: "Example string"}
        self.created_model = self.model2test.objects.create(**self.model2test_data)


class JmarcastarjetasTestsCase(ExampleViewSetTestCase):
    def setUp(self):
        super().setUp()
        self.model2test = Jmarcastarjetas
        self.model_name = self.model2test.__name__.lower()
        self.field_name = "marcatarjeta"
        self.data_field = f"descripcion{self.field_name}"
        self.model2test_data = {self.data_field: "Example string"}
        self.created_model = self.model2test.objects.create(**self.model2test_data)


class JprioridadesTestsCase(ExampleViewSetTestCase):
    def setUp(self):
        super().setUp()
        self.model2test = Jprioridades
        self.model_name = self.model2test.__name__.lower()
        self.field_name = self.model_name[1:-2]
        self.data_field = f"descripcion{self.field_name}"
        self.model2test_data = {self.data_field: "Example string"}
        self.created_model = self.model2test.objects.create(**self.model2test_data)


class JtipostarjetasTestsCase(ExampleViewSetTestCase):
    def setUp(self):
        super().setUp()
        self.model2test = Jtipostarjetas
        self.model_name = self.model2test.__name__.lower()
        self.field_name = "tipotarjeta"
        self.data_field = f"descripcion{self.field_name}"
        self.model2test_data = {self.data_field: "Example string"}
        self.created_model = self.model2test.objects.create(**self.model2test_data)


class JtarjetasTestsCase(ExampleViewSetTestCase):
    def setUp(self):
        super().setUp()
        self.model2test = Jtarjetas
        self.model_name = self.model2test.__name__.lower()
        self.field_name = self.model_name[1:-1]
        self.data_field = f"numero{self.field_name}"
        self.model2test_data = {self.data_field: "Example string"}
        self.created_model = self.model2test.objects.create(**self.model2test_data)


class JtiposcomentariosTestsCase(ExampleViewSetTestCase):
    def setUp(self):
        super().setUp()
        self.model2test = Jtiposcomentarios
        self.model_name = self.model2test.__name__.lower()
        self.field_name = "tipocomentario"
        self.data_field = f"descripcion{self.field_name}"
        self.model2test_data = {self.data_field: "Example string"}
        self.created_model = self.model2test.objects.create(**self.model2test_data)


class JtickettiposTestsCase(ExampleViewSetTestCase):
    def setUp(self):
        super().setUp()
        self.model2test = Jtickettipos
        self.model_name = self.model2test.__name__.lower()
        self.field_name = "tipoticket"
        self.data_field = f"descripcion{self.field_name}"
        self.model2test_data = {self.data_field: "Example string"}
        self.created_model = self.model2test.objects.create(**self.model2test_data)


class JtipostransaccionesTestsCase(ExampleViewSetTestCase):
    def setUp(self):
        super().setUp()
        self.model2test = Jtipostransacciones
        self.model_name = self.model2test.__name__.lower()
        self.field_name = "tipotransaccion"
        self.data_field = f"descripcion{self.field_name}"
        self.model2test_data = {self.data_field: "Example string"}
        self.created_model = self.model2test.objects.create(**self.model2test_data)
