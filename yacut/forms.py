from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms import SubmitField, URLField
from wtforms.validators import (
    DataRequired, Length,
    Optional, Regexp,
    URL, ValidationError
)

from .models import URLMap

PATTERN_SHORT_LINK = r'[a-zA-Z0-9]+'
USER_LENGTH_SHORT_LINK = 16
RESERVED_WORD = 'files'


class URLMapForm(FlaskForm):
    """Форма для создания короткокой ссылки."""
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле'), URL()]
    )
    custom_id = URLField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(
                max=USER_LENGTH_SHORT_LINK,
                message=(
                    f'Ссылка не может быть'
                    f'длинее {USER_LENGTH_SHORT_LINK} символов'
                )
            ),
            Optional(),
            Regexp(
                regex=PATTERN_SHORT_LINK,
                message=(
                    'Можно использовать только латинские буквы и цифры'
                ))
        ]
    )
    submit = SubmitField('Создать')

    def validate_custom_id(self, field):
        """Проверяет, что пользовательская коротка ссылка не повторяется
        в БД и, что для короткой ссылки не используется
        зарезирвированное слово."""
        if field.data is not None:
            if (URLMap.query.filter_by(short=field.data).first() is not None
                    or field.data == RESERVED_WORD):
                raise ValidationError(
                    'Предложенный вариант короткой ссылки уже существует.'
                )
        return field.data


class FilesForm(FlaskForm):
    """Форма для загрузки файлов."""
    files = MultipleFileField(
        validators=[
            DataRequired(message='Должен быть загружен минимум один файл')
        ]
    )
    submit = SubmitField('Загрузить')
