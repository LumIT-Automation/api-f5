from rest_framework import serializers


class F5PoolMemberStatsSerializer(serializers.Serializer):
    monitorRule = serializers.CharField(max_length=255, required=False)
    monitorStatus = serializers.CharField(max_length=255, required=False)
    serverside_curConns = serializers.CharField(max_length=255, required=False)
    status_availabilityState =serializers.CharField(max_length=255, required=False)
    status_enabledState = serializers.CharField(max_length=255, required=False)
    status_statusReason = serializers.CharField(max_length=255, required=False)



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
