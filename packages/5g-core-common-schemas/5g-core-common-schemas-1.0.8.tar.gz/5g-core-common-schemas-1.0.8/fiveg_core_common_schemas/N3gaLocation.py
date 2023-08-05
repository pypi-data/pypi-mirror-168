# Copyright 2022 Guillaume Belanger
# See LICENSE file for licensing details.

from pydantic import BaseModel

from fiveg_core_common_schemas.Gci import Gci
from fiveg_core_common_schemas.Gli import Gli
from fiveg_core_common_schemas.HfcNodeId import HfcNodeId
from fiveg_core_common_schemas.Ipv4Addr import Ipv4Addr
from fiveg_core_common_schemas.Ipv6Addr import Ipv6Addr
from fiveg_core_common_schemas.LineType import LineType
from fiveg_core_common_schemas.Tai import Tai
from fiveg_core_common_schemas.TnapId import TnapId
from fiveg_core_common_schemas.TwapId import TwapId
from fiveg_core_common_schemas.Uinteger import Uinteger


class N3gaLocation(BaseModel):
    n3gppTai: Tai = None
    n3IwfId: str = None
    ueIpv4Addr: Ipv4Addr = None
    ueIpv6Addr: Ipv6Addr = None
    portNumber: Uinteger = None
    tnapId: TnapId = None
    twapId: TwapId = None
    hfcNodeId: HfcNodeId = None
    gli: Gli = None
    w5gbanLineType: LineType = None
    gci: Gci = None
