from enum import Enum

class SectorType(Enum):
    PUBLIC = "Public"
    PRIVATE = "Private"
    MIXED = "Mixed"

class Sector:
    def __init__(self, name: str, sector_type: SectorType):
        self.name = name
        self.sector_type = sector_type
        self.gdp_share = 0.0
        self.employment_share = 0.0
        self.efficiency = 0.0
        self.innovation_rate = 0.0
