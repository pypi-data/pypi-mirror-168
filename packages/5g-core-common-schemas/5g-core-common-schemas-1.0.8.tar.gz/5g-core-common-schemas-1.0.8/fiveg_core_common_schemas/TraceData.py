# Copyright 2022 Guillaume Belanger
# See LICENSE file for licensing details.


from pydantic import BaseModel

from fiveg_core_common_schemas.Ipv4Addr import Ipv4Addr
from fiveg_core_common_schemas.Ipv6Addr import Ipv6Addr
from fiveg_core_common_schemas.TraceDepth import TraceDepth


class TraceData(BaseModel):
    traceRef: str
    traceDepth: TraceDepth
    neTypeList: str
    eventList: str
    collectionEntityIpv4Addr: Ipv4Addr = None
    collectionEntityIpv6Addr: Ipv6Addr = None
    interfaceList: str = None
