from enum import Enum
from datetime import datetime
from typing import List, Dict, Optional, TYPE_CHECKING
import random
import uuid

#from .citizen import *
#from .legislative import Parliament

import importlib
citizen = importlib.import_module(".citizen", package=__package__)
legislative = importlib.import_module(".legislative", package=__package__)

# if TYPE_CHECKING:
#     from .citizen import Citizen
#     from .legislative import Parliament

class ReferendumType(Enum):
    NATIONAL = "National"
    REGIONAL = "Regional"
    LOCAL = "Local"
    PRESIDENTIAL_REVIEW = "Presidential Review" #TODO: is this needed?

class ReferendumStatus(Enum):
    PROPOSED = "Proposed"
    ACTIVE = "Active"
    COMPLETED = "Completed"
    FAILED = "Failed"

class Referendum:
    def __init__(self, title: str, description: str, referendum_type: ReferendumType):
        self.id = str(uuid.uuid4())
        self.title: str = title
        self.description: str = description
        self.type: ReferendumType = referendum_type
        self.status: ReferendumStatus = ReferendumStatus.PROPOSED
        self.votes_for: int = 0
        self.votes_against: int = 0
        self.total_votes: int = 0
        self.quorum: int = 0
        self.min_votes: int = 0
        self.start_date: Optional[datetime] = None
        self.end_date: Optional[datetime] = None
        self.documentation: str = ""
        self.summary: str = ""
        self.blockchain_hash: str = ""
        
        # Add impact areas with default False
        self.affects_economic: bool = False
        self.affects_social: bool = False
        self.affects_political: bool = False
        self.affects_environmental: bool = False
        self.affects_foreign: bool = False
        
        # Determine impacts based on title and description
        self._analyze_impacts()
    
    def _analyze_impacts(self) -> None:
        """Analyze title and description to determine what areas this referendum affects"""
        text = (self.title + " " + self.description).lower()
        
        # Economic impacts
        economic_keywords = {'economy', 'economic', 'tax', 'budget', 'financial', 'fiscal', 'trade'}
        self.affects_economic = any(keyword in text for keyword in economic_keywords)
        
        # Social impacts
        social_keywords = {'social', 'welfare', 'education', 'health', 'housing', 'community'}
        self.affects_social = any(keyword in text for keyword in social_keywords)
        
        # Political impacts
        political_keywords = {'political', 'government', 'election', 'voting', 'parliament'}
        self.affects_political = any(keyword in text for keyword in political_keywords)
        
        # Environmental impacts
        environmental_keywords = {'environment', 'climate', 'pollution', 'energy', 'green'}
        self.affects_environmental = any(keyword in text for keyword in environmental_keywords)
        
        # Foreign policy impacts
        foreign_keywords = {'foreign', 'international', 'diplomatic', 'treaty', 'eu', 'nato'}
        self.affects_foreign = any(keyword in text for keyword in foreign_keywords)

class ExpertOrganization:
    def __init__(self, name: str, expertise_area: str):
        self.name: str = name
        self.expertise_area: str = expertise_area
        self.reputation: float = 0.5  # 0 to 1 scale
        self.delegated_votes: int = 0

class ReferendumSystem:
    def __init__(self, parliament):
        self.parliament = parliament
        self.referendums: List[Referendum] = []
        self.expert_organizations: List[ExpertOrganization] = []
        self.participation_points: Dict[int, int] = {}  # Citizen ID to points
        self.min_voting_age: int = 16
        self.quorum_percentage: float = 0.5  # Default 50%
        self.min_votes_percentage: float = 0.3  # Default 30%

    def propose_referendum(self, title: str, description: str, referendum_type: ReferendumType) -> Referendum:
        referendum = Referendum(title, description, referendum_type)
        self.referendums.append(referendum)
        return referendum

    def start_referendum(self, referendum: Referendum) -> bool:
        if referendum.status == ReferendumStatus.PROPOSED:
            referendum.status = ReferendumStatus.ACTIVE
            referendum.start_date = datetime.now()
            referendum.quorum = int(self.parliament.total_seats * self.quorum_percentage)
            referendum.min_votes = int(self.parliament.total_seats * self.min_votes_percentage)
            return True
        return False

    def vote(self, citizen, referendum: Referendum, vote: bool) -> bool:
        if referendum.status == ReferendumStatus.ACTIVE and citizen.age >= self.min_voting_age:
            if vote:
                referendum.votes_for += 1
            else:
                referendum.votes_against += 1
            referendum.total_votes += 1
            self.award_participation_points(citizen.id)
            return True
        return False

    def delegate_vote(self, citizen, expert: ExpertOrganization, referendum: Referendum) -> bool:
        if referendum.type in [ReferendumType.REGIONAL, ReferendumType.LOCAL]:
            expert.delegated_votes += 1
            return True
        return False

    def complete_referendum(self, referendum: Referendum) -> bool:
        if referendum.status == ReferendumStatus.ACTIVE:
            referendum.end_date = datetime.now()
            if referendum.total_votes >= referendum.quorum and referendum.total_votes >= referendum.min_votes:
                referendum.status = ReferendumStatus.COMPLETED
            else:
                referendum.status = ReferendumStatus.FAILED
            self.record_blockchain(referendum)
            return True
        return False

    def award_participation_points(self, citizen_id: int) -> None:
        if citizen_id not in self.participation_points:
            self.participation_points[citizen_id] = 0
        self.participation_points[citizen_id] += 1

    def record_blockchain(self, referendum: Referendum) -> None:
        # Simulate a blockchain recording
        referendum.blockchain_hash = f"hash_{random.randint(1000, 9999)}"

    def update_quorum_requirements(self) -> None:
        # This method would be called biannually to update quorum requirements
        pass

    def monitor_referendums(self) -> Dict[str, int]:
        # Simple monitoring method
        return {
            "total": len(self.referendums),
            "active": sum(1 for ref in self.referendums if ref.status == ReferendumStatus.ACTIVE),
            "completed": sum(1 for ref in self.referendums if ref.status == ReferendumStatus.COMPLETED),
            "failed": sum(1 for ref in self.referendums if ref.status == ReferendumStatus.FAILED)
        }

    def create_presidential_review_referendum(self, law, president) -> Referendum:
    #def create_presidential_review_referendum(self, law: 'Law', president: 'President') -> Referendum:
        """
        Creates a special referendum for a presidential review of an already promulgated law.
        
        Args:
            law: The promulgated law to be reviewed
            president: The president initiating the review
            
        Returns:
            Referendum: The created referendum object
        """
        title = f"Presidential Review: {law.title}"
        description = (
            f"Presidential review referendum initiated by {president.name} "
            f"for the law: {law.title}.\n\n"
            f"Original Law Description: {law.description}"
        )
        
        referendum = self.propose_referendum(
            title=title,
            description=description,
            referendum_type=ReferendumType.PRESIDENTIAL_REVIEW
        )
        
        # Set special parameters for presidential review referendums
        referendum.documentation = law.full_text
        referendum.summary = (
            f"This referendum was initiated by the President to review "
            f"the previously promulgated law '{law.title}'. "
            f"If the referendum fails, the law will be returned to Parliament "
            f"for revision or repeal."
        )
        
        # Presidential review referendums start immediately
        self.start_referendum(referendum)
        return referendum

    def handle_presidential_review_result(self, referendum: Referendum) -> bool:
        """
        Handles the result of a presidential review referendum.
        
        Args:
            referendum: The completed presidential review referendum
            
        Returns:
            bool: True if the law is confirmed, False if it should be returned to Parliament
        """
        if referendum.status != ReferendumStatus.COMPLETED:
            return False
            
        # Law is confirmed if majority votes in favor
        return referendum.votes_for > referendum.votes_against
