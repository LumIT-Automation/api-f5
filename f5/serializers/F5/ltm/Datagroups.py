from rest_framework import serializers

from f5.serializers.F5.ltm.Datagroup import F5DatagroupSerializer


class F5DatagroupsSerializer(serializers.Serializer):
    items = F5DatagroupSerializer(many=True)
