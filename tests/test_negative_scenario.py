import unittest
from datetime import datetime
from unittest.mock import patch

from simulation import Simulation
from models.society import *
from models.society_state import *
from models.government import *
from models.legislative import *
from models.referendum import *
from models.economy import *
from models.media import *
from models.president import *

class TestNegativeScenario(unittest.TestCase):
    def setUp(self):
        self.simulation = Simulation()

        self.simulation.society = SocietySystem(initial_population=10_000)  # Start with 10K citizens
        self.society_state = SocietyState()

        self.government = Government("Test PM")
        self.parliament = Parliament(300)
        self.president = President("Test president")
        self.referendum_system = ReferendumSystem(self.parliament)
        self.economy = EconomicModel()
        self.media_landscape = MediaLandscape()

        # Fill the parliament with active members
        for _ in range(300):
            member = Parliamentarian(Chamber.DEPUTIES)
            member.status = ParliamentaryStatus.ACTIVE
            self.parliament.add_member(member)

    def test_negative_scenario(self):
        # Simulate an unpopular austerity measure implemented by the government
        self.government.implement_austerity()

        # Simulate an unpopular legislation proposed by the government
        unpopular_legislation = Legislation(
            title="Unpopular Law",
            proposer="John Doe",
            content="A highly unpopular law that will negatively impact the economy and public opinion."
        )

        # The SOMEONE proposes an 'unpopular' law
        self.parliament.propose_legislation(f"Increase taxation", "John Doe", f"Content increase taxation plan", ignore_quorum = False)

        # Parliament votes and approves the law
        self.parliament.proposed_legislation.append(unpopular_legislation)
        self.assertTrue(self.parliament.vote_on_legislation(unpopular_legislation, ignore_quorum=True))

        # Add the referendum to the system
        referendum = self.referendum_system.propose_referendum(
            title=unpopular_legislation.title,
            description=unpopular_legislation.content,
            referendum_type=ReferendumType.NATIONAL
        )
        # The president sends the law to a referendum
        if self.president.call_referendum(unpopular_legislation):
            self.referendum_system.referendums.append(referendum)
        else:
            self.assertTrue(2 == 3,"The refferendum failed")

        # Simulate citizens voting against the law
        referendum = self.referendum_system.referendums[-1]
        referendum.status = ReferendumStatus.ACTIVE
        with patch.object(self.simulation, 'process_news_cycle'):
            for citizen in self.simulation.society.citizens:
                self.referendum_system.vote(citizen, referendum, False)

        # Complete the referendum
        referendum.total_votes = 300;
        referendum.quorum = 400
        referendum.min_votes = 100
        self.referendum_system.complete_referendum(referendum)

        # Check that the austerity measure was rejected in the referendum
        self.assertEqual(referendum.status, ReferendumStatus.FAILED)

        # Simulate negative economic consequences
        with patch.object(self.economy, 'simulate_month') as mock_simulate_month:
            # Decrease GDP growth by 2%
            mock_simulate_month.side_effect = lambda: setattr(self.economy, 'gdp', self.economy.gdp * 0.98)
            for _ in range(4):  # Simulate 4 months
                self.economy.simulate_month()

        # Check that GDP growth is too small
        self.assertLess(self.economy.get_gdp_growth(), 0.1)

        # Simulate negative media coverage
        self.media_landscape.media_trust_score -= 30  # Decrease in media trust

        # Check the consequences
        self.assertLess(self.media_landscape.media_trust_score, 60)

if __name__ == '__main__':
    unittest.main() 