from django.core.exceptions import ValidationError
from django.db import models


class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=13, blank=True, null=True)
    email = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} phone: {self.phone_number}"

    @staticmethod
    def validate_phone_number(phone_number=None, error_to_raise=None):
        if phone_number:
            if not phone_number.startswith("+"):
                raise error_to_raise("Phone number must start with a '+'.")

            if not phone_number[1:].isdigit():
                raise error_to_raise("Phone number must contain only digits after '+'.")

            if len(phone_number) != 13:
                raise error_to_raise("Make sure this field contains 11 characters.")

    def clean(self):
        Contact.validate_phone_number(self.phone_number, error_to_raise=ValidationError)

    def save(self, *args, **kwargs):
        self.full_clean()

        return super(Contact, self).save(*args, **kwargs)
