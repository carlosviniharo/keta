import pdb

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from .models import (
    Jusuarios,
    Jpersonas,
    Jcargos,
    Jdepartamentos,
    Jcorporaciones,
    Jgeneros,
    Jroles,
    Jsucursales,
    Jtiposidentificaciones,
    Jtipospersonas,
)


class JusuariosRegisterViewTestCase(APITestCase):
    fixtures = ["users_test.json"]

    def setUp(self):
        self.client = APIClient()
        self.persona_data = {
            "idgenero": "http://127.0.0.1:8000/users/api/generos/1/",
            "idtipoidentificacion": "http://127.0.0.1:8000/users/api/tiposidentificaciones/1/",
            "idtipopersona": "http://127.0.0.1:8000/users/api/tipospersonas/2/",
            "identificacion": "1111111111",
            "nombre": "Christian Bladimir",
            "apellido": "Sisa Maliza",
            "emailclientecliente": "",
            "celular": "0999999999",
            "telefono": "062922066",
            "direccion": "Otavalo",
        }
        self.persona_data_updated = {
            "idgenero": "http://127.0.0.1:8000/users/api/generos/1/",
            "idtipoidentificacion": "http://127.0.0.1:8000/users/api/tiposidentificaciones/1/",
            "idtipopersona": "http://127.0.0.1:8000/users/api/tipospersonas/2/",
            "identificacion": "1111111111",
            "nombre": "Christian",
            "apellido": "Sisa",
            "emailclientecliente": "",
            "celular": "0999999999",
            "telefono": "062922068",
            "direccion": "Quito",
        }
        self.usuario_data = {
            "idrol": "http://127.0.0.1:8000/users/api/roles/1/",
            "iddepartamento": "http://127.0.0.1:8000/users/api/departamentos/2/",
            "idcargo": "http://127.0.0.1:8000/users/api/cargos/2/",
            "password": "1234",
            "email": "bladimir@pilahuintio.ec",
            "username": "Bladi",
        }

        self.usuario_data_second_account = {
            "idrol": "http://127.0.0.1:8000/users/api/roles/1/",
            "iddepartamento": "http://127.0.0.1:8000/users/api/departamentos/2/",
            "idcargo": "http://127.0.0.1:8000/users/api/cargos/2/",
            "password": "1234",
            "email": "bladimir@gmail.ec",
            "username": "Bladi",
        }

    def test_register_new_user(self):
        data = {"persona": self.persona_data, "usuario": self.usuario_data}
        data_second_account = {
            "persona": self.persona_data_updated,
            "usuario": self.usuario_data_second_account,
        }
        response = self.client.post(reverse("jusuarios-list"), data, format="json")

        self.assertEqual(Jusuarios.objects.count(), 1)
        self.assertEqual(Jpersonas.objects.count(), 1)
        # Check that the created user's details are correct
        created_user = Jusuarios.objects.first()
        self.assertEqual(created_user.username, "Bladi")
        self.assertEqual(created_user.email, "bladimir@pilahuintio.ec")

        created_persona = Jpersonas.objects.first()
        self.assertEqual(created_persona.nombre, "Christian Bladimir")
        self.assertEqual(created_persona.apellido, "Sisa Maliza")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that persona is updated and a second account is created
        response_updated = self.client.post(
            reverse("jusuarios-list"), data_second_account, format="json"
        )
        self.assertEqual(Jusuarios.objects.count(), 2)
        # pdb.set_trace()
        self.assertEqual(Jpersonas.objects.count(), 1)
        # Check the if the fields are updated rightfully.
        persona_updated = Jpersonas.objects.first()
        self.assertEqual(persona_updated.nombre, "Christian")
        self.assertEqual(persona_updated.apellido, "Sisa")
        self.assertEqual(persona_updated.direccion, "Quito")

        self.assertEqual(response_updated.status_code, status.HTTP_201_CREATED)


class JususarioRegisterViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a Jusuarios instance for testing
        self.user = Jusuarios.objects.create(
            email="test@users.com", password="testpassword"
        )

    def test_retrieve_user_by_email(self):
        response = self.client.get(
            reverse("profile", kwargs={"email": self.user.email})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_nonexistent(self):
        response = self.client.get(
            reverse("profile", kwargs={"email": "fake@user.com"})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CustomTokenObtainPairViewTest(APITestCase):
    fixtures = ["users_test.json"]
    
    def setUp(self):
        self.client = APIClient()
        self.user = Jusuarios.objects.create_user(
            email="test@users.com",
            password="testpass",
            idrol=Jroles.objects.get(idrol=1),
        )

    def test_user_login(self):
        data = {"email": "test@users.com", "password": "testpass"}
        response = self.client.post(reverse("token_obtain_pair"), data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

        # Retrieve the user instance again from the database to refresh the last_login field
        user = Jusuarios.objects.get(email="test@users.com")
        self.assertIsNotNone(user.last_login)
        self.assertTrue(
            user.last_login >= (timezone.now() - timezone.timedelta(minutes=1))
        )


class ExampleViewSetTestCase(APITestCase):
    def setUp(self):
        self.model2test = Jcargos
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


class JdepartamentosTestCase(ExampleViewSetTestCase):
    def setUp(self):
        super().setUp()
        self.model2test = Jdepartamentos
        self.model_name = self.model2test.__name__.lower()
        self.field_name = self.model_name[1:-1]
        self.model2test_data = {f"descripcion{self.field_name}": "Example string"}
        self.created_model = self.model2test.objects.create(**self.model2test_data)
        # pdb.set_trace()


class JcorporacionesTestCase(ExampleViewSetTestCase):
    def setUp(self):
        super().setUp()
        self.model2test = Jcorporaciones
        self.model_name = self.model2test.__name__.lower()
        self.field_name = self.model_name[1:-2]
        self.model2test_data = {f"descripcion{self.field_name}": "Example string"}
        self.created_model = self.model2test.objects.create(**self.model2test_data)


class JgenerosTestCase(ExampleViewSetTestCase):
    def setUp(self):
        super().setUp()
        self.model2test = Jgeneros
        self.model_name = self.model2test.__name__.lower()
        self.field_name = self.model_name[1:-1]
        self.model2test_data = {f"descripcion{self.field_name}": "Example string"}
        self.created_model = self.model2test.objects.create(**self.model2test_data)


class JrolesTestCase(ExampleViewSetTestCase):
    def setUp(self):
        super().setUp()
        self.model2test = Jroles
        self.model_name = self.model2test.__name__.lower()
        self.field_name = self.model_name[1:-2]
        self.model2test_data = {f"descripcion{self.field_name}": "Example string"}
        self.created_model = self.model2test.objects.create(**self.model2test_data)


class JsucursalesTestCase(ExampleViewSetTestCase):
    def setUp(self):
        super().setUp()
        self.model2test = Jsucursales
        self.model_name = self.model2test.__name__.lower()
        self.field_name = self.model_name[1:-2]
        self.model2test_data = {f"descripcion{self.field_name}": "Example string"}
        self.created_model = self.model2test.objects.create(**self.model2test_data)


class JtiposidentificacionesTestCase(ExampleViewSetTestCase):
    def setUp(self):
        super().setUp()
        self.model2test = Jtiposidentificaciones
        self.model_name = self.model2test.__name__.lower()
        # Due to inconsistencies in the database it is setup manually
        self.field_name = "tipoidentificacion"
        self.model2test_data = {f"descripcion{self.field_name}": "Example string"}
        self.created_model = self.model2test.objects.create(**self.model2test_data)


class JtipospersonasTestCase(ExampleViewSetTestCase):
    def setUp(self):
        super().setUp()
        self.model2test = Jtipospersonas
        self.model_name = self.model2test.__name__.lower()
        # Due to inconsistencies in the database it is set up manually
        self.field_name = "tipopersona"
        self.model2test_data = {f"descripcion{self.field_name}": "Example string"}
        self.created_model = self.model2test.objects.create(**self.model2test_data)
