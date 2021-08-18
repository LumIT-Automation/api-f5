from rest_framework import serializers


class F5SnatPoolSerializer(serializers.Serializer):
    class F5SnatPoolInnerSerializer(serializers.Serializer):
        class F5SnatPoolItemsMembersReferenceSerializer(serializers.Serializer):
            link = serializers.CharField(max_length=255, required=True)

        name = serializers.CharField(max_length=255, required=True)
        fullPath = serializers.CharField(max_length=255, required=False)
        generation = serializers.IntegerField(required=False)
        selfLink = serializers.CharField(max_length=255, required=False)
        members = serializers.ListField(
            child=serializers.CharField(max_length=255, required=True),
            required=True
        )
        membersReference = F5SnatPoolItemsMembersReferenceSerializer(required=False, many=False)

    data = F5SnatPoolInnerSerializer(required=True)
