from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.db import models
from django.contrib.auth.models import User


# Объявление первая модель
class Bb(models.Model):
    class Kinds(models.TextChoices):
        __empty__ = 'Выберите тип публикуемого объявления'
        BUY = 'b', 'Куплю'
        SELL = 's', 'Продам'
        EXCHANGE = 'c', 'Обменяю'
        RENT = 'r', 'Арендую'

    # KINDS = (
    #     ('b', 'Куплю'),
    #     ('s', 'Продам'),
    #     ('c', 'Обменяю'),
    # )

    # KINDS = (
    #     (None, 'Выберите тип публикуемого объявления'),
    #     ('Купля-Продажа', (
    #         ('b', 'Куплю'),
    #         ('s', 'Продам'),
    #     )),
    #     ('Обмен', (
    #         ('c', 'Обменяю'),
    #     ))
    # )
    kind = models.CharField(max_length=8, choices=Kinds.choices, default=Kinds.SELL, verbose_name='Тип сделки')
    # kind = models.CharField(max_length=1, choices=KINDS, verbose_name='Тип сделки')
    # kind = models.CharField(max_length=1, choices=KINDS, default='s', verbose_name='Тип сделки') # в этой строке по умолчанию выбран s Продам
    title = models.CharField(max_length=50, verbose_name='Товар')
    content = models.TextField(null=True, blank=True, verbose_name='Описание')
    price = models.FloatField(null=True, blank=True, verbose_name='Цена')
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')
    rubric = models.ForeignKey('Rubric', null=True, on_delete=models.PROTECT, verbose_name='Рубрика')

    # def title_and_price(self):
    #     if self.price:
    #         return '%s (%.2f)' % (self.title, self.price)
    #     else:
    #         return self.title
    # title_and_price.short_description = 'Название и цена'
    #  Свой текст на ошибки
    def clean(self):
        errors = {}
        if not self.content:
            errors['content'] = ValidationError('Укажите описание товара')

        if self.price and self.price < 0:
            errors['price'] = ValidationError('Укажите положительное значение цены')

        if errors:
            raise ValidationError(errors)

    class Meta:
        verbose_name_plural = 'Объявления'
        verbose_name = 'Объявление'
        # get_latest_by = '-published'
        ordering = ['-published']

    def __str__(self):
        return self.title


# Модель рубрик доски
class Rubric(models.Model):
    name = models.CharField(max_length=20, db_index=True, verbose_name='Название')

    # def get_absolute_url(self):
    #     return "/bboard/%s" % self.pk

    class Meta:
        verbose_name_plural = 'Рубрики'
        verbose_name = 'Рубрика'
        ordering = ['name']

    def __str__(self):
        return self.name


#  Модель дополнительных полей у пользователя

class AdvUser(models.Model):
    is_activated = models.BinaryField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
