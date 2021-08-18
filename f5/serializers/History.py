from rest_framework import serializers


class HistorySerializer(serializers.Serializer):
    class HistoryInnerSerializer(serializers.Serializer):
        class HistoryItemsSerializer(serializers.Serializer):
            username = serializers.CharField(max_length=255, required=True)
            action = serializers.CharField(max_length=255, required=True)
            asset_id = serializers.IntegerField(required=True)
            config_object_type = serializers.CharField(max_length=255, required=True)
            config_object = serializers.CharField(max_length=255, required=True)
            status = serializers.CharField(max_length=255, required=True)
            date = serializers.CharField(max_length=255, required=True)

        items = HistoryItemsSerializer(many=True)

    data = HistoryInnerSerializer(required=True)
