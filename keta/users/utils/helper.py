import uuid
import socket
import requests
from rest_framework import viewsets, status
from rest_framework.exceptions import APIException
from rest_framework.generics import RetrieveAPIView
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
        if hasattr(instance, 'is_active'):
            instance.is_active = False
        else:
            instance.status = False
        instance.save()
        instance_data = self.get_serializer(instance)
        return Response(instance_data.data, status=status.HTTP_202_ACCEPTED)


class BaseRetrieveView(RetrieveAPIView):
    """
    Base class for retrieval views.
    """
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return Response(
            {
                "message": "success",
                "data": response.data
            },
            status=status.HTTP_200_OK
        )


def get_query_by_id(parm_name, param_value, model):
    """
    Gets the query that matches a specific id in the model.
    :param parm_name: str
    :param param_value: str
    :param model: ORM object
    :return: a set of objects
    """

    if param_value is None or param_value == "":
        raise APIException(f"{parm_name} not provided")

    objects_retrieved = model.objects.filter(**{parm_name: param_value})

    if not objects_retrieved:
        raise APIException(f"There was not found record with this id {param_value}")
    return objects_retrieved
