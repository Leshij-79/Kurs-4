from django.db import models
from django.utils import timezone

from users.models import CustomUser


class Recipients(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="ФИО получателя",
        help_text="ФИО получателя рассылки",
    )

    email = models.EmailField(
        unique=True,
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
        verbose_name="Текст рассылки",
        help_text="Текст рассылки",
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
    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('completed', 'Завершена'),
    ]

    start_time = models.DateTimeField(
        verbose_name="Дата и время начала рассылки",
        help_text="ДД.ММ.ГГГГ ЧЧ:ММ",
    )

    end_time = models.DateTimeField(
        verbose_name="Дата и время окончания рассылки",
        help_text="ДД.ММ.ГГГГ ЧЧ:ММ",
    )

    status = models.CharField(
        max_length=9,
        choices=STATUS_CHOICES,
        default='created',
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

    recipients = models.ManyToManyField(
        Recipients,
        verbose_name="Получатели рассылки",
        help_text="Множественный выбор через CTRL",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Активность рассылки"
    )

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["message"]

    def __str__(self):
        return self.message.subject

    def update_status(self):
        now_data = timezone.now()
        if now_data < self.start_time:
            self.status = 'created'
            self.is_active = False
            self.save()
        elif self.start_time < now_data < self.end_time:
            self.status = "started"
            self.is_active = True
            self.save()
        elif now_data > self.end_time:
            self.status = "completed"
            self.is_active = False
            self.save()


class WorkMailing(models.Model):
    STATUS_CHOICES = [
        ('success', 'Успешно'),
        ('failed', 'Не успешно'),
    ]

    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        related_name="work_mailing",
        verbose_name="Рассылка",
        help_text="Рассылка",
    )

    recipient = models.ForeignKey(
        Recipients,
        on_delete=models.CASCADE,
        related_name="work_mailing_recipient",
        verbose_name="Получатель рассылки",
    )

    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="work_mailing_owner",
        verbose_name="Владелец рассылки",
        help_text="Владелец рассылки",
    )

    attempt_time = models.DateTimeField(
        verbose_name="Дата и время рассылки",
        help_text="Дата и время рассылки",
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        verbose_name="Статус выполнения рассылки",
        help_text="Статус выполения рассылки",
    )

    server_response = models.TextField(
        blank=True,
        verbose_name="Ответ сервера",
        help_text="Ответ сервера",
    )


    class Meta:
        verbose_name = "Состояние рассылки"
        verbose_name_plural = "Состояние рассылок"
        ordering = ["mailing"]

    def __str__(self):
        return f"{self.mailing.message.subject} - {self.attempt_time} - {self.recipient.email} - {self.status}"
