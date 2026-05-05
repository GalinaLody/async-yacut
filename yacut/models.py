from datetime import datetime

from yacut import db


class URLMap(db.Model):
    """Модель хранит связь оригинальной ссылки и короткой ссылки."""
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String, nullable=False)
    short = db.Column(db.String(16), nullable=False, unique=True)
    timestamp = db.Column(db.DateTime, default=datetime.now)

    API_FIELDS_MAPPING = {
        'url': 'original',
        'custom_id': 'short'
    }

    def to_dict(self):
        """Преодразует объект модели в словарь для API."""
        return dict(
            id=self.id,
            original=self.original,
            short=self.short,
            timestamp=self.timestamp
        )

    def from_dict(self, data):
        """Десериализует данные API-запроса(словарь) в объект модели."""
        for data_key, field_model in self.API_FIELDS_MAPPING.items():
            if data_key in data:
                setattr(self, field_model, data[data_key])
