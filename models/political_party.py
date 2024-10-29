from enum import Enum
from typing import List, Dict
import random
from config import *

from .citizen import Citizen
from .legislative import *

class Ideology(Enum):
    LEFT = "Left"
    CENTER_LEFT = "Center-Left"
    CENTER = "Center"
    CENTER_RIGHT = "Center-Right"
    RIGHT = "Right"

class PolicyArea(Enum):
    ECONOMY = "Economy"
    HEALTHCARE = "Healthcare"
    EDUCATION = "Education"
    ENVIRONMENT = "Environment"
    FOREIGN_POLICY = "Foreign Policy"
    SOCIAL_WELFARE = "Social Welfare"

class IdeologyScore:
    scores = {
        Ideology.LEFT: -1.0,
        Ideology.CENTER_LEFT: -0.5,
        Ideology.CENTER: 0.0,
        Ideology.CENTER_RIGHT: 0.5,
        Ideology.RIGHT: 1.0
    }

    @classmethod
    def get_score(cls, ideology: Ideology) -> float:
        return cls.scores.get(ideology, 0.0)

class PoliticalParty:
    def __init__(self, name: str, ideology: Ideology):
        self.name = name
        self.ideology = ideology
        self.members: List[int] = []  # List of citizen IDs
        self.popularity: float = 0.0
        self.funds: float = INITIAL_PARTY_FUNDS
        self.policies: Dict[PolicyArea, float] = {area: random.uniform(-1, 1) for area in PolicyArea}

    def recruit_member(self, citizen_id: int) -> None:
        if citizen_id not in self.members:
            self.members.append(citizen_id)
            self.popularity += 0.01

    def lose_member(self, citizen_id: int) -> None:
        if citizen_id in self.members:
            self.members.remove(citizen_id)
            self.popularity = max(0, self.popularity - 0.01)

    def campaign(self, budget: float) -> None:
        if self.funds >= budget:
            self.funds -= budget
            self.popularity += CAMPAIGN_POPULARITY_FACTOR * (budget / CAMPAIGN_COST_FACTOR) * random.random()

    def propose_policy(self, area: PolicyArea, strength: float) -> None:
        self.policies[area] = max(-1, min(1, strength))  # Ensure policy strength is between -1 and 1

    def receive_donation(self, amount: float) -> None:
        self.funds += amount

    def calculate_alignment(self, citizen: 'Citizen') -> float:
        return sum(abs(self.policies[area] - getattr(citizen, area.value.lower(), 0)) for area in PolicyArea)

class PoliticalSystem:
    def __init__(self):
        self.parties: List[PoliticalParty] = []

    def register_party(self, party: PoliticalParty) -> None:
        self.parties.append(party)

    def get_most_popular_parties(self, n: int) -> List[PoliticalParty]:
        return sorted(self.parties, key=lambda x: x.popularity, reverse=True)[:n]

    def total_popularity(self) -> float:
        return sum(party.popularity for party in self.parties)

    # NOTE: there are no parliamentary elections in this model
    def form_parliament(self, parliament: 'Parliament') -> None:
        total_seats = len(parliament.members)
        for party in self.parties:
            seats = int((party.popularity / self.total_popularity()) * total_seats)
            for _ in range(seats):
                if len(parliament.members) < total_seats:
                    new_member = Parliamentarian(None, Chamber.DEPUTIES)
                    new_member.party = party
                    parliament.add_member(new_member)

    def propose_legislation(self, parliament: 'Parliament') -> None:
        for party in self.get_most_popular_parties(3):  # Top 3 parties can propose legislation
            if random.random() < party.popularity / 5:  # Popularity affects chance of proposal
                policy_area = random.choice(list(PolicyArea))
                title = f"{party.ideology.value} {policy_area.value} Reform Act"
                content = f"Proposed by {party.name} to reform {policy_area.value} according to {party.ideology.value} principles."
                parliament.propose_legislation(title, party.name, content)

    def get_stability_score(self) -> float:
        """
        Calculate political stability based on:
        - Party system fragmentation
        - Total party popularity
        - Ideological distribution
        Returns value between 0 and 1
        """
        if not self.parties:
            return 0.0
            
        # Calculate party system fragmentation (less fragmentation = more stability)
        total_popularity = self.total_popularity()
        fragmentation = sum((party.popularity / total_popularity) ** 2 for party in self.parties)
        
        # Calculate ideological distribution (more centered = more stable)
        weighted_ideology = sum(IdeologyScore.get_score(party.ideology) * (party.popularity / total_popularity) 
                              for party in self.parties)
        ideology_stability = 1 - abs(weighted_ideology)  # Closer to center = more stable
        
        # Combine scores (weighted average)
        stability = (fragmentation * 0.6 + ideology_stability * 0.4)
        
        return stability
