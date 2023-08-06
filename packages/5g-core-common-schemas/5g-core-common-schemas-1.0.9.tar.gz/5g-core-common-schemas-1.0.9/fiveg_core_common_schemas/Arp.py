# Copyright 2022 Guillaume Belanger
# See LICENSE file for licensing details.

from pydantic import BaseModel

from fiveg_core_common_schemas.ArpPriorityLevel import ArpPriorityLevel
from fiveg_core_common_schemas.PreemptionCapability import PreemptionCapability
from fiveg_core_common_schemas.PreemptionVulnerability import PreemptionVulnerability


class Arp(BaseModel):
    priorityLevel: ArpPriorityLevel
    preemptCap: PreemptionCapability
    preemptVuln: PreemptionVulnerability
