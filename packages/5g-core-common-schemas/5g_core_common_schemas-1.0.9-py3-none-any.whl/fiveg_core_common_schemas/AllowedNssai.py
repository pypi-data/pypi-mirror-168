# Copyright 2022 Guillaume Belanger
# See LICENSE file for licensing details.

from typing import List

from pydantic import BaseModel

from fiveg_core_common_schemas.AllowedSNssai import AllowedSNssai


class AllowedNssai(BaseModel):
    allowedSNssai: List[AllowedSNssai]
