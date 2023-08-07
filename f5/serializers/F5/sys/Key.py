from rest_framework import serializers


class F5KeyInnerSerializer(serializers.Serializer):
    assetId = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=255, required=True) # @todo: only alphanumeric chars + .
    partition = serializers.CharField(max_length=255, required=False)
    fullPath = serializers.CharField(max_length=65535, required=False)
    generation = serializers.IntegerField(required=False)
    selfLink = serializers.CharField(max_length=65535, required=False)
    keySize = serializers.IntegerField(required=False)
    keyType = serializers.CharField(max_length=65535, required=False)
    securityType = serializers.CharField(max_length=65535, required=False)
    content_base64 = serializers.CharField(max_length=65535, required=True)

class F5KeySerializer(serializers.Serializer):
    key = F5KeyInnerSerializer(required=True)
