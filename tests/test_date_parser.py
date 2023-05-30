from datetime import datetime, date
import pytest
from utils.date_parser import parse_date


def test_parse_date():

    default_date = date.today()

    # Test when value is None
    assert parse_date(None, default_date) == default_date

    # Test when value is a date
    date_value = date(2022, 12, 31)
    assert parse_date(date_value, default_date) == date_value

    # Test when value is a datetime
    datetime_value = datetime(2022, 12, 31, 10, 30)
    assert parse_date(datetime_value, default_date) == date_value

    # Test when value is a string
    string_value = "2022-12-31"
    assert parse_date(string_value, default_date) == date_value

    # Test when value is a malformed string - should raise ValueError
    with pytest.raises(ValueError):
        parse_date("malformed", default_date)
