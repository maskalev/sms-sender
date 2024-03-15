from datetime import datetime, timedelta

import pytest
import pytz

from api.forms import MailingAdminForm

utc = pytz.UTC


@pytest.mark.django_db
class TestMailingAdminForm:
    def test_clean_valid_data(self):
        form_data = {
            "datetime_start": utc.localize(datetime.now() + timedelta(days=1)),
            "datetime_end": utc.localize(datetime.now() + timedelta(days=2)),
            "text": "Test Mailing",
            "client_filter": "Tag",
            "clients_count": 0,
            "created_messages": 0,
            "cancelled_messages": 0,
            "scheduled_messages": 0,
            "delivered_messages": 0,
            "undelivered_messages": 0,
            "send_interval_time_start": datetime.time(
                datetime(2022, 1, 1, 9, 00)
            ),
            "send_interval_time_end": datetime.time(
                datetime(2022, 1, 1, 23, 59)
            ),
        }
        form = MailingAdminForm(data=form_data)
        assert form.is_valid(), form.errors
        assert form.cleaned_data == form_data

    def test_clean_invalid_data(self):
        form_data = {
            "datetime_start": utc.localize(datetime.now() + timedelta(days=1)),
            "datetime_end": utc.localize(datetime.now() - timedelta(days=2)),
            "text": "Test Mailing",
            "client_filter": "Tag",
            "created_messages": 0,
            "delivered_messages": 0,
            "undelivered_messages": 0,
        }
        form = MailingAdminForm(data=form_data)
        assert not form.is_valid(), form.errors
        assert (
            "Datetime end must be later than datetime start"
            in form.errors["datetime_end"]
        )

        form_data = {
            "datetime_start": utc.localize(datetime.now() - timedelta(days=2)),
            "datetime_end": utc.localize(datetime.now() - timedelta(days=1)),
            "text": "Test Mailing",
            "client_filter": "Tag",
            "created_messages": 0,
            "delivered_messages": 0,
            "undelivered_messages": 0,
        }
        form = MailingAdminForm(data=form_data)
        assert not form.is_valid(), form.errors
        assert (
            "Datetime end must be later than the current time"
            in form.errors["datetime_end"]
        )
