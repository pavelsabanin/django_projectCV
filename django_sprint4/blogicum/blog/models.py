from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
MAX_LENGTH = 256


class PublishedModel(models.Model):
    is_published = models.BooleanField('Опубликовано', default=True,
                                       help_text='Снимите галочку, '
                                                 'чтобы скрыть публикацию.')
    created_at = models.DateTimeField('Добавлено',
                                      auto_now_add=True)

    class Meta:
        abstract = True


class Location(PublishedModel):
    name = models.CharField('Название места', max_length=MAX_LENGTH)

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Category(PublishedModel):
    title = models.CharField('Заголовок', max_length=MAX_LENGTH)
    description = models.TextField('Описание')
    slug = models.SlugField(
        'Идентификатор',
        unique=True,
        help_text=('Идентификатор страницы для URL;'
                   ' разрешены символы латиницы, цифры,'
                   ' дефис и подчёркивание.')
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Post(PublishedModel):
    title = models.CharField('Заголовок', max_length=MAX_LENGTH)
    text = models.TextField('Текст')
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        help_text=('Если установить дату и время в будущем —'
                   ' можно делать отложенные публикации.')
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
        related_name='posts',
        blank=True
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        verbose_name='Местоположение',
        null=True,
        blank=True,
        related_name='posts'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        null=True,
        related_name='posts'
    )
    image = models.ImageField(
        'Фото',
        upload_to='posts_images',
        blank=True
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField('Комментарий')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('created_at',)

    def __str__(self):
        return self.text
