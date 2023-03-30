from rest_framework import serializers


class ActionHistorySerializer(serializers.Serializer):
    class ActionHistoryItemsSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=True)
        asset_id = serializers.IntegerField(required=True)
        action = serializers.CharField(max_length=255, required=True)
        response_status = serializers.IntegerField(required=True)
        username = serializers.CharField(max_length=255, allow_blank=True, required=True)
        date = serializers.CharField(max_length=255, required=True)

    items = ActionHistoryItemsSerializer(many=True)
