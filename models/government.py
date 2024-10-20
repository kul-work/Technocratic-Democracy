from enum import Enum
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import random

from citizen import Citizen, CitizenshipStatus
from president import President
from legislative import Parliamentarian, Parliament, Chamber

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
        self.budget: 0.0

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

    def update_efficiency(self) -> None: # TODO - where to use this??
        if self.minister:
            self.efficiency = (self.efficiency + self.minister.expertise) / 2
        self.efficiency = max(0.5, min(1.0, self.efficiency))

class Government:
    def __init__(self, prime_minister: Parliamentarian):
        self.prime_minister = prime_minister
        self.ministries = {ministry_type: Ministry(ministry_type) for ministry_type in MinistryType}
        self.government_managers = []
        self.status = GovernmentStatus.ACTIVE
        self.formation_date = datetime.now()
        self.dissolution_date = self.formation_date + timedelta(days=3*365)
        self.emergency_end_date = None

    def appoint_government_manager(self, parliamentarian: Parliamentarian) -> bool:
        if len(self.government_managers) <= 3:
            self.government_managers.append(parliamentarian)
            return True
        return False

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
        # Simplified approval rating update based on ministry efficiencies
        avg_efficiency = sum(ministry.efficiency for ministry in self.ministries.values()) / len(self.ministries)
        self.approval_rating = (self.approval_rating + avg_efficiency * 100) / 2
        self.approval_rating = max(0, min(100, self.approval_rating))
