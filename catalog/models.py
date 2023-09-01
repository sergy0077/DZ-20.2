from distutils.version import Version
from typing import Optional
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.db import models
from PIL import Image

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Product(models.Model):
    objects = None
    DoesNotExist = None
    title = models.CharField(max_length=155, verbose_name='Наименование товара')
    text = models.TextField(max_length=15500, verbose_name='Описание товара', **NULLABLE)
    image = models.ImageField(verbose_name='Изображение товара', blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория товара', blank=True,
                                 null=True)
    price = models.IntegerField(verbose_name='цена', blank=True, null=True)
    date_creation = models.DateTimeField(verbose_name='дата создания', auto_now_add=True)
    date_change = models.DateTimeField(verbose_name='дата последнего изменения', auto_now=True)
    is_allowed = models.BooleanField(default=True)  # поле для контроля разрешенных продуктов
    active_versions = models.ManyToManyField('Version', related_name='products_with_active_version', blank=True)
    slug = models.SlugField(max_length=100, verbose_name='slug')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='владелец', blank=True, null=True)

    def __str__(self):
        # Cтроковое отображение объекта
        return f'{self.title} ({self.text} {self.category})'

    class Meta:
        verbose_name = 'продукт'  # настройка наименования для одного объекта
        verbose_name_plural = 'продукты'
        ordering = ('title',)

    def clean(self):
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                           'радар']
        for word in forbidden_words:
            if word in self.title.lower() or word in self.text.lower():
                raise ValidationError(f"Запрещенное слово '{word}' найдено в названии или описании продукта.")

        if self.image:
            img = Image.open(self.image)
            allowed_formats = ['JPEG', 'PNG']
            if img.format not in allowed_formats:
                raise ValidationError(
                    f"Недопустимый формат изображения. Допустимые форматы: {', '.join(allowed_formats)}.")

    def save(self, *args, **kwargs):
        self.clean()  # Вызываем валидацию перед сохранением
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('catalog:index')

    def get_active_versions(self):
        return self.version_set.filter(is_active=True)


class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name='наименование')
    text = models.TextField(max_length=15000, verbose_name='описание')
    slug = models.SlugField(max_length=100, verbose_name='slug', unique=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.version_set = None

    def __str__(self):
        # Cтроковое отображение объекта
        return f'{self.title} ({self.text})'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ('title',)

    @property
    def active_version(self) -> Optional['Version']:
        active_versions = self.version_set.filter(is_active=True)
        return active_versions.last()


class Version(models.Model):
    product = models.ForeignKey('Product', on_delete=models.PROTECT, verbose_name='Наименование')
    version_number = models.CharField(max_length=20, verbose_name='Номер версии')
    version_name = models.CharField(max_length=100, verbose_name='Название версии')
    is_active = models.BooleanField(verbose_name='Текущая версия', default=True)

    def __str__(self):
        return f'{self.product} - {self.version_name}'

    def active_versions(self):
        return Version.objects.filter(product=self, is_active=True)

    class Meta:
        verbose_name = 'версия'
        verbose_name_plural = 'версии'


class Contacts(models.Model):
    city = models.CharField(max_length=50, verbose_name='Город')
    address = models.TextField(verbose_name='Адрес')
    phone = models.CharField(max_length=30, verbose_name='телефон')
    email = models.EmailField(verbose_name='почта')

    def __str__(self):
        return f'{self.city} - {self.phone}'

    class Meta:
        verbose_name = 'контакт'
        verbose_name_plural = 'контакты'
