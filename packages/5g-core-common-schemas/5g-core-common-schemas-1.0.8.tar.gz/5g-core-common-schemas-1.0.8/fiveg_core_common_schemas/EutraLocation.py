# Copyright 2022 Guillaume Belanger
# See LICENSE file for licensing details.

from pydantic import BaseModel

from fiveg_core_common_schemas.DateTime import DateTime
from fiveg_core_common_schemas.Ecgi import Ecgi
from fiveg_core_common_schemas.GlobalRanNodeId import GlobalRanNodeId
from fiveg_core_common_schemas.Tai import Tai


class EutraLocation(BaseModel):
    tai: Tai
    ecgi: Ecgi
    ignoreEcgi: bool = None
    ageOfLocationInformation: int = None
    ueLocationTimestamp: DateTime = None
    geographicalInformation: str = None
    geodeticInformation: str = None
    globalNgenbId: GlobalRanNodeId = None
    globalENbId: GlobalRanNodeId = None
