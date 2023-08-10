from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient
from .models import *


class JusuariosRegisterViewTestCase(TestCase):

    fixtures = ['users_test.json']

    def setUp(self):
        self.client = APIClient()

    def test_register_new_user(self):
        data = {
            "persona": {
                "idgenero": 1,
                "idtipoidentificacion": 1,
                "idtipopersona": 2,
                "identificacion": "1111111111",
                "nombre": "Christian Bladimir",
                "apellido": "Sisa Maliza",
                "emailclientecliente": "",
                "celular": "0999999999",
                "telefono": "062922066",
                "direccion": "Otavalo"
            },
            "usuario": {
                "idrol": 1,
                "iddepartamento": 2,
                "idcargo": 2,
                "password": "1234",
                "email": "bladimir@pilahuintio.ec",
                "username": "Bladi"
            }
        }
        response = self.client.post(reverse("sign_up"), data, format="json")
        # Assertions
        self.assertEqual(Jusuarios.objects.count(), 1)
        self.assertEqual(Jpersonas.objects.count(), 1)
        # Check that the created user's details are correct
        created_user = Jusuarios.objects.first()
        self.assertEqual(created_user.username, 'Bladi')
        self.assertEqual(created_user.email, 'bladimir@pilahuintio.ec')

        created_persona = Jpersonas.objects.first()
        self.assertEqual(created_persona.nombre, 'Christian Bladimir')
        self.assertEqual(created_persona.apellido, 'Sisa Maliza')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class JususarioRegisterViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a Jusuarios instance for testing
        self.user = Jusuarios.objects.create(email="test@users.com", password="testpassword")

    def test_retrieve_user_by_email(self):
        response = self.client.get(reverse("profile", kwargs={"email": self.user.email}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class BaseListViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_retrieve_all_jcargos(self):
        # Create some test data
        Jcargos.objects.create(descripcioncargo='Manager')
        Jcargos.objects.create(descripcioncargo='Employee')

        response = self.client.get(reverse('cargos_list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        # Test if the response data matches the created instances
        self.assertEqual(response.data[0]['descripcioncargo'], 'Manager')
        self.assertEqual(response.data[1]['descripcioncargo'], 'Employee')


class CustomTokenObtainPairViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = Jusuarios.objects.create_user(
            email='test@users.com', username='testuser', password='testpass'
        )

    def test_user_login(self):
        data = {
            'email': 'test@users.com',
            'password': 'testpass'
        }
        response = self.client.post(reverse('token_obtain_pair'), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

        # Retrieve the user instance again from the database to refresh the last_login field
        user = Jusuarios.objects.get(email='test@users.com')
        self.assertIsNotNone(user.last_login)
        self.assertTrue(user.last_login >= timezone.now() - timezone.timedelta(minutes=1))


class JususarioRegisterViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = Jusuarios.objects.create_user(
            email='test@users.com', username='testuser', password='testpass'
        )

    def test_user_retrieve(self):
        response = self.client.get(reverse('profile', kwargs={'email': self.user.email}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)

    def test_retrieve_nonexistent(self):
        response = self.client.get(reverse('profile', kwargs={'email': "fake@user.com"}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


