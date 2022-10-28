from rest_framework import serializers

from f5.serializers.Permission.Permission import PermissionSerializer


class PermissionsSerializer(serializers.Serializer):
    items = PermissionSerializer(many=True)
