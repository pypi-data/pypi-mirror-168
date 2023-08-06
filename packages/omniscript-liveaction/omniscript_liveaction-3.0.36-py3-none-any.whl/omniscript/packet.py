"""Packet class.
"""
#Copyright (c) LiveAction, Inc. 2022. All rights reserved.
#Copyright (c) Savvius, Inc. 2013-2019. All rights reserved.
#Copyright (c) WildPackets, Inc. 2013-2014. All rights reserved.

import six

import omniscript

from .omniaddress import EthernetAddress, IPv4Address
from .omnierror import OmniError
from .omniport import OmniPort
from .peektime import PeekTime
# from .readstream import ReadStream

# from .omniscript import get_id_protocol_names


_packet_prop_dict = {
    'absoluteTime': 'timestamp',
    'address1': 'address_1',
    'address2': 'address_2',
    'address3': 'address_3',
    'address4': 'address_4',
    'application': 'application',
    'applicationId': 'application_id',
    'applicationColor': 'application_color',
    'band': 'band',
    'bssid': 'bssid',
    'dataRate': 'data_rate',
    'date': 'date',
    'deltaTime': 'delta_time',
    'destination': 'destination',
    'destinationCity': 'destination_city',
    'destinationCountry': 'destination_country',
    'destinationLatitude': 'destination_latitude',
    'destinationLogical': 'destination_logical',
    'destinationLongitude': 'destination_longitude',
    'destinationPhysical': 'destination_physical',
    'destinationPort': 'destination_port',
    'expert': 'expert',
    'filter': 'filter',
    'flags': 'flags',
    'flags80211': 'flags80211',
    'flowId': 'flow_id',
    'frequency': 'frequency',
    'fullDuplexChannel': 'full_duplex_channel',
    'ipIdentifier': 'ip_identifier',
    'ipLength': 'ip_length',
    'ipTTL': 'ip_ttl',
    'mcs': 'mcs',
    'mpls': 'mpls',
    'noisedBm': 'noise_dbm',
    'noiseStrength': 'noise_strength',
    'packetNumber': 'number',
    'protocol': 'protocol',
    'receiver': 'receiver',
    'relativeTime': 'relative_time',
    'signaldBm': 'signal_dbm',
    'signalStrength': 'signal_strength',
    'size': 'size',
    'sizeBar': 'size_bar',
    'source': 'source',
    'sourceCity': 'source_city',
    'sourceCountry': 'source_country',
    'sourceLatitude': 'source_latitude',
    'sourceLogical': 'source_logical',
    'sourceLongitude': 'source_longitude',
    'sourcePhysical': 'source_physical',
    'sourcePort': 'source_port',
    'spatialStreams': 'spatial_streams',
    'summary': 'summary',
    'summarySource': 'summary_source',
    'transmitter': 'transmitter',
    'vlan': 'vlan',
    'wanDirection': 'wan_direction',
    'wirelessChannel': 'wireless_channel'
}


class Packet(object):
    """The Packet class has packet information.
    The 
    :func:`get_packets() 
    <omniscript.capture.Capture.get_packets>`
    function returns a list of Packet objects.

    Packet number vs index: the packet number, which starts at 0, is a
    counter of the packets as they are captured. When a packet is
    captured the packet counter becomes the packet number of the packet
    and then the packet counter is incremented.
    The packet index is the index into the list of packets called the
    packet buffer.
    The first index in the packet buffer is 0. The first packet in the
    packet buffer, index 0, always contains the packet with the lowest
    packet number.
    
    A capture buffer can only hold a finite number of packets. Once
    the buffer  has filled and a new packet is captured then the
    first packet in the packet buffer (index 0) is deleted makeing what
    was the second packet (index 1) into the first packet (index 0).
    And the newly captured packet becomes the last packet in the buffer.

    The first_packet attribute of a
    :class:`Capture <omniscript.capture.Capture>`
    is the packet number of the first packet in the capture buffer.
    """

    address_1 = None
    """The first address."""

    address_2 = None
    """The second address.."""

    address_3 = None
    """The third address.."""

    address_4 = None
    """The fourth address.."""

    application = ''

    application_id = ''

    application_color = ''

    band = ''
    """   """

    bssid = ''
    """   """

    data = None
    """The packet data."""

    data_rate = 0
    """   """

    date = None
    """   """

    delta_time = None
    """   """

    destination = ''
    """Physical desination MAC Address."""

    destination_city = ''
    """   """

    destination_country = ''
    """   """

    destination_latitude = ''
    """   """

    destination_logical = ''
    """   """

    destination_longitude = ''
    """   """

    destination_physical = None
    """   """

    destination_port = None
    """   """

    expert = ''
    """   """

    filter = ''
    """   """

    flags = None
    """   """

    flags80211 = ''
    """   """

    flow_id = 0
    """   """

    frequency = ''
    """   """

    full_duplex_channel = ''
    """   """

    index = 0
    """The packet's index from the starting of the capture buffer."""

    ip_identifier = ''
    """   """

    ip_length = 0
    """   """

    ip_ttl = ''
    """   """

    mcs = ''
    """   """

    mpls = ''
    """   """

    noise_dbm = ''
    """   """

    noise_strength = ''
    """   """

    number = 0
    """The packet's number starting from when the capture starts."""

    packet_length = 0
    """   """

    protocol = ''
    """The packet's protocol."""

    receiver = ''
    """   """

    relative_time = None
    """   """

    signal_dbm = ''
    """   """

    signal_strength = ''
    """   """

    size_bar = ''
    """   """

    source = ''
    """Physical source MAC Address."""

    source_city = ''
    """   """

    source_country = ''
    """   """

    source_latitude = ''
    """   """

    source_logical = ''
    """   """

    source_longitude = ''
    """   """

    source_physical = ''
    """   """

    source_port = ''
    """   """

    spatial_streams = ''
    """   """

    status = 0
    """The packet's status."""

    summary = ''
    """   """

    summary_source = ''
    """   """

    timestamp = None
    """The packet's timestamp as
    :class:`PeekTime <omniscript.peektime.PeekTime>`.
    """

    transmitter = ''
    """   """

    vlan = ''
    """   """

    wan_direction = ''
    """   """

    wireless_channel = ''
    """   """

    def __init__(self, number=None, props=None, data=None):
        self.number = number if number and (number > 0) else Packet.number
        self.application = Packet.application
        self.data = Packet.data
        self.packet_length = Packet.packet_length
        self.flags = Packet.flags
        self.flow_id = Packet.flow_id
        self.packet_length = Packet.packet_length
        self.protocol = Packet.protocol
        self.status = Packet.status
        self.timestamp = None
        self.data = Packet.data
        self._load(props)
        self._load_data(data)

    def __str__(self):
        return f'Packet: {self.index}'

    @property
    def id(self):
        """The packet's identifier. (Read Only)"""
        return self.number

    @property
    def name(self):
        """The packet's number. (Read Only)"""
        return self.number

    @classmethod
    def get_prop_dict(cls):
        return _packet_prop_dict

    def _load(self, props):
        """Set attributes from a dictionary."""
        if isinstance(props, dict):
            missed = 0
            for k,v in props.items():
                a = _packet_prop_dict.get(k)
                if a is None or not hasattr(self, a):
                    continue
                if isinstance(getattr(self, a), six.string_types):
                    setattr(self, a, v if v else '')
                elif isinstance(getattr(self, a), int):
                    setattr(self, a, int(v) if v else 0)
                elif getattr(self, a) is None:
                    if a in ('address_1', 'address_2', 'address_3', 'address_4', 'destination',
                                'destination_logical', 'destination_physical', 'source',
                                'source_logical', 'source_physical'):
                        try:
                            setattr(self, a, EthernetAddress(v) if v else None)
                        except:
                            setattr(self, a, v)
                    elif a in ('destination_logical', 'source_logical'):
                        setattr(self, a, IPv4Address(v) if v else None)
                    elif a in ('destination_port', 'source_port'):
                        setattr(self, a, OmniPort(v) if v else None)
                    elif a in ('date', 'delta_time', 'relative_time', 'timestamp'):
                        setattr(self, a, PeekTime(v) if v else None)
                    elif a == 'flags':
                        setattr(self, a, v if v else [])
                    else:
                        missed += 1
                else:
                    missed += 1000

    def _load_data(self, data):
        if not data:
            return
        self.data = data
        self.packet_length = len(self.data)

    def data_length(self):
        """The number of bytes in the packet."""
        if self.data is not None:
            return len(self.data)
        return 0

    def is_sliced(self):
        """Is the packet sliced."""
        if self.data is None:
            return False
        return len(self.data) < self.packet_length

    def protocol_name(self):
        """The protocol name of the packet."""
        protocol_id_names = omniscript.get_id_protocol_names()
        if self.proto_spec & 0x0FFFF:
            return protocol_id_names[self.proto_spec & 0x0FFFF]
        return 'Unknown'


def _create_packet_list(props, first=0):
    if not isinstance(props, dict):
        return
    lst = []
    packets = props.get('packets')
    if isinstance(packets, list):
        for p in packets:
            lst.append(Packet(props=p))
    return lst
