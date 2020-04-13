from django.views.generic import CreateView
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.vary import vary_on_headers
from django.conf import settings
from honeypot.decorators import check_honeypot
from .forms import ContactForm


class JsonResponseMixin:
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(
                {
                    'errors': dict(form.errors.items()),
                    'success': False
                }
            )
        return response

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.is_ajax():
            self.request.session['message'] = """
Thanks for reaching out! I'll be in touch soon
            """
            self.request.session['level'] = 'success'
            return JsonResponse({
                'url': self.success_url,
                'success': True
            })
        return response


@method_decorator(
    check_honeypot(field_name=settings.HONEYPOT_FIELD_NAME),
    name='dispatch'
)
@method_decorator(vary_on_headers('X-Requested-With'), name='dispatch')
class ContactView(JsonResponseMixin, CreateView):
    form_class = ContactForm
    template_name = 'contact/contact.html'
    success_url = '/'
