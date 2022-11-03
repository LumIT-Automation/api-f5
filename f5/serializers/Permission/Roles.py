from rest_framework import serializers

from f5.serializers.Permission.Role import RoleSerializer


class RolesSerializer(serializers.Serializer):
    items = RoleSerializer(many=True)
