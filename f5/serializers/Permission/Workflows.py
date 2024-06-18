from rest_framework import serializers

from f5.serializers.Permission.Workflow import WorkflowSerializer


class WorkflowsSerializer(serializers.Serializer):
    items = WorkflowSerializer(many=True)
