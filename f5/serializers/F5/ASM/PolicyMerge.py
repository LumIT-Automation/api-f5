from rest_framework import serializers


class F5PolicyMergeSerializer(serializers.Serializer):
    importedPolicyId = serializers.CharField(max_length=255, required=True)
    ignoreDiffs = serializers.JSONField(required=True)
    deleteDiffsOnDestination = serializers.JSONField(required=True)
