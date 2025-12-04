from rest_framework import serializers


## 1. Serializer for Nested References

class F5SelfReferenceSerializer(serializers.Serializer):
    """Map reference fields as 'trafficGroupReference' or 'vlanReference'."""
    link = serializers.CharField(max_length=255, required=False)


## 2. Serializer for Single Item Self IP

class F5SelfItemSerializer(serializers.Serializer):
    """
    Serializer for a single Self IP object (the one shown in the JSON),
    which will be an 'item' in the API collection.
    """

    # System fields and identification
    kind = serializers.CharField(max_length=255, required=False)
    name = serializers.CharField(max_length=255, required=True)
    partition = serializers.CharField(max_length=255, required=False)
    fullPath = serializers.CharField(max_length=255, required=False)
    generation = serializers.IntegerField(required=False)
    selfLink = serializers.CharField(max_length=255, required=False)
    assetId = serializers.IntegerField(required=False)

    # Self IP specific fields
    address = serializers.CharField(max_length=255, required=True)
    addressSource = serializers.CharField(max_length=255, required=False)

    floating = serializers.CharField(max_length=255, required=False)
    inheritedTrafficGroup = serializers.CharField(max_length=255, required=False)

    trafficGroup = serializers.CharField(max_length=255, required=False)
    vlan = serializers.CharField(max_length=255, required=False)

    unit = serializers.IntegerField(required=False)

    # Nested Reference fields
    trafficGroupReference = F5SelfReferenceSerializer(required=False)
    vlanReference = F5SelfReferenceSerializer(required=False)


## 3. Root Serializer for Collection (Used by Controller)

class F5SelfsSerializer(serializers.Serializer):
    """
    Main serializer: Map collection API F5 (getList response)
    which contains a list of Self IPs under the 'items' key.
    """
    items = F5SelfItemSerializer(many=True, required=True)