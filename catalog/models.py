from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(**NULLABLE)

    def __str__(self):
        return self.name


class Product(models.Model):
    objects = None
    DoesNotExist = None
    name = models.CharField(max_length=255, verbose_name='Наименование товара')
    description = models.TextField()
    category = models.CharField(max_length=100, verbose_name='Категория товара')
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.name} ({self.category})'

    class Meta:
        verbose_name = 'товар'
