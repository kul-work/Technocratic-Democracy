from enum import Enum
from datetime import datetime, timedelta
from typing import List, Dict, Optional, TYPE_CHECKING
import random

#from .citizen import *
#from .legislative import *

import importlib
citizen = importlib.import_module(".citizen", package=__package__)
legislative = importlib.import_module(".legislative", package=__package__)

# if TYPE_CHECKING:
#     from .citizen import Citizen
#     from .legislative import Parliament

MAX_ADVISORS = 12
EMERGENCY_DURATION = 120  # days

class MinistryType(Enum):
    ECONOMY = "Ministry of Economy"
    FOREIGN_AFFAIRS = "Ministry of Foreign Affairs"
    DEFENSE = "Ministry of National Defense"
    EDUCATION = "Ministry of Education"
    HEALTH = "Ministry of Health"
    LABOR = "Ministry of Labor"
    CULTURE = "Ministry of Culture"

class GovernmentStatus(Enum):
    ACTIVE = "Active"
    DISSOLVED = "Dissolved"
    EMERGENCY = "State of Emergency"

class Advisor:
    def __init__(self, name: str):
        self.name = name
        self.is_minister = False
        self.expertise = random.uniform(0.5, 1.0)  # scale
        self.efficiency: float = random.uniform(0.5, 1.0)  # scale

class Ministry:
    def __init__(self, ministry_type: MinistryType):
        self.type = ministry_type
        self.advisors = []
        self.minister = None
        self.budget = 0.0
        self.efficiency = random.uniform(0.6, 0.9)  # Start with a random baseline efficiency

    def add_advisor(self, advisor: Advisor) -> bool:
        if len(self.advisors) <= MAX_ADVISORS:
            self.advisors.append(advisor)
            return True
        return False

    def set_minister(self, advisor: Advisor) -> bool:
        if advisor in self.advisors:
            if self.minister:
                self.minister.is_minister = False
            advisor.is_minister = True
            self.minister = advisor
            return True
        return False
    
    def allocate_budget(self, amount: float) -> None:
        self.budget = amount

    def update_efficiency(self) -> None:
        base_efficiency = self.efficiency
        
        # Minister's expertise influences efficiency
        if self.minister:
            minister_influence = self.minister.expertise * 0.3
            advisor_influence = sum(advisor.efficiency for advisor in self.advisors) / (len(self.advisors) if self.advisors else 1) * 0.2
            
            # Add some random fluctuation (-5% to +5%)
            random_factor = random.uniform(-0.05, 0.05)
            
            self.efficiency = base_efficiency + minister_influence + advisor_influence + random_factor
            self.efficiency = max(0.5, min(1.0, self.efficiency))

class Government:
    def __init__(self, prime_minister):
        self.prime_minister = prime_minister
        self.ministries = {ministry_type: Ministry(ministry_type) for ministry_type in MinistryType}
        self.government_managers = []
        self.status = GovernmentStatus.ACTIVE
        self.formation_date = datetime.now()
        self.dissolution_date = self.formation_date + timedelta(days=3*365)
        self.emergency_end_date = None
        self.total_budget = 0.0
        self.approval_rating = 50.0  # Start with a neutral approval rating

    def appoint_government_manager(self, parliamentarian) -> bool:
        if len(self.government_managers) <= 3:
            self.government_managers.append(parliamentarian)
            return True
        return False
    
    def form_ministries(self):
        for ministry_type in MinistryType:
            ministry = self.ministries[ministry_type]
            # Create some advisors
            for _ in range(random.randint(3, MAX_ADVISORS)):
                advisor = Advisor(f"Advisor {_}")
                ministry.add_advisor(advisor)
            
            # Set a random advisor as minister
            if ministry.advisors:
                minister = random.choice(ministry.advisors)
                ministry.set_minister(minister)

        self.allocate_budget()

    def initiate_emergency_decree(self, region: str) -> bool:
        # Simplified implementation
        return random.choice([True, False])

    def approve_emergency_decree(self, decree: str, affected_population: int) -> bool:
        # Simplified simulation of referendum
        return random.random() > 0.5

    def check_dissolution(self) -> bool:
        if datetime.now() >= self.dissolution_date:
            self.status = GovernmentStatus.DISSOLVED
            return True
        return False

    def declare_emergency(self) -> bool:
        if self.status != GovernmentStatus.EMERGENCY:
            self.status = GovernmentStatus.EMERGENCY
            self.emergency_end_date = datetime.now() + timedelta(days=120)
            return True
        return False

    def check_emergency_status(self) -> bool:
        if self.status == GovernmentStatus.EMERGENCY and datetime.now() >= self.emergency_end_date:
            self.status = GovernmentStatus.ACTIVE
            self.emergency_end_date = None
            return True
        return False
    
    def allocate_budget(self) -> None:
        for ministry in self.ministries.values():
            ministry.allocate_budget(self.total_budget / len(self.ministries))

    def update_approval_rating(self) -> None:
        # First update each ministry's efficiency
        for ministry in self.ministries.values():
            ministry.update_efficiency()
        
        # Calculate new approval rating based on ministry efficiencies
        avg_efficiency = sum(ministry.efficiency for ministry in self.ministries.values()) / len(self.ministries)
        self.approval_rating = (self.approval_rating + avg_efficiency * 100) / 2
        self.approval_rating = max(0, min(100, self.approval_rating))

    def adjust_economic_policy(self, influence_factor: float) -> None:
        """
        Adjusts the economic policy based on external influences (like news impact).
        
        Args:
            influence_factor (float): A factor that influences economic policy
                - Positive values (0 to 1) represent favorable economic conditions
                - Negative values (-1 to 0) represent unfavorable economic conditions
                
        Effects:
            - Adjusts the Ministry of Economy's efficiency
            - Updates the budget allocation if the impact is significant
            - May trigger emergency measures for extreme values
        """
        economy_ministry = self.ministries[MinistryType.ECONOMY]
        
        # Adjust ministry efficiency based on the influence factor
        # Clamp the result between 0.5 and 1.0
        new_efficiency = economy_ministry.efficiency + (influence_factor * 0.1)
        economy_ministry.efficiency = max(0.5, min(1.0, new_efficiency))
        
        # For significant economic changes, adjust the budget allocation
        if abs(influence_factor) > 0.5:
            # Increase or decrease the ministry's budget by up to 10%
            budget_change = economy_ministry.budget * (influence_factor * 0.1)
            economy_ministry.budget += budget_change
            
        # For extreme negative conditions, consider emergency measures
        if influence_factor < -0.8:
            self.declare_emergency()
