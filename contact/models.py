from django.db import models
from django.core.validators import RegexValidator


class Contact(models.Model):
    name = models.CharField(max_length=255)
    phone_validator = RegexValidator(
        r'^(\+\d{1,3})?,?\s?\d{8,14}',
        message='Please enter your phone number with an optional country code',
    )
    phone = models.CharField(
        validators=[phone_validator], blank=True, max_length=17
    )
    email = models.EmailField()
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} ({self.email}), {self.date.strftime("%D %H:%M")}'
