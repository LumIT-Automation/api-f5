from rest_framework import serializers


class F5CertificateItemsSerializer(serializers.Serializer):
    class F5CertificatesRawSerializer(serializers.Serializer):
        certificateKeySize = serializers.CharField(max_length=255, required=False)
        expiration = serializers.CharField(max_length=255, required=False)
        issuer = serializers.CharField(max_length=255, required=False)
        publicKeyType = serializers.CharField(max_length=255, required=False)

    class F5CertificatesValidatorsSerializer(serializers.Serializer):
        link = serializers.CharField(max_length=255, required=False)
        isSubcollection = serializers.BooleanField(required=False)

    assetId = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=255, required=True) # @todo: only alphanumeric chars + .
    partition = serializers.CharField(max_length=255, required=False)
    fullPath = serializers.CharField(max_length=65535, required=False)
    generation = serializers.IntegerField(required=False)
    selfLink = serializers.CharField(max_length=65535, required=False)
    apiRawValues = F5CertificatesRawSerializer(required=False)
    city = serializers.CharField(max_length=65535, required=False)
    commonName = serializers.CharField(max_length=65535, required=False)
    country = serializers.CharField(max_length=65535, required=False)
    emailAddress = serializers.CharField(max_length=65535, required=False)
    fingerprint = serializers.CharField(max_length=65535, required=False)
    organization = serializers.CharField(max_length=65535, required=False)
    ou = serializers.CharField(max_length=65535, required=False)
    state = serializers.CharField(max_length=65535, required=False)
    certValidatorsReference = F5CertificatesValidatorsSerializer(required=False)
    content_base64 = serializers.CharField(max_length=65535, required=True)



class F5CertificateSerializer(serializers.Serializer):
    certificate = F5CertificateItemsSerializer(required=True)
