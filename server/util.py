import datetime


def date_to_ordinal(dt: datetime) -> int | None:
    """Given a DateTime or None value ``dt``, return either None of the ordinal value for that DateTime.  Used for preparing to serialise to JSON.

    Args:
        dt (DateTime): The DateTime object to be converted to its ordinal value.
    """
    if dt is None:
        return None
    elif isinstance(dt, datetime.datetime):
        return dt.toordinal()
    else:
        return "unknown"
