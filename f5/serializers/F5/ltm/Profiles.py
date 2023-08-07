from rest_framework import serializers

from f5.serializers.F5.ltm.Profile import F5ProfileSerializer


class F5ProfilesSerializer(serializers.Serializer):
    items = F5ProfileSerializer(many=True)
