# Copyright 2022 Guillaume Belanger
# See LICENSE file for licensing details.

from pydantic import BaseModel

from fiveg_core_common_schemas.BitRate import BitRate


class Ambr(BaseModel):
    uplink: BitRate
    downlink: BitRate
