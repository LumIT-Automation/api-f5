from rest_framework import serializers

from f5.serializers.F5.sys.Key import F5KeyInnerSerializer


class F5KeysSerializer(serializers.Serializer):
    items = F5KeyInnerSerializer(many=True)
