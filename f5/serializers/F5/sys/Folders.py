from rest_framework import serializers

from f5.serializers.F5.sys.Folder import F5FolderSerializer


class F5FoldersSerializer(serializers.Serializer):
    items = F5FolderSerializer(many=True)
