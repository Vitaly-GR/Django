import random

from django.db import models
from django.contrib.auth.models import AbstractUser
from .utilites import get_timestamp_path
from transliterate import translit


class Bb(models.Model):
    title = models.CharField(max_length=50, verbose_name='Товар')
    content = models.TextField(null=True, blank=True, verbose_name='Описание')
    price = models.FloatField(null=True, blank=True, verbose_name='Цена')
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')
    category = models.ForeignKey('SubRubric', null=True, on_delete=models.PROTECT, verbose_name='Категория')
    image = models.ImageField(blank=True, upload_to=get_timestamp_path, verbose_name='Изображение')
    author = models.ForeignKey('AdvUser', on_delete=models.CASCADE, verbose_name='Автор', null=True)
    contacts = models.TextField(verbose_name='Контакты', null=True)
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='Выводить в списке?')
    slug = models.SlugField(db_index=True, null=True, unique=True)

    def delete(self, *args, **kwargs):
        for ai in self.additionalimage_set.all():
            ai.delete()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        c_alph = 'abcdefghijklmnopqrstuvwxyz'
        if self.title[0].lower() in c_alph:
            a = translit(self.title, 'ru')
        else:
            a = self.title
        b = random.randint(1, 1000)
        self.slug = translit(a, reversed=True) + f'{b}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Объявления'
        verbose_name = 'Объявление'
        ordering = ['-published']


class Category(models.Model):
    name = models.CharField(max_length=20, db_index=True, unique=True, verbose_name='Название')
    super_category = models.ForeignKey('SuperCategory', on_delete=models.PROTECT,
                                       null=True, blank=True, verbose_name='Надкатегория')
    slug = models.SlugField(db_index=True, null=True, )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']


class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Активирован?')
    send_messages = models.BooleanField(default=True, verbose_name='Включить уведомления?')

    def delete(self, *args, **kwargs):
        for bb in self.bb_set.all():
            bb.delete()
        super().delete(*args, **kwargs)

    class Meta(AbstractUser.Meta):
        pass


class SuperCatManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_category__isnull=True)


class SuperCategory(Category):
    objects = SuperCatManager()

    def __str__(self):
        return self.name

    class Meta:
        proxy = True
        ordering = ('name',)
        verbose_name = 'Надкатегория'
        verbose_name_plural = 'Надкатегории'


class SubCatManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_category__isnull=False)


class SubRubric(Category):
    objects = SubCatManager()

    def __str__(self):
        return f'{self.name}'

    class Meta:
        proxy = True
        ordering = ('super_category__name', 'name')
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'


class AdditionalImage(models.Model):
    bb = models.ForeignKey(Bb, on_delete=models.CASCADE, verbose_name='Объявление')
    image = models.ImageField(upload_to=get_timestamp_path, verbose_name='Изображение')

    class Meta:
        verbose_name_plural = 'Дополнительные иллюстрации'
        verbose_name = 'Дополнительная иллюстрация'
