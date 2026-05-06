from http import HTTPStatus
import re

from flask import Blueprint, jsonify, request, url_for

from . import db
from .error_handlers import InvalidAPIUsage
from .forms import RESERVED_WORD, USER_LENGTH_SHORT_LINK, PATTERN_SHORT_LINK
from .models import URLMap
from .utils import get_unique_short_id


api_bp = Blueprint('api', __name__, url_prefix='/api/id')


def validate_custom_id(custom_id):
    """Проверяет переданную короткую ссылку на соответствие
    требованиям документации."""
    if (len(custom_id) > USER_LENGTH_SHORT_LINK
            or re.fullmatch(PATTERN_SHORT_LINK, custom_id) is None):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    if (URLMap.query.filter_by(short=custom_id).first() is not None
            or custom_id == RESERVED_WORD):
        raise InvalidAPIUsage(
            'Предложенный вариант короткой ссылки уже существует.'
        )


@api_bp.route('/', methods=['POST'])
def create_short_link():
    """Создает новую короткую ссылку."""
    data = request.get_json(silent=True)
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    elif 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    elif 'custom_id' in data and data['custom_id'] != '':
        validate_custom_id(data['custom_id'])
    else:
        data['custom_id'] = get_unique_short_id()
    url_map = URLMap()
    url_map.from_dict(data)
    db.session.add(url_map)
    db.session.commit()
    return jsonify({
        'url': url_map.original,
        'short_link': url_for(
            'views.redirect_to_original_link',
            short_id=url_map.short,
            _external=True
        )
    }), HTTPStatus.CREATED


@api_bp.route('/<string:short_id>/', methods=['GET'])
def get_url(short_id):
    """Получает оригинальную ссылку по указанному короткому идентификатору."""
    url_map = URLMap.query.filter_by(
        short=short_id
    ).first()
    if url_map is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original}), HTTPStatus.OK
