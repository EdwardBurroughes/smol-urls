from django.db.transaction import atomic
from . import models


@atomic
def get_or_create_shortened_url(hash_id: str, url: str) -> models.URL:
    return models.URL.objects.get_or_create(shortened_id=hash_id, original_url=url)