from rest_framework import serializers


class PermissionSerializer(serializers.Serializer):
    class PermissionPermissionSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=64, required=True)
        id_asset = serializers.IntegerField(required=True)

    identity_group_name = serializers.CharField(max_length=64, required=True)
    identity_group_identifier = serializers.CharField(max_length=255, required=True)
    role = serializers.CharField(max_length=64, required=True)
    partition = PermissionPermissionSerializer(required=True)
