from enum import Enum
import random

class EconomySectorType(Enum):
    PUBLIC = "Public"
    PRIVATE = "Private"
    MIXED = "Mixed"

class EconomySector:
    def __init__(self, name: str, sector_type: EconomySectorType):
        self.name = name
        self.sector_type = sector_type
        self.gdp_share = 0.0
        self.employment_share = 0.0
        self.efficiency = random.uniform(0.6, 0.9)
        self.innovation_rate = random.uniform(0.1, 0.3)
        self.budget = 0.0