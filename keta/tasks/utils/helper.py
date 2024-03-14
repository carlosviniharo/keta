import base64
import io
from binascii import Error as BinasciiError
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.utils import timezone

from users.models import Jdiasfestivos


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


def calculate_weekends(create_time, optimal_time, extended_time):

    end_optimal_date = create_time + timezone.timedelta(days=int(optimal_time))
    end_extended_date = create_time + timezone.timedelta(days=int(extended_time))

    optimal_weekends = count_weekends(create_time, end_optimal_date)
    extended_weekends = count_weekends(create_time, end_extended_date)

    optimal_date = (
            create_time + timezone.timedelta(days=int(optimal_time)) + timezone.timedelta(days=int(optimal_weekends))
    )

    optimal_date += timezone.timedelta(days=calculate_holidays(create_time, optimal_date))

    extended_date = (
            create_time + timezone.timedelta(days=int(extended_time)) + timezone.timedelta(days=int(extended_weekends))
    )

    extended_date += timezone.timedelta(days=calculate_holidays(create_time, extended_date))

    if optimal_date.weekday() > 4:
        optimal_date += timezone.timedelta(7 - optimal_date.weekday())
    if extended_date.weekday() > 4:
        extended_date += timezone.timedelta(7 - extended_date.weekday())

    return optimal_date, extended_date


def count_weekends(start_date, end_date) -> int:
    """
    Count the number of weekends (Saturdays and Sundays) between two dates, inclusive.

    Args:
        start_date (datetime): The start date.
        end_date (datetime): The end date.

    Returns:
        int: The count of weekends between the two dates.
    """
    # Calculate total days (inclusive)
    total_days: int = (end_date - start_date).days + 1

    # Calculate complete weeks
    complete_weeks: int = total_days // 7

    # Multiply by 2 for weekends in complete weeks
    weekend_count: int = complete_weeks * 2

    # Check remaining days
    remaining_days: int = total_days % 7

    # Check if the start date is on a weekday
    if start_date.weekday() <= 4:
        # Add the minimum of remaining days and 2 for weekends
        weekend_count += min(remaining_days, 2)

    # Check if there are any remaining days after complete weeks
    if remaining_days > 0:
        # Check if start_date or end_date is Saturday or Sunday
        if start_date.weekday() == 5 or end_date.weekday() == 5:  # Saturday
            weekend_count += 1
        elif start_date.weekday() == 6 or end_date.weekday() == 6:  # Sunday
            weekend_count += 1

    return weekend_count


def calculate_holidays(start_date, end_date):
    holidays = Jdiasfestivos.objects.filter(fecha__date__range=(start_date, end_date), status=True)
    return len(holidays) if holidays else 0
