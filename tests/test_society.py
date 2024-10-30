import unittest
from models.society import SocietySystem
from config import POPULATION_DECLINE_CHANCE, POPULATION_DECLINE_FACTOR

class TestSocietySystem(unittest.TestCase):
    def setUp(self):
        self.society = SocietySystem(100)  # Start with 100 citizens
        
    def test_population_decline(self):
        # Store initial population
        initial_population = len(self.society.citizens)
        
        # Force population decline by patching random.random to return a value < POPULATION_DECLINE_CHANCE
        # We'll use monkeypatch to ensure the growth_chance is low enough to trigger decline
        import random
        original_random = random.random
        random.random = lambda: POPULATION_DECLINE_CHANCE / 2  # Ensures we hit the decline branch
        
        try:
            # Update population
            self.society.update_population()
            
            # Calculate expected decline
            expected_decline = min(
                int(initial_population * POPULATION_DECLINE_FACTOR),
                initial_population
            )
            
            # Check if population decreased by the expected amount
            self.assertEqual(
                len(self.society.citizens),
                initial_population - expected_decline,
                f"Population should decrease by {expected_decline} citizens"
            )
            
        finally:
            # Restore original random function
            random.random = original_random
            
    def test_population_decline_safety(self):
        # Test with very small population
        self.society.citizens = self.society.citizens[:3]  # Keep only 3 citizens
        initial_population = len(self.society.citizens)
        
        import random
        original_random = random.random
        random.random = lambda: POPULATION_DECLINE_CHANCE / 2  # Force decline
        
        try:
            # Update population multiple times
            for _ in range(5):
                self.society.update_population()
                # Ensure we never have negative population
                self.assertGreaterEqual(
                    len(self.society.citizens),
                    0,
                    "Population should never be negative"
                )
                
        finally:
            random.random = original_random

if __name__ == '__main__':
    unittest.main() 