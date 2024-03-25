import uuid
import socket
import requests
from rest_framework import viewsets, status
from rest_framework.response import Response


def get_mac_address():
    # Get the MAC address of the computer
    mac_address = ":".join(
        ["{:02x}".format((uuid.getnode() >> ele) & 0xFF) for ele in range(0, 48, 8)]
    )
    return mac_address


def get_public_ip_address():
    # Method 1: Use a public API to get the IP address
    try:
        response = requests.get("https://api64.ipify.org?format=json")
        if response.status_code == 200:
            data = response.json()
            return data.get("ip")
    except requests.RequestException:
        pass

    # Method 2: Use a socket to connect to a remote server
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except socket.error:
        pass

    return None


class BaseViewSet(viewsets.ModelViewSet):
    """
    Base class for set views.
    """

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        instance_data = self.get_serializer(instance)
        return Response(instance_data.data, status=status.HTTP_202_ACCEPTED)
