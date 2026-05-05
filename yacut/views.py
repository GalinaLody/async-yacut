from flask import Blueprint, redirect, render_template, url_for

from . import db
from .forms import FilesForm, URLMapForm
from .models import URLMap
from .utils import get_unique_short_id
from .yandexdisk import async_upload_files_to_yadisk

views_bp = Blueprint('views', __name__)


@views_bp.route('/', methods=['GET', 'POST'])
def index_view():
    """Главная страница. Создает короткие ссылки для пользователя."""
    form = URLMapForm()
    if form.validate_on_submit():
        short_id = form.custom_id.data
        if not short_id:
            short_id = get_unique_short_id()
        url_map = URLMap(
            original=form.original_link.data,
            short=short_id,
        )
        db.session.add(url_map)
        db.session.commit()
        short_link = url_for(
            'views.redirect_to_original_link',
            short_id=short_id,
            _external=True
        )
        return render_template('index.html', form=form, short_link=short_link)
    return render_template('index.html', form=form)


@views_bp.route('/<string:short_id>')
def redirect_to_original_link(short_id):
    """Перенаправляет с короткой ссылки на оригинальную сслыку."""
    url_map = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(url_map.original)


@views_bp.route('/files', methods=['GET', 'POST'])
async def files_view():
    """Страница загрузки файлов.
    Загружает файлы на ЯДиск и предоставляет коротокую ссылку
    для их скачивания."""
    form = FilesForm()
    upload_files_links = []
    if form.validate_on_submit():
        filenames_links = await async_upload_files_to_yadisk(form.files.data)
        for filename, link in filenames_links:
            short_id = get_unique_short_id()
            url_map = URLMap(
                original=link,
                short=short_id
            )
            db.session.add(url_map)
            db.session.commit()
            short_link = url_for(
                'views.redirect_to_original_link',
                short_id=short_id,
                _external=True
            )
            upload_files_links.append((filename, short_link))
        return render_template(
            'files.html',
            form=form,
            upload_files_links=upload_files_links
        )
    return render_template('files.html', form=form)
