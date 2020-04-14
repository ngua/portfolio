from django.forms import ModelForm
from .models import Contact
from .tasks import mail_admins_async


class ContactForm(ModelForm):
    def send_mail(self):
        name = self.cleaned_data['name']
        message = self.cleaned_data['message']
        mail_admins_async.delay(
            subject=f'{name} contacted you',
            message=message
        )

    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'message']
