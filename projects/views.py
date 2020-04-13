from django.shortcuts import render
from django.views.generic import DetailView, ListView
from .models import Project


def index(request):
    return render(request, 'projects/index.html')


class ProjectList(ListView):
    model = Project


class ProjectDetail(DetailView):
    model = Project
    sort_by = ['category']
