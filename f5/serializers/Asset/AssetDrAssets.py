from rest_framework import serializers


class F5AssetDrAssetsSerializer(serializers.Serializer):
    assetDrId = serializers.IntegerField(required=True)
    enabled = serializers.BooleanField(required=False)
