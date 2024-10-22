from rest_framework import serializers


class PermissionWorkflowSerializer(serializers.Serializer):
    # Not using composition here, for simpler data structure exposed to consumer.

    class PermissionPermissionSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=64, required=True)
        id_asset = serializers.IntegerField(required=False)

    id = serializers.IntegerField(required=False)
    identity_group_name = serializers.CharField(max_length=64, required=False)
    identity_group_identifier = serializers.CharField(max_length=255, required=True)
    workflow = serializers.CharField(max_length=64, required=True)
    partition = PermissionPermissionSerializer(required=True)
