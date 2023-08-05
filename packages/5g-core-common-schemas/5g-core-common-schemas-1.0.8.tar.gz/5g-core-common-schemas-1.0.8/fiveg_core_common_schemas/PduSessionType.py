# Copyright 2022 Guillaume Belanger
# See LICENSE file for licensing details.

from enum import Enum


class PduSessionType(str, Enum):
    IPV4 = "IPV4"
    IPV6 = "IPV6"
    IPV4V6 = "IPV4V6"
    UNSTRUCTURED = "UNSTRUCTURED"
    ETHERNET = "ETHERNET"
