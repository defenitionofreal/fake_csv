from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import MyUsernameValidator  # для валидации по символам


from django.urls import reverse
# Create your models here.


class CustomUser(AbstractUser):
    """ Custom user model """
    username = models.CharField(max_length=50, unique=True,
                                validators=[MyUsernameValidator()],
                                error_messages={
                                    'unique': ("Этот логин занят. Попробуйте другой."),
                                },
                                )
    is_activated = models.BooleanField(
        default=True, db_index=True, verbose_name='Прошел активизацию?')
