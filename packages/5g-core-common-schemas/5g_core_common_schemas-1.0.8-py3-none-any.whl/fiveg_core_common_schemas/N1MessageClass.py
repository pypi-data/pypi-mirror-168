# Copyright 2022 Guillaume Belanger
# See LICENSE file for licensing details.

from enum import Enum


class N1MessageClass(str, Enum):
    fiveg_mm = "5GMM"
    sm = "SM"
    lpp = "LPP"
    sms = "SMS"
    updp = "UPDP"
    lcs = "LCS"
