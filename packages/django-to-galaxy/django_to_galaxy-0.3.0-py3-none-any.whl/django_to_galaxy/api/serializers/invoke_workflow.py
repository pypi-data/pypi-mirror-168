from rest_framework import serializers


class InvokeWorkflowSerializer(serializers.Serializer):
    workflow_id = serializers.IntegerField()
    history_id = serializers.IntegerField()
    datamap = serializers.DictField()
