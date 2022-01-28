from rest_framework import serializers


class F5PoolMemberStatsSerializer(serializers.Serializer):
    monitorRule = serializers.CharField(max_length=255, required=True)
    monitorStatus = serializers.CharField(max_length=255, required=True)
    serverside_curConns = serializers.CharField(max_length=255, required=True)
    status_availabilityState =serializers.CharField(max_length=255, required=True)
    status_enabledState = serializers.CharField(max_length=255, required=True)
    status_statusReason = serializers.CharField(max_length=255, required=True)



def sanitize(data: dict) -> dict:
    # Invalid key for a serializer: sanitize it.
    # "status.enabledState": {
    #     "description": "enabled"
    # },
    cleanData = dict()

    for k, v in data.items():
        if "." in k:
            k = k.replace(".", "_")

        if "value" in v:
            cleanData[k] = v["value"]

        if "description" in v:
            cleanData[k] = v["description"]

    return cleanData
