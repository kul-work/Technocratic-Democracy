class Citizen:
    def __init__(self, age, sex, location):
        # Caracteristici demografice
        self.age = age
        self.sex = sex
        self.location = location
        
        # Factori economici
        self.income = 0
        self.savings = 0
        self.debt = 0
        # Evaluare combinată a statutului socioeconomic (0-100)
        # Poate include factori precum venit, educație, ocupație
        self.socioeconomic_rating = 0
        
        # Factori sociali
        self.education_level = 0
        self.health = 100
        self.happiness = 50
        self.social_capital = 0
        self.trust_in_institutions = 0
        
        # Factori de muncă
        self.employment_status = "Unemployed"
        self.job_satisfaction = 0
        self.work_life_balance = 0
        
        # Factori politici și de valori
        self.political_leaning = 0  # De la -1 (stânga) la 1 (dreapta)
        self.civic_engagement = 0
        self.environmental_concern = 0
        
        # Comportament și stil de viață
        self.consumption = 0
        self.media_usage = {}
        self.leisure_activities = []
        
    def update(self, economy, policies, social_environment):
        # Logica pentru actualizarea stării cetățeanului
        pass
