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
                monitorSubPath = serializers.CharField(max_length=255, required=False, allow_blank=True)
                type = serializers.CharField(max_length=255, required=True)
                send = serializers.CharField(max_length=255, required=False)
                recv = serializers.CharField(max_length=255, required=False)

            class F5WorkflowVirtualServerInnerIruleSerializer(serializers.Serializer):
                name = serializers.CharField(max_length=255, required=True)
                iruleSubPath = serializers.CharField(max_length=255, required=False, allow_blank=True)
                code = serializers.CharField(max_length=255, required=False, allow_blank=True)

            class F5WorkflowVirtualServerInnerProfileSerializer(serializers.Serializer):
                name = serializers.CharField(max_length=255, required=True)
                profileSubPath = serializers.CharField(max_length=255, required=False, allow_blank=True)
                type = serializers.CharField(max_length=255, required=True)
                defaultsFrom = serializers.CharField(max_length=255, required=False)
                context = serializers.ChoiceField(required=False, choices=("all", "clientside", "serverside"))
                cert = serializers.CharField(max_length=65535, required=False)
                certName = serializers.CharField(max_length=65535, required=False, allow_blank=True)
                key = serializers.CharField(max_length=65535, required=False)
                keyName = serializers.CharField(max_length=65535, required=False, allow_blank=True)
                chain = serializers.CharField(max_length=65535, required=False, allow_blank=True)
                chainName = serializers.CharField(max_length=65535, required=False, allow_blank=True)
                idleTimeout = serializers.IntegerField(required=False)

            class F5WorkflowVirtualServerInnerSnatPoolSerializer(serializers.Serializer):
                name = serializers.CharField(max_length=255, required=True)
                snatPoolSubPath = serializers.CharField(max_length=255, required=False, allow_blank=True)
                members = serializers.ListField(
                    child=serializers.IPAddressField(required=False),
                    required=False
                )

            class F5WorkflowVirtualServerInnerVSSerializer(serializers.Serializer):
                name = serializers.CharField(max_length=255, required=True)
                subPath = serializers.CharField(max_length=255, required=False, allow_blank=True)
                type = serializers.ChoiceField(required=True, choices=("L4", "L7"))
                snat = serializers.ChoiceField(required=True, choices=("none", "automap", "snat"))
                routeDomainId = serializers.CharField(max_length=255, required=False, allow_blank=True)
                destination = serializers.RegexField(
                    regex='^([01]?\d\d?|2[0-4]\d|25[0-5])(?:\.(?:[01]?\d\d?|2[0-4]\d|25[0-5])){3}(:\d*)?$',
                    required=True
                )
                mask = serializers.RegexField(
                    regex='(^(((255\.){3}(255|254|252|248|240|224|192|128|0+))|((255\.){2}(255|254|252|248|240|224|192|128|0+)\.0)|((255\.)(255|254|252|248|240|224|192|128|0+)(\.0+){2})|((255|254|252|248|240|224|192|128|0+)(\.0+){3}))$|any|any4|any6)',
                    required=True
                )
                source = serializers.RegexField(
                    regex='^([01]?\d\d?|2[0-4]\d|25[0-5])(?:\.(?:[01]?\d\d?|2[0-4]\d|25[0-5])){3}(?:/\d*)?$',
                    required=True
                )

            class F5WorkflowVirtualServerInnerPoolSerializer(serializers.Serializer):
                class F5WorkflowVirtualServerInnerNodesSerializer(serializers.Serializer):
                    name = serializers.CharField(max_length=255, required=True)
                    nodeSubPath = serializers.CharField(max_length=255, required=False, allow_blank=True)
                    address = serializers.RegexField(
                        regex=r"(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))(%[0-9]+)?$|^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}(%[0-9]+)?$|^any[46]?$",
                        required=True
                    )
                    port = serializers.IntegerField(required=True)

                name = serializers.CharField(max_length=255, required=True)
                poolSubPath = serializers.CharField(max_length=255, required=False, allow_blank=True)
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
