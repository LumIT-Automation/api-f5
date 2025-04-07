from rest_framework import serializers


class F5AssetSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    fqdn = serializers.CharField(max_length=255, required=True)
    protocol = serializers.CharField(max_length=16, required=False)
    port = serializers.IntegerField(required=False)
    path = serializers.CharField(max_length=255, required=False)
    tlsverify = serializers.BooleanField(required=False)
    baseurl = serializers.CharField(max_length=255, required=False)
    datacenter = serializers.CharField(max_length=255, required=False, allow_blank=True)
    environment = serializers.CharField(max_length=255, required=True)
    position = serializers.CharField(max_length=255, required=False, allow_blank=True)
    username = serializers.CharField(max_length=64, required=False)
    password = serializers.CharField(max_length=64, required=False)
