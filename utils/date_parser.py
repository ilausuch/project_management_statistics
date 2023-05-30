from datetime import datetime, date


def parse_date(value, default_value):
    if value is None:
        return default_value

    if isinstance(value, datetime):
        print("**")
        return value.date()

    if isinstance(value, date):
        return value

    return datetime.strptime(value, '%Y-%m-%d').date()
