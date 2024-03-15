from datetime import datetime, timedelta

import pytz

from api.models import Message


def get_message_send_time(mailing, client, interval=0):
    """
    Calculate the time to send a message based on the mailing and client time zones and intervals.

    Args:
        mailing (Mailing): The mailing object containing start and end datetime and interval times.
        client (Client): The client object containing the time zone.
        interval (int, optional): The time (in sec) after which the message should be sent. Defaults to 0.

    Returns:
        datetime: The time to send the message in UTC time zone.
    """

    start = max(
        mailing.datetime_start.astimezone(client.time_zone),
        (datetime.now() + timedelta(seconds=interval)).astimezone(
            client.time_zone
        ),
    )
    end = mailing.datetime_end.astimezone(client.time_zone)

    if not mailing.send_interval_time_start:
        return start.astimezone(pytz.utc)

    start_interval = mailing.send_interval_time_start.strftime("%H:%M")
    end_interval = mailing.send_interval_time_end.strftime("%H:%M")

    start_loc = start.replace(
        hour=int(start_interval[:2]), minute=int(start_interval[3:])
    )
    end_loc = start.replace(
        hour=int(end_interval[:2]), minute=int(end_interval[3:])
    )

    if start_loc < end_loc:
        if start < start_loc:
            if start_loc < end:
                return start_loc.astimezone(pytz.utc)
            return None
        if start_loc < start < end_loc:
            return start.astimezone(pytz.utc)
        if end_loc < start:
            if start_loc + timedelta(days=1) < end:
                return (start_loc + timedelta(days=1)).astimezone(pytz.utc)
            return None
    if start < end_loc:
        return start.astimezone(pytz.utc)
    if end_loc < start < start_loc:
        if end > start_loc:
            return start_loc.astimezone(pytz.utc)
        return None
    if start_loc < start:
        return start.astimezone(pytz.utc)


def get_mailing_messages(mailing, created=False):
    """
    Returns messages' list of current mailing.

    Args:
        mailing (Mailing): The mailing object containing start and end datetime and interval times.
        created (bool, optional): Indicates whether the mailing is new. Defaults to False.

    Returns:
        list: Messages' list of current mailing
    """
    if created:
        clients = [
            client
            for client in mailing.get_mailing_clients()
            if get_message_send_time(mailing, client)
        ]
        mailing.set_clients_count(clients)
        return list(
            Message.objects.create(mailing=mailing, client=client)
            for client in clients
        )
    return [message for message in Message.objects.filter(mailing=mailing)]
