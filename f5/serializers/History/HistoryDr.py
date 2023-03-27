from rest_framework import serializers


class HistoryDrSerializer(serializers.Serializer):
    class HistoryDrItemsSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=True, allow_null=True)
        pr_asset_id = serializers.IntegerField(required=True)
        dr_asset_id = serializers.IntegerField(required=True, allow_null=True)
        dr_asset_fqdn = serializers.CharField(max_length=255, allow_blank=True, required=True)
        username = serializers.CharField(max_length=255,  allow_blank=True, required=True)
        action_name = serializers.CharField(max_length=255, required=True)
        request = serializers.CharField(max_length=8192, required=True)
        pr_status = serializers.CharField(max_length=15, allow_blank=True,required=True)
        dr_status = serializers.CharField(max_length=15, allow_blank=True, required=True)
        pr_response = serializers.CharField(max_length=4096, allow_blank=True, required=True)
        dr_response = serializers.CharField(max_length=4096, allow_blank=True, required=True)
        pr_date = serializers.CharField(max_length=255, required=True)
        dr_date = serializers.CharField(max_length=255, required=True)

    items = HistoryDrItemsSerializer(many=True)
