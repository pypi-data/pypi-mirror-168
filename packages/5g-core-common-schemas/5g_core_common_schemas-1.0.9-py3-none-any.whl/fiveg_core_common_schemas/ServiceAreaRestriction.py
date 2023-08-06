# Copyright 2022 Guillaume Belanger
# See LICENSE file for licensing details.

from typing import List

from pydantic import BaseModel

from fiveg_core_common_schemas.Area import Area
from fiveg_core_common_schemas.RestrictionType import RestrictionType
from fiveg_core_common_schemas.Uinteger import Uinteger


class ServiceAreaRestriction(BaseModel):
    restrictionType: RestrictionType = None
    areas: List[Area] = None
    maxNumOfTAs: Uinteger = None
    maxNumOfTAsForNotAllowedAreas: Uinteger = None
