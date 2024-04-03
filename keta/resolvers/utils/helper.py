import base64
import requests
from decouple import config
from rest_framework.exceptions import APIException


def build_json(data, typeemial):

    if typeemial == "create_ticket_email":
        request_body = {
            "GeneralData": {
                "FromName": "Cooperativa PilahuinTio",
                "From": "saludos@jakaysa.com",
                "To": {"Email": [data["emailcliente"]]},
                "Message": {
                    "Subject": "Cooperativa PalanquinTio notificaciones",
                    "Classification": "C",
                    "BasedOn": {"Id": "1", "Type": "Template"},
                    "Body": {
                        "Format": "html",
                        "Value": "obligatorio",
                        "Variables": [
                            {"Name": "NOMBRE", "Value": f"{data['fullname']}"},
                            {"Name": "IDTICKET", "Value": data["idtarea"]},
                            {"Name": "FECHA", "Value": data["date"]},
                            {"Name": "AGENCIA", "Value": data["agency"]},
                            {"Name": "TIPORECLAMO", "Value": data["tickettype"]}
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
                "From":  "saludos@jakaysa.com",
                "To": {"Email": [str(data["email_asignado"])]},
                "Message": {
                    "Subject": "Nuevo Ticket Asignado",
                    "Classification": "C",
                    "BasedOn": {"Id": "7", "Type": "Template"},
                    "Body": {
                        "Format": "html",
                        "Value": "obligatorio",
                        "Variables": [
                            {"Name": "NOMBRE", "Value": "Ejemplo"},
                            {"Name": "IDTICKET", "Value":  "Ejemplo"},
                            {"Name": "FECHA", "Value":  "Ejemplo"},
                            {"Name": "AGENCIA", "Value": "Ejemplo"},
                            {"Name": "TIPORECLAMO", "Value":  "Ejemplo"}
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
                "From":  "saludos@jakaysa.com",
                "To": {"Email": [str(data["email_asignador"])]},
                "Message": {
                    "Subject": "Ticket Rechazado",
                    "Classification": "C",
                    "BasedOn": {"Id": "7", "Type": "Template"},
                    "Body": {
                        "Format": "html",
                        "Value": "obligatorio",
                        "Variables": [
                            {"Name": "NOMBRE", "Value": "Ejemplo"},
                            {"Name": "IDTICKET", "Value": "Ejemplo"},
                            {"Name": "FECHA", "Value": "Ejemplo"},
                            {"Name": "AGENCIA", "Value": "Ejemplo"},
                            {"Name": "TIPORECLAMO", "Value": "Ejemplo"}
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

    else:
        request_body = {
            "GeneralData": {
                "FromName": "Cooperativa PilahuinTio",
                "From":  "saludos@jakaysa.com",
                "To": {"Email": [str(data["emailcliente"])]},
                "Message": {
                    "Subject": "Cooperativa PilahuinTio notificaciones",
                    "Classification": "C",
                    "BasedOn": {"Id": "7", "Type": "Template"},
                    "Body": {
                        "Format": "html",
                        "Value": "obligatorio",
                        "Variables": [
                            {"Name": "NOMBRE", "Value": "Example"},
                            {"Name": "IDTICKET", "Value": "Example"},
                            {"Name": "FECHA", "Value": "Example"},
                            {"Name": "AGENCIA", "Value": "Example"},
                            {"Name": "TIPORECLAMO", "Value": "Example"}
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
        print(response.status_code)
