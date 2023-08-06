# Copyright 2022 Guillaume Belanger
# See LICENSE file for licensing details.

from pydantic import BaseModel

from fiveg_core_common_schemas.AmfId import AmfId
from fiveg_core_common_schemas.PlmnId import PlmnId


class Guami(BaseModel):
    plmnId: PlmnId
    amfId: AmfId
