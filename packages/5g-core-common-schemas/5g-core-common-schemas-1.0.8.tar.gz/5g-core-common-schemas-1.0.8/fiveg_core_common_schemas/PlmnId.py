# Copyright 2022 Guillaume Belanger
# See LICENSE file for licensing details.

from pydantic import BaseModel

from fiveg_core_common_schemas.Mcc import Mcc
from fiveg_core_common_schemas.Mnc import Mnc


class PlmnId(BaseModel):
    mcc: Mcc
    mnc: Mnc
