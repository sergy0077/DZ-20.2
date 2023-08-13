from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Blog(models.Model):
    DoesNotExist = None
    object = None
    title = models.CharField(max_length=150, verbose_name='название')
    slug = models.CharField(max_length=150, verbose_name='slug', **NULLABLE)
    description = models.TextField(verbose_name='содержание')
    preview = models.ImageField(upload_to='blog/', verbose_name='изображение', **NULLABLE)
    creation_date = models.DateTimeField(verbose_name='дата создания')
    is_published = models.BooleanField(default=True, verbose_name='опубликовано')
    views_count = models.PositiveIntegerField(default=0, verbose_name='просмотры')

    def __str__(self):
        return f'{self.title} ({self.description})'

    class Meta:
        verbose_name = 'блог'
        verbose_name_plural = 'статьи'