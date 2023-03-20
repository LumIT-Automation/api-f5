from rest_framework import serializers


class F5AssetDrAssetSerializer(serializers.Serializer):
    enabled = serializers.BooleanField(required=False)
