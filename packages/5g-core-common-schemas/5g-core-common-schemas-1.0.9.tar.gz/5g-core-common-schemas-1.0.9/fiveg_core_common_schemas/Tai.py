# Copyright 2022 Guillaume Belanger
# See LICENSE file for licensing details.

from pydantic import BaseModel

from fiveg_core_common_schemas.PlmnId import PlmnId
from fiveg_core_common_schemas.Tac import Tac


class Tai(BaseModel):
    plmnId: PlmnId
    tac: Tac
