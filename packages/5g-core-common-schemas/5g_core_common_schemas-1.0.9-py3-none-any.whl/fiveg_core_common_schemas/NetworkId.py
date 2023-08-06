# Copyright 2022 Guillaume Belanger
# See LICENSE file for licensing details.

from pydantic import BaseModel

from fiveg_core_common_schemas.Mcc import Mcc
from fiveg_core_common_schemas.Mnc import Mnc


class NetworkId(BaseModel):
    mcc: Mcc = None
    mnc: Mnc = None
