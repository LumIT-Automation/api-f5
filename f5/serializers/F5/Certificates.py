from rest_framework import serializers


class F5CertificatesSerializer(serializers.Serializer):
    class F5CertificatesInnerSerializer(serializers.Serializer):
        class F5CertificatesItemsSerializer(serializers.Serializer):
            class F5CertificatesRawSerializer(serializers.Serializer):
                certificateKeySize = serializers.CharField(max_length=255, required=True)
                expiration = serializers.CharField(max_length=255, required=True)
                issuer = serializers.CharField(max_length=255, required=True)
                publicKeyType = serializers.CharField(max_length=255, required=True)

            class F5CertificatesValidatorsSerializer(serializers.Serializer):
                link = serializers.CharField(max_length=255, required=True)
                isSubcollection = serializers.BooleanField(required=True)

            name = serializers.CharField(max_length=255, required=True)
            fullPath = serializers.CharField(max_length=65535, required=True)
            generation = serializers.IntegerField(required=True)
            selfLink = serializers.CharField(max_length=65535, required=True)
            apiRawValues = F5CertificatesRawSerializer(required=True)
            city = serializers.CharField(max_length=65535, required=False)
            commonName = serializers.CharField(max_length=65535, required=False)
            country = serializers.CharField(max_length=65535, required=False)
            emailAddress = serializers.CharField(max_length=65535, required=False)
            fingerprint = serializers.CharField(max_length=65535, required=True)
            organization = serializers.CharField(max_length=65535, required=False)
            ou = serializers.CharField(max_length=65535, required=False)
            state = serializers.CharField(max_length=65535, required=False)
            certValidatorsReference = F5CertificatesValidatorsSerializer(required=True)

        items = F5CertificatesItemsSerializer(many=True)

    data = F5CertificatesInnerSerializer(required=True)
