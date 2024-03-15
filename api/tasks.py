import logging

import requests
from celery import current_app, shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Count
from django.utils import timezone
from dotenv import load_dotenv
from requests.exceptions import HTTPError, RequestException, Timeout
from tabulate import SEPARATING_LINE, tabulate

from api.utils import get_message_send_time

from .models import Message

logger = logging.getLogger("api")

load_dotenv()

api_url = settings.API_URL
api_token = settings.API_TOKEN
email_host_user = settings.EMAIL_HOST_USER
recipient_list = list(settings.EMAIL_RECIPIENTS.values())


class TaskManager:
    @staticmethod
    def create_message_celery_task(message):
        message_send_time = get_message_send_time(
            message.mailing, message.client
        )
        task = send_mailing.apply_async(
            args=[message.id], eta=message_send_time
        )
        celery_task_id = task.id
        message.celery_task_id = celery_task_id
        message.save(update_fields=["celery_task_id"])

    @staticmethod
    def delete_message_celery_task(message):
        celery_task_id = message.celery_task_id
        task_state = current_app.AsyncResult(celery_task_id).state
        if task_state not in ("SUCCESS", "FAILURE", "REVOKED"):
            current_app.control.revoke(celery_task_id, terminate=True)
        message.status = Message.Status.CANCELLED
        message.save(update_fields=["status"])

    @staticmethod
    def update_message_celery_task(message):
        TaskManager.create_new_message_and_send(message)
        TaskManager.delete_message_celery_task(message)

    @staticmethod
    def create_new_message_and_send(message, interval=0):
        message_send_time = get_message_send_time(
            message.mailing, message.client, interval=interval
        )
        if message_send_time and message.status != Message.Status.DELIVERED:
            new_message = Message.objects.create(
                client=message.client,
                mailing=message.mailing,
            )
            task = send_mailing.apply_async(
                args=[new_message.id], eta=message_send_time
            )
            celery_task_id = task.id
            new_message.celery_task_id = celery_task_id
            new_message.save(update_fields=["celery_task_id"])


task_manager = TaskManager()


def get_mailings_stats(queryset):
    stats = {}
    for group in queryset:
        mailing_id = group["mailing_id"]
        if mailing_id not in stats:
            stats[mailing_id] = {}
        status = group["status"]
        message_count = group["message_count"]
        stats[mailing_id][status] = message_count
    return stats


@shared_task(bind=True, acks_late=True, name="Mailing")
def send_mailing(self, message_id):
    try:
        message = Message.objects.get(id=message_id)
        try:
            api_data = {
                "id": message.id,
                "phone": message.client.phone,
                "text": message.mailing.text,
            }
            headers = {
                "Authorization": api_token,
            }
            response = requests.post(
                api_url + str(api_data["id"]), json=api_data, headers=headers
            )
            logger.info(
                f"Sending request to external service. Message_{message.id} (Mailing_{message.mailing.id}) to Client_{message.client.id}"
            )
            response.raise_for_status()
            logger.info(
                f"Message_{message.id} (Mailing_{message.mailing.id} to Client_{message.client.id} was sent successfully. Status code: {response.status_code}"
            )
            message.status = Message.Status.DELIVERED
        except (Timeout, HTTPError, RequestException) as e:
            logger.error(
                f"Message_{message.id} (Mailing_{message.mailing.id} to Client_{message.client.id} was sent unsuccessfully. Error: {e}"
            )
            message.status = Message.Status.NOT_DELIVERED
            task_manager.create_new_message_and_send(message, interval=10)
        except Exception as e:
            logger.warning(
                f"Message_{message.id} (Mailing_{message.mailing.id} to Client_{message.client.id} was sent unsuccessfully. Unexpected error: {e}"
            )
            message.status = Message.Status.NOT_DELIVERED
            task_manager.create_new_message_and_send(message, interval=10)
        finally:
            message.save(update_fields=["status"])
    except Message.DoesNotExist as e:
        logger.error(f"Message_{message_id} error: {e}")
        self.retry(exc=e, countdown=10)


@shared_task(name="Statictics Email")
def send_daily_statistics_email():
    yesterday = timezone.now() - timezone.timedelta(days=1)
    messages = Message.objects.filter(datetime_send__date=yesterday)
    total_messages = messages.count()
    scheduled_messages = messages.filter(
        status=Message.Status.SCHEDULED
    ).count()
    delivered_messages = messages.filter(
        status=Message.Status.DELIVERED
    ).count()
    undelivered_messages = messages.filter(
        status=Message.Status.NOT_DELIVERED
    ).count()
    cancelled_messages = messages.filter(
        status=Message.Status.CANCELLED
    ).count()

    grouped_messages = messages.values("mailing_id", "status").annotate(
        message_count=Count("id")
    )
    mailings = get_mailings_stats(grouped_messages)

    table_mailings = [
        [
            "Mailing ID",
            "Scheduled",
            "Delivered",
            "Not Delivered",
            "Cancelled",
            "Total",
        ]
    ]
    for mailing_id in mailings:
        table_mailings.append(
            [
                str(mailing_id),
                str(mailings[mailing_id].get("SC", 0)),
                str(mailings[mailing_id].get("DL", 0)),
                str(mailings[mailing_id].get("ND", 0)),
                str(mailings[mailing_id].get("CA", 0)),
                str(sum(v for v in mailings[mailing_id].values())),
            ]
        )
    table_mailings.append(SEPARATING_LINE)
    table_mailings.append(
        [
            "Total",
            str(scheduled_messages),
            str(delivered_messages),
            str(undelivered_messages),
            str(cancelled_messages),
            str(total_messages),
        ]
    )

    formatted_date = yesterday.strftime("%d-%m-%Y")
    subject = f"Fbrq_API statictics for {formatted_date}"
    message = (
        f"{total_messages} messages was created {formatted_date}.\n\n"
        "Below are the statistics on the mailings\n\n"
        f'{tabulate(table_mailings, headers="firstrow", tablefmt="simple")}\n\n'
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=email_host_user,
        recipient_list=recipient_list,
    )
