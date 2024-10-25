from enum import Enum
from typing import List, Dict
import random

from .legislative import *
from .economy_sector import EconomySectorType

class CauseType(Enum):
    ENVIRONMENTAL = "Environmental"
    SOCIAL_JUSTICE = "Social Justice"
    EDUCATION = "Education"
    HEALTHCARE = "Healthcare"
    HUMAN_RIGHTS = "Human Rights"
    ECONOMIC_EQUALITY = "Economic Equality"

class ActivityType(Enum):
    PROTEST = "Protest"
    PETITION = "Petition"
    AWARENESS_CAMPAIGN = "Awareness Campaign"
    LOBBYING = "Lobbying"
    LEGAL_ACTION = "Legal Action"
    RESEARCH = "Research"

class CivicOrganization:
    def __init__(self, name: str, cause: CauseType):
        self.name = name
        self.cause = cause
        self.members: List[int] = []  # List of citizen IDs
        self.influence: float = 0.0
        self.funds: float = 1000.0  # Starting funds
        self.sector_focus = random.choice([EconomySectorType.PUBLIC, EconomySectorType.PRIVATE, None])  # None means both
        self.sector_influence = {
            EconomySectorType.PUBLIC: random.uniform(0, 1),
            EconomySectorType.PRIVATE: random.uniform(0, 1)
        }

    def recruit_member(self, citizen_id: int) -> None:
        if citizen_id not in self.members:
            self.members.append(citizen_id)
            self.influence += 0.1

    def lose_member(self, citizen_id: int) -> None:
        if citizen_id in self.members:
            self.members.remove(citizen_id)
            self.influence = max(0, self.influence - 0.1)

    def organize_activity(self, activity: ActivityType, target_sector: EconomySectorType = None) -> bool:
        """Organize activity with specific sector focus"""
        if target_sector is None:
            target_sector = self.sector_focus if self.sector_focus else random.choice([EconomySectorType.PUBLIC, EconomySectorType.PRIVATE])
            
        cost = {
            ActivityType.PROTEST: 500,
            ActivityType.PETITION: 100,
            ActivityType.AWARENESS_CAMPAIGN: 1000,
            ActivityType.LOBBYING: 2000,
            ActivityType.LEGAL_ACTION: 5000,
            ActivityType.RESEARCH: 3000
        }

        if self.funds >= cost[activity]:
            self.funds -= cost[activity]
            self.influence += 0.5 * random.random()
            # Increase influence in target sector
            self.sector_influence[target_sector] += 0.1 * random.random()
            # Normalize influence
            self.sector_influence[target_sector] = min(1.0, self.sector_influence[target_sector])
            return True
        return False

    def propose_candidate(self, chamber):
        # Simplified candidate proposal
        return Parliamentarian(chamber)

    def receive_donation(self, amount: float) -> None:
        self.funds += amount
        self.influence += 0.01 * amount

class CivilSociety:
    def __init__(self):
        self.organizations: List[CivicOrganization] = []

    def register_organization(self, org: CivicOrganization) -> None:
        self.organizations.append(org)

    def get_most_influential_orgs(self, n: int) -> List[CivicOrganization]:
        return sorted(self.organizations, key=lambda x: x.influence, reverse=True)[:n]

    def total_influence(self) -> float:
        return sum(org.influence for org in self.organizations)

    #TODO: add Parliamentarian DEPUTY as link
    def propose_legislation(self, parliament) -> None:
        for org in self.get_most_influential_orgs(3):  # Top 3 orgs can propose legislation
            if random.random() < org.influence / 10:  # Influence affects chance of proposal
                title = f"{org.cause.value} Improvement Act"
                content = f"Proposed by {org.name} to address {org.cause.value} issues."
                parliament.propose_legislation(title, org.name, content)

    def react_to_legislation(self, legislation: 'Legislation') -> None:
        for org in self.organizations:
            if legislation.title.lower().find(org.cause.value.lower()) != -1:
                activity = random.choice(list(ActivityType))
                if org.organize_activity(activity):
                    print(f"{org.name} organized a {activity.value} in response to '{legislation.title}'")

    def get_cohesion_score(self) -> float:
        """
        Calculate social cohesion based on:
        - Organization diversity
        - Member participation
        - Cross-organization collaboration
        Returns value between 0 and 1
        """
        if not self.organizations:
            return 0.0
        
        # Calculate cause diversity
        unique_causes = len(set(org.cause for org in self.organizations))
        cause_diversity = min(1.0, unique_causes / len(CauseType))
        
        # Calculate member participation
        avg_members = sum(len(org.members) for org in self.organizations) / len(self.organizations)
        member_participation = min(1.0, avg_members / 1000)  # Normalize to 0-1
        
        # Calculate average influence
        avg_influence = sum(org.influence for org in self.organizations) / len(self.organizations)
        
        # Combine scores
        cohesion = (cause_diversity * 0.3 + 
                    member_participation * 0.4 + 
                    avg_influence * 0.3)
        
        return cohesion

    def increase_activism(self) -> None:
        """
        Increases civic activism during social unrest:
        - Intensifies organization activities
        - Increases influence gain
        - Organizes more frequent activities
        """
        for org in self.organizations:
            # Increase organization activities
            for _ in range(3):  # Organize multiple activities
                activity = random.choice(list(ActivityType))
                if org.organize_activity(activity):
                    # Double the normal influence gain during increased activism
                    org.influence += 0.5 * random.random()
            
            # Increase member recruitment efforts
            if org.funds >= 1000:
                org.funds -= 1000
                org.influence += 0.2  # Additional influence from increased visibility
