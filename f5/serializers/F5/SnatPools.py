from rest_framework import serializers

from f5.serializers.F5.SnatPool import F5SnatPoolSerializer


class F5SnatPoolsSerializer(serializers.Serializer):
    items = F5SnatPoolSerializer(many=True)
