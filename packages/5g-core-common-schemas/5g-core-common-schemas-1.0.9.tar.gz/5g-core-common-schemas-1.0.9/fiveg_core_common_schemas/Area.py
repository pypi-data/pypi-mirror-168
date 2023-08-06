# Copyright 2022 Guillaume Belanger
# See LICENSE file for licensing details.


from typing import List

from pydantic import BaseModel

from fiveg_core_common_schemas.AreaCode import AreaCode
from fiveg_core_common_schemas.Tac import Tac


class Area(BaseModel):
    tacs: List[Tac] = None
    areaCode: AreaCode = None
