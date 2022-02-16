from rest_framework import serializers


class F5SnatPoolsSerializer(serializers.Serializer):
    class F5SnatPoolsItemsSerializer(serializers.Serializer):
        class F5SnatPoolsItemsMembersReferenceSerializer(serializers.Serializer):
            link = serializers.CharField(max_length=255, required=True)

        assetId = serializers.IntegerField(required=True)
        name = serializers.CharField(max_length=255, required=True)
        partition = serializers.CharField(max_length=255, required=True)
        fullPath = serializers.CharField(max_length=255, required=True)
        generation = serializers.IntegerField(required=True)
        selfLink = serializers.CharField(max_length=255, required=True)
        members = serializers.ListField(
            child=serializers.RegexField(
                regex='^/.*/([01]?\d\d?|2[0-4]\d|25[0-5])(?:\.(?:[01]?\d\d?|2[0-4]\d|25[0-5])){3}$',
                required=False
            )
        )
        membersReference = F5SnatPoolsItemsMembersReferenceSerializer(required=False, many=True)

    items = F5SnatPoolsItemsSerializer(many=True)
