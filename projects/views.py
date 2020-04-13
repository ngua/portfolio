from django.shortcuts import render
from django.contrib import messages
from django.views.generic import DetailView, ListView
from .models import Project


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
    return render(request, 'projects/index.html')


class ProjectList(ListView):
    model = Project


class ProjectDetail(DetailView):
    model = Project
    sort_by = ['category']
