from rest_framework import serializers

from f5.serializers.F5.ltm.Node import F5NodeSerializer


class F5NodesSerializer(serializers.Serializer):
    items = F5NodeSerializer(many=True)
