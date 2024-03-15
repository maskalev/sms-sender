from datetime import datetime as dt

import pytest
import pytz
from django.conf import settings
from django.test import RequestFactory
from rest_framework.test import APIClient

from api.admin import MailingAdmin
from api.handlers.sso_handler import SSOHandler
from api.models import Client, Mailing, Message
from api.views import MailingViewSet

utc = pytz.UTC


@pytest.fixture
def mailing_instance_one():
    datetime_start = dt(2024, 1, 2, 12, 0, 0, tzinfo=pytz.UTC)
    datetime_end = dt(2024, 1, 2, 13, 0, 0, tzinfo=pytz.UTC)
    send_interval_time_start = dt.time(dt(2022, 1, 1, 9, 00))
    send_interval_time_end = dt.time(dt(2022, 1, 1, 21, 00))
    text = "Test Mailing"
    client_filter = "Tag"
    return Mailing.objects.create(
        datetime_start=datetime_start,
        datetime_end=datetime_end,
        send_interval_time_start=send_interval_time_start,
        send_interval_time_end=send_interval_time_end,
        text=text,
        client_filter=client_filter,
    )


@pytest.fixture
def mailing_instance_two():
    datetime_start = dt(2024, 1, 2, 12, 0, 0, tzinfo=pytz.UTC)
    datetime_end = dt(2024, 1, 2, 13, 0, 0, tzinfo=pytz.UTC)
    text = "Test Mailing"
    client_filter = "Tag1"
    return Mailing.objects.create(
        datetime_start=datetime_start,
        datetime_end=datetime_end,
        text=text,
        client_filter=client_filter,
    )


@pytest.fixture
def mailing_json_data():
    datetime_start = dt(2024, 1, 2, 12, 0, 0, tzinfo=pytz.UTC)
    datetime_end = dt(2024, 1, 2, 13, 0, 0, tzinfo=pytz.UTC)
    text = "Test Mailing"
    client_filter = "Tag"
    return {
        "datetime_start": datetime_start,
        "datetime_end": datetime_end,
        "text": text,
        "client_filter": client_filter,
    }


@pytest.fixture
def client_instance_one():
    phone = "71234567890"
    tag = "Tag"
    return Client.objects.create(phone=phone, tag=tag)


@pytest.fixture
def client_instance_two():
    phone = "79991234567"
    tag = "Tag"
    return Client.objects.create(phone=phone, tag=tag)


@pytest.fixture
def client_instance_three():
    phone = "79991234568"
    tag = "Tag1"
    return Client.objects.create(phone=phone, tag=tag)


@pytest.fixture
def message_instance_one(mailing_instance_one, client_instance_one):
    datetime_send = utc.localize(dt.now())
    status = Message.Status.SCHEDULED
    return Message.objects.create(
        datetime_send=datetime_send,
        status=status,
        mailing=mailing_instance_one,
        client=client_instance_one,
    )


@pytest.fixture
def message_instance_two(mailing_instance_one, client_instance_two):
    datetime_send = utc.localize(dt.now())
    status = Message.Status.DELIVERED
    return Message.objects.create(
        datetime_send=datetime_send,
        status=status,
        mailing=mailing_instance_one,
        client=client_instance_two,
    )


@pytest.fixture
def message_instance_three(mailing_instance_one, client_instance_one):
    datetime_send = utc.localize(dt.now())
    status = Message.Status.NOT_DELIVERED
    return Message.objects.create(
        datetime_send=datetime_send,
        status=status,
        mailing=mailing_instance_one,
        client=client_instance_one,
    )


@pytest.fixture
def message_instance_four(mailing_instance_one, client_instance_two):
    datetime_send = utc.localize(dt.now())
    status = Message.Status.CANCELLED
    return Message.objects.create(
        datetime_send=datetime_send,
        status=status,
        mailing=mailing_instance_one,
        client=client_instance_two,
    )


@pytest.fixture
def mailing_admin():
    return MailingAdmin(Mailing, None)


@pytest.fixture
def request_():
    return RequestFactory()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture(scope="session")
def celery_config():
    return {
        "broker_url": "pyamqp://guest:guest@localhost:5672//",
    }


@pytest.fixture
def celery_enable_logging():
    return True


@pytest.fixture
def mailing_view_set():
    return MailingViewSet()


@pytest.fixture
def sso_handler():
    return SSOHandler(
        auth0_client_id=settings.AUTH0_CLIENT_ID,
        auth0_client_secret=settings.AUTH0_CLIENT_SECRET,
        auth0_domain=settings.AUTH0_DOMAIN,
    )
