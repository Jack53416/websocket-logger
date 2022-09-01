import re
from datetime import datetime, timezone
from re import Match


def to_camel_case(snake_str: str) -> str:
    first, *others = snake_str.split('_')
    return ''.join([first.lower(), *map(str.title, others)])


def to_snake_case(camel_str: str) -> str:
    reg = r'(.+?)([A-Z])'

    def snake(match: Match):
        return f'{match.group(1).lower()}_{match.group(2).lower()}'

    return re.sub(reg, snake, camel_str, 0)


def convert_datetime_to_real_world(dt: datetime) -> str:
    return dt.replace(tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")
