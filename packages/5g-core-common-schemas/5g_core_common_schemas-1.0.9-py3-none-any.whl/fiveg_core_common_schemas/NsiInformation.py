# Copyright 2022 Guillaume Belanger
# See LICENSE file for licensing details.

from pydantic import BaseModel

from fiveg_core_common_schemas.Fqdn import Fqdn
from fiveg_core_common_schemas.NsiId import NsiId


class NsiInformation(BaseModel):
    nrfId: Fqdn
    nsiId: NsiId = None
