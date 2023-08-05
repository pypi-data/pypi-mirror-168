# Copyright 2022 Guillaume Belanger
# See LICENSE file for licensing details.

from pydantic import BaseModel

from fiveg_core_common_schemas.ENbId import ENbId
from fiveg_core_common_schemas.GNbId import GNbId
from fiveg_core_common_schemas.N3IwfId import N3IwfId
from fiveg_core_common_schemas.NgeNbId import NgeNbId
from fiveg_core_common_schemas.Nid import Nid
from fiveg_core_common_schemas.PlmnId import PlmnId
from fiveg_core_common_schemas.TngfId import TngfId
from fiveg_core_common_schemas.WAgfId import WAgfId


class GlobalRanNodeId(BaseModel):
    plmnId: PlmnId
    n3IwfId: N3IwfId = None
    gNbId: GNbId = None
    ngeNbId: NgeNbId = None
    wagfId: WAgfId = None
    tngfId: TngfId = None
    nid: Nid = None
    eNbId: ENbId = None
