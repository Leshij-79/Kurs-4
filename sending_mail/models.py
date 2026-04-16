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
        related_name="recipients",
        verbose_name="Владелец получателя",
        help_text="Владелец получателя",
    )

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"
        ordering = ["name"]

    def __str__(self):
        return self.name


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
        related_name="messages",
        verbose_name="Владелец сообщения",
        help_text="Владелец сообщения",
    )

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["subject"]

    def __str__(self):
        return self.subject


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
        related_name="message",
        verbose_name="Рассылка",
        help_text="Рассылка",
    )

    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="mailing",
        verbose_name="Владелец рассылки",
        help_text="Владелец рассылки",
    )

    recipients = models.ManyToManyField(Recipients)

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["message"]

    def __str__(self):
        return self.message


class WorkMailing(models.Model):
    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        related_name="work_mailing",
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

    class Meta:
        verbose_name = "Состояние рассылки"
        verbose_name_plural = "Состояние рассылок"
        ordering = ["mailing"]

    def __str__(self):
        return self.mailing
