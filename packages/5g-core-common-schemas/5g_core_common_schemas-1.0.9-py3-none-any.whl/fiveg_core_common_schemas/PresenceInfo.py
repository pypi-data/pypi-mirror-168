# Copyright 2022 Guillaume Belanger
# See LICENSE file for licensing details.

from typing import List

from pydantic import BaseModel

from fiveg_core_common_schemas.Ecgi import Ecgi
from fiveg_core_common_schemas.GlobalRanNodeId import GlobalRanNodeId
from fiveg_core_common_schemas.Ncgi import Ncgi
from fiveg_core_common_schemas.PresenceState import PresenceState
from fiveg_core_common_schemas.Tai import Tai


class PresenceInfo(BaseModel):
    praId: str = None
    presenceState: PresenceState = None
    trackingAreaList: List[Tai] = None
    ecgiList: List[Ecgi] = None
    ncgiList: List[Ncgi] = None
    globalRanNodeIdList: List[GlobalRanNodeId] = None
