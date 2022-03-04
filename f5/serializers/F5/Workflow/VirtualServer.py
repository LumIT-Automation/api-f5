from rest_framework import serializers


class F5WorkflowVirtualServerSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class F5WorkflowVirtualServerInnerSerializer(serializers.Serializer):
            def __init__(self, plType, *args_, **kwargs_):
                super().__init__(*args_, **kwargs_)

                # Build different serializer basing on plType value.
                if plType.lower() == "pl4_snat":
                    pass # currently unused.

            class F5WorkflowVirtualServerInnerMonitorSerializer(serializers.Serializer):
                name = serializers.CharField(max_length=255, required=True)
                type = serializers.CharField(max_length=255, required=True)
                send = serializers.CharField(max_length=255, required=False)
                recv = serializers.CharField(max_length=255, required=False)

            class F5WorkflowVirtualServerInnerIruleSerializer(serializers.Serializer):
                name = serializers.CharField(max_length=255, required=True)
                code = serializers.CharField(max_length=255, required=False, allow_blank=True)

            class F5WorkflowVirtualServerInnerProfileSerializer(serializers.Serializer):
                name = serializers.CharField(max_length=255, required=True)
                type = serializers.CharField(max_length=255, required=True)
                defaultsFrom = serializers.CharField(max_length=255, required=False)
                context = serializers.ChoiceField(required=False, choices=("all", "clientside", "serverside"))
                cert = serializers.CharField(max_length=65535, required=False)
                key = serializers.CharField(max_length=65535, required=False)
                chain = serializers.CharField(max_length=65535, required=False, allow_blank=True)
                idleTimeout = serializers.IntegerField(required=False)

            class F5WorkflowVirtualServerInnerSnatPoolSerializer(serializers.Serializer):
                name = serializers.CharField(max_length=255, required=True)
                members = serializers.ListField(
                    child=serializers.IPAddressField(required=False),
                    required=False
                )

            class F5WorkflowVirtualServerInnerVSSerializer(serializers.Serializer):
                name = serializers.CharField(max_length=255, required=True)
                type = serializers.ChoiceField(required=True, choices=("L4", "L7"))
                snat = serializers.ChoiceField(required=True, choices=("none", "automap", "snat"))
                routeDomainId = serializers.CharField(max_length=255, required=False, allow_blank=True)
                destination = serializers.RegexField(
                    regex='^([01]?\d\d?|2[0-4]\d|25[0-5])(?:\.(?:[01]?\d\d?|2[0-4]\d|25[0-5])){3}(:\d*)?$',
                    required=True
                )
                mask = serializers.IPAddressField(required=True)
                source = serializers.RegexField(
                    regex='^([01]?\d\d?|2[0-4]\d|25[0-5])(?:\.(?:[01]?\d\d?|2[0-4]\d|25[0-5])){3}(?:/\d*)?$',
                    required=True
                )

            class F5WorkflowVirtualServerInnerPoolSerializer(serializers.Serializer):
                class F5WorkflowVirtualServerInnerNodesSerializer(serializers.Serializer):
                    name = serializers.CharField(max_length=255, required=True)
                    address = serializers.IPAddressField(required=True)
                    port = serializers.IntegerField(required=True)

                name = serializers.CharField(max_length=255, required=True)
                loadBalancingMode = serializers.CharField(max_length=255, required=False)
                nodes = F5WorkflowVirtualServerInnerNodesSerializer(required=True, many=True)

            virtualServer = F5WorkflowVirtualServerInnerVSSerializer(required=True)
            profiles = F5WorkflowVirtualServerInnerProfileSerializer(required=True, many=True)
            pool = F5WorkflowVirtualServerInnerPoolSerializer(required=True)
            snatPool = F5WorkflowVirtualServerInnerSnatPoolSerializer(required=False)
            monitor = F5WorkflowVirtualServerInnerMonitorSerializer(required=True)
            irules = F5WorkflowVirtualServerInnerIruleSerializer(required=False, many=True)

        # Build son serializer dynamically, passing the plType parameter.
        self.fields["data"] = F5WorkflowVirtualServerInnerSerializer(
            required=True,
            plType=kwargs["data"]["data"]["virtualServer"]["type"]
        )
