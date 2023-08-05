# Copyright 2022 Guillaume Belanger
# See LICENSE file for licensing details.

from pydantic import BaseModel

from fiveg_core_common_schemas.EutraCellId import EutraCellId
from fiveg_core_common_schemas.Nid import Nid
from fiveg_core_common_schemas.PlmnId import PlmnId


class Ecgi(BaseModel):
    plmnId: PlmnId
    eutraCellId: EutraCellId
    nid: Nid = None
