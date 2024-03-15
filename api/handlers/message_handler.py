import functools

from django.db import transaction

from api.models import Mailing
from api.tasks import TaskManager
from api.utils import get_mailing_messages

task_manager = TaskManager()


class MessageHandler:
    @transaction.atomic
    @staticmethod
    def create_messages(self, instance_id):
        mailing = Mailing.objects.get(id=instance_id)
        messages = get_mailing_messages(mailing, created=True)
        for message in messages:
            transaction.on_commit(
                functools.partial(
                    task_manager.create_message_celery_task,
                    message=message,
                )
            )

    @transaction.atomic
    @staticmethod
    def update_messages(self, instance):
        messages = get_mailing_messages(instance)
        for message in messages:
            transaction.on_commit(
                functools.partial(
                    task_manager.update_message_celery_task,
                    message=message,
                )
            )

    @transaction.atomic
    @staticmethod
    def delete_messages(self, instance):
        messages = get_mailing_messages(instance)
        for message in messages:
            transaction.on_commit(
                functools.partial(
                    task_manager.delete_message_celery_task,
                    message=message,
                )
            )
