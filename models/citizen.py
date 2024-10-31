from enum import Enum
from typing import Dict, List, Optional, TYPE_CHECKING
import random
from config import *

MIN_LEGAL_VOTING_AGE = 16

import importlib
economy = importlib.import_module(".economy", package=__package__)

# if TYPE_CHECKING:
#     from .economy import Economy

class CitizenshipStatus(Enum):
    CITIZEN = "Citizen"
    PERMANENT_RESIDENT = "Permanent Resident"
    TEMPORARY_RESIDENT = "Temporary Resident"
    UNDOCUMENTED = "Undocumented"

class EmploymentStatus(Enum):
    UNEMPLOYED = "Unemployed"
    EMPLOYED = "Employed"
    SELF_EMPLOYED = "Self-employed"
    STUDENT = "Student"
    RETIRED = "Retired"

class Religion(Enum):
    CHRISTIAN = "Christian"
    MUSLIM = "Muslim"
    JEWISH = "Jewish"
    BUDDHIST = "Buddhist"
    HINDU = "Hindu"
    ATHEIST = "Atheist"
    OTHER = "Other"

class Ethnicity(Enum):
    MAJORITY = "Majority"
    MINORITY_A = "Minority A"
    MINORITY_B = "Minority B"
    MINORITY_C = "Minority C"
    IMMIGRANT = "Immigrant"
    OTHER = "Other"

class RegionType(Enum):
    URBAN = "Urban"
    SUBURBAN = "Suburban"
    RURAL = "Rural"

class Citizen:
    def __init__(self, age: int, sex: str, region: str):
        # Basic demographics
        self.age = age
        self.sex = sex
        self.region = region
        
        # Identity attributes
        self.ethnicity = random.choice(list(Ethnicity))
        self.religion = random.choice(list(Religion))
        self.region_type = random.choice(list(RegionType))
        
        # Social metrics (0-100 scale)
        self.happiness = random.uniform(40, 80)
        self.trust_in_institutions = random.uniform(30, 70)
        self.socioeconomic_rating = random.uniform(20, 80)
        
        # Economic attributes
        self.income = random.uniform(1000, 5000)
        self.wealth = random.uniform(5000, 50000)
        
        # Social interaction factors
        self.social_mobility = random.uniform(0, 1)
        self.community_involvement = random.uniform(0, 1)
        self.political_engagement = random.uniform(0, 1)

    def has_voting_rights(self) -> bool:
        """Determine if citizen can vote based on age and other factors"""
        return self.age >= 18  # Basic age check, could add more conditions

    def update(self, economy_state, social_state, political_state):
        """Update citizen attributes based on various state factors"""
        # Update happiness based on economic situation
        if economy_state:
            self.happiness += random.uniform(-5, 5)
            self.socioeconomic_rating += random.uniform(-2, 2)
        
        # Update trust based on political situation
        if political_state:
            self.trust_in_institutions += random.uniform(-3, 3)
        
        # Update social factors
        if social_state:
            self.community_involvement += random.uniform(-0.1, 0.1)
            self.political_engagement += random.uniform(-0.1, 0.1)
        
        # Ensure values stay within bounds
        self.happiness = max(0, min(100, self.happiness))
        self.trust_in_institutions = max(0, min(100, self.trust_in_institutions))
        self.socioeconomic_rating = max(0, min(100, self.socioeconomic_rating))
        self.community_involvement = max(0, min(1, self.community_involvement))
        self.political_engagement = max(0, min(1, self.political_engagement))

        # Age the citizen
        self.age += 1/12  # Assuming monthly updates

