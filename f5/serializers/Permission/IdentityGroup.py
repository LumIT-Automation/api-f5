from rest_framework import serializers
from f5.models.Permission.Privilege import Privilege
from f5.models.Permission.Role import Role


class IdentityGroupsAssestRolesSubItems(serializers.Serializer):
    assetId = serializers.IntegerField(required=True)
    partition = serializers.CharField(max_length=64, required=True)

class IdentityGroupsAssestRolesItems(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Adding dynamic fields as taken from the Roles model.
        additionalFields = []
        r = Role.list()
        for additionalField in r:
            if "role" in additionalField:
                additionalFields.append(additionalField["role"])

        for af in additionalFields:
            self.fields[af] = IdentityGroupsAssestRolesSubItems(many=True, required=False)

class IdentityGroupsAssestPrivilegeItems(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Adding dynamic fields as taken from the Privilege model.
        additionalFields = []
        r = Privilege.list()
        for additionalField in r:
            if "privilege" in additionalField:
                additionalFields.append(additionalField["privilege"])

        for af in additionalFields:
            self.fields[af] = IdentityGroupsAssestRolesSubItems(many=True, required=False)

class IdentityGroupSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=64, required=True)
    identity_group_identifier = serializers.CharField(max_length=255, required=True)

    roles_partition = IdentityGroupsAssestRolesItems(required=False)
    privileges_partition = IdentityGroupsAssestPrivilegeItems(required=False)
