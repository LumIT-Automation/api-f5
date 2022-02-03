from rest_framework import serializers


class F5AssetSerializer(serializers.Serializer):
    address = serializers.CharField(max_length=64, required=True) # @todo: only valid data.
    fqdn = serializers.CharField(max_length=255, required=True, allow_blank=True) # @todo: only valid data.
    baseurl = serializers.CharField(max_length=255, required=True) # @todo: only valid data.
    tlsverify = serializers.IntegerField(required=True)
    datacenter = serializers.CharField(max_length=255, required=True, allow_blank=True)
    environment = serializers.CharField(max_length=255, required=True)
    position = serializers.CharField(max_length=255, required=True, allow_blank=True)
    username = serializers.CharField(max_length=64, required=True)
    password = serializers.CharField(max_length=64, required=True)
