from enum import Enum
from typing import List, Dict, TYPE_CHECKING
from datetime import datetime, timedelta
import random
from config import *

if TYPE_CHECKING:
    from .citizen import Citizen
    from .legislative import *
from .government import *

class Ideology(Enum):
    FAR_LEFT = "Far-Left"
    LEFT = "Left"
    CENTER_LEFT = "Center-Left"
    CENTER = "Center"
    CENTER_RIGHT = "Center-Right"
    RIGHT = "Right"
    FAR_RIGHT = "Far-Right"

class PolicyArea(Enum):
    ECONOMY = "Economy"
    HEALTHCARE = "Healthcare"
    EDUCATION = "Education"
    ENVIRONMENT = "Environment"
    FOREIGN_POLICY = "Foreign Policy"
    SOCIAL_WELFARE = "Social Welfare"

class IdeologyScore:
    scores = {
        Ideology.FAR_LEFT: -1.0,
        Ideology.LEFT: -0.6,
        Ideology.CENTER_LEFT: -0.3,
        Ideology.CENTER: 0.0,
        Ideology.CENTER_RIGHT: 0.3,
        Ideology.RIGHT: 0.6,
        Ideology.FAR_RIGHT: 1.0
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

    def campaign_for_referendum(self, referendum) -> None:
        """
        Conducts a campaign regarding a referendum
        
        Args:
            referendum: The referendum object to campaign for/against
        """
        # Determine party stance (-1.0 to 1.0, where positive means support)
        party_stance = random.uniform(-1.0, 1.0)
        
        # Campaign intensity (0.0 to 1.0)
        campaign_intensity = random.uniform(0.3, 1.0)
        
        # Calculate campaign effectiveness based on party resources and popularity
        campaign_effectiveness = (
            self.resources * 0.4 +  # Party resources impact
            self.popularity * 0.4 +  # Party popularity impact
            campaign_intensity * 0.2  # Campaign intensity impact
        ) if hasattr(self, 'resources') and hasattr(self, 'popularity') else 0.5
        
        # Log campaign activity
        if hasattr(self, 'logger'):
            self.logger.info(
                f"Party {self.name} campaigning for referendum '{referendum.title}' "
                f"with stance {party_stance:.2f} and effectiveness {campaign_effectiveness:.2f}"
            )
        
        # Store campaign data in referendum object if it has the attribute
        if hasattr(referendum, 'campaign_data'):
            referendum.campaign_data[self.name] = {
                'stance': party_stance,
                'effectiveness': campaign_effectiveness,
                'intensity': campaign_intensity
            }

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
    
    def initiate_emergency_election(self) -> None:
        """Initiate emergency election procedures"""
        self.emergency_election_scheduled = True
        self.election_date = datetime.now() + timedelta(days=30)  # Schedule within 30 days
        
        # Notify all parties
        for party in self.parties:
            party.prepare_emergency_campaign()
        
        # Reset election-related variables
        self.votes_cast = 0
        self.election_results = {}

    def can_form_government(self) -> bool:
        """Check if conditions are met to form a new government"""
        if not self.emergency_election_scheduled:
            return False
            
        # Check if election date has passed
        if datetime.now() < self.election_date:
            return False
            
        # Check if there's a clear winner or viable coalition
        winning_party = max(self.election_results.items(), 
                          key=lambda x: x[1])[0] if self.election_results else None
        
        return winning_party is not None and self.election_results[winning_party] > 0.5

    def form_new_government(self) -> 'Government':
        """Form new government after emergency election"""
        if not self.can_form_government():
            raise ValueError("Cannot form government: conditions not met")
            
        winning_party = max(self.election_results.items(), key=lambda x: x[1])[0]
        prime_minister = winning_party.nominate_prime_minister()
        
        # Reset emergency election state
        self.emergency_election_scheduled = False
        self.election_date = None
        
        # Create and return new government
        return Government(prime_minister)

    def get_party_positions(self, referendum) -> Dict['PoliticalParty', float]:
    #def get_party_positions(self, referendum: 'Referendum') -> Dict['PoliticalParty', float]:
        """Get party positions on referendum (-1.0 to 1.0 scale)"""
        positions = {}
        for party in self.parties:
            # Calculate position based on party ideology and referendum type
            base_position = random.uniform(-0.3, 0.3)  # Some randomness
            ideology_factor = self._calculate_ideology_alignment(party, referendum)
            positions[party] = max(-1.0, min(1.0, base_position + ideology_factor))
        return positions

    def _calculate_ideology_alignment(self, party, referendum) -> float:
    #def _calculate_ideology_alignment(self, party: 'PoliticalParty', referendum: 'Referendum') -> float:
        """Calculate how well referendum aligns with party ideology"""
        # Implementation depends on your ideology and referendum type systems
        return random.uniform(-0.7, 0.7)  # Simplified version 
