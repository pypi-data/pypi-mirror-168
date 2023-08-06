# Copyright 2022 Guillaume Belanger
# See LICENSE file for licensing details.

from enum import Enum


class AccessType(str, Enum):
    threegpp_access = "3GPP_ACCESS"
    non_threegpp_access = "NON_3GPP_ACCESS"
