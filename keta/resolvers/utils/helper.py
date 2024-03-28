import base64
import requests
from decouple import config
from rest_framework.exceptions import APIException


def send_email(data, typeemial):
    
    try:
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

        ticket_data_creation = {
            "FromName": "Cooperativa PilahuinTio",
            "From": "notificaciones@pilahuintio.fin.ec",
            "To": {"Email": [data["emailcliente"]]},
            "Message": {
                "Subject": "Cooperativa PalanquinTio notificaciones",
                "Classification": "C",
                "BasedOn": {"Id": "7", "Type": "Template"},
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

        ticket_data_assigment = {
            "FromName": "Cooperativa PilahuinTio",
            "From": "notificaciones@pilahuintio.fin.ec",
            "To": {"Email": [data["emailcliente"]]},
            "Message": {
                "Subject": "Cooperativa PilahuinTio notificaciones",
                "Classification": "C",
                "BasedOn": {"Id": "7", "Type": "Template"},
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

        ticket_data_rejection = {
            "FromName": "Cooperativa PilahuinTio",
            "From": "notificaciones@pilahuintio.fin.ec",
            "To": {"Email": [data["emailcliente"]]},
            "Message": {
                "Subject": "Cooperativa PalanquinTio notificaciones",
                "Classification": "C",
                "BasedOn": {"Id": "7", "Type": "Template"},
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

        ticket_data_resolution = {
            "FromName": "Cooperativa PilahuinTio",
            "From": "notificaciones@pilahuintio.fin.ec",
            "To": {"Email": [data["emailcliente"]]},
            "Message": {
                "Subject": "Cooperativa PilahuinTio notificaciones",
                "Classification": "C",
                "BasedOn": {"Id": "7", "Type": "Template"},
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

        if typeemial == "create_ticket_email":
            request_body = {"GeneralData": ticket_data_creation}
        elif typeemial == "assign_ticket_email":
            request_body = {"GeneralData": ticket_data_assigment}
        elif typeemial == "rejection_ticket_email":
            request_body = {"GeneralData": ticket_data_rejection}
        else:
            request_body = {"GeneralData": ticket_data_resolution}

        # Make the API request
        response = requests.post(
            "https://api2019.masterbase.com/UniqueMail/v3/ALYGUTAY2MKTEC",
            headers=headers,
            json=request_body,
            timeout=30,
        )

        # Process the response
        if response.status_code == 200:
            # Success in sending the email
            return True
    
    except Exception as exc:
        raise APIException(exc) from exc
    return False
