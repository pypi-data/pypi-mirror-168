import datetime
import re
from typing import Optional, Any, List, Union

from dateutil.parser import parse as dateutil_parse
from dateutil.tz import tzlocal, tzutc, UTC

# RFC3339: Date and Time on the Internet: Timestamps
#
# A string format for dates. A subset/profile of the ISO 8601 standard.
# examples:
#    2020-03-04T23:33:45.1234+01:00
#    2020-03-04T23:33:45.1234Z
#    2020-03-04T23:33:45Z
#
# See https://www.ietf.org/rfc/rfc3339.txt

RFC3339_PARSE_PATTERN_NOZULU = re.compile(
    r'([0-9][0-9][0-9][0-9])-([0-9][0-9])-([0-9][0-9])T([0-9][0-9]):([0-9][0-9]):([0-9][0-9])(.([0-9]+))?(([+-])([0-9][0-9]):00)')

RFC3339_PARSE_PATTERN_ZULU = re.compile(
    r'([0-9][0-9][0-9][0-9])-([0-9][0-9])-([0-9][0-9])T([0-9][0-9]):([0-9][0-9]):([0-9][0-9])(.([0-9]+))?Z')


def _fast_parse_rfc3339(text: str) -> Optional[datetime.datetime]:
    if (text.endswith('Z')):
        match = RFC3339_PARSE_PATTERN_ZULU.match(text)
        tzinfo = UTC
    else:
        match = RFC3339_PARSE_PATTERN_NOZULU.match(text)
        if match:
            assert match.group(10) in ('-', '+')
            sign = -1 if match.group(10) == '-' else 1
            tzhours = int(match.group(11))
            tzinfo = datetime.timezone(sign * datetime.timedelta(hours=tzhours, minutes=0))
        else:
            tzinfo = None
    if match:
        if match.group(7):
            msec_str = match.group(8)
            if len(msec_str) > 6:
                msec_str = msec_str[0:6]
            else:
                msec_str += '0' * (6 - len(msec_str))
            microsecond = int(msec_str)
        else:
            microsecond = 0
        return datetime.datetime(year=int(match.group(1)), month=int(match.group(2)), day=int(match.group(3)),
                          hour=int(match.group(4)), minute=int(match.group(5)), second=int(match.group(6)),
                          microsecond=microsecond,
                          tzinfo=tzinfo)
    else:
        return None


def parse_rfc3339(text: Optional[str], *, none_if_empty_tz=False) -> Optional[datetime.datetime]:
    """
    Parse an RFC3339 string representation of a time into a timezone aware datetime object
    Returns None if the provided string is None

    :param text: A string with an RFC3339 representation of a time
    :param none_if_empty_tz: If True, return None if the timezone in the string is empty. default: raise an error
    :return: A timezone aware datetime object, or None if the provided string is None
    """

    if text is None:
        return None
    # this is a lot faster than dateutil.parser.parse,
    # but might fail for some edge cases, or non-RFC3999 ISO8601 dates
    res = _fast_parse_rfc3339(text)
    if res is None:
        # This can handle more than just RFC3339 (full ISO 8601), but that's OK
        res = dateutil_parse(text)
    if res is not None and res.tzinfo is None:
        # enforce timezone aware (non-naive) datetime
        if none_if_empty_tz:
            return None
        else:
            raise ValueError('parsed date has no timezone: {!r}'.format(text))
    return res


def parse_rfc3339_no_none(text: str) -> datetime.datetime:
    """
    Parse an RFC3339 string representation of a time into a timezone aware datetime object
    Raises ValueError if the given string is None

    :param text: A string with an RFC3339 representation of a time
    :return: A timezone aware datetime object
    """
    res = parse_rfc3339(text)
    if res is None:
        raise ValueError('date parse error: {!r}'.format(text))
    return res


def dump_rfc3339(dt: Optional[datetime.datetime], zulu=True, no_milliseconds=True) -> str:
    """
    Convert the datetime object to an RFC3339 string representation of the time
    :param dt: The datetime to convert to string
    :param zulu: Force the timezone to "Zulu" (Z or UTC timezone)
    :param no_milliseconds: No sub second precision. This rounds the returned time down to the closest second.
    :return: An RFC3339 string representation of the provided datetime object, or None if the provided datetime is None.
    """
    if dt is None:
        return None
    assert isinstance(dt, datetime.datetime), 'not datetime.datetime but {}'.format(type(dt).__name__)
    if dt.tzinfo is None:
        raise ValueError('Naive datetimes are not supported. '
                         '(Because they can only cause trouble. Always use a timezone!)')
    assert dt.tzinfo is not None  # enforce timezone aware (non-naive) datetime
    if zulu:
        dt = dt.astimezone(tzutc())
    # else:
    #     dt = dt.astimezone(tzlocal())
    if no_milliseconds and dt.microsecond != 0:
        dt = dt.replace(microsecond=0)
    assert dt.tzinfo is not None  # enforce timezone aware (non-naive) datetime
    res = dt.isoformat()
    if res.endswith('+00:00'):
        res = res[:-6] + 'Z'
    return res


def datetime_now(zulu=False, no_milliseconds=True) -> datetime.datetime:
    """
    Get a timezone aware "now" time.

    :param zulu: force timezone to be "zulu" (Z or UTC timezone)
    :param no_milliseconds: No sub second precision. This rounds the returned time down to the closest second.
    :return: a timezone aware datetime object representing "now"
    """
    res = datetime.datetime.now(datetime.timezone.utc)
    if not zulu:
        res = res.astimezone(tzlocal())
    if no_milliseconds:
        res = res.replace(microsecond=0)
    assert res.tzinfo is not None  # enforce timezone aware (non-naive) datetime
    return res
