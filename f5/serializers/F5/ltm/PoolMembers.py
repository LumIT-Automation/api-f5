from rest_framework import serializers

from f5.serializers.F5.ltm.PoolMember import F5PoolMemberSerializer


class F5PoolMembersSerializer(serializers.Serializer):
    items = F5PoolMemberSerializer(many=True)
