import logging
from datetime import datetime
from typing import Optional

from pycountry import countries

logger = logging.getLogger(__name__)


def convert_datetime_to_aws_format(datetime_obj: datetime) -> str:
    return f'{datetime_obj.strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:-4]}Z'


def get_current_datetime_aws_format() -> str:
    return convert_datetime_to_aws_format(datetime.now())


def convert_country_str_to_iso_code(country_string: str) -> Optional[str]:
    """
    Converts a country string to a 2-letter ISO 3166 Alpha-2 country code
    :param country_string: input country string. E.g. United States
    :return: 2 letter country code. E.g. US
    """
    # special handling for UK
    if country_string == 'UK':
        return 'GB'

    possible_country_matches = countries.search_fuzzy(country_string)
    if len(possible_country_matches) > 0:
        return possible_country_matches[0].alpha_2


def convert_date_string_to_datetime_string(date_string: str) -> Optional[str]:
    """
    Converts a date string to a datetime string. Date string can be in the format of YYYY-MM-DD, YYYY-MM, or YYYY.
    :param date_string: E.g. 2021-01-01, 2021-01, or 2021
    :return:
    """
    length = len(date_string)
    try:
        if length == 10:
            return convert_datetime_to_aws_format(datetime.strptime(date_string, "%Y-%m-%d"))
        if length == 7:
            return convert_datetime_to_aws_format(datetime.strptime(date_string, "%Y-%m"))
        if length == 4:
            return convert_datetime_to_aws_format(datetime.strptime(date_string, "%Y"))
        logger.warning(f'Invalid date string format: {date_string}')
    except ValueError as e:
        logger.warning(f'Unable to convert date string {date_string} to datetime string. Error: {e}')
        return None
