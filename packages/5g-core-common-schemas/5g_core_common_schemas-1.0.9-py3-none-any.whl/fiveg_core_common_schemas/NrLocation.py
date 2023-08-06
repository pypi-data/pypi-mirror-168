# Copyright 2022 Guillaume Belanger
# See LICENSE file for licensing details.

from pydantic import BaseModel

from fiveg_core_common_schemas.DateTime import DateTime
from fiveg_core_common_schemas.GlobalRanNodeId import GlobalRanNodeId
from fiveg_core_common_schemas.Ncgi import Ncgi
from fiveg_core_common_schemas.Tai import Tai


class NrLocation(BaseModel):
    tai: Tai
    ncgi: Ncgi
    ignoreNcgi: bool = None
    ageOfLocationInformation: int = None
    ueLocationTimestamp: DateTime = None
    geographicalInformation: str = None
    geodeticInformation: str = None
    globalGnbId: GlobalRanNodeId = None
