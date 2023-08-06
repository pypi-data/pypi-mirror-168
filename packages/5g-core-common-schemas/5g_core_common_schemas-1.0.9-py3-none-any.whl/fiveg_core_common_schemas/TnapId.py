# Copyright 2022 Guillaume Belanger
# See LICENSE file for licensing details.

from pydantic import BaseModel


class TnapId(BaseModel):
    ssId: str = None
    bssId: str = None
    civicAddress: bytes = None
