from enum import Enum
from typing import List, Dict
import random

from .legislative import *

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

    def recruit_member(self, citizen_id: int) -> None:
        if citizen_id not in self.members:
            self.members.append(citizen_id)
            self.influence += 0.1

    def lose_member(self, citizen_id: int) -> None:
        if citizen_id in self.members:
            self.members.remove(citizen_id)
            self.influence = max(0, self.influence - 0.1)

    def organize_activity(self, activity: ActivityType) -> bool:
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
            return True
        return False

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

    #TODO - add Parliamentarian DEPUTY as link
    def propose_legislation(self, parliament: 'Parliament') -> None:
        for org in self.get_most_influential_orgs(3):  # Top 3 orgs can propose legislation
            if random.random() < org.influence / 10:  # Influence affects chance of proposal
                title = f"{org.cause.value} Improvement Act"
                content = f"Proposed by {org.name} to address {org.cause.value} issues."
                parliament.propose_legislation(title, org.name, content)

    #TODO - is this need it?
    def react_to_legislation(self, legislation: 'Legislation') -> None:
        for org in self.organizations:
            if legislation.title.lower().find(org.cause.value.lower()) != -1:
                activity = random.choice(list(ActivityType))
                if org.organize_activity(activity):
                    print(f"{org.name} organized a {activity.value} in response to '{legislation.title}'")
