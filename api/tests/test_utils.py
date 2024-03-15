from datetime import datetime as dt

import pytest
import pytz
from freezegun import freeze_time

from api.utils import get_message_send_time


@freeze_time("2024-01-01 00:00:00")
@pytest.mark.django_db
class TestMailingDateTimeStartInFuture:
    def get_message_send_time_no_interval_time(
        self, mailing_instance_one, client_instance_one
    ):
        mailing_instance_one.datetime_start = dt(
            2024, 1, 2, 12, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.datetime_end = dt(
            2024, 1, 2, 20, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.send_interval_time_start = None
        mailing_instance_one.send_interval_time_end = None
        exp = dt(2024, 1, 2, 12, 0, tzinfo=pytz.UTC)
        res = get_message_send_time(mailing_instance_one, client_instance_one)
        assert res == exp, res

    def test_get_message_send_time_same_time_zone_start_before_end_1(
        self, mailing_instance_one, client_instance_one
    ):
        mailing_instance_one.datetime_start = dt(
            2024, 1, 2, 12, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.datetime_end = dt(
            2024, 1, 2, 20, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.send_interval_time_start = dt.time(
            dt(2022, 1, 1, 9, 00)
        )
        mailing_instance_one.send_interval_time_end = dt.time(
            dt(2022, 1, 1, 21, 00)
        )
        client_instance_one.time_zone = pytz.UTC
        exp = dt(2024, 1, 2, 12, 0, tzinfo=pytz.UTC)
        res = get_message_send_time(mailing_instance_one, client_instance_one)
        assert res == exp, res

    def test_get_message_send_time_same_time_zone_start_before_end_2(
        self, mailing_instance_one, client_instance_one
    ):
        mailing_instance_one.datetime_start = dt(
            2024, 1, 2, 23, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.datetime_end = dt(
            2024, 1, 3, 6, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.send_interval_time_start = dt.time(
            dt(2022, 1, 1, 9, 00)
        )
        mailing_instance_one.send_interval_time_end = dt.time(
            dt(2022, 1, 1, 21, 00)
        )
        client_instance_one.time_zone = pytz.UTC
        res = get_message_send_time(mailing_instance_one, client_instance_one)
        assert res is None, res

    def test_get_message_send_time_same_time_zone_start_before_end_3(
        self, mailing_instance_one, client_instance_one
    ):
        mailing_instance_one.datetime_start = dt(
            2024, 1, 2, 23, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.datetime_end = dt(
            2024, 1, 3, 11, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.send_interval_time_start = dt.time(
            dt(2022, 1, 1, 9, 00)
        )
        mailing_instance_one.send_interval_time_end = dt.time(
            dt(2022, 1, 1, 21, 00)
        )
        client_instance_one.time_zone = pytz.UTC
        exp = dt(2024, 1, 3, 9, 0, tzinfo=pytz.UTC)
        res = get_message_send_time(mailing_instance_one, client_instance_one)
        assert res == exp, res

    def test_get_message_send_time_same_time_zone_start_before_end_4(
        self, mailing_instance_one, client_instance_one
    ):
        mailing_instance_one.datetime_start = dt(
            2024, 1, 2, 6, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.datetime_end = dt(
            2024, 1, 2, 8, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.send_interval_time_start = dt.time(
            dt(2022, 1, 1, 9, 00)
        )
        mailing_instance_one.send_interval_time_end = dt.time(
            dt(2022, 1, 1, 21, 00)
        )
        client_instance_one.time_zone = pytz.UTC
        res = get_message_send_time(mailing_instance_one, client_instance_one)
        assert res is None, res

    def test_get_message_send_time_same_time_zone_start_before_end_5(
        self, mailing_instance_one, client_instance_one
    ):
        mailing_instance_one.datetime_start = dt(
            2024, 1, 2, 6, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.datetime_end = dt(
            2024, 1, 2, 14, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.send_interval_time_start = dt.time(
            dt(2022, 1, 1, 9, 00)
        )
        mailing_instance_one.send_interval_time_end = dt.time(
            dt(2022, 1, 1, 21, 00)
        )
        client_instance_one.time_zone = pytz.UTC
        exp = dt(2024, 1, 2, 9, 0, tzinfo=pytz.UTC)
        res = get_message_send_time(mailing_instance_one, client_instance_one)
        assert res == exp, res

    def test_get_message_send_time_same_time_zone_start_after_end_1(
        self, mailing_instance_one, client_instance_one
    ):
        mailing_instance_one.datetime_start = dt(
            2024, 1, 2, 11, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.datetime_end = dt(
            2024, 1, 2, 16, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.send_interval_time_start = dt.time(
            dt(2022, 1, 1, 21, 00)
        )
        mailing_instance_one.send_interval_time_end = dt.time(
            dt(2022, 1, 1, 9, 00)
        )
        client_instance_one.time_zone = pytz.UTC
        res = get_message_send_time(mailing_instance_one, client_instance_one)
        assert res is None, res

    def test_get_message_send_time_same_time_zone_start_after_end_2(
        self, mailing_instance_one, client_instance_one
    ):
        mailing_instance_one.datetime_start = dt(
            2024, 1, 2, 11, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.datetime_end = dt(
            2024, 1, 2, 23, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.send_interval_time_start = dt.time(
            dt(2022, 1, 1, 21, 00)
        )
        mailing_instance_one.send_interval_time_end = dt.time(
            dt(2022, 1, 1, 9, 00)
        )
        client_instance_one.time_zone = pytz.UTC
        exp = dt(2024, 1, 2, 21, 0, tzinfo=pytz.UTC)
        res = get_message_send_time(mailing_instance_one, client_instance_one)
        assert res == exp, res

    def test_get_message_send_time_same_time_zone_start_after_end_3(
        self, mailing_instance_one, client_instance_one
    ):
        mailing_instance_one.datetime_start = dt(
            2024, 1, 2, 23, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.datetime_end = dt(
            2024, 1, 3, 20, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.send_interval_time_start = dt.time(
            dt(2022, 1, 1, 21, 00)
        )
        mailing_instance_one.send_interval_time_end = dt.time(
            dt(2022, 1, 1, 9, 00)
        )
        client_instance_one.time_zone = pytz.UTC
        exp = dt(2024, 1, 2, 23, 0, tzinfo=pytz.UTC)
        res = get_message_send_time(mailing_instance_one, client_instance_one)
        assert res == exp, res

    def test_get_message_send_time_same_time_zone_start_after_end_4(
        self, mailing_instance_one, client_instance_one
    ):
        mailing_instance_one.datetime_start = dt(
            2024, 1, 2, 6, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.datetime_end = dt(
            2024, 1, 2, 11, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.send_interval_time_start = dt.time(
            dt(2022, 1, 1, 21, 00)
        )
        mailing_instance_one.send_interval_time_end = dt.time(
            dt(2022, 1, 1, 9, 00)
        )
        client_instance_one.time_zone = pytz.UTC
        exp = dt(2024, 1, 2, 6, 0, tzinfo=pytz.UTC)
        res = get_message_send_time(mailing_instance_one, client_instance_one)
        assert res == exp, res

    def test_get_message_send_time_diff_time_zone_start_before_end_1(
        self, mailing_instance_one, client_instance_one
    ):
        mailing_instance_one.datetime_start = dt(
            2024, 1, 2, 7, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.datetime_end = dt(
            2024, 1, 2, 15, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.send_interval_time_start = dt.time(
            dt(2022, 1, 1, 9, 00)
        )
        mailing_instance_one.send_interval_time_end = dt.time(
            dt(2022, 1, 1, 21, 00)
        )
        client_instance_one.time_zone = pytz.timezone("Asia/Yekaterinburg")
        exp = dt(2024, 1, 2, 7, 0, tzinfo=pytz.UTC)
        res = get_message_send_time(mailing_instance_one, client_instance_one)
        assert res == exp, res

    def test_get_message_send_time_diff_time_zone_start_before_end_2(
        self, mailing_instance_one, client_instance_one
    ):
        mailing_instance_one.datetime_start = dt(
            2024, 1, 2, 18, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.datetime_end = dt(
            2024, 1, 3, 1, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.send_interval_time_start = dt.time(
            dt(2022, 1, 1, 9, 00)
        )
        mailing_instance_one.send_interval_time_end = dt.time(
            dt(2022, 1, 1, 21, 00)
        )
        client_instance_one.time_zone = pytz.timezone("Asia/Yekaterinburg")
        res = get_message_send_time(mailing_instance_one, client_instance_one)
        assert res is None, res

    def test_get_message_send_time_diff_time_zone_start_before_end_3(
        self, mailing_instance_one, client_instance_one
    ):
        mailing_instance_one.datetime_start = dt(
            2024, 1, 2, 18, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.datetime_end = dt(
            2024, 1, 3, 6, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.send_interval_time_start = dt.time(
            dt(2022, 1, 1, 9, 00)
        )
        mailing_instance_one.send_interval_time_end = dt.time(
            dt(2022, 1, 1, 21, 00)
        )
        client_instance_one.time_zone = pytz.timezone("Asia/Yekaterinburg")
        exp = dt(2024, 1, 3, 4, 0, tzinfo=pytz.UTC)
        res = get_message_send_time(mailing_instance_one, client_instance_one)
        assert res == exp, res

    def test_get_message_send_time_diff_time_zone_start_before_end_4(
        self, mailing_instance_one, client_instance_one
    ):
        mailing_instance_one.datetime_start = dt(
            2024, 1, 2, 1, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.datetime_end = dt(
            2024, 1, 2, 3, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.send_interval_time_start = dt.time(
            dt(2022, 1, 1, 9, 00)
        )
        mailing_instance_one.send_interval_time_end = dt.time(
            dt(2022, 1, 1, 21, 00)
        )
        client_instance_one.time_zone = pytz.timezone("Asia/Yekaterinburg")
        res = get_message_send_time(mailing_instance_one, client_instance_one)
        assert res is None, res

    def test_get_message_send_time_diff_time_zone_start_before_end_5(
        self, mailing_instance_one, client_instance_one
    ):
        mailing_instance_one.datetime_start = dt(
            2024, 1, 2, 1, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.datetime_end = dt(
            2024, 1, 2, 9, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.send_interval_time_start = dt.time(
            dt(2022, 1, 1, 9, 00)
        )
        mailing_instance_one.send_interval_time_end = dt.time(
            dt(2022, 1, 1, 21, 00)
        )
        client_instance_one.time_zone = pytz.timezone("Asia/Yekaterinburg")
        exp = dt(2024, 1, 2, 4, 0, tzinfo=pytz.UTC)
        res = get_message_send_time(mailing_instance_one, client_instance_one)
        assert res == exp, res

    def test_get_message_send_time_diff_time_zone_start_after_end_1(
        self, mailing_instance_one, client_instance_one
    ):
        mailing_instance_one.datetime_start = dt(
            2024, 1, 2, 6, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.datetime_end = dt(
            2024, 1, 2, 11, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.send_interval_time_start = dt.time(
            dt(2022, 1, 1, 21, 00)
        )
        mailing_instance_one.send_interval_time_end = dt.time(
            dt(2022, 1, 1, 9, 00)
        )
        client_instance_one.time_zone = pytz.timezone("Asia/Yekaterinburg")
        res = get_message_send_time(mailing_instance_one, client_instance_one)
        assert res is None, res

    def test_get_message_send_time_diff_time_zone_start_after_end_2(
        self, mailing_instance_one, client_instance_one
    ):
        mailing_instance_one.datetime_start = dt(
            2024, 1, 2, 6, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.datetime_end = dt(
            2024, 1, 2, 18, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.send_interval_time_start = dt.time(
            dt(2022, 1, 1, 21, 00)
        )
        mailing_instance_one.send_interval_time_end = dt.time(
            dt(2022, 1, 1, 9, 00)
        )
        client_instance_one.time_zone = pytz.timezone("Asia/Yekaterinburg")
        exp = dt(2024, 1, 2, 16, 0, tzinfo=pytz.UTC)
        res = get_message_send_time(mailing_instance_one, client_instance_one)
        assert res == exp, res

    def test_get_message_send_time_diff_time_zone_start_after_end_3(
        self, mailing_instance_one, client_instance_one
    ):
        mailing_instance_one.datetime_start = dt(
            2024, 1, 2, 18, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.datetime_end = dt(
            2024, 1, 3, 15, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.send_interval_time_start = dt.time(
            dt(2022, 1, 1, 21, 00)
        )
        mailing_instance_one.send_interval_time_end = dt.time(
            dt(2022, 1, 1, 9, 00)
        )
        client_instance_one.time_zone = pytz.timezone("Asia/Yekaterinburg")
        exp = dt(2024, 1, 2, 18, 0, tzinfo=pytz.UTC)
        res = get_message_send_time(mailing_instance_one, client_instance_one)
        assert res == exp, res

    def test_get_message_send_time_diff_time_zone_start_after_end_4(
        self, mailing_instance_one, client_instance_one
    ):
        mailing_instance_one.datetime_start = dt(
            2024, 1, 2, 1, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.datetime_end = dt(
            2024, 1, 2, 6, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.send_interval_time_start = dt.time(
            dt(2022, 1, 1, 21, 00)
        )
        mailing_instance_one.send_interval_time_end = dt.time(
            dt(2022, 1, 1, 9, 00)
        )
        client_instance_one.time_zone = pytz.timezone("Asia/Yekaterinburg")
        exp = dt(2024, 1, 2, 1, 0, tzinfo=pytz.UTC)
        res = get_message_send_time(mailing_instance_one, client_instance_one)
        assert res == exp, res


@pytest.mark.django_db
class TestMailingDateTimeStartInPast:
    @freeze_time("2024-01-02 15:00:00")
    def get_message_send_time_no_interval_time(
        self, mailing_instance_one, client_instance_one
    ):
        mailing_instance_one.datetime_start = dt(
            2024, 1, 2, 12, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.datetime_end = dt(
            2024, 1, 2, 20, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.send_interval_time_start = None
        mailing_instance_one.send_interval_time_end = None
        exp = dt(2024, 1, 2, 15, 0, tzinfo=pytz.UTC)
        res = get_message_send_time(mailing_instance_one, client_instance_one)
        assert res == exp, res

    @freeze_time("2024-01-02 15:00:00")
    def test_get_message_send_time_same_time_zone_start_before_end_1(
        self, mailing_instance_one, client_instance_one
    ):
        mailing_instance_one.datetime_start = dt(
            2024, 1, 2, 12, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.datetime_end = dt(
            2024, 1, 2, 20, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.send_interval_time_start = dt.time(
            dt(2022, 1, 1, 9, 00)
        )
        mailing_instance_one.send_interval_time_end = dt.time(
            dt(2022, 1, 1, 21, 00)
        )
        client_instance_one.time_zone = pytz.UTC
        exp = dt(2024, 1, 2, 15, 0, tzinfo=pytz.UTC)
        res = get_message_send_time(mailing_instance_one, client_instance_one)
        assert res == exp, res

    @freeze_time("2024-01-03 02:00:00")
    def test_get_message_send_time_same_time_zone_start_before_end_2(
        self, mailing_instance_one, client_instance_one
    ):
        mailing_instance_one.datetime_start = dt(
            2024, 1, 2, 23, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.datetime_end = dt(
            2024, 1, 3, 6, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.send_interval_time_start = dt.time(
            dt(2022, 1, 1, 9, 00)
        )
        mailing_instance_one.send_interval_time_end = dt.time(
            dt(2022, 1, 1, 21, 00)
        )
        client_instance_one.time_zone = pytz.UTC
        res = get_message_send_time(mailing_instance_one, client_instance_one)
        assert res is None, res

    @freeze_time("2024-01-03 8:00:00")
    def test_get_message_send_time_same_time_zone_start_before_end_3(
        self, mailing_instance_one, client_instance_one
    ):
        mailing_instance_one.datetime_start = dt(
            2024, 1, 2, 23, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.datetime_end = dt(
            2024, 1, 3, 11, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.send_interval_time_start = dt.time(
            dt(2022, 1, 1, 9, 00)
        )
        mailing_instance_one.send_interval_time_end = dt.time(
            dt(2022, 1, 1, 21, 00)
        )
        client_instance_one.time_zone = pytz.UTC
        exp = dt(2024, 1, 3, 9, 0, tzinfo=pytz.UTC)
        res = get_message_send_time(mailing_instance_one, client_instance_one)
        assert res == exp, res

    @freeze_time("2024-01-03 10:00:00")
    def test_get_message_send_time_same_time_zone_start_before_end_4(
        self, mailing_instance_one, client_instance_one
    ):
        mailing_instance_one.datetime_start = dt(
            2024, 1, 2, 23, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.datetime_end = dt(
            2024, 1, 3, 11, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.send_interval_time_start = dt.time(
            dt(2022, 1, 1, 9, 00)
        )
        mailing_instance_one.send_interval_time_end = dt.time(
            dt(2022, 1, 1, 21, 00)
        )
        client_instance_one.time_zone = pytz.UTC
        exp = dt(2024, 1, 3, 10, 0, tzinfo=pytz.UTC)
        res = get_message_send_time(mailing_instance_one, client_instance_one)
        assert res == exp, res

    @freeze_time("2024-01-02 07:00:00")
    def test_get_message_send_time_same_time_zone_start_before_end_5(
        self, mailing_instance_one, client_instance_one
    ):
        mailing_instance_one.datetime_start = dt(
            2024, 1, 2, 6, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.datetime_end = dt(
            2024, 1, 2, 8, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.send_interval_time_start = dt.time(
            dt(2022, 1, 1, 9, 00)
        )
        mailing_instance_one.send_interval_time_end = dt.time(
            dt(2022, 1, 1, 21, 00)
        )
        client_instance_one.time_zone = pytz.UTC
        res = get_message_send_time(mailing_instance_one, client_instance_one)
        assert res is None, res

    @freeze_time("2024-01-02 07:00:00")
    def test_get_message_send_time_same_time_zone_start_before_end_6(
        self, mailing_instance_one, client_instance_one
    ):
        mailing_instance_one.datetime_start = dt(
            2024, 1, 2, 6, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.datetime_end = dt(
            2024, 1, 2, 14, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.send_interval_time_start = dt.time(
            dt(2022, 1, 1, 9, 00)
        )
        mailing_instance_one.send_interval_time_end = dt.time(
            dt(2022, 1, 1, 21, 00)
        )
        client_instance_one.time_zone = pytz.UTC
        exp = dt(2024, 1, 2, 9, 0, tzinfo=pytz.UTC)
        res = get_message_send_time(mailing_instance_one, client_instance_one)
        assert res == exp, res

    @freeze_time("2024-01-02 10:00:00")
    def test_get_message_send_time_same_time_zone_start_before_end_7(
        self, mailing_instance_one, client_instance_one
    ):
        mailing_instance_one.datetime_start = dt(
            2024, 1, 2, 6, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.datetime_end = dt(
            2024, 1, 2, 14, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.send_interval_time_start = dt.time(
            dt(2022, 1, 1, 9, 00)
        )
        mailing_instance_one.send_interval_time_end = dt.time(
            dt(2022, 1, 1, 21, 00)
        )
        client_instance_one.time_zone = pytz.UTC
        exp = dt(2024, 1, 2, 10, 0, tzinfo=pytz.UTC)
        res = get_message_send_time(mailing_instance_one, client_instance_one)
        assert res == exp, res

    @freeze_time("2024-01-02 12:00:00")
    def test_get_message_send_time_same_time_zone_start_after_end_1(
        self, mailing_instance_one, client_instance_one
    ):
        mailing_instance_one.datetime_start = dt(
            2024, 1, 2, 11, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.datetime_end = dt(
            2024, 1, 2, 16, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.send_interval_time_start = dt.time(
            dt(2022, 1, 1, 21, 00)
        )
        mailing_instance_one.send_interval_time_end = dt.time(
            dt(2022, 1, 1, 9, 00)
        )
        client_instance_one.time_zone = pytz.UTC
        res = get_message_send_time(mailing_instance_one, client_instance_one)
        assert res is None, res

    @freeze_time("2024-01-02 13:00:00")
    def test_get_message_send_time_same_time_zone_start_after_end_2(
        self, mailing_instance_one, client_instance_one
    ):
        mailing_instance_one.datetime_start = dt(
            2024, 1, 2, 11, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.datetime_end = dt(
            2024, 1, 2, 23, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.send_interval_time_start = dt.time(
            dt(2022, 1, 1, 21, 00)
        )
        mailing_instance_one.send_interval_time_end = dt.time(
            dt(2022, 1, 1, 9, 00)
        )
        client_instance_one.time_zone = pytz.UTC
        exp = dt(2024, 1, 2, 21, 0, tzinfo=pytz.UTC)
        res = get_message_send_time(mailing_instance_one, client_instance_one)
        assert res == exp, res

    @freeze_time("2024-01-02 22:00:00")
    def test_get_message_send_time_same_time_zone_start_after_end_3(
        self, mailing_instance_one, client_instance_one
    ):
        mailing_instance_one.datetime_start = dt(
            2024, 1, 2, 11, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.datetime_end = dt(
            2024, 1, 2, 23, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.send_interval_time_start = dt.time(
            dt(2022, 1, 1, 21, 00)
        )
        mailing_instance_one.send_interval_time_end = dt.time(
            dt(2022, 1, 1, 9, 00)
        )
        client_instance_one.time_zone = pytz.UTC
        exp = dt(2024, 1, 2, 22, 0, tzinfo=pytz.UTC)
        res = get_message_send_time(mailing_instance_one, client_instance_one)
        assert res == exp, res

    @freeze_time("2024-01-03 02:00:00")
    def test_get_message_send_time_same_time_zone_start_after_end_4(
        self, mailing_instance_one, client_instance_one
    ):
        mailing_instance_one.datetime_start = dt(
            2024, 1, 2, 23, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.datetime_end = dt(
            2024, 1, 3, 20, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.send_interval_time_start = dt.time(
            dt(2022, 1, 1, 21, 00)
        )
        mailing_instance_one.send_interval_time_end = dt.time(
            dt(2022, 1, 1, 9, 00)
        )
        client_instance_one.time_zone = pytz.UTC
        exp = dt(2024, 1, 3, 2, 0, tzinfo=pytz.UTC)
        res = get_message_send_time(mailing_instance_one, client_instance_one)
        assert res == exp, res

    @freeze_time("2024-01-03 10:00:00")
    def test_get_message_send_time_same_time_zone_start_after_end_5(
        self, mailing_instance_one, client_instance_one
    ):
        mailing_instance_one.datetime_start = dt(
            2024, 1, 2, 23, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.datetime_end = dt(
            2024, 1, 3, 20, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.send_interval_time_start = dt.time(
            dt(2022, 1, 1, 21, 00)
        )
        mailing_instance_one.send_interval_time_end = dt.time(
            dt(2022, 1, 1, 9, 00)
        )
        client_instance_one.time_zone = pytz.UTC
        res = get_message_send_time(mailing_instance_one, client_instance_one)
        assert res is None, res

    @freeze_time("2024-01-02 07:00:00")
    def test_get_message_send_time_same_time_zone_start_after_end_6(
        self, mailing_instance_one, client_instance_one
    ):
        mailing_instance_one.datetime_start = dt(
            2024, 1, 2, 6, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.datetime_end = dt(
            2024, 1, 2, 11, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.send_interval_time_start = dt.time(
            dt(2022, 1, 1, 21, 00)
        )
        mailing_instance_one.send_interval_time_end = dt.time(
            dt(2022, 1, 1, 9, 00)
        )
        client_instance_one.time_zone = pytz.UTC
        exp = dt(2024, 1, 2, 7, 0, tzinfo=pytz.UTC)
        res = get_message_send_time(mailing_instance_one, client_instance_one)
        assert res == exp, res

    @freeze_time("2024-01-02 10:00:00")
    def test_get_message_send_time_same_time_zone_start_after_end_7(
        self, mailing_instance_one, client_instance_one
    ):
        mailing_instance_one.datetime_start = dt(
            2024, 1, 2, 6, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.datetime_end = dt(
            2024, 1, 2, 11, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.send_interval_time_start = dt.time(
            dt(2022, 1, 1, 21, 00)
        )
        mailing_instance_one.send_interval_time_end = dt.time(
            dt(2022, 1, 1, 9, 00)
        )
        client_instance_one.time_zone = pytz.timezone("Asia/Yekaterinburg")
        res = get_message_send_time(mailing_instance_one, client_instance_one)
        assert res is None, res

    @freeze_time("2024-01-02 10:00:00")
    def test_get_message_send_time_diff_time_zone_start_before_end_1(
        self, mailing_instance_one, client_instance_one
    ):
        mailing_instance_one.datetime_start = dt(
            2024, 1, 2, 7, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.datetime_end = dt(
            2024, 1, 2, 15, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.send_interval_time_start = dt.time(
            dt(2022, 1, 1, 9, 00)
        )
        mailing_instance_one.send_interval_time_end = dt.time(
            dt(2022, 1, 1, 21, 00)
        )
        client_instance_one.time_zone = pytz.timezone("Asia/Yekaterinburg")
        exp = dt(2024, 1, 2, 10, 0, tzinfo=pytz.UTC)
        res = get_message_send_time(mailing_instance_one, client_instance_one)
        assert res == exp, res

    @freeze_time("2024-01-02 21:00:00")
    def test_get_message_send_time_diff_time_zone_start_before_end_2(
        self, mailing_instance_one, client_instance_one
    ):
        mailing_instance_one.datetime_start = dt(
            2024, 1, 2, 18, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.datetime_end = dt(
            2024, 1, 3, 1, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.send_interval_time_start = dt.time(
            dt(2022, 1, 1, 9, 00)
        )
        mailing_instance_one.send_interval_time_end = dt.time(
            dt(2022, 1, 1, 21, 00)
        )
        client_instance_one.time_zone = pytz.timezone("Asia/Yekaterinburg")
        res = get_message_send_time(mailing_instance_one, client_instance_one)
        assert res is None, res

    @freeze_time("2024-01-03 3:00:00")
    def test_get_message_send_time_diff_time_zone_start_before_end_3(
        self, mailing_instance_one, client_instance_one
    ):
        mailing_instance_one.datetime_start = dt(
            2024, 1, 2, 18, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.datetime_end = dt(
            2024, 1, 3, 6, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.send_interval_time_start = dt.time(
            dt(2022, 1, 1, 9, 00)
        )
        mailing_instance_one.send_interval_time_end = dt.time(
            dt(2022, 1, 1, 21, 00)
        )
        client_instance_one.time_zone = pytz.timezone("Asia/Yekaterinburg")
        exp = dt(2024, 1, 3, 4, 0, tzinfo=pytz.UTC)
        res = get_message_send_time(mailing_instance_one, client_instance_one)
        assert res == exp, res

    @freeze_time("2024-01-03 05:00:00")
    def test_get_message_send_time_diff_time_zone_start_before_end_4(
        self, mailing_instance_one, client_instance_one
    ):
        mailing_instance_one.datetime_start = dt(
            2024, 1, 2, 18, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.datetime_end = dt(
            2024, 1, 3, 6, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.send_interval_time_start = dt.time(
            dt(2022, 1, 1, 9, 00)
        )
        mailing_instance_one.send_interval_time_end = dt.time(
            dt(2022, 1, 1, 21, 00)
        )
        client_instance_one.time_zone = pytz.timezone("Asia/Yekaterinburg")
        exp = dt(2024, 1, 3, 5, 0, tzinfo=pytz.UTC)
        res = get_message_send_time(mailing_instance_one, client_instance_one)
        assert res == exp, res

    @freeze_time("2024-01-02 02:00:00")
    def test_get_message_send_time_diff_time_zone_start_before_end_5(
        self, mailing_instance_one, client_instance_one
    ):
        mailing_instance_one.datetime_start = dt(
            2024, 1, 2, 1, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.datetime_end = dt(
            2024, 1, 2, 3, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.send_interval_time_start = dt.time(
            dt(2022, 1, 1, 9, 00)
        )
        mailing_instance_one.send_interval_time_end = dt.time(
            dt(2022, 1, 1, 21, 00)
        )
        client_instance_one.time_zone = pytz.timezone("Asia/Yekaterinburg")
        res = get_message_send_time(mailing_instance_one, client_instance_one)
        assert res is None, res

    @freeze_time("2024-01-02 02:00:00")
    def test_get_message_send_time_diff_time_zone_start_before_end_6(
        self, mailing_instance_one, client_instance_one
    ):
        mailing_instance_one.datetime_start = dt(
            2024, 1, 2, 1, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.datetime_end = dt(
            2024, 1, 2, 9, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.send_interval_time_start = dt.time(
            dt(2022, 1, 1, 9, 00)
        )
        mailing_instance_one.send_interval_time_end = dt.time(
            dt(2022, 1, 1, 21, 00)
        )
        client_instance_one.time_zone = pytz.timezone("Asia/Yekaterinburg")
        exp = dt(2024, 1, 2, 4, 0, tzinfo=pytz.UTC)
        res = get_message_send_time(mailing_instance_one, client_instance_one)
        assert res == exp, res

    @freeze_time("2024-01-02 05:00:00")
    def test_get_message_send_time_diff_time_zone_start_before_end_7(
        self, mailing_instance_one, client_instance_one
    ):
        mailing_instance_one.datetime_start = dt(
            2024, 1, 2, 1, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.datetime_end = dt(
            2024, 1, 2, 9, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.send_interval_time_start = dt.time(
            dt(2022, 1, 1, 9, 00)
        )
        mailing_instance_one.send_interval_time_end = dt.time(
            dt(2022, 1, 1, 21, 00)
        )
        client_instance_one.time_zone = pytz.timezone("Asia/Yekaterinburg")
        exp = dt(2024, 1, 2, 5, 0, tzinfo=pytz.UTC)
        res = get_message_send_time(mailing_instance_one, client_instance_one)
        assert res == exp, res

    @freeze_time("2024-01-02 07:00:00")
    def test_get_message_send_time_diff_time_zone_start_after_end_1(
        self, mailing_instance_one, client_instance_one
    ):
        mailing_instance_one.datetime_start = dt(
            2024, 1, 2, 6, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.datetime_end = dt(
            2024, 1, 2, 11, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.send_interval_time_start = dt.time(
            dt(2022, 1, 1, 21, 00)
        )
        mailing_instance_one.send_interval_time_end = dt.time(
            dt(2022, 1, 1, 9, 00)
        )
        client_instance_one.time_zone = pytz.timezone("Asia/Yekaterinburg")
        res = get_message_send_time(mailing_instance_one, client_instance_one)
        assert res is None, res

    @freeze_time("2024-01-02 08:00:00")
    def test_get_message_send_time_diff_time_zone_start_after_end_2(
        self, mailing_instance_one, client_instance_one
    ):
        mailing_instance_one.datetime_start = dt(
            2024, 1, 2, 6, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.datetime_end = dt(
            2024, 1, 2, 18, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.send_interval_time_start = dt.time(
            dt(2022, 1, 1, 21, 00)
        )
        mailing_instance_one.send_interval_time_end = dt.time(
            dt(2022, 1, 1, 9, 00)
        )
        client_instance_one.time_zone = pytz.timezone("Asia/Yekaterinburg")
        exp = dt(2024, 1, 2, 16, 0, tzinfo=pytz.UTC)
        res = get_message_send_time(mailing_instance_one, client_instance_one)
        assert res == exp, res

    @freeze_time("2024-01-02 17:00:00")
    def test_get_message_send_time_diff_time_zone_start_after_end_3(
        self, mailing_instance_one, client_instance_one
    ):
        mailing_instance_one.datetime_start = dt(
            2024, 1, 2, 6, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.datetime_end = dt(
            2024, 1, 2, 18, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.send_interval_time_start = dt.time(
            dt(2022, 1, 1, 21, 00)
        )
        mailing_instance_one.send_interval_time_end = dt.time(
            dt(2022, 1, 1, 9, 00)
        )
        client_instance_one.time_zone = pytz.timezone("Asia/Yekaterinburg")
        exp = dt(2024, 1, 2, 17, 0, tzinfo=pytz.UTC)
        res = get_message_send_time(mailing_instance_one, client_instance_one)
        assert res == exp, res

    @freeze_time("2024-01-02 21:00:00")
    def test_get_message_send_time_diff_time_zone_start_after_end_4(
        self, mailing_instance_one, client_instance_one
    ):
        mailing_instance_one.datetime_start = dt(
            2024, 1, 2, 18, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.datetime_end = dt(
            2024, 1, 3, 15, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.send_interval_time_start = dt.time(
            dt(2022, 1, 1, 21, 00)
        )
        mailing_instance_one.send_interval_time_end = dt.time(
            dt(2022, 1, 1, 9, 00)
        )
        client_instance_one.time_zone = pytz.timezone("Asia/Yekaterinburg")
        exp = dt(2024, 1, 2, 21, 0, tzinfo=pytz.UTC)
        res = get_message_send_time(mailing_instance_one, client_instance_one)
        assert res == exp, res

    @freeze_time("2024-01-03 05:00:00")
    def test_get_message_send_time_diff_time_zone_start_after_end_5(
        self, mailing_instance_one, client_instance_one
    ):
        mailing_instance_one.datetime_start = dt(
            2024, 1, 2, 18, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.datetime_end = dt(
            2024, 1, 3, 15, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.send_interval_time_start = dt.time(
            dt(2022, 1, 1, 21, 00)
        )
        mailing_instance_one.send_interval_time_end = dt.time(
            dt(2022, 1, 1, 9, 00)
        )
        client_instance_one.time_zone = pytz.timezone("Asia/Yekaterinburg")
        res = get_message_send_time(mailing_instance_one, client_instance_one)
        assert res is None, res

    @freeze_time("2024-01-02 02:00:00")
    def test_get_message_send_time_diff_time_zone_start_after_end_6(
        self, mailing_instance_one, client_instance_one
    ):
        mailing_instance_one.datetime_start = dt(
            2024, 1, 2, 1, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.datetime_end = dt(
            2024, 1, 2, 6, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.send_interval_time_start = dt.time(
            dt(2022, 1, 1, 21, 00)
        )
        mailing_instance_one.send_interval_time_end = dt.time(
            dt(2022, 1, 1, 9, 00)
        )
        client_instance_one.time_zone = pytz.timezone("Asia/Yekaterinburg")
        exp = dt(2024, 1, 2, 2, 0, tzinfo=pytz.UTC)
        res = get_message_send_time(mailing_instance_one, client_instance_one)
        assert res == exp, res

    @freeze_time("2024-01-02 05:00:00")
    def test_get_message_send_time_diff_time_zone_start_after_end_7(
        self, mailing_instance_one, client_instance_one
    ):
        mailing_instance_one.datetime_start = dt(
            2024, 1, 2, 1, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.datetime_end = dt(
            2024, 1, 2, 6, 0, 0, tzinfo=pytz.UTC
        )
        mailing_instance_one.send_interval_time_start = dt.time(
            dt(2022, 1, 1, 21, 00)
        )
        mailing_instance_one.send_interval_time_end = dt.time(
            dt(2022, 1, 1, 9, 00)
        )
        client_instance_one.time_zone = pytz.timezone("Asia/Yekaterinburg")
        res = get_message_send_time(mailing_instance_one, client_instance_one)
        assert res is None, res
