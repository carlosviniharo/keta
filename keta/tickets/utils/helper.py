import uuid


def generate_ticket_id():
    return str(uuid.uuid4()).split("-")[-1]
