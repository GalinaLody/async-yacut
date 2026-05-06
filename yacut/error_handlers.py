from http import HTTPStatus

from flask import Blueprint, jsonify, render_template


errors_bp = Blueprint('errors', __name__)


class InvalidAPIUsage(Exception):
    """Исключение для API-ошибок."""
    status_code = HTTPStatus.BAD_REQUEST

    def __init__(self, message, status_code=None):
        """Сохраняет текст ошибки и при необходимости переопределяет статус."""
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        """Преобразует сообщение об ошибке в словарь JSON."""
        return {'message': self.message}


@errors_bp.app_errorhandler(InvalidAPIUsage)
def invalid_api_usage(error):
    """Преобразует API-ошибку в JSON отввет."""
    return jsonify(error.to_dict()), error.status_code


@errors_bp.app_errorhandler(HTTPStatus.NOT_FOUND)
def page_not_found(error):
    """При ошибке 404 возвращает кастомную страницу ошибки."""
    return render_template('404.html'), HTTPStatus.NOT_FOUND
