from django.core.cache import cache
from .models import Category


def get_categories():
    # Попробуем получить данные из кеша
    categories = cache.get('categories')

    # Если данные в кеше отсутствуют, выполним запрос к базе данных и закешируем результат
    if not categories:
        categories = Category.objects.all()
        # Закешируем данные на 1 час (или другое удобное вам время)
        cache.set('categories', categories, 3600)

    return categories
