# Copyright 2022 Guillaume Belanger
# See LICENSE file for licensing details.


from pydantic import BaseModel

from fiveg_core_common_schemas.Nid import Nid
from fiveg_core_common_schemas.NrCellId import NrCellId
from fiveg_core_common_schemas.PlmnId import PlmnId


class Ncgi(BaseModel):
    plmnId: PlmnId
    nrCellId: NrCellId
    nid: Nid = None
