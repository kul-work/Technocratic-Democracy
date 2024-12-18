import random
from typing import List, Optional
from config import *

from .citizen import Citizen
from .legislative import Law

class SocietySystem:
    def __init__(self, initial_population: int):
        self.citizens: List[Citizen] = []
        self.create_initial_population(initial_population)
        self.social_tension_factors = {
            'income_inequality': 0.0,
            'ethnic_tensions': 0.0,
            'generational_divide': 0.0,
            'urban_rural_divide': 0.0,
            'religious_tensions': 0.0
        }

    def create_initial_population(self, population_size: int) -> None:
        for _ in range(population_size):
            citizen = self.create_random_citizen()
            self.citizens.append(citizen)
            #TODO: Add more factors to the citizen, sync / write updates for those factors

    def create_random_citizen(self) -> Citizen:
        age = random.randint(0, 90)
        sex = random.choice(['Male', 'Female'])
        region = f"Region_{random.randint(1, 10)}"
        return Citizen(age, sex, region)

    def get_random_citizens(self, n: int) -> List[Citizen]:
        return random.sample(self.citizens, min(n, len(self.citizens)))

    def get_voting_population(self) -> List[Citizen]:
        return [citizen for citizen in self.citizens if citizen.has_voting_rights()]

    # This method would handle births, deaths, aging, etc.
    def update_population(self) -> None:
        """
        This method handles births, deaths, aging, etc.
        """
        # Calculate batch sizes based on current population
        current_pop = len(self.citizens)
        growth_batch = int(current_pop * POPULATION_GROWTH_FACTOR)
        decline_batch = int(current_pop * POPULATION_DECLINE_FACTOR)
        
        # Minimum batch size of 1 if population exists
        growth_batch = max(1, growth_batch) if current_pop > 0 else 1
        decline_batch = max(1, decline_batch) if current_pop > 0 else 0

        # Add random population changes in batches        
        growth_chance = random.random()        
        if growth_chance > (1 - POPULATION_GROWTH_CHANCE):
            # Ensure we don't remove more than existing
            for _ in range(growth_batch):
                if len(self.citizens) < MAX_POPULATION:
                    new_citizen = self.create_random_citizen()
                    self.citizens.append(new_citizen)        
        elif growth_chance < POPULATION_DECLINE_CHANCE:
            for _ in range(min(decline_batch, current_pop)):
                if self.citizens:
                    self.citizens.pop()

        # Create basic state dictionaries for updates
        economy_state = {'growth': random.uniform(-0.02, 0.04)}
        social_state = {'cohesion': random.uniform(0.3, 0.7)}
        political_state = {'stability': random.uniform(0.4, 0.8)}

        # Update existing citizens
        for citizen in self.citizens:
            citizen.update(economy_state, social_state, political_state)

    def get_satisfaction_score(self) -> float:
        """
        Calculate overall citizen satisfaction based on:
        - Average happiness
        - Average trust in institutions
        - Average socioeconomic status
        Returns value between 0 and 1
        """
        if not self.citizens:
            return random.uniform(0.4, 0.6)  # Return reasonable default if no citizens
        
        # Calculate average happiness
        avg_happiness = sum(citizen.happiness for citizen in self.citizens) / len(self.citizens)
        
        # Calculate average trust
        avg_trust = sum(citizen.trust_in_institutions for citizen in self.citizens) / len(self.citizens)
        
        # Calculate average socioeconomic status
        avg_socioeconomic = sum(citizen.socioeconomic_rating for citizen in self.citizens) / len(self.citizens)
        
        # Add some random variation to make it more dynamic
        base_satisfaction = (avg_happiness / 100 * 0.4 + 
                            avg_trust / 100 * 0.3 + 
                            avg_socioeconomic / 100 * 0.3)
        
        variation = random.uniform(-0.05, 0.05)  # +/- 5% variation
        return max(0.0, min(1.0, base_satisfaction + variation))

    def calculate_social_tensions(self, 
                            economy, 
                            media_influence: float = 0.0,
                            policy_effects: Optional[List[Law]] = None,
                            government_approval: float = 50.0) -> float:
        """
        Calculate overall social tension level based on various factors
        
        Args:
            economy: Economy object for economic indicators
            media_influence: Impact of media on social tensions (default 0.0)
            policy_effects: List of active laws affecting social tension (default None)
            government_approval: Current government approval rating (default 50.0)
            
        Returns:
            float: Tension score between 0.0 and 1.0
        """
        if policy_effects is None:
            policy_effects = []

        # Base tension calculation
        base_tension = (
            economy.get_gini_coefficient() * 0.25 +  # Income inequality
            self.get_ethnic_diversity_tension() * 0.15 +
            self.get_age_group_conflicts() * 0.15 +
            self.get_urban_rural_disparity() * 0.15 +
            self.get_religious_conflicts() * 0.15 +
            media_influence * 0.15  # Media's contribution to social tension
        )
        
        # Calculate policy impact on tension
        policy_impact = 0.0
        for law in policy_effects:
            if hasattr(law, 'social_impact'):
                policy_impact += law.social_impact
            else:
                # Default small reduction in tension for any active law
                policy_impact -= 0.01
                
        # Government approval impact (inverse relationship - higher approval means lower tension)
        government_tension = (100 - government_approval)

    def get_ethnic_diversity_tension(self) -> float:
        """Calculate ethnic tension based on citizen diversity and interaction"""
        # Simplified calculation based on ethnic groups distribution
        ethnic_groups = {}
        for citizen in self.citizens:
            ethnic_groups[citizen.ethnicity] = ethnic_groups.get(citizen.ethnicity, 0) + 1
        
        # More diverse population might lead to higher tension
        diversity_factor = len(ethnic_groups) / 10  # Normalized by assumed max of 10 ethnic groups
        return self.social_tension_factors['ethnic_tensions'] * diversity_factor

    def get_age_group_conflicts(self) -> float:
        """Calculate generational tension based on age distribution"""
        age_groups = {'young': 0, 'middle': 0, 'elderly': 0}
        for citizen in self.citizens:
            if citizen.age < 30:
                age_groups['young'] += 1
            elif citizen.age < 60:
                age_groups['middle'] += 1
            else:
                age_groups['elderly'] += 1
        
        # Calculate imbalance between age groups
        total = len(self.citizens)
        age_disparity = max(abs(age_groups['young']/total - age_groups['elderly']/total), 0.1)
        return self.social_tension_factors['generational_divide'] * age_disparity

    def get_urban_rural_disparity(self) -> float:
        """Calculate urban-rural divide tension"""
        urban_count = sum(1 for citizen in self.citizens if citizen.region.startswith('Urban'))
        rural_count = len(self.citizens) - urban_count
        
        # Calculate disparity ratio
        disparity = abs((urban_count - rural_count) / len(self.citizens))
        return self.social_tension_factors['urban_rural_divide'] * disparity

    def get_religious_conflicts(self) -> float:
        """Calculate religious tension based on religious diversity"""
        religious_groups = {}
        for citizen in self.citizens:
            religious_groups[citizen.religion] = religious_groups.get(citizen.religion, 0) + 1
            
        # More religious groups might indicate higher potential for conflict
        diversity_factor = len(religious_groups) / 5  # Normalized by assumed max of 5 major religions
        return self.social_tension_factors['religious_tensions'] * diversity_factor
