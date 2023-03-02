from rest_framework import serializers


class F5PolicyMergeSerializer(serializers.Serializer):
    diffReferenceId = serializers.CharField(max_length=255, required=True)
    mergeDiffsIds = serializers.JSONField(required=True)
    deleteDiffsOnDestination = serializers.JSONField(required=True)
