from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse

from .models import Jcanalesrecepciones


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
        response = self.create_jproblemas({
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
        self.assertEquals(response.data["persona"]["idpersona"], response_new_person.data["persona"]["idpersona"])
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
    
    
    class ExampleViewSetTestCase(APITestCase):
        def setUp(self):
            self.model2test = Jcanalesrecepciones
            self.model_name = self.model2test.__name__.lower()
            self.field_name = self.model_name[1:-1]
            self.model2test_data = {f"descripcion{self.field_name}": "Example string"}
            self.created_model = self.model2test.objects.create(**self.model2test_data)
        
        def test_list(self):
            url = reverse(f"{self.model_name}-list")
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 1)
        
        def test_retrieve(self):
            url = reverse(
                f"{self.model_name}-detail",
                kwargs={"pk": getattr(self.created_model, f"id{self.field_name}")},
            )
            response = self.client.get(url)
            # pdb.set_trace()
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(
                response.data[f"descripcion{self.field_name}"],
                getattr(self.created_model, f"descripcion{self.field_name}"),
            )
        
        def test_create(self):
            new_data = {f"descripcion{self.field_name}": "Other example"}
            url = reverse(f"{self.model_name}-list")
            response = self.client.post(url, new_data, format="json")
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(self.model2test.objects.count(), 2)
        
        def test_update(self):
            updated_data = {f"descripcion{self.field_name}": "updated example"}
            
            url = reverse(
                f"{self.model_name}-detail",
                kwargs={"pk": getattr(self.created_model, f"id{self.field_name}")},
            )
            response = self.client.patch(url, updated_data, format="json")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.created_model.refresh_from_db()
            self.assertEqual(
                getattr(self.created_model, f"descripcion{self.field_name}"),
                updated_data[f"descripcion{self.field_name}"],
            )
        
        def test_delete_tipopersona(self):
            url = reverse(
                f"{self.model_name}-detail",
                kwargs={"pk": getattr(self.created_model, f"id{self.field_name}")},
            )
            # pdb.set_trace()
            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            self.assertEqual(self.model2test.objects.count(), 0)