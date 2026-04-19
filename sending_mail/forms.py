from django.core.exceptions import ValidationError
from django.forms import BooleanField, forms, ModelForm

from sending_mail.models import Messages, Recipients, Mailing


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class MessageDetailForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Messages
        exclude = (
            "owner",
        )


class MessageCUForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Messages
        exclude = (
            "owner",
        )

    def clean_subject(self):
        subject = self.cleaned_data["subject"]

        if not subject:
            raise ValidationError("Поле тема сообщения не должно быть пустым")

        return subject

    def clean_body(self):
        mail_body = self.cleaned_data["mail_body"]

        if not mail_body:
            raise ValidationError("Поле текст сообщения не должно быть пустым")

        return mail_body


class RecipientDetailForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Recipients
        exclude = (
            "owner",
        )


class RecipientCUForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Recipients
        exclude = (
            "owner",
        )

    def clean_name(self):
        name = self.cleaned_data["name"]

        if not name:
            raise ValidationError("Поле имя не должно быть пустым")

        return name

    def clean_email(self):
        email = self.cleaned_data["email"]

        if not email:
            raise ValidationError("Поле email не должно быть пустым")

        return email


class MailingDetailForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Mailing
        exclude = (
            "owner",
        )


class MailingCUForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Mailing
        exclude = (
            "owner",
            "is_active"
        )

    def clean_name(self):
        name = self.cleaned_data["name"]

        if not name:
            raise ValidationError("Поле имя не должно быть пустым")

        return name

    def clean_email(self):
        email = self.cleaned_data["email"]

        if not email:
            raise ValidationError("Поле email не должно быть пустым")

        return email
