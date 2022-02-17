from rest_framework import serializers

from f5.serializers.F5.Monitor import F5MonitorSerializer


class F5MonitorsSerializer(serializers.Serializer):
    items = F5MonitorSerializer(many=True)
