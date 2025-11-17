from rest_framework import serializers


## 1. Serializer per i campi annidati (sflow e interfacesReference)

class F5VlanSflowSerializer(serializers.Serializer):
    """Mappa la sezione 'sflow'."""
    pollInterval = serializers.IntegerField(required=False)
    pollIntervalGlobal = serializers.CharField(max_length=255, required=False)
    samplingRate = serializers.IntegerField(required=False)
    samplingRateGlobal = serializers.CharField(max_length=255, required=False)


class F5VlanInterfacesReferenceSerializer(serializers.Serializer):
    """Mappa il campo 'interfacesReference'."""
    link = serializers.CharField(max_length=255, required=False)
    isSubcollection = serializers.BooleanField(required=False)


## 2. Serializer per il Singolo Item VLAN (il tuo oggetto JSON)

class F5VlanItemSerializer(serializers.Serializer):
    """Serializer per un singolo elemento VLAN all'interno della lista 'items'."""

    # Campi principali
    name = serializers.CharField(max_length=255, required=True)
    partition = serializers.CharField(max_length=255, required=False)
    fullPath = serializers.CharField(max_length=255, required=False)
    selfLink = serializers.CharField(max_length=255, required=False)

    # Campi intero
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

    # Campi stringa (char)
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

    # Campi annidati
    sflow = F5VlanSflowSerializer(required=False)
    interfacesReference = F5VlanInterfacesReferenceSerializer(required=False)


## 3. Serializer Radice (quello richiesto dal tuo controller)

class F5VlansSerializer(serializers.Serializer):
    """
    Serializer radice: Mappa la collezione API F5 (risposta della getList)
    che contiene una lista di VLAN sotto la chiave 'items'.
    """
    items = F5VlanItemSerializer(many=True, required=True)