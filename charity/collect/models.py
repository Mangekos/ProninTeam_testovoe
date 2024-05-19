from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()
TYPE_PAYMETS = (
    ("Единоразовое пожертвование", "Единоразовое пожертвование"),
    ("Многоразовое пожертвование", "Многоразовое пожертвование"),
)


class Collect(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Автор"
    )
    first_name = models.CharField(max_length=200, verbose_name="Имя")
    last_name = models.CharField(max_length=200, verbose_name="Фамилия")
    occasion = models.CharField(max_length=200, verbose_name="Повод")
    description = models.TextField(verbose_name="Описание")
    target = models.IntegerField(verbose_name="Цель", blank=True, default=0)
    image = models.ImageField(
        upload_to="media/", blank=True, verbose_name="Изображение"
    )
    collection_period = models.DateField(verbose_name="Срок сбора")

    class Meta:
        verbose_name = "Сбор"
        verbose_name_plural = "Сборы"

    def __str__(self) -> str:
        return self.name


class Payment(models.Model):
    type_payment = models.CharField(
        max_length=200, choices=TYPE_PAYMETS, verbose_name="Тип пожертвования"
    )
    sum_payment = models.IntegerField(verbose_name="Сумма пожертвования")
    first_name = models.CharField(max_length=200, verbose_name="Имя")
    last_name = models.CharField(max_length=200, verbose_name="Фамилия")
    email = models.EmailField(max_length=254, verbose_name="Email")
    comment = models.TextField(verbose_name="Комментарий")
    collect = models.ForeignKey(
        Collect,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="Сбор",
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата пожертвования",
    )
    is_show = models.BooleanField(verbose_name="Показывать", default=True)

    class Meta:
        verbose_name = "Пожертвование"
        verbose_name_plural = "Пожертвования"

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
