from rest_framework import serializers


class F5SnatPoolSerializer(serializers.Serializer):
    class F5SnatPoolItemsMembersReferenceSerializer(serializers.Serializer):
        link = serializers.CharField(max_length=255, required=False)

    assetId = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=255, required=True)
    partition = serializers.CharField(max_length=255, required=False)
    fullPath = serializers.CharField(max_length=255, required=False)
    generation = serializers.IntegerField(required=False)
    selfLink = serializers.CharField(max_length=255, required=False)
    members = serializers.ListField(
        child=serializers.RegexField(
            regex='^/.*/([01]?\d\d?|2[0-4]\d|25[0-5])(?:\.(?:[01]?\d\d?|2[0-4]\d|25[0-5])){3}(%\d)?$',
            required=False
        )
    )
    membersReference = F5SnatPoolItemsMembersReferenceSerializer(required=False, many=True)
