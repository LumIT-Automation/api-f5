from rest_framework import serializers


class HistorySerializer(serializers.Serializer):
    class HistoryItemsSerializer(serializers.Serializer):
        username = serializers.CharField(max_length=255, required=True)
        action = serializers.CharField(max_length=2048, required=True)
        asset_id = serializers.IntegerField(required=True)
        config_object_type = serializers.CharField(max_length=255, required=True)
        config_object = serializers.CharField(max_length=255, required=True)
        status = serializers.CharField(max_length=255, required=True)
        date = serializers.CharField(max_length=255, required=True)
        dr_replica_flow = serializers.CharField(max_length=255, required=False, allow_blank=True)

    items = HistoryItemsSerializer(many=True)
