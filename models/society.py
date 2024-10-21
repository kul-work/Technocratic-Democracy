import random
from typing import List

from .citizen import Citizen

class SocietySystem:
    def __init__(self, initial_population: int):
        self.citizens: List[Citizen] = []
        self.create_initial_population(initial_population)

    def create_initial_population(self, population_size: int) -> None:
        for _ in range(population_size):
            age = random.randint(0, 90)
            sex = random.choice(['Male', 'Female'])
            region = f"Region_{random.randint(1, 10)}"
            citizen = Citizen(age, sex, region)            
            self.citizens.append(citizen)
            #TODO: Add more factors to the citizen, sync / write updates for those factors

    def get_voting_population(self) -> List[Citizen]:
        return [citizen for citizen in self.citizens if citizen.has_voting_rights()]

    def update_population(self) -> None:
        # This method would handle births, deaths, aging, etc.
        for citizen in self.citizens:
            citizen.update(None, None, None)  # Placeholder for now

    def get_random_citizens(self, n: int) -> List[Citizen]:
        return random.sample(self.citizens, min(n, len(self.citizens)))
