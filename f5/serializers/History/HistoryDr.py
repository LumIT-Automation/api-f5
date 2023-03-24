from rest_framework import serializers


class HistoryDrSerializer(serializers.Serializer):
    class HistoryDrItemsSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=True, allow_null=True)
        username = serializers.CharField(max_length=255, required=True)
        action = serializers.CharField(max_length=255, required=True)
        pr_asset_id = serializers.IntegerField(required=True, allow_null=True)
        dr_asset_id = serializers.IntegerField(required=True, allow_null=True)
        dr_asset_fqdn = serializers.CharField(max_length=255, required=True)
        config_object_type = serializers.CharField(max_length=255, required=True)
        config_object = serializers.CharField(max_length=255, required=True)
        pr_status = serializers.CharField(max_length=32, required=True)
        dr_status = serializers.CharField(max_length=32, required=True)
        pr_response = serializers.CharField(max_length=4096, required=True)
        dr_response = serializers.CharField(max_length=4096, required=True)
        pr_date = serializers.CharField(max_length=255, required=True)
        dr_date = serializers.CharField(max_length=255, required=True)

    items = HistoryDrItemsSerializer(many=True)
