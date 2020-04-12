from django.contrib import admin
from .models import Project, Screenshot, Category


admin.site.register(Category)


class ScreenshotInline(admin.TabularInline):
    model = Screenshot

    def get_extra(self, request, obj=None, **kwargs):
        return 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [ScreenshotInline, ]
