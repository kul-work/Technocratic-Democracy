import random
from typing import List

from .citizen import Citizen

class SocietySystem:
    def __init__(self, initial_population: int):
        self.citizens: List[Citizen] = []
        self.create_initial_population(initial_population)

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
        growth_batch = int(current_pop * 0.1)  # 10% of current population
        decline_batch = int(current_pop * 0.05)  # 5% of current population
        
        # Minimum batch size of 1 if population exists
        growth_batch = max(1, growth_batch) if current_pop > 0 else 1
        decline_batch = max(1, decline_batch) if current_pop > 0 else 0

        # Add random population changes in batches        
        growth_chance = random.random()
        if growth_chance > 0.8:  # 20% chance for population growth
            for _ in range(growth_batch):
                new_citizen = self.create_random_citizen()
                self.citizens.append(new_citizen)
        elif growth_chance < 0.1:  # 10% chance for population decline
            for _ in range(min(decline_batch, current_pop)):  # Ensure we don't remove more than existing #TODO: Check if this is correct
                if self.citizens:
                    self.citizens.pop()

        # Update existing citizens
        for citizen in self.citizens:
            citizen.update(None, None, None)  # Placeholder for now
