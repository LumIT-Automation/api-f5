from rest_framework import serializers


class F5NodeSerializer(serializers.Serializer):
    class F5NodesItemFQDNSerializer(serializers.Serializer):
        addressFamily = serializers.CharField(max_length=255, required=False)
        autopopulate = serializers.CharField(max_length=255, required=False)
        interval = serializers.CharField(max_length=255, required=False)
        downInterval = serializers.IntegerField(required=False)

    assetId = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=255, required=True)
    partition = serializers.CharField(max_length=255, required=False)
    fullPath = serializers.CharField(max_length=255, required=False)
    generation = serializers.IntegerField(required=False)
    selfLink = serializers.CharField(max_length=255, required=False)
    address = serializers.RegexField(
        regex=r"(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))(%[0-9]+)?$|^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}(%[0-9]+)?$|^any[46]?$",
        required=True
    )
    connectionLimit = serializers.IntegerField(required=False)
    dynamicRatio = serializers.IntegerField(required=False)
    ephemeral = serializers.CharField(max_length=255, required=False)
    fqdn = F5NodesItemFQDNSerializer(required=False)
    logging = serializers.CharField(max_length=255, required=False)
    monitor = serializers.CharField(max_length=255, required=False)
    rateLimit = serializers.CharField(max_length=255, required=False)
    ratio = serializers.IntegerField(required=False)
    session = serializers.CharField(max_length=255, required=False)
    state = serializers.CharField(max_length=255, required=False)
