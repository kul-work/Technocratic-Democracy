from enum import Enum
from datetime import datetime
from typing import List, Dict, Optional
import random

# Assuming these are imported from other modules
from citizen import Citizen
from legislative import Parliament

class ReferendumType(Enum):
    NATIONAL = "National"
    REGIONAL = "Regional"
    LOCAL = "Local"

class ReferendumStatus(Enum):
    PROPOSED = "Proposed"
    ACTIVE = "Active"
    COMPLETED = "Completed"
    FAILED = "Failed"

class Referendum:
    def __init__(self, title: str, description: str, referendum_type: ReferendumType):
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

class ExpertOrganization:
    def __init__(self, name: str, expertise_area: str):
        self.name: str = name
        self.expertise_area: str = expertise_area
        self.reputation: float = 0.5  # 0 to 1 scale
        self.delegated_votes: int = 0

class ReferendumSystem:
    def __init__(self, parliament: Parliament):
        self.parliament: Parliament = parliament
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

    def vote(self, citizen: Citizen, referendum: Referendum, vote: bool) -> bool:
        if referendum.status == ReferendumStatus.ACTIVE and citizen.age >= self.min_voting_age:
            if vote:
                referendum.votes_for += 1
            else:
                referendum.votes_against += 1
            referendum.total_votes += 1
            self.award_participation_points(citizen.id)
            return True
        return False

    def delegate_vote(self, citizen: Citizen, expert: ExpertOrganization, referendum: Referendum) -> bool:
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

# Example usage
parliament = Parliament(300)
citizens = [Citizen(random.randint(16, 80), f"Region_{i}") for i in range(10)]

# Propose and start a referendum
referendum = parliament.propose_referendum("New Economic Policy", "Description of the policy", ReferendumType.NATIONAL)
parliament.referendum_system.start_referendum(referendum)

# Simulate voting
for citizen in citizens:
    parliament.referendum_system.vote(citizen, referendum, random.choice([True, False]))

# Complete the referendum
parliament.referendum_system.complete_referendum(referendum)

# Check results
print(f"Referendum '{referendum.title}' results:")
print(f"Votes For: {referendum.votes_for}")
print(f"Votes Against: {referendum.votes_against}")
print(f"Total Votes: {referendum.total_votes}")
print(f"Status: {referendum.status}")
print(f"Blockchain Hash: {referendum.blockchain_hash}")

# Monitor referendums
print("\nReferendum Monitoring:")
monitoring_results = parliament.referendum_system.monitor_referendums()
for key, value in monitoring_results.items():
    print(f"{key.capitalize()}: {value}")
