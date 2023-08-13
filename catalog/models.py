from django.db import models

NULLABLE = {'blank': True, 'null': True}  # Константы для необязательного поля


class Product(models.Model):
    objects = None
    DoesNotExist = None
    title = models.CharField(max_length=155, verbose_name='Наименование товара')
    text = models.TextField(max_length=15500, verbose_name='Описание товара')
    image = models.ImageField(verbose_name='Изображение товара', blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория товара', blank=True, null=True)
    price = models.IntegerField(verbose_name='цена', blank=True, null=True)
    date_creation = models.DateTimeField(verbose_name='дата создания', auto_now_add=True)
    date_change = models.DateTimeField(verbose_name='дата изменений', auto_now=True)

    def __str__(self):
        # Cтроковое отображение объекта
        return f'{self.title} ({self.text})'

    class Meta:
        verbose_name = 'продукт'  # настройка наименования для одного объекта
        verbose_name_plural = 'продукты'
        ordering = ('title',)


class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name='наименование')
    text = models.TextField(max_length=15000, verbose_name='описание')

    def __str__(self):
        #Cтроковое отображение объекта
        return f'{self.title} ({self.text})'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ('title',)
