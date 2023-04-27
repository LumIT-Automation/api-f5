from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField


class F5AssetSerializer(serializers.Serializer):
    class F5AssetAssetDrInnerSerializer(serializers.Serializer):
        asset = RecursiveField("F5AssetSerializer", required=False)
        enabled = serializers.BooleanField(required=False)

    id = serializers.IntegerField(required=False)
    address = serializers.CharField(max_length=64, required=True) # @todo: only valid data.
    fqdn = serializers.CharField(max_length=255, required=True, allow_blank=True) # @todo: only valid data.
    baseurl = serializers.CharField(max_length=255, required=True) # @todo: only valid data.
    tlsverify = serializers.IntegerField(required=True)
    datacenter = serializers.CharField(max_length=255, required=True, allow_blank=True)
    environment = serializers.CharField(max_length=255, required=True)
    position = serializers.CharField(max_length=255, required=True, allow_blank=True)
    username = serializers.CharField(max_length=64, required=False)
    password = serializers.CharField(max_length=64, required=False)

    assetsDr = F5AssetAssetDrInnerSerializer(many=True, required=False)
