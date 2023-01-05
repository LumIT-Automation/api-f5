from rest_framework import serializers


class F5PolicyApplySerializer(serializers.Serializer):
    policyId = serializers.CharField(max_length=255, required=True)
