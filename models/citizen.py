from enum import Enum

class CitizenshipStatus(Enum):
    CITIZEN = "Citizen"
    PERMANENT_RESIDENT = "Permanent Resident"
    TEMPORARY_RESIDENT = "Temporary Resident"
    UNDOCUMENTED = "Undocumented"

class Citizen:
    def __init__(self, age, sex, region):
        # Demographic characteristics
        self.age = age
        self.sex = sex
        self.region = region
        # TODO: Add 'county' attribute and link it with 'region'
        self.citizenship_status = CitizenshipStatus.CITIZEN
        self.is_immigrant = False
        self.years_in_country = 0  # To immigrants only
        
        # Economic factors
        self.income = 0
        self.savings = 0
        self.debt = 0
        # Evaluation of socioeconomic status (0-100)
        # Can include factors such as income, education, occupation
        self.socioeconomic_rating = 0
        
        # Social factors
        self.education_level = 0
        self.health = 100
        self.happiness = 50
        self.social_capital = 0
        self.trust_in_institutions = 0
        
        # Work factors
        self.employment_status = "Unemployed"
        self.job_satisfaction = 0
        self.work_life_balance = 0
        
        # Behavior and lifestyle
        self.political_leaning = 0  # From -1 (left wing) to 1 (right wing)
        self.civic_engagement = 0
        self.environmental_concern = 0
        
        # Comportament și stil de viață
        self.consumption = 0
        self.media_usage = {}
        self.leisure_activities = []

    def has_voting_rights(self):
        return self.citizenship_status == CitizenshipStatus.CITIZEN and self.age >= 16
        
    def update(self, economy, policies, social_environment):
        # Logic for updating the citizen's state
        pass
