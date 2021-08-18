from rest_framework import serializers


class F5CertificateSerializer(serializers.Serializer):
    class F5CertificateInnerSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=255, required=True) # @todo: only alphanumeric chars + .
        content_base64 = serializers.CharField(max_length=65535, required=True)
        partition = serializers.CharField(max_length=65535, required=False)

    certificate = F5CertificateInnerSerializer(required=True)
