# Copyright 2022 Guillaume Belanger
# See LICENSE file for licensing details.

from typing import List

from pydantic import BaseModel

from fiveg_core_common_schemas.NsiInformation import NsiInformation
from fiveg_core_common_schemas.Snssai import Snssai


class AllowedSNssai(BaseModel):
    allowedSNssai: Snssai
    nsiInformation: List[NsiInformation] = None
    mappedHomeSNssai: Snssai = None
