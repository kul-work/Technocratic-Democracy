import random
from enum import Enum

class Chamber(Enum):
    SENATE = "Senate"
    DEPUTIES = "Chamber of Deputies"

class ParliamentaryStatus(Enum):
    ACTIVE = "Active"
    ON_BREAK = "On Break"
    FORMER = "Former"

class Parliamentarian:
    def __init__(self, id, chamber):
        self.id = id
        self.chamber = chamber
        self.years_served = 0
        self.consecutive_terms = 0
        self.activity_score = 0
        self.status = ParliamentaryStatus.ACTIVE
        self.is_minority = False
        self.is_scholarship = False
        self.admission_committee_member = False
        self.legislative_initiatives = 0
        self.speeches_given = 0
        self.committee_participations = 0

    def update_status(self):
        if self.years_served >= 10:
            self.status = ParliamentaryStatus.ON_BREAK
            self.years_served = 0
            self.consecutive_terms = 0

    def calculate_activity_score(self):
        # Simple calculation, can be made more complex
        self.activity_score = (
            self.legislative_initiatives * 3 +
            self.speeches_given +
            self.committee_participations * 2
        )

class CivicOrganization:
    def __init__(self, name):
        self.name = name

    def propose_candidate(self, chamber):
        # Simplified candidate proposal
        return Parliamentarian(0, chamber)

class Parliament:
    def __init__(self, total_seats):
        self.total_seats = total_seats
        self.senate_seats = int(total_seats * 0.3)
        self.deputy_seats = total_seats - self.senate_seats
        self.members = []
        self.admission_committee = []

    def add_member(self, member):
        if len(self.members) < self.total_seats:
            member.id = len(self.members) + 1
            self.members.append(member)
            return True
        return False

    def remove_member(self, member):
        self.members.remove(member)

    def update_all_members(self):
        for member in self.members:
            member.years_served += 1
            member.update_status()
            member.calculate_activity_score()

    def conduct_admission_interview(self, candidate):
        # Simplified admission process
        return random.random() > 0.3  # 70% chance of admission

    def propose_legislation(self, organization):
        # Simplified legislation proposal
        return random.random() > 0.5  # 50% chance of proposal acceptance

    def vote_no_confidence(self):
        # Simplified no-confidence vote
        return random.random() > 0.7  # 30% chance of success

    def nominate_for_admission_committee(self, member):
        if member.years_served >= 5 and member.activity_score > 50:
            return True
        return False

    def vote_for_admission_committee(self, nominee):
        # Simplified voting process
        return random.random() > 0.4  # 60% chance of approval

# Example usage
parliament = Parliament(300)  # 300 total seats

# Create a civic organization
org = CivicOrganization("Social Equality Group")

# Propose and add a scholarship candidate
candidate = org.propose_candidate(Chamber.DEPUTIES)
candidate.is_scholarship = True
if parliament.conduct_admission_interview(candidate):
    parliament.add_member(candidate)
    print("New scholarship member admitted")

# Simulate a year passing
parliament.update_all_members()

# Nominate a member for the admission committee
for member in parliament.members:
    if parliament.nominate_for_admission_committee(member):
        if parliament.vote_for_admission_committee(member):
            member.admission_committee_member = True
            parliament.admission_committee.append(member)
            print(f"Member {member.id} added to the admission committee")
            break

# Simulate legislation proposal
if parliament.propose_legislation(org):
    print("Legislation proposed successfully")

# Simulate no-confidence vote
if parliament.vote_no_confidence():
    print("No-confidence vote succeeded")
