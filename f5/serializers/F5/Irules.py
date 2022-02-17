from rest_framework import serializers

from f5.serializers.F5.Irule import F5IruleSerializer


class F5IrulesSerializer(serializers.Serializer):
    items = F5IruleSerializer(many=True)
