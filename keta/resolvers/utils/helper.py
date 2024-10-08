import base64
import requests
from decouple import config
from rest_framework.exceptions import APIException

from reports.utils.helper import format_date


def build_json(data, typeemial):
    request_body = {}

    if typeemial == "create_ticket_email":
        request_body = {
            "GeneralData": {
                "FromName": "Cooperativa PilahuinTio",
                "From": "notificaciones@pilahuintio.fin.ec",
                "To": {"Email": [data["emailcliente"]]},
                "Message": {
                    "Subject": "Cooperativa PilahuinTio notificaciones",
                    "Classification": "C",
                    "BasedOn": {"Id": "3", "Type": "Template"},
                    "Body": {
                        "Format": "html",
                        "Value": "obligatorio",
                        "Variables": [
                            {"Name": "fullname", "Value": f"{data['fullname']}"},
                            {"Name": "codigo", "Value": data["codigo"]},
                            {"Name": "date", "Value": data["date"]},
                            {"Name": "agency", "Value": data["agency"]},
                            {"Name": "tickettype", "Value": data["tickettype"]}
                        ]
                    },
                    # "Attachment": [
                    #     {
                    #         "FileName": "Boletos Participantes.pdf",
                    #         "Encode": "Base64",
                    #         "Size": "178",
                    #         "Value": data["Mpdf"],
                    #     }
                    # ],
                },
                "Options": {
                    "OpenTracking": "true",
                    "ClickTracking": "false",
                    "TextHtmlTracking": "true",
                    "AutoTextBody": "false",
                    "Personalization": "true",
                },
            }
        }

    elif typeemial == "assign_ticket_email":
        request_body = {
            "GeneralData": {
                "FromName": "Cooperativa PilahuinTio",
                "From":  "notificaciones@pilahuintio.fin.ec",
                "To": {"Email": [str(data["email_asignado"])]},
                "Message": {
                    "Subject": "Nuevo Ticket Asignado",
                    "Classification": "C",
                    "BasedOn": {"Id": "2", "Type": "Template"},
                    "Body": {
                        "Format": "html",
                        "Value": "obligatorio",
                        "Variables": [
                            {"Name": "nombres_tecnico", "Value": data["nombres_tecnico"]},
                            {"Name": "codigo", "Value":  data["codigo"]},
                            {"Name": "titulo_tarea", "Value": data["titulo_tarea"]},
                            {"Name": "prioridad", "Value": data["prioridad"]},
                            {"Name": "tipo_ticket", "Value":  data["tipo_ticket"]},
                            {"Name": "fechaentrega", "Value": format_date(data["fechaentrega"])},
                            {"Name": "nombres_asignador", "Value": data["nombres_asignador"]},
                            {"Name": "cargo_asignador", "Value": data["cargo_asignador"]}
                        ]
                    },
                    # "Attachment": [
                    #     {
                    #         "FileName": "Boletos Participantes.pdf",
                    #         "Encode": "Base64",
                    #         "Size": "178",
                    #         "Value": data["Mpdf"],
                    #     }
                    # ],
                },
                "Options": {
                    "OpenTracking": "true",
                    "ClickTracking": "false",
                    "TextHtmlTracking": "true",
                    "AutoTextBody": "false",
                    "Personalization": "true",
                },
            }
        }

    elif typeemial == "rejection_ticket_email":
        request_body = {
            "GeneralData": {
                "FromName": "Cooperativa PilahuinTio",
                "From":  "notificaciones@pilahuintio.fin.ec",
                "To": {"Email": [str(data["email_asignador"])]},
                "Message": {
                    "Subject": "Ticket Rechazado",
                    "Classification": "C",
                    "BasedOn": {"Id": "5", "Type": "Template"},
                    "Body": {
                        "Format": "html",
                        "Value": "obligatorio",
                        "Variables": [
                            {"Name": "nombres_asignador", "Value": data["nombres_asignador"]},
                            {"Name": "codigo", "Value":  data["codigo"]},
                            {"Name": "max_fechacreacion", "Value": format_date(data["max_fechacreacion"])},
                            {"Name": "detalles_rechazo", "Value": data["detalles_rechazo"]},
                            {"Name": "nombres_tecnico", "Value": data["nombres_tecnico"]},
                            {"Name": "email_asignado", "Value": data["email_asignado"]},
                            {"Name": "cargo_asignado", "Value": data["cargo_asignado"]}
                        ]
                    },
                    # "Attachment": [
                    #     {
                    #         "FileName": "Boletos Participantes.pdf",
                    #         "Encode": "Base64",
                    #         "Size": "178",
                    #         "Value": data["Mpdf"],
                    #     }
                    # ],
                },
                "Options": {
                    "OpenTracking": "true",
                    "ClickTracking": "false",
                    "TextHtmlTracking": "true",
                    "AutoTextBody": "false",
                    "Personalization": "true",
                },
            }
        }

    elif typeemial == "resolution_ticket_email":
        request_body = {
            "GeneralData": {
                "FromName": "Cooperativa PilahuinTio",
                "From":  "notificaciones@pilahuintio.fin.ec",
                "To": {"Email": [str(data["emailcliente"])]},
                "Message": {
                    "Subject": "Cooperativa PilahuinTio notificaciones",
                    "Classification": "C",
                    "BasedOn": {"Id": "4", "Type": "Template"},
                    "Body": {
                        "Format": "html",
                        "Value": "obligatorio",
                        "Variables": [
                            {"Name": "fullname", "Value": data["fullname"]},
                            {"Name": "codigo", "Value": data["codigo"]},
                            {"Name": "fecharesolucion", "Value": data["date"]},
                            {"Name": "agency", "Value": data["agency"]},
                            {"Name": "tickettype", "Value": data["tickettype"]}
                        ]
                    },
                    # "Attachment": [
                    #     {
                    #         "FileName": "Boletos Participantes.pdf",
                    #         "Encode": "Base64",
                    #         "Size": "178",
                    #         "Value": data["Mpdf"],
                    #     }
                    # ],
                },
                "Options": {
                    "OpenTracking": "true",
                    "ClickTracking": "false",
                    "TextHtmlTracking": "true",
                    "AutoTextBody": "false",
                    "Personalization": "true",
                },
            }
        }
    return request_body


def send_email(data_email, typeemial):

    # Define authentication credentials
    usermaster = config("USERMASTER")
    password = config("PASSWORD")

    # Construct the authorization headers
    auth_header = f"{usermaster}:{password}"
    encoded_auth_header = base64.b64encode(auth_header.encode()).decode()
    headers = {
        "Authorization": f"Basic {encoded_auth_header}",
        "Content-Type": "application/json",
    }
    request_body = build_json(data_email, typeemial)

    try:
        # Make the API request
        response = requests.post(
            "https://api2019.masterbase.com/UniqueMail/v3/JAKAYSAMKTEC",
            headers=headers,
            json=request_body,
            timeout=30,
        )
    except Exception as exc:
        raise APIException(exc) from exc
        # Process the response

    if response.status_code == 200:
        # Success in sending the email
        print(response.status_code)
    else:
        raise APIException(f"Response code {response.status_code} and auth_header = {usermaster}:{password}")
