import re
from trackers.serializers import JnotificacionesSerilaizer


def create_notification(response, request):
    ticket_updated = response.data
    ticket_number = ticket_updated["idtarea"]
    notification_dic = {
        "idtarea": ticket_updated["url"],
    }
    # Checking the state of the ticket
    pattern = r"/(?P<estado>\d+)/$"
    match = re.search(pattern, ticket_updated["idestado"])

    if int(match.group("estado")) == 3:
        notification_dic["notification_type"] = "Assignation Notification"
        notification_dic["idusuario"] = ticket_updated["idusuarioasignado"]
        notification_dic["message"] = (
            f"The claim with ticket number {ticket_number} has been assigned to you"
        )
    
    elif int(match.group("estado")) == 6:
        notification_dic["notification_type"] = "Resolution Notification"
        notification_dic["idusuario"] = ticket_updated["idusuarioqasigno"]
        notification_dic["message"] = (
            f"The claim with ticket number {ticket_number} "
            f"has been solved"
        )
    else:
        return
    
    notification = JnotificacionesSerilaizer(
        data=notification_dic,
        context={"request": request}
    )
    notification.is_valid(raise_exception=True)
    notification.save()
