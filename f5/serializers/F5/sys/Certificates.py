from rest_framework import serializers

from f5.serializers.F5.sys.Certificate import F5CertificateItemsSerializer


class F5CertificatesSerializer(serializers.Serializer):
    items = F5CertificateItemsSerializer(many=True)
