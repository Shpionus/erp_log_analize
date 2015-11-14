def format_datetime(date, fmt=None):
    if not fmt:
        fmt = "%Y-%m-%d %H:%M:%S"
    return date.strftime(fmt)


def last_date(dates):
    return max(dates)

jinia_filters = {
    'format_datetime': format_datetime,
    'last_date': last_date,
}