import string
import random

from .forms import RESERVED_WORD
from .models import URLMap


FORMAT_SHORT_ID = string.ascii_letters + string.digits
LENGTH_SHORT_ID = 6


def get_unique_short_id():
    """Генерирует уникалльный идентификатор для кароткой ссылки."""
    short_id = ''.join(random.choices(FORMAT_SHORT_ID, k=LENGTH_SHORT_ID))
    while URLMap.query.filter_by(
        short=short_id
    ).first() is not None or short_id == RESERVED_WORD:
        short_id = ''.join(random.choices(FORMAT_SHORT_ID, k=LENGTH_SHORT_ID))
    return short_id
