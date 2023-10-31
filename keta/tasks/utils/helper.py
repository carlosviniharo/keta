import base64
import io
from binascii import Error as BinasciiError
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


def convert_pdf_to_b64(pdf_file):
    
    if not isinstance(pdf_file, bytes):
        # Save the PDF file to a temporary location on disk
        temp_file_path = default_storage.save("temp_pdf.pdf", ContentFile(pdf_file.read()))
    
        # Read the PDF file as binary data
        with open(temp_file_path, "rb") as pdf_data:
            pdf_binary_data = pdf_data.read()
            
        default_storage.delete(temp_file_path)
    else:
        pdf_binary_data = pdf_file
        
    try:
        # Encode the binary data in base64
        base64_encoded_pdf = base64.b64encode(pdf_binary_data).decode("utf-8")
    except BinasciiError as exc:
        raise f"Invalid {exc}"
    
    return base64_encoded_pdf


def convert_base64_to_pdf(base64_string, filename, mimetype):
    try:
        # Decode the Base64 string into binary data
        pdf_data = base64.b64decode(base64_string)

        # Create an in-memory binary stream
        pdf_stream = io.BytesIO(pdf_data)

        # Create an HTTP response with the PDF content
        response = HttpResponse(pdf_stream.read(), content_type=mimetype)
        response["Content-Disposition"] = f'filename="{filename}.pdf"'

        return response
    except Exception as exc:
        # Handle any decoding errors or other exceptions
        raise ValidationError("Unable to decode Base64 string") from exc
