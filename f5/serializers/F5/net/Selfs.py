from rest_framework import serializers


## 1. Serializer per i Riferimenti Annidati (References)

class F5SelfReferenceSerializer(serializers.Serializer):
    """Mappa i campi di riferimento come 'trafficGroupReference' o 'vlanReference'."""
    link = serializers.CharField(max_length=255, required=False)


## 2. Serializer per il Singolo Item Self IP

class F5SelfItemSerializer(serializers.Serializer):
    """
    Serializer per un singolo oggetto Self IP (quello mostrato nel JSON),
    che sarà un 'item' nella collezione API.
    """

    # Campi di sistema e identificazione
    kind = serializers.CharField(max_length=255, required=False)
    name = serializers.CharField(max_length=255, required=True)
    partition = serializers.CharField(max_length=255, required=False)
    fullPath = serializers.CharField(max_length=255, required=False)
    generation = serializers.IntegerField(required=False)
    selfLink = serializers.CharField(max_length=255, required=False)
    assetId = serializers.IntegerField(required=False)

    # Campi specifici del Self IP
    address = serializers.CharField(max_length=255, required=True)  # Es: 10.177.10.6/23
    addressSource = serializers.CharField(max_length=255, required=False)

    floating = serializers.CharField(max_length=255, required=False)  # 'enabled' o 'disabled'
    inheritedTrafficGroup = serializers.CharField(max_length=255, required=False)  # 'true' o 'false'

    trafficGroup = serializers.CharField(max_length=255, required=False)  # /Common/traffic-group-1
    vlan = serializers.CharField(max_length=255, required=False)  # /Common/DMZ_ADS1_10.177.10.0

    unit = serializers.IntegerField(required=False)

    # Campi Riferimento annidati
    trafficGroupReference = F5SelfReferenceSerializer(required=False)
    vlanReference = F5SelfReferenceSerializer(required=False)


## 3. Serializer Radice per la Collezione (Usato dal Controller)

class F5SelfsSerializer(serializers.Serializer):
    """
    Serializer principale: Mappa la collezione API F5 (risposta della getList)
    che contiene una lista di Self IP sotto la chiave 'items'.
    """
    items = F5SelfItemSerializer(many=True, required=True)