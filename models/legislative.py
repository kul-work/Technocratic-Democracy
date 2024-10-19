from enum import Enum
from typing import List, Optional
import random

class Chamber(Enum):
    SENATE = "Senate"
    DEPUTIES = "Chamber of Deputies"

class ParliamentaryStatus(Enum):
    ACTIVE = "Active"
    ON_BREAK = "On Break"
    FORMER = "Former"  # Useful for historical tracking and analytics
    GOVERNMENT_MEMBER = "Government Member"

class GovernmentRole(Enum):
    NONE = "None"
    PRIME_MINISTER = "Prime Minister"
    GOVERNMENT_MANAGER = "Government Manager"

class ActivityScore:
    def __init__(self):
        self.legislative_initiatives = 0
        self.speeches_given = 0
        self.committee_participations = 0

    def calculate(self) -> int:
        return (
            self.legislative_initiatives * 3 +
            self.speeches_given +
            self.committee_participations * 2
        )

class Parliamentarian:
    def __init__(self, id: Optional[int], chamber: Optional[Chamber]):
        self.id = id
        self.chamber = chamber
        self.years_served = 0
        self.consecutive_terms = 0  # TODO: Implement detailed term logic (2 vs 4 years, max 3 consecutive terms)
        self.activity_score = ActivityScore()
        self.status = ParliamentaryStatus.ACTIVE
        self.is_minority = False
        self.is_scholarship = False
        self.admission_committee_member = False
        self.government_role = GovernmentRole.NONE
        self.political_party: None


    def update_status(self) -> None:
        if self.government_role != GovernmentRole.NONE:
            self.status = ParliamentaryStatus.GOVERNMENT_MEMBER
        elif self.years_served >= 10:
            self.status = ParliamentaryStatus.ON_BREAK
            self.years_served = 0
            self.consecutive_terms = 0
        else:
            self.status = ParliamentaryStatus.ACTIVE

    def get_activity_score(self) -> int:
        return self.activity_score.calculate()
    
    def assign_government_role(self, role) -> None:
        self.government_role = role
        self.update_status()

    def remove_government_role(self) -> None:
        self.government_role = GovernmentRole.NONE
        self.update_status()

# TODO: Move this to a separate file for civic organizations
class CivicOrganization:
    def __init__(self, name: str):
        self.name = name

    def propose_candidate(self, chamber) -> Parliamentarian:
        # Simplified candidate proposal
        return Parliamentarian(None, chamber)
    
class Legislation:
    def __init__(self, title: str, proposer: str, content: str):
        self.title = title
        self.proposer = proposer
        self.content = content
        self.votes_for = 0
        self.votes_against = 0
        self.abstentions = 0
        self.status = "Proposed"

    def calculate_result(self) -> bool:
        return self.votes_for > self.votes_against

class Parliament:
    def __init__(self, total_seats):
        self.total_seats = total_seats
        self.senate_seats = int(total_seats * 0.3)
        self.deputy_seats = total_seats - self.senate_seats
        self.members = []
        self.admission_committee = []
        self.quorum_percentage = 0.5  # 50% of members required for quorum
        self.proposed_legislation = []
        self.passed_legislation = []
        self.failed_legislation = []

    def add_member(self, member: Parliamentarian) -> bool:
        if len(self.members) < self.total_seats:
            member.id = len(self.members) + 1
            self.members.append(member)
            return True
        return False

    def remove_member(self, member: Parliamentarian) -> None:
        self.members.remove(member)
        member.status = ParliamentaryStatus.FORMER

    def update_all_members(self) -> None:
        for member in self.members:
            member.years_served += 1
            member.update_status()

    def conduct_admission_interview(self, candidate: Parliamentarian) -> bool:
        # Simplified admission process
        return random.random() > 0.3  # 70% chance of admission
        
    def has_quorum(self):
        active_members = sum(1 for member in self.members if member.status == ParliamentaryStatus.ACTIVE)
        return active_members >= self.total_seats * self.quorum_percentage

    # TODO: remove this??
    def propose_internal_legislation(self) -> bool:
        if not self.has_quorum():
            print("Cannot propose legislation: No quorum")
            return False
        # Simplified internal legislation proposal
        return random.random() > 0.5  # 50% chance of proposal acceptance

    # TODO: remove this??
    def process_external_legislation(self, organization: CivicOrganization) -> bool:
        if not self.has_quorum():
            print("Cannot process legislation: No quorum")
            return False
        # Simplified external legislation proposal
        return random.random() > 0.6  # 40% chance of proposal acceptance
    
    def propose_legislation(self, title: str, proposer: str, content: str) -> bool:
        if not self.has_quorum():
            print("Cannot propose legislation: No quorum")
            return False
        legislation = Legislation(title, proposer, content)
        self.proposed_legislation.append(legislation)
        return True

    def vote_on_legislation(self, legislation: Legislation) -> bool:
        if not self.has_quorum():
            print("Cannot vote: No quorum")
            return False
        for member in self.members:
            if member.status == ParliamentaryStatus.ACTIVE:
                vote = random.random()
                if vote > 0.6:
                    legislation.votes_for += 1
                elif vote > 0.3:
                    legislation.votes_against += 1
                else:
                    legislation.abstentions += 1
        result = legislation.calculate_result()
        if result:
            self.passed_legislation.append(legislation)
            legislation.status = "Passed"
        else:
            self.failed_legislation.append(legislation)
            legislation.status = "Failed"
        self.proposed_legislation.remove(legislation)
        return result

    def vote_no_confidence(self) -> bool:
        if not self.has_quorum():
            print("Cannot vote: No quorum")
            return False
        # Simplified no-confidence vote
        return random.random() > 0.7  # 30% chance of success

    def nominate_for_admission_committee(self, member: Parliamentarian) -> bool:
        if member.years_served >= 10 and member.get_activity_score() > 50:
            return True
        return False

    def vote_for_admission_committee(self, nominee: Parliamentarian) -> bool:
        # Simplified voting process
        return random.random() > 0.4  # 60% chance of approval
    
    def initiate_presidential_suspension(self) -> bool:
        # Simplified logic for initiating presidential suspension
        return random.random() > 0.9

    def conduct_suspension_referendum(self) -> bool:
        # Simplified logic for conducting a suspension referendum
        return random.random() > 0.7

# Example usage
parliament = Parliament(300)  # 300 total seats

# Create a civic organization
org = CivicOrganization("Social Equality Group")

# Propose and add a candidate (scholarship and regular)
for is_scholarship in [True, False]:
    candidate = org.propose_candidate(Chamber.DEPUTIES)
    candidate.is_scholarship = is_scholarship
    if parliament.conduct_admission_interview(candidate):
        parliament.add_member(candidate)
        print(f"New {'scholarship' if is_scholarship else 'regular'} member admitted")

# Simulate a year passing # TODO : where's the time param??
parliament.update_all_members()

# Nominate a member for the admission committee
for member in parliament.members:
    if parliament.nominate_for_admission_committee(member):
        if parliament.vote_for_admission_committee(member):
            member.admission_committee_member = True
            parliament.admission_committee.append(member)
            print(f"Member {member.id} added to the admission committee")
            break

# Simulate internal legislation proposal
if parliament.propose_internal_legislation():
    print("Internal legislation proposed successfully")

# Simulate external legislation proposal
if parliament.process_external_legislation(org):
    print("External legislation from civic organization processed successfully")

# Simulate legislation proposal
if parliament.propose_legislation("Economic Reform", "Parliament", "Content of the economic reform..."):
    print("Legislation proposed successfully")

legislation = parliament.proposed_legislation[0]
if parliament.vote_on_legislation(legislation):
    print(f"Legislation '{legislation.title}' passed")
else:
    print(f"Legislation '{legislation.title}' failed")

# Simulate no-confidence vote
if parliament.has_quorum():
    if parliament.vote_no_confidence():
        print("No-confidence vote succeeded")
else:
    print("Cannot hold no-confidence vote: No quorum")
