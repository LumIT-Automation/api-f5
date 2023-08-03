from rest_framework import serializers

from f5.serializers.F5.ltm.VirtualServer import F5VirtualServerSerializer


class F5VirtualServersSerializer(serializers.Serializer):
    items = F5VirtualServerSerializer(many=True)
