from rest_framework import serializers

from f5.serializers.F5.Pool import F5PoolSerializer


class F5PoolsSerializer(serializers.Serializer):
    items = F5PoolSerializer(many=True)
