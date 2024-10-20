from enum import Enum
from typing import Dict, List, Optional
import random

MIN_LEGAL_VOTING_AGE = 16

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

class Citizen:
    def __init__(self, age: int, sex: str, region: str):

        # Electronic identity
        self.id = random.randint(10_000_000, 99_999_999)  # Simplified ID, should be a CNP
        self.electronic_signature = f"sig_{self.id}"  # Simplified signature

        # Demographic characteristics
        self.age = age
        self.sex = sex
        self.region = region
        # TODO: Add 'county' attribute and link it with 'region'
        self.citizenship_status = CitizenshipStatus.CITIZEN
        self.is_immigrant = False
        self.years_in_country = 0  # To immigrants only
        
        # Economic factors
        self.income = 0
        self.savings = 0
        self.debt = 0
        # Evaluation of socioeconomic status (0-100)
        # Can include factors such as income, education, occupation
        self.socioeconomic_rating = 0
        
        # Social factors
        self.education_level = 0
        self.health = 100
        self.happiness = 50
        self.social_capital = 0
        self.trust_in_institutions = 0
        
        # Work factors
        self.employment_status = "Unemployed"
        self.job_satisfaction = 0
        self.work_life_balance = 0
        
        # Political factors
        self.political_leaning = float = random.uniform(-1, 1)  # From -1 (left wing) to 1 (right wing)
        self.civic_engagement = 0
        self.environmental_concern = 0
        
        # Behavior and lifestyle
        self.consumption = 0
        self.media_usage = {} # e.g., {"social_media": 70, "tv": 30, "newspapers": 20}
        self.leisure_activities = []

    def has_voting_rights(self) -> bool:
        return self.citizenship_status == CitizenshipStatus.CITIZEN and self.age >= MIN_LEGAL_VOTING_AGE
        
    def update(self, economy, policies, social_environment) -> None:
    #def update(self, economy: 'Economy', policies: List['Policy'], social_environment: 'SocialEnvironment') -> None:
        # Logic for updating the citizen's state based on external factors
        self._update_economic_status(economy)
        self._update_social_factors(social_environment)
        self._apply_policy_effects(policies)
        self._age()

    def _update_economic_status(self, economy) -> None:
    #def _update_economic_status(self, economy: 'Economy') -> None:
        # Update income, savings, and debt based on economic conditions
        pass

    def _update_social_factors(self, social_environmen) -> None:
    #def _update_social_factors(self, social_environment: 'SocialEnvironment') -> None:
        # Update happiness, social capital, and trust based on social conditions
        pass

    def _apply_policy_effects(self, policies) -> None:
    #def _apply_policy_effects(self, policies: List['Policy']) -> None:
        # Apply the effects of various policies on the citizen
        pass

    def _age(self) -> None:
        # Increment age and apply age-related changes
        self.age += 1
        # TODO: Add logic for life events, retirement, etc.

# TODO: link the 'Economy' class to EconomicModel
# TODO: develop the 'Policy' and 'SocialEnvironment' classes
