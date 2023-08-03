from rest_framework import serializers

from f5.serializers.F5.ltm.Policy import F5PolicySerializer


class F5PoliciesSerializer(serializers.Serializer):
    items = F5PolicySerializer(many=True)
