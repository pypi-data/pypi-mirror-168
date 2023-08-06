# Copyright 2022 Guillaume Belanger
# See LICENSE file for licensing details.

from enum import Enum


class RestrictionType(Enum):
    allowed_areas = "ALLOWED_AREAS"
    not_allowed_areas = "NOT_ALLOWED_AREAS"
