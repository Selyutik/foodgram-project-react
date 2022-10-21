from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import default_token_generator
from django.db import models
from django.db.models import F, Q
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    USER_ROLES = (
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
        (USER, 'Пользователь'),
    )

    username = models.CharField(
        verbose_name=_('Логин'),
        max_length=150,
        unique=True,
        error_messages={
            'unique': _('Пользователь с таким никнеймом уже существует!'),
        },
        help_text=_('Укажите свой никнейм'),
    )
    first_name = models.CharField(
        verbose_name=_('Имя'),
        max_length=150,
        blank=True,
        help_text=_('Укажите своё имя'),
    )
    last_name = models.CharField(
        verbose_name=_('Фамилия'),
        max_length=150,
        blank=True,
        help_text=_('Укажите свою фамилию'),
    )
    email = models.EmailField(
        verbose_name=_('Адрес email'),
        max_length=254,
        unique=True,
        blank=False,
        error_messages={
            'unique': _('Пользователь с таким email уже существует!'),
        },
        help_text=_('Укажите свой email'),
    )
    role = models.CharField(
        verbose_name=_('статус'),
        max_length=20,
        choices=USER_ROLES,
        default=USER
    )
    date_joined = models.DateTimeField(
        verbose_name=_('Дата регистрации'),
        auto_now_add=True,
    )
    password = models.CharField(
        verbose_name=_('Пароль'),
        max_length=150,
        help_text=_('Введите пароль'),
    )

    class Meta:
        swappable = 'AUTH_USER_MODEL'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.get_full_name()

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    def make_code(self):
        return default_token_generator.make_token(self)

    def send_confirmation(self, confirmation_code):
        self.email_user(
            'YaMDb Confirmation Code',
            f'Hi! Your confirmation code: {confirmation_code}'
        )


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор рецепта',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='uniq_follow',
            ),
            models.CheckConstraint(
                check=~Q(user=F('author')),
                name='self_following',
            ),
        )

    def __str__(self):
        return f'{self.user} - {self.author}'
