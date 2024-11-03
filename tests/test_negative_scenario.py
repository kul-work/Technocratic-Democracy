import unittest
from datetime import datetime
from unittest.mock import patch

from simulation import Simulation
from models.government import Government
from models.legislative import Parliament, Law
from models.referendum import ReferendumSystem, ReferendumType, ReferendumStatus
from models.economy import EconomicModel
from models.media import MediaLandscape

class TestNegativeScenario(unittest.TestCase):
    def setUp(self):
        self.simulation = Simulation()
        self.government = Government("Test PM")
        self.parliament = Parliament(300)
        self.referendum_system = ReferendumSystem(self.parliament)
        self.economy = EconomicModel()
        self.media_landscape = MediaLandscape()

    def test_negative_scenario(self):

        # Simulate an unpopular austerity measure implemented by the government
        self.government.implement_austerity()

        # Simulate an unpopular law proposed by the government
        unpopular_law = Law(
            title="Unpopular Law",
            description="A highly unpopular law that will negatively impact the economy and public opinion.",
            full_text="This is the full text of the unpopular law..."
        )

        # The government proposes the law
        self.government.propose_legislation(unpopular_law)

        # Parliament votes and approves the law
        self.parliament.proposed_legislation.append(unpopular_law)
        self.assertTrue(self.parliament.vote_on_legislation(unpopular_law))

        # The president sends the law to a referendum
        self.assertTrue(self.simulation.president.send_law_to_referendum(unpopular_law, self.referendum_system))

        # Simulate citizens voting against the law
        referendum = self.referendum_system.referendums[-1]
        with patch.object(self.simulation, 'process_news_cycle'):
            for citizen in self.simulation.society.citizens:
                self.referendum_system.vote(citizen, referendum, False)

        # Complete the referendum
        self.referendum_system.complete_referendum(referendum)

        # Check that the austerity measure was rejected in the referendum
        self.assertEqual(referendum.status, ReferendumStatus.REJECTED)

        # Simulate negative economic consequences and negative media coverage
        self.economy.gdp_growth -= 0.02  # Decrease in economic growth
        self.media_landscape.trust_score -= 0.1  # Decrease in media trust

        # Check the consequences
        self.assertLess(self.economy.gdp_growth, 0)
        self.assertLess(self.media_landscape.trust_score, 0.9)

if __name__ == '__main__':
    unittest.main() 