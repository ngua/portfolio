from django.views.generic import CreateView
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.vary import vary_on_headers
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.shortcuts import render
from honeypot.decorators import check_honeypot
from .forms import ContactForm


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


@cache_page(CACHE_TTL)
def bio(request):
    return render(request, 'contact/bio.html')


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
        form.save()
        form.send_mail()
        response = super().form_valid(form)
        self.request.session['message'] = (
            "Thanks for reaching out! I'll be in touch soon"
        )
        self.request.session['level'] = 'success'
        if self.request.is_ajax():
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
    success_url = reverse_lazy('index')
