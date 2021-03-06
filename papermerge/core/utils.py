import logging
import re
from datetime import datetime

from django.utils.html import format_html
from django.urls import reverse

logger = logging.getLogger(__name__)


def date_2int(kv_format, str_value):
    # maps PAPERMERGE_METADATA_DATE_FORMATS to
    # https://docs.python.org/3.8/library/datetime.html#strftime-and-strptime-format-codes

    if not str_value:
        return 0

    format_map = {
        'dd.mm.yy': '%d.%m.%y',
        'dd.mm.yyyy': '%d.%m.%Y',
        'dd.M.yyyy': '%d.%B.%Y',
        'month': '%B'
    }
    try:
        _date_instance = datetime.strptime(
            str_value, format_map[kv_format]
        )
    except Exception as e:
        # this is expected because of automated
        # extraction of metadata may fail.
        logger.debug(
            f"While converting date user format {e}"
        )
        return 0

    return _date_instance.timestamp()


def money_2int(kv_format, str_value):
    return number_2int(kv_format, str_value)


def number_2int(kv_format, str_value):
    """
    kv_format for number is usually something like this:

        dddd
        d,ddd
        d.ddd

    So converting to an integer means just remove from string
    non-numeric characters and cast remaining str to integer.
    """
    if str_value:
        line = re.sub(r'[\,\.]', '', str_value)
        return line

    return 0


def node_tag(node):

    node_url = reverse("core:node", args=(node.id,))
    tag = format_html(
        "<a href='{}'>{}</a>",
        node_url,
        node.title
    )

    return tag