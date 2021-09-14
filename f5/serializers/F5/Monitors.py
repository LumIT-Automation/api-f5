from rest_framework import serializers


class F5MonitorsSerializer(serializers.Serializer):
    class F5MonitorsInnerSerializer(serializers.Serializer):
        class F5MonitorsReferencesSerializer(serializers.Serializer):
            name = serializers.CharField(max_length=255, required=True)
            partition = serializers.CharField(max_length=255, required=True)
            fullPath = serializers.CharField(max_length=255, required=True)
            generation = serializers.IntegerField(required=True)
            selfLink = serializers.CharField(max_length=255, required=True)
            defaultsFrom = serializers.CharField(max_length=255, required=False)
            destination = serializers.CharField(max_length=255, required=True)
            interval = serializers.IntegerField(required=True)
            manualResume = serializers.CharField(max_length=255, required=True)
            timeUntilUp = serializers.IntegerField(required=True)
            timeout = serializers.IntegerField(required=True)
            transparent = serializers.CharField(max_length=255, required=False)
            upInterval = serializers.IntegerField(required=True)
            adaptive = serializers.CharField(max_length=255, required=False)
            adaptiveDivergenceType = serializers.CharField(max_length=255, required=False)
            adaptiveDivergenceValue = serializers.IntegerField(required=False)
            adaptiveLimit = serializers.IntegerField(required=False)
            adaptiveSamplingTimespan = serializers.IntegerField(required=False)
            ipDscp = serializers.IntegerField(required=False)
            reverse = serializers.CharField(max_length=255, required=False)
            send = serializers.CharField(max_length=255, required=False)
            recv = serializers.CharField(max_length=255, required=False)

        items = F5MonitorsReferencesSerializer(many=True)

    data = F5MonitorsInnerSerializer(required=True)
