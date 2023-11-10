from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User  # If you use authentication
from .models import Jarchivos  # Import your model
from .serializers import JarchivosSerializer  # Import your serializer
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse


class JarchivosViewSetTestCase(APITestCase):

    def setUp(self):
        self.pdf_file = SimpleUploadedFile("test.pdf", b"file_content")

    def test_create_jarchivos(self):


        # Prepare data for your request
        
        data = {
            "pdf_file": pdf_file,
            # Add other required data here
        }

        url = reverse('jarchivos-list')  # Use the correct URL name for your viewset
        response = self.client.post(url, data, format='multipart')

        # Assert the response status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Optionally, assert the response data matches your expectations
        self.assertEqual(Jarchivos.objects.count(), 1)  # Check if an object was created
        jarchivo = Jarchivos.objects.first()
        self.assertEqual(jarchivo.name, "test.pdf")
        # Add more assertions based on your data and expectations

