# Copyright 2022 Guillaume Belanger
# See LICENSE file for licensing details.

from pydantic import BaseModel

from fiveg_core_common_schemas.Snssai import Snssai


class ConfiguredSnssai(BaseModel):
    configuredSnssai: Snssai
    mappedHomeSnssai: Snssai = None
