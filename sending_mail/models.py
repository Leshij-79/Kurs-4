from django.db import models

from users.models import CustomUser


class Recipients(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="ФИО получателя",
        help_text="ФИО получателя рассылки",
    )

    email = models.EmailField(
        verbose_name="email",
        help_text="Email получателя рассылки",
    )

    comment = models.TextField(
        blank=True,
        verbose_name="Комментарий",
        help_text="Комментарий",
    )

    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="owners",
        verbose_name="Владелец получателя",
        help_text="Владелец получателя",
    )


class Messages(models.Model):
    subject = models.CharField(
        max_length=200,
        verbose_name="Тема рассылки",
        help_text="Тема рассылки",
    )

    mail_body = models.TextField(
        verbose_name="Комментарий",
        help_text="Комментарий",
    )

    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="owners",
        verbose_name="Владелец сообщения",
        help_text="Владелец сообщения",
    )


class Mailing(models.Model):
    start_time = models.DateTimeField(
        verbose_name="Дата и время начала рассылки",
        help_text="Дата и время начала рассылки",
    )

    end_time = models.DateTimeField(
        verbose_name="Дата и время окончания рассылки",
        help_text="Дата и время окончания рассылки",
    )

    status = models.CharField(
        max_length=9,
        verbose_name="Статус рассылки",
        help_text="Статус рассылки",
    )

    message = models.ForeignKey(
        Messages,
        on_delete=models.CASCADE,
        related_name="mailing",
        verbose_name="Рассылка",
        help_text="Рассылка",
    )

    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="owners",
        verbose_name="Владелец рассылки",
        help_text="Владелец рассылки",
    )

    recipients = models.ManyToManyField(Recipients)

    is_active = models.BooleanField(default=True)


class work_mailing(models.Model):
    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="mailing",
        verbose_name="Рассылка",
        help_text="Рассылка",
    )

    attempt_time = models.DateTimeField(
        verbose_name="Дата и время рассылки",
        help_text="Дата и время рассылки",
    )

    status = models.BooleanField(default=False)

    server_response = models.TextField(
        verbose_name="Ответ сервера",
        help_text="Ответ сервера",
    )
