import logging

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Client, Mailing, Message

logger = logging.getLogger("api")


@receiver(post_save, sender=Message)
def update_messages_info_handler(
    sender, instance, update_fields, created, **kwargs
):
    if created or update_fields and "status" in update_fields:
        mailing = instance.mailing
        mailing.update_messages_info()


@receiver(post_save, sender=Mailing)
def mailing_create_or_update_handler(sender, instance, created, **kwargs):
    action = "created" if created else "updated"
    logger.info(
        f"{sender.__name__}_{instance.id} {action}. Attributes: {instance.__dict__}"
    )


@receiver(post_save, sender=Client)
def client_create_or_update_handler(sender, instance, created, **kwargs):
    action = "created" if created else "updated"
    logger.info(
        f"{sender.__name__}_{instance.id} {action}. Attributes: {instance.__dict__}"
    )


@receiver(post_save, sender=Message)
def message_create_or_update_handler(sender, instance, created, **kwargs):
    action = "created" if created else "updated"
    logger.info(
        f"{sender.__name__}_{instance.id} {action}. Attributes: {instance.__dict__}"
    )


@receiver(post_delete, sender=Mailing)
def mailing_delete_handler(sender, instance, **kwargs):
    logger.info(f"{sender.__name__}_{instance.id} deleted")


@receiver(post_delete, sender=Client)
def client_delete_handler(sender, instance, **kwargs):
    logger.info(f"{sender.__name__}_{instance.id} deleted")


@receiver(post_delete, sender=Message)
def message_delete_handler(sender, instance, **kwargs):
    logger.info(f"{sender.__name__}_{instance.id} deleted")
