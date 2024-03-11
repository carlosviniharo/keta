import base64
import requests
from decouple import config
from rest_framework.exceptions import APIException


def send_email(data, idtemplate):
    
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

        # Construct the request body with dynamic data
        general_data = {
            "FromName": "Cooperativa PilahuinTio",
            "From": "notificaciones@pilahuintio.fin.ec",
            "To": {"Email": [data["emailcliente"]]},
            "Message": {
                "Subject": "Cooperativa PilahuinTio notificaciones",
                "Classification": "C",
                "BasedOn": {"Id": idtemplate, "Type": "Template"},
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

        request_body = {"GeneralData": general_data}
        timeout = 30

        # Make the API request
        response = requests.post(
            "https://api2019.masterbase.com/UniqueMail/v3/ALYGUTAY2MKTEC",
            headers=headers,
            json=request_body,
            timeout=timeout,
        )

        # Process the response
        if response.status_code == 200:
            # Success in sending the email
            return True
    
    except Exception as exc:
        raise APIException(exc) from exc
    return False
