from enum import Enum
from typing import Dict, List, Optional, TYPE_CHECKING
import random
from config import *

MIN_LEGAL_VOTING_AGE = 16

import importlib
economy = importlib.import_module(".economy", package=__package__)
media = importlib.import_module(".media", package=__package__)

# if TYPE_CHECKING:
#     from .economy import Economy
#     from .media import NewsCategory

from .political_party import Ideology, IdeologyScore

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
        # Electronic identity
        self.id = random.randint(10_000_000, 99_999_999)  # Simplified ID, should be a CNP
        self.electronic_signature = f"sig_{self.id}"  # Simplified signature

        # Basic demographics
        self.age = age
        self.sex = sex
        self.region = region
        # TODO: Add 'county' attribute and link it with 'region' | later
        self.citizenship_status = CitizenshipStatus.CITIZEN
        self.is_immigrant = False
        self.years_in_country = 0  # To immigrants only
        
        # Economic attributes
        self.income = random.uniform(1000, 5000)
        self.wealth = random.uniform(5000, 50000)
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
        self.political_ideology = random.uniform(-1, 1)  # Add this line: -1 (progressive) to 1 (conservative)
        self.civic_engagement = 0
        self.environmental_concern = 0
        
        # Behavior and lifestyle
        self.consumption = 0
        self.media_usage = {} # e.g., {"social_media": 70, "tv": 30, "newspapers": 20}
        self.leisure_activities = []
        
        # Identity attributes
        self.ethnicity = random.choice(list(Ethnicity))
        self.religion = random.choice(list(Religion))
        self.region_type = random.choice(list(RegionType))
        
        # Social metrics (0-100 scale)
        self.happiness = random.uniform(40, 80)
        self.trust_in_institutions = random.uniform(30, 70)
        self.socioeconomic_rating = random.uniform(20, 80)
                
        # Social interaction factors
        self.social_mobility = random.uniform(0, 1)
        self.community_involvement = random.uniform(0, 1)
        self.political_engagement = random.uniform(0, 1)

        self.trust_in_government = random.uniform(30, 70)  # Initial trust between 30-70%
        self.satisfaction_level = random.uniform(40, 60)   # Initial satisfaction between 40-60%
        self.education_level = random.uniform(0, 100)      # Education level 0-100%
        
        # Ensure we have an ID for tracking
        self.id = id(self)  # Use object id as unique identifier

    def has_voting_rights(self) -> bool:
        return self.citizenship_status == CitizenshipStatus.CITIZEN and self.age >= MIN_LEGAL_VOTING_AGE
    
    def update(self, economy, policies, social_environment) -> None:
    #def update(self, economy: 'Economy', policies: List['Policy'], social_environment: 'SocialEnvironment') -> None:
        # Logic for updating the citizen's state based on external factors
        if economy:
            self._update_economic_status(economy)
        if social_environment:
            self._update_social_factors(social_environment)
        if policies:
            self._apply_policy_effects(policies)
        self._age()

        # Ensure values stay within bounds
        # TODO: extend to all attributes
        self.happiness = max(0, min(100, self.happiness))
        self.trust_in_institutions = max(0, min(100, self.trust_in_institutions))
        self.socioeconomic_rating = max(0, min(100, self.socioeconomic_rating))
        self.community_involvement = max(0, min(1, self.community_involvement))
        self.political_engagement = max(0, min(1, self.political_engagement))

    def _update_economic_status(self, economy) -> None:
    #def _update_economic_status(self, economy: 'EconomyModel') -> None:
        # Update income, savings, and debt based on economic conditions
        # Check if economy is an instance of EconomicModel or a dict
        if hasattr(economy, 'simulate_month'):
            economy.simulate_month()
            # Use direct economy model data
            economic_impact = economy.get_gdp_growth()
        else:
            # Handle dictionary case
            # Use the economic indicators from the state dictionary
            economic_impact = (economy.get('gdp_growth', 0) 
                             if isinstance(economy, dict) else 0)

        # Update happiness and socioeconomic rating based on economic conditions
        self.happiness += random.uniform(-5, 5) + (economic_impact * 10)
        self.socioeconomic_rating += random.uniform(-2, 2) + (economic_impact * 5)
        
    def _update_social_factors(self, social_environment) -> None:
        # Handle both dictionary and object cases
        if isinstance(social_environment, dict):
            # Extract values from dictionary
            society_satisfaction = social_environment.get('citizen_satisfaction', 0)
            social_cohesion = social_environment.get('social_cohesion', 0)
            media_trust = social_environment.get('media_trust', 0)
        else:
            # Use object methods
            society_satisfaction = social_environment.get_satisfaction_score()
            social_cohesion = getattr(social_environment, 'social_cohesion', 0)
            media_trust = getattr(social_environment, 'media_trust', 0)

        # Update citizen's social attributes
        social_impact = (society_satisfaction + social_cohesion + media_trust) / 3
        self.happiness += random.uniform(-3, 3) + (social_impact * 5)
        #self.social_satisfaction += random.uniform(-2, 2) + (social_impact * 3)

    def _apply_policy_effects(self, policies) -> None:
        if not policies:
            return

        for policy in policies:
            # Handle both string and Policy object cases
            if isinstance(policy, str):
                policy_area = policy
                policy_strength = 0.5  # Default strength if not provided
            else:
                policy_area = policy.area.value if hasattr(policy.area, 'value') else policy.area
                policy_strength = policy.strength

            # Apply effects based on policy area
            if policy_area == 'ECONOMY':
                self.happiness += random.uniform(-2, 2) + (policy_strength * 3)
                self.economic_satisfaction += random.uniform(-1, 1) + (policy_strength * 2)
            elif policy_area == 'SOCIAL_WELFARE':
                self.happiness += random.uniform(-1, 3) + (policy_strength * 4)
                self.social_satisfaction += random.uniform(0, 2) + (policy_strength * 3)
            elif policy_area == 'HEALTHCARE':
                self.happiness += random.uniform(0, 2) + (policy_strength * 2)
                self.health += random.uniform(-1, 1) + (policy_strength * 2)
            # Add more policy areas as needed

        self.trust_in_institutions += random.uniform(-3, 3)

    def _age(self) -> None:
        # Increment age and apply age-related changes
        self.age += 1/12  # Assuming monthly updates
        # TODO: Add logic for life events, retirement, etc.

    def process_media_influence(self, news_cycle: List[Dict]) -> None:
        """Process media influence on citizen opinions and trust"""
        for news in news_cycle:
            # Base influence depends on citizen's education and media literacy
            influence_factor = min(1.0, (self.education_level / 100) * 0.7 + 0.3)
            
            # Add some randomness to make changes more likely
            random_factor = random.uniform(0.8, 1.2)
            
            # Get sentiment with a default of 0 if not present
            sentiment = news.get('sentiment', 0)
            
            # Calculate impact based on news properties and random factor
            impact = sentiment * influence_factor * random_factor * 20  # Increased multiplier
            
            # Apply changes to both trust and satisfaction
            self.trust_in_government += impact
            self.satisfaction_level += impact * 0.8  # Slightly less impact on satisfaction
            
            # Ensure values stay within bounds
            self.trust_in_government = max(0, min(100, self.trust_in_government))
            self.satisfaction_level = max(0, min(100, self.satisfaction_level))

    def decide_referendum_vote(self, referendum, media_coverage: Dict, party_positions: Dict) -> bool:
        """
        Decide vote on referendum based on multiple factors
        Returns: bool indicating support (True) or opposition (False)
        """
        # Use IdeologyScore class for ideology mapping
        for party, position in party_positions.items():
            party_ideology_position = IdeologyScore.get_score(party.ideology)
            if abs(self.political_ideology - party_ideology_position) < 0.3:
                # More likely to follow party's position if ideologically aligned
                return position

        # Base likelihood influenced by citizen's characteristics
        support_likelihood = 0.5  # Start neutral
        
        # Consider media influence
        media_influence = media_coverage.get('support_ratio', 0.5) - 0.5  # Convert to -0.5 to 0.5
        support_likelihood += media_influence * (1 - self.education_level/100) * 0.3
        
        # Personal factors
        if referendum.affects_economic:
            support_likelihood += (self.economic_satisfaction - 50) / 100 * 0.2
        if referendum.affects_social:
            support_likelihood += (self.social_satisfaction - 50) / 100 * 0.2
        
        # Add some randomness
        support_likelihood += random.uniform(-0.1, 0.1)
        
        return random.random() < max(0, min(1, support_likelihood))
