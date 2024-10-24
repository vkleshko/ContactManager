from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Contact


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ("id", "first_name", "last_name", "email", "phone_number")


class ContactCreateSerializer(ContactSerializer):
    def validate(self, attrs):
        super().validate(attrs)
        Contact.validate_phone_number(
            phone_number=attrs.get("phone_number"), error_to_raise=ValidationError
        )
        return attrs


class ContactDetailSerializer(ContactSerializer):
    class Meta(ContactSerializer.Meta):
        fields = ("id", "first_name", "last_name", "email", "phone_number")
