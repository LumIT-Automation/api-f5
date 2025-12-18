from rest_framework import serializers


## 1. Serializer for nested field (sflow e interfacesReference)

class F5VlanSflowSerializer(serializers.Serializer):
    """Maps 'sflow' section."""
    pollInterval = serializers.IntegerField(required=False)
    pollIntervalGlobal = serializers.CharField(max_length=255, required=False)
    samplingRate = serializers.IntegerField(required=False)
    samplingRateGlobal = serializers.CharField(max_length=255, required=False)


class F5VlanInterfacesReferenceSerializer(serializers.Serializer):
    """Maps 'interfacesReference' field."""
    link = serializers.CharField(max_length=255, required=False)
    isSubcollection = serializers.BooleanField(required=False)


## 2. Serializer for the single Item VLAN

class F5VlanItemSerializer(serializers.Serializer):
    """Serializer a single VLAN element of 'items'."""

    # Main fields
    name = serializers.CharField(max_length=255, required=True)
    partition = serializers.CharField(max_length=255, required=False)
    fullPath = serializers.CharField(max_length=255, required=False)
    selfLink = serializers.CharField(max_length=255, required=False)

    # Int
    generation = serializers.IntegerField(required=False)
    failsafeTimeout = serializers.IntegerField(required=False)
    ifIndex = serializers.IntegerField(required=False)
    ipv6PrefixLen = serializers.IntegerField(required=False)
    mtu = serializers.IntegerField(required=False)
    nti = serializers.IntegerField(required=False)
    synFloodRateLimit = serializers.IntegerField(required=False)
    syncacheThreshold = serializers.IntegerField(required=False)
    tag = serializers.IntegerField(required=False)
    assetId = serializers.IntegerField(required=False)

    # string
    kind = serializers.CharField(max_length=255, required=False)
    autoLasthop = serializers.CharField(max_length=255, required=False)
    cmpHash = serializers.CharField(max_length=255, required=False)
    dagAdjustment = serializers.CharField(max_length=255, required=False)
    dagRoundRobin = serializers.CharField(max_length=255, required=False)
    dagTunnel = serializers.CharField(max_length=255, required=False)
    failsafe = serializers.CharField(max_length=255, required=False)
    failsafeAction = serializers.CharField(max_length=255, required=False)
    fwdMode = serializers.CharField(max_length=255, required=False)
    hardwareSyncookie = serializers.CharField(max_length=255, required=False)
    learning = serializers.CharField(max_length=255, required=False)
    sourceChecking = serializers.CharField(max_length=255, required=False)

    # Nested
    sflow = F5VlanSflowSerializer(required=False)
    interfacesReference = F5VlanInterfacesReferenceSerializer(required=False)


## 3. Serializer Root

class F5VlansSerializer(serializers.Serializer):
    """
    Serializer root: Maps API F5 collection (getList response) which contains a list of VLAN under 'items' key.
    """
    items = F5VlanItemSerializer(many=True, required=True)