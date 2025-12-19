from typing import List, Dict

from f5.models.F5.net.backend.Interface import Interface as Backend

class Interface:
    def __init__(self, assetId: int, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.assetId: int = int(assetId)
        self.name: str = ""
        self.id: int = 0
        self.partition: str = ""
        self.fullPath: str = ""
        self.generation: int = 0
        self.connectionLimit: int = 0
        self.selfLink: str = ""

        self.strict: str = ""
        self.throughputCapacity: str = ""

        self.bundle: str = ""                   #Enables or disables bundle capability.
        self.bundleSpeed: str = ""              #Sets the bundle speed.The speed is applicable only when the bundle is enabled.
        self.description: str = ""              #User defined description.
        self.disabled: bool = False             #Disables the specified interfaces from passing traffic.
        self.enabled: bool = True               #Enables the specified interfaces to pass traffic.

        self.flowControl: str = ""              #Specifies how the system controls the sending of PAUSE frames.The default value is tx - rx.
        self.forceGigabitFiber: str = ""        #Enables or disables forcing of gigabit fiber media.If this is enabled for a gigabit fiber interface, the media setting will be forced, and no auto-negotiation will be performed.If it is disabled, auto-negotiation will be performed with just a single gigabit fiber option advertised.
        self.forwardErrorCorrection: str = ""   #Enables or disables IEEE 802.3bm Clause 91 Reed - Solomon Forward Error Correction(RS - FEC) on 100 G interfaces.Not valid for LR4 media.
        self.ifAlias: str = ""
        self.ifIndex: int                       #Displays the index assigned to this interface.It is a unique identifier assigned for all objects displayed in the SNMP IF-MIB.
        self.lldpAdmin: str = ""
        self.lldpTlvmap: int
        self.macAddress: str = ""               #Displays the MAC address(6 - byte Ethernet address in hexadecimal colon notation, for example, 00: 0 b: 0 9: 88:00: 9 a) of the interface.This is the hardware address.
        self.media: str = ""                    #Specifies the settings for the interface.When you set the media option, the system automatically sets the media-sfp or media-fixed option based on whether the interface is a small form factor pluggable (SFP) interface, or for combo ports whether SFP is the preferred port.
        self.mediaActive: str = ""              #Displays the current media settings for the interface.
        self.mediaFixed: str = ""               #Specifies the settings for a fixed( non - pluggable) interface.Use this option only with a combo port to specify the media type for the fixed interface, when it is not the preferred port.
        self.mediaMax: str = ""                 #Displays the maximum media value for the interface.
        self.mediaSfp: str = ""                 #Specifies the settings for an SFP( pluggable) interface.Use this option only with a combo port to specify the media type for the SFP interface, when it is not the preferred port.
        self.moduleDescription: str = ""
        self.mtu: int                           #Displays the maximum Transmission Unit(MTU) of the interface, which is the maximum number of bytes in a frame without IP fragmentation.
        self.portFwdMode: str = ""
        self.preferPort: str = ""               #Indicates which side of a combo port the interface uses, if both sides have the potential for an external link.The default value for a combo port is sfp.Do not use this option for non-combo ports.
        self.qinqEthertype: str = ""            #Specifies the protocol identifier associated with the tagged mode of the interface.
        self.serial: str = ""                   #Displays the serial number of the pluggable unit on an interface.
        self.stp: str = ""                      #Enables or disables STP.If you disable STP, no STP, RSTP, or MSTP packets are transmitted or received on the interface or trunk, and spanning tree has no control over forwarding or learning on the port or the trunk.The default value is enabled.
        self.stpAutoEdgePort: str = ""          #Sets STP automatic edge port detection for the interface.The default value is true.When automatic edge port detection is set to true for an interface, the system monitors the interface for incoming STP, RSTP, or MSTP packets.If no such packets are received for a sufficient period of time (about three seconds), the interface is automatically given edge port status.When automatic edge port detection is set to false for an interface, the system never gives the interface edge port status automatically.Any STP setting set on a per-interface basis applies to all spanning tree instances.
        self.stpEdgePort: str = ""              #Specifies whether the interface connects to an end station instead of another spanning tree bridge.The default value is true.
        self.stpLinkType: str = ""              #Specifies the STP link type for the interface.The default value is auto.The spanning tree system includes important optimizations that can only be used on point-to-point links, that is, on links which connect just two bridges.If these optimizations are used on shared links, incorrect or unstable behavior may result.By default, the implementation assumes that full-duplex links are point-to-point and that half-duplex links are shared.
        self.stpReset: bool                     #Resets STP, which forces a migration check.
        self.vendor: str = ""                   #Displays the name of the vendor of the pluggable unit on an interface.
        self.vendorOui: str = ""
        self.vendorPartnum: str = ""
        self.vendorRevision: str = ""



    ####################################################################################################################
    # Public static methods
    ####################################################################################################################

    @staticmethod
    def dataList(assetId: int) -> list:
        try:
            l = Backend.list(assetId)
            for el in l:
                el["assetId"] = assetId

            return l
        except Exception as e:
            raise e
