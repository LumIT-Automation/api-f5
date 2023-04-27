from rest_framework import serializers

from f5.serializers.Asset.Asset import F5AssetSerializer


class F5AssetsSerializer(serializers.Serializer):
    items = F5AssetSerializer(many=True)
