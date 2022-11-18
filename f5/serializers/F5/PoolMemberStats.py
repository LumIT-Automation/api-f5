from rest_framework import serializers


def sanitize(data: dict) -> dict:
    cleanData = dict()

    for k, v in data.items():
        if not "." in k:
            kn = k
        else:
            kn = k.replace(".", "_") # k is immutable.

        if "value" in v:
            cleanData[kn] = v["value"]
        elif "description" in v:
            cleanData[kn] = v["description"]
        else:
            cleanData[kn] = v

    return cleanData

class F5PoolMemberDescriptionDictSerializer(serializers.Serializer):
    description = serializers.CharField(max_length=255, required=False)

class F5PoolMemberValueDictSerializer(serializers.Serializer):
    value = serializers.IntegerField(required=False)

class F5PoolMemberStatsSerializer(serializers.Serializer):

    def to_internal_value(self, data):
        try:
            newData = sanitize(data)

            return super().to_internal_value(newData)
        except Exception as e:
            raise e

    monitorRule = serializers.CharField(max_length=255, required=False)
    monitorStatus = serializers.CharField(max_length=255, required=False)
    serverside_curConns =  serializers.IntegerField(required=False)
    status_availabilityState =  serializers.CharField(max_length=255, required=False)
    status_enabledState =  serializers.CharField(max_length=255, required=False)
    status_statusReason = serializers.CharField(max_length=255, required=False)
