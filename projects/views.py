from django.shortcuts import render
from django.contrib import messages
from django.views.generic import DetailView, ListView
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings
from .models import Project


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


def index(request):
    if 'message' in request.session:
        message = request.session.pop('message')
        level = request.session.pop('level', 'info')
        {
            'success': messages.success,
            'info': messages.info,
            'warning': messages.warning,
            'error': messages.error
        }.get(level)(request, message)
    return render(request, 'index.html')


@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class ProjectList(ListView):
    model = Project


@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class ProjectDetail(DetailView):
    model = Project
    sort_by = ['category']


# Errors

def handler_404(request, exception):
    status = 404
    return render(request, 'errors/404.html', {'status': status})


def handler_403(request, exception):
    status = 403
    return render(request, 'errors/403.html', {'status': status})


def handler_500(request):
    status = 500
    return render(request, 'errors/500.html', {'status': status})
