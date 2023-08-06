from rest_framework import serializers

from django_to_galaxy.models.workflow import Workflow


class WorkflowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workflow
        fields = ["id", "galaxy_id", "name", "annotation", "published", "galaxy_owner"]
