# Copyright 2022 Guillaume Belanger
# See LICENSE file for licensing details.


from pydantic import BaseModel

from fiveg_core_common_schemas.Auts import Auts
from fiveg_core_common_schemas.Rand import Rand


class ResynchronizationInfo(BaseModel):
    rand: Rand
    auts: Auts
