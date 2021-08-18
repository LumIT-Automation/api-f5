from rest_framework import serializers


class F5PoolMemberStatsSerializer(serializers.Serializer):
    class F5PoolMemberStatsInnerSerializer(serializers.Serializer):
        monitorRule = serializers.CharField(max_length=255, required=True)
        monitorStatus = serializers.CharField(max_length=255, required=True)
        serverside_curConns = serializers.CharField(max_length=255, required=True)
        status_availabilityState =serializers.CharField(max_length=255, required=True)
        status_enabledState = serializers.CharField(max_length=255, required=True)
        status_statusReason = serializers.CharField(max_length=255, required=True)

    data = F5PoolMemberStatsInnerSerializer(required=True)


def sanitize(data: dict) -> dict:
    # Invalid key for a serializer: sanitize it.
    # "status.enabledState": {
    #     "description": "enabled"
    # },
    cleanData = {
        "data": dict()
    }

    for k, v in data["data"].items():
        if "." in k:
            k = k.replace(".", "_")

        if "value" in v:
            cleanData["data"][k] = v["value"]

        if "description" in v:
            cleanData["data"][k] = v["description"]

    return cleanData
