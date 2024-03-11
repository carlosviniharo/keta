import re

from django.shortcuts import get_object_or_404
from django.urls import reverse
from trackers.serializers import JnotificacionesSerilaizer, JseguimientostareasSerializer

from users.models import Jusuarios


# def create_notification(response, request):
#     ticket_updated = response.data
#     ticket_number = ticket_updated["idtarea"]
#
#     notification_dic = {
#         "idtarea": ticket_updated["url"],
#     }
#     tracker_dic = {
#         "idtarea": ticket_updated["url"],
#     }
#
#     # Checking the state of the ticket
#     pattern = r"/(?P<estado>\d+)/$"
#     match = re.search(pattern, ticket_updated["idestado"])
#     state = int(match.group("estado"))
#
#     if state == 2:
#         notification_dic["notification_type"] = "Creation Notification"
#         notification_dic["idusuario"] = ticket_updated["idusuarioasignado"]
#         notification_dic["message"] = f"A new claim with ticket number {ticket_number} has been opened"
#
#         tracker_dic["tituloseguimientotarea"] = "Creacion de Tarea"
#         tracker_dic["detalleresolucion"] = f"Se a registrado el reclamo numero {ticket_number} en KETA"
#         tracker_dic["idusuario"] = ticket_updated["idusuarioqasigno"]
#
#     elif state == 3:
#         notification_dic["notification_type"] = "Assignation Notification"
#         notification_dic["idusuario"] = ticket_updated["idusuarioasignado"]
#         notification_dic["message"] = f"The claim with ticket number ticket_number has been assigned to you"
#
#         user_id = int(ticket_updated['idusuarioasignado'].split('/')[-2])
#         user_assigned = get_object_or_404(Jusuarios, idusuario=user_id)
#         tracker_dic["tituloseguimientotarea"] = "Assignacion de Tarea"
#         tracker_dic["detalleresolucion"] = (f"El reclamo numero {ticket_number} "
#                                             f"ha sido asignado a {user_assigned.email}")
#         tracker_dic["idusuario"] = ticket_updated["idusuarioqasigno"]
#
#     elif state == 6:
#         notification_dic["notification_type"] = "Resolution Notification"
#         notification_dic["idusuario"] = ticket_updated["idusuarioqasigno"]
#         notification_dic["message"] = f"The claim with ticket number {ticket_number} has been solved"
#
#     notification = JnotificacionesSerilaizer(
#         data=notification_dic,
#         context={"request": request}
#     )
#
#     notification.is_valid(raise_exception=True)
#     notification.save()
#
#     if len(tracker_dic) > 1:
#         track = JseguimientostareasSerializer(
#             data=tracker_dic,
#             context={"request": request}
#         )
#
#         track.is_valid(raise_exception=True)
#         track.save()
def create_notification_new_claim(response, request):
    ticket_updated = response.data
    ticket_number = ticket_updated["idtarea"]

    notification_dic = {
        "idtarea": ticket_updated["url"],
    }
    tracker_dic = {
        "idtarea": ticket_updated["url"],
    }
    handle_creation_notification(notification_dic, ticket_updated, ticket_number, tracker_dic)
    create_notification_entry(notification_dic, request)
    create_tracker_entry(tracker_dic, request)


def create_notification(response, request):
    ticket_updated = response.data
    ticket_number = ticket_updated["idtarea"]

    notification_dic = {
        "idtarea": ticket_updated["url"],
    }
    tracker_dic = {
        "idtarea": ticket_updated["url"],
    }

    state = get_ticket_state(ticket_updated)

    if state == 3:
        handle_assignation_notification(notification_dic, ticket_updated, ticket_number, tracker_dic)
    elif state == 6:
        handle_resolution_notification(notification_dic, ticket_updated, ticket_number)

    create_notification_entry(notification_dic, request)
    if len(tracker_dic) > 1:
        create_tracker_entry(tracker_dic, request)


def get_ticket_state(ticket_updated):
    pattern = r"/(?P<estado>\d+)/$"
    match = re.search(pattern, ticket_updated["idestado"])
    return int(match.group("estado"))


def handle_creation_notification(notification_dic, ticket_updated, ticket_number, tracker_dic):
    notification_dic.update({
        "notification_type": "Creation Notification",
        "idusuario": ticket_updated["idusuarioasignado"],
        "message": f"A new claim with ticket number {ticket_number} has been opened"
    })

    tracker_dic.update({
        "tituloseguimientotarea": "Creacion de Tarea",
        "detalleresolucion": f"Se a registrado el reclamo numero {ticket_number} en KETA",
        "idusuario": ticket_updated["idusuarioqasigno"]
    })


def handle_assignation_notification(notification_dic, ticket_updated, ticket_number, tracker_dic):
    notification_dic.update({
        "notification_type": "Assignation Notification",
        "idusuario": ticket_updated["idusuarioasignado"],
        "message": f"The claim with ticket number {ticket_number} has been assigned to you"
    })

    user_id = int(ticket_updated['idusuarioasignado'].split('/')[-2])
    user_assigned = get_object_or_404(Jusuarios, idusuario=user_id)

    tracker_dic.update({
        "tituloseguimientotarea": "Assignacion de Tarea",
        "detalleresolucion": f"El reclamo numero {ticket_number} ha sido asignado a {user_assigned.email}",
        "idusuario": ticket_updated["idusuarioqasigno"]
    })


def handle_resolution_notification(notification_dic, ticket_updated, ticket_number):
    notification_dic.update({
        "notification_type": "Resolution Notification",
        "idusuario": ticket_updated["idusuarioqasigno"],
        "message": f"The claim with ticket number {ticket_number} has been solved"
    })


def create_notification_entry(notification_dic, request):
    notification = JnotificacionesSerilaizer(
        data=notification_dic,
        context={"request": request}
    )
    notification.is_valid(raise_exception=True)
    notification.save()


def create_tracker_entry(tracker_dic, request):
    track = JseguimientostareasSerializer(
        data=tracker_dic,
        context={"request": request}
    )
    track.is_valid(raise_exception=True)
    track.save()
