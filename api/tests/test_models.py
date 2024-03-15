from datetime import datetime as dt

import pytest
import pytz
from freezegun import freeze_time


@pytest.mark.django_db
class TestMailingModelTest:
    def test_get_mailing_clients_with_filter(
        self,
        mailing_instance_one,
        client_instance_one,
        client_instance_two,
        client_instance_three,
    ):
        filtered_clients = mailing_instance_one.get_mailing_clients()
        assert filtered_clients.count() == 2
        assert client_instance_one in filtered_clients
        assert client_instance_two in filtered_clients
        assert client_instance_three not in filtered_clients

        mailing_instance_one.client_filter = "999"
        mailing_instance_one.save()
        filtered_clients = mailing_instance_one.get_mailing_clients()
        assert filtered_clients.count() == 2
        assert client_instance_one not in filtered_clients
        assert client_instance_two in filtered_clients
        assert client_instance_three in filtered_clients

        mailing_instance_one.client_filter = "999, Tag"
        mailing_instance_one.save()
        filtered_clients = mailing_instance_one.get_mailing_clients()
        assert filtered_clients.count() == 3
        assert client_instance_one in filtered_clients
        assert client_instance_two in filtered_clients
        assert client_instance_three in filtered_clients

        mailing_instance_one.client_filter = "Tag1"
        mailing_instance_one.save()
        filtered_clients = mailing_instance_one.get_mailing_clients()
        assert filtered_clients.count() == 1
        assert client_instance_one not in filtered_clients
        assert client_instance_two not in filtered_clients
        assert client_instance_three in filtered_clients

        mailing_instance_one.client_filter = "Tag2"
        mailing_instance_one.save()
        filtered_clients = mailing_instance_one.get_mailing_clients()
        assert filtered_clients.count() == 0

    def test_get_mailing_clients_without_filter(
        self,
        mailing_instance_one,
        client_instance_one,
        client_instance_two,
        client_instance_three,
    ):
        mailing_instance_one.client_filter = ""
        mailing_instance_one.save()
        filtered_clients = mailing_instance_one.get_mailing_clients()
        assert filtered_clients.count() == 3
        assert client_instance_one in filtered_clients
        assert client_instance_two in filtered_clients
        assert client_instance_three in filtered_clients

    def test_get_client_name(self, client_instance_one):
        assert str(client_instance_one) == "71234567890"

    def test_update_messages_info(
        self, mailing_instance_one, message_instance_one, message_instance_two
    ):
        mailing_instance_one.update_messages_info()
        assert mailing_instance_one.created_messages == 2
        assert mailing_instance_one.delivered_messages == 1
        assert mailing_instance_one.undelivered_messages == 0


@freeze_time("2024-01-01 00:00:00")
@pytest.mark.django_db
class TestClientModelTest:
    def test_get_local_time(self, client_instance_one):
        client_instance_one.time_zone = pytz.UTC
        assert (
            client_instance_one.get_local_time()
            == dt(2024, 1, 1, 0, 0, tzinfo=pytz.UTC).time()
        )
        client_instance_one.time_zone = pytz.timezone("Asia/Yekaterinburg")
        assert (
            client_instance_one.get_local_time()
            == dt(2024, 1, 1, 5, 0, tzinfo=pytz.UTC).time()
        )
