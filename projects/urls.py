from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('projects/', views.ProjectList.as_view(), name='projects'),
    path('projects/<slug:slug>/', views.ProjectDetail.as_view(), name='project-detail'),
]
