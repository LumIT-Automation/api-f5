from rest_framework import serializers


class F5CertificateUpdateSerializer(serializers.Serializer):
    class F5CertificateUpdateInnerSerializer(serializers.Serializer):
        class F5CertificateSerializer(serializers.Serializer):
            name = serializers.CharField(max_length=255, required=True) # @todo: only alphanumeric chars + .
            content_base64 = serializers.CharField(max_length=65535, required=True)

        class F5KeySerializer(serializers.Serializer):
            name = serializers.CharField(max_length=255, required=True) # @todo: only alphanumeric chars + .
            content_base64 = serializers.CharField(max_length=65535, required=True)

        virtualServerName = serializers.CharField(max_length=255, required=False)
        certificate = F5CertificateSerializer(required=True)
        key = F5KeySerializer(required=False)

    data = F5CertificateUpdateInnerSerializer(required=True)
