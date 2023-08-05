# Copyright 2022 Guillaume Belanger
# See LICENSE file for licensing details.

from pydantic import BaseModel

from fiveg_core_common_schemas.EutraLocation import EutraLocation
from fiveg_core_common_schemas.N3gaLocation import N3gaLocation
from fiveg_core_common_schemas.NrLocation import NrLocation


class UserLocation(BaseModel):
    eutraLocation: EutraLocation = None
    nrLocation: NrLocation = None
    n3gaLocation: N3gaLocation = None
