from enum import Enum
from datetime import datetime, timedelta
import random

from citizen import Citizen, CitizenshipStatus
from president import President
from legislative import Parliamentarian, Parliament, Chamber


MAX_ADVISORS = 12

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
    def __init__(self, name):
        self.name = name
        self.is_minister = False

class Ministry:
    def __init__(self, ministry_type):
        self.type = ministry_type
        self.advisors = []
        self.minister = None

    def add_advisor(self, advisor):
        if len(self.advisors) <= MAX_ADVISORS:
            self.advisors.append(advisor)
            return True
        return False

    def set_minister(self, advisor):
        if advisor in self.advisors:
            if self.minister:
                self.minister.is_minister = False
            advisor.is_minister = True
            self.minister = advisor
            return True
        return False

class Government:
    def __init__(self, prime_minister):
        self.prime_minister = prime_minister
        self.ministries = {ministry_type: Ministry(ministry_type) for ministry_type in MinistryType}
        self.government_managers = []
        self.status = GovernmentStatus.ACTIVE
        self.formation_date = datetime.now()
        self.dissolution_date = self.formation_date + timedelta(days=3*365)
        self.emergency_end_date = None

    def appoint_government_manager(self, parliamentarian):
        if len(self.government_managers) <= 3:
            self.government_managers.append(parliamentarian)
            return True
        return False

    def initiate_emergency_decree(self, region):
        # Simplified implementation
        return random.choice([True, False])

    def approve_emergency_decree(self, decree, affected_population):
        # Simplified simulation of referendum
        return random.random() > 0.5

    def check_dissolution(self):
        if datetime.now() >= self.dissolution_date:
            self.status = GovernmentStatus.DISSOLVED
            return True
        return False

    def declare_emergency(self):
        if self.status != GovernmentStatus.EMERGENCY:
            self.status = GovernmentStatus.EMERGENCY
            self.emergency_end_date = datetime.now() + timedelta(days=120)
            return True
        return False

    def check_emergency_status(self):
        if self.status == GovernmentStatus.EMERGENCY and datetime.now() >= self.emergency_end_date:
            self.status = GovernmentStatus.ACTIVE
            self.emergency_end_date = None
            return True
        return False


# Example usage
president = President()
parliament = Parliament(300)  # Using the Parliament class from legislative.py

# Add some parliamentarians
for _ in range(100):
    citizen = Citizen(random.randint(25, 70), random.choice(["Male", "Female"]), "Region1")
    citizen.citizenship_status = CitizenshipStatus.CITIZEN
    parliamentarian = Parliamentarian(parliament.total_seats + 1, random.choice(list(Chamber)))
    parliament.add_member(parliamentarian)

# Simulate prime minister selection
if parliament.has_quorum():
    prime_minister = president.choose_prime_minister(parliament)
    print(f"{prime_minister} has been elected as Prime Minister.")
    government = Government(prime_minister)

    for ministry in government.ministries.values():
        for _ in range(random.randint(3, MAX_ADVISORS)):
            advisor = Advisor(f"Advisor {random.randint(1000, 9999)}")
            ministry.add_advisor(advisor)
        ministry.set_minister(random.choice(ministry.advisors))

    # Ratify the government
    if parliament.has_quorum() and parliament.propose_internal_legislation():
        print("Government successfully formed and ratified!")
    else:
        print("Government ratification failed.")
else:
    print("Parliament lacks quorum. Cannot proceed with government formation.")

# Simulate time passage and check for dissolution
if 'government' in locals():
    government.formation_date = datetime.now() - timedelta(days=1095)
    if government.check_dissolution():
        print("Government automatically dissolved after 3 years.")

    # Simulate state of emergency
    if government.declare_emergency():
        print("State of emergency declared for 4 months.")
        government.formation_date = datetime.now() - timedelta(days=1155)  # 3 years and 2 months
        if government.check_emergency_status():
            print("State of emergency expired.")
        if government.check_dissolution():
            print("Government dissolved after the expiration of the state of emergency.")

# Check for quorum in Parliament
if parliament.has_quorum():
    print("Parliament has quorum and can conduct business.")
else:
    print("Parliament lacks quorum and cannot conduct business.")
