from rest_framework import serializers

from f5.serializers.Permission.IdentityGroup import IdentityGroupSerializer


class IdentityGroupsSerializer(serializers.Serializer):
    items = IdentityGroupSerializer(many=True)
