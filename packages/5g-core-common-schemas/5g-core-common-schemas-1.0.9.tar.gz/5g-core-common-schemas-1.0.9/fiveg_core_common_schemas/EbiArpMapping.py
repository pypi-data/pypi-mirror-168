# Copyright 2022 Guillaume Belanger
# See LICENSE file for licensing details.

from pydantic import BaseModel

from fiveg_core_common_schemas.Arp import Arp
from fiveg_core_common_schemas.EpsBearerId import EpsBearerId


class EbiArpMapping(BaseModel):
    epsBearerId: EpsBearerId
    arp: Arp
