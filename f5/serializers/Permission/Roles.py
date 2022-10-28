from rest_framework import serializers

from f5.serializers.Permission.Role import IdentityRoleSerializer


class IdentityRolesSerializer(serializers.Serializer):
    items = IdentityRoleSerializer(many=True)
