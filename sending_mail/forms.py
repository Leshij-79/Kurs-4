from django.core.exceptions import ValidationError
from django.forms import BooleanField, forms, ModelForm

from sending_mail.models import Messages


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