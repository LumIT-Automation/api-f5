from rest_framework import serializers


class F5FolderSerializer(serializers.Serializer):
    class F5FolderTrafficGroupReferenceSerializers(serializers.Serializer):
        link = serializers.CharField(max_length=255, required=False)

    assetId = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=255, required=False)
    partition = serializers.CharField(max_length=255, required=False)
    fullPath = serializers.CharField(max_length=255, required=False)
    generation = serializers.IntegerField(required=False)
    selfLink = serializers.CharField(max_length=255, required=False)
    deviceGroup = serializers.CharField(max_length=255, required=False)
    hidden = serializers.BooleanField(required=False)
    inheritedDevicegroup = serializers.BooleanField(required=False)
    inheritedTrafficGroup = serializers.BooleanField(required=False)
    noRefCheck = serializers.BooleanField(required=False)
    trafficGroup = serializers.CharField(max_length=255, required=False)
    trafficGroupReference = F5FolderTrafficGroupReferenceSerializers(required=False)
