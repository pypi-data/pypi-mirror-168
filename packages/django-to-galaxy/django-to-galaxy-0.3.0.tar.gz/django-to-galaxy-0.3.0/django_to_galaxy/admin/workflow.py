from django.contrib import admin

from django_to_galaxy.models.workflow import Workflow

from .galaxy_element import GalaxyElementAdmin


@admin.register(Workflow)
class WorkflowAdmin(GalaxyElementAdmin):
    list_display = (
        "id",
        "name",
        "annotation",
        "galaxy_id",
        "published",
        "galaxy_owner",
    )
    readonly_fields = (
        "id",
        "name",
        "annotation",
        "galaxy_id",
        "published",
        "galaxy_owner",
    )
