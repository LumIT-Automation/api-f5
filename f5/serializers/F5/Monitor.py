from rest_framework import serializers


class F5MonitorSerializer(serializers.Serializer):
    class F5MonitorInnerSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=255, required=True)
        partition = serializers.CharField(max_length=255, required=False)
        fullPath = serializers.CharField(max_length=255, required=False)
        generation = serializers.IntegerField(required=False)
        selfLink = serializers.CharField(max_length=255, required=False)
        defaultsFrom = serializers.CharField(max_length=255, required=False)
        destination = serializers.CharField(max_length=255, required=False)
        interval = serializers.IntegerField(required=False)
        manualResume = serializers.CharField(max_length=255, required=False)
        timeUntilUp = serializers.IntegerField(required=False)
        timeout = serializers.IntegerField(required=False)
        transparent = serializers.CharField(max_length=255, required=False)
        upInterval = serializers.IntegerField(required=False)
        adaptive = serializers.CharField(max_length=255, required=False)
        adaptiveDivergenceType = serializers.CharField(max_length=255, required=False)
        adaptiveDivergenceValue = serializers.IntegerField(required=False)
        adaptiveLimit = serializers.IntegerField(required=False)
        adaptiveSamplingTimespan = serializers.IntegerField(required=False)
        ipDscp = serializers.IntegerField(required=False)
        reverse = serializers.CharField(max_length=255, required=False)
        send = serializers.CharField(max_length=255, required=False)

    data = F5MonitorInnerSerializer(required=True)
