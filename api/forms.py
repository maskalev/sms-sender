from django import forms
from rest_framework import serializers

from .models import Client, Mailing
from .serializers import ClientSerializer, MailingSerializer


class MailingAdminForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        serializer = MailingSerializer(data=cleaned_data)
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            for field, errors in e.detail.items():
                self.add_error(field, ", ".join(errors))


class ClientAdminForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        serializer = ClientSerializer(data=cleaned_data)
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            for field, errors in e.detail.items():
                self.add_error(field, ", ".join(errors))
