from django.core.management.base import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Fill the database with initial data'

    def handle(self, *args, **options):
        self.stdout.write('Удаление старых данных...')
        Category.objects.all().delete()
        Product.objects.all().delete()

        self.stdout.write('Создание категории...')
        Category.objects.create(title='Бытовая техника', text='произведено в России')
        Category.objects.create(title='Продукты', text='выращено в Краснодарском крае')

        self.stdout.write('Создание продукта...')
        category1 = Category.objects.get(title='Электроника')
        Product.objects.create(title='Телевизор', text='Горизонт',
                               category=category1, price=100)

        category2 = Category.objects.get(title='Кофе')
        Product.objects.create(title='зерновой Якобс', text='в упаковке по 200 гр',
                               category=category2, price=150)

        self.stdout.write(self.style.SUCCESS('База успешно заполнена!'))
