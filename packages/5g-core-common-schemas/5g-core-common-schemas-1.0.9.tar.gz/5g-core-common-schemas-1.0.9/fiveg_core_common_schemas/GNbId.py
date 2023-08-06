# Copyright 2022 Guillaume Belanger
# See LICENSE file for licensing details.

from pydantic import BaseModel


class GNbId(BaseModel):
    bitLength: int
    gNBValue: str
