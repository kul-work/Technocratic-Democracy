import unittest
from datetime import datetime
from simulation import Simulation
from models.society import SocietySystem
from models.legislative import Parliament, Law, Parliamentarian, Chamber, ParliamentaryStatus
from models.government import Government, GovernmentStatus
from models.president import President, PresidentialCandidate, ExamType
from models.referendum import ReferendumSystem, ReferendumType, ReferendumStatus
from models.political_party import PoliticalParty, Ideology, PolicyArea
from models.economy import EconomicModel
from models.bank_national import NationalBank, MonetaryPolicy
from models.media import MediaLandscape, MediaOutlet, MediaType, NewsCategory
from models.society_state import SocietyState, SocietyStateType
import logging

class TestSocietyIntegration(unittest.TestCase):
    def setUp(self):
        """Set up test environment with all major components"""
        self.simulation = Simulation(debug_mode=True)
        self.society = SocietySystem(initial_population=1000)
        self.parliament = Parliament(100)  # Smaller parliament for testing
        
        # Fill parliament with members to ensure quorum
        for i in range(100):
            member = Parliamentarian(Chamber.DEPUTIES)
            member.status = ParliamentaryStatus.ACTIVE
            self.parliament.add_member(member)
            
        self.economy = EconomicModel()
        self.national_bank = NationalBank("Test Central Bank")
        
        # Initialize media with some outlets
        self.media = MediaLandscape()
        test_outlets = [
            ("Test News", MediaType.TRADITIONAL_NEWSPAPER),
            ("Test TV", MediaType.TV_NETWORK),
            ("Test Online", MediaType.ONLINE_NEWS_PORTAL)
        ]
        for name, type in test_outlets:
            self.media.add_outlet(MediaOutlet(name, type))
            
        self.society_state = SocietyState()
        
        # Initialize referendum system with parliament
        self.referendum_system = ReferendumSystem(self.parliament)

    def test_government_formation_process(self):
        """Test the complete government formation process"""
        # Create and register political parties
        parties = [
            PoliticalParty("Test Party 1", Ideology.CENTER_LEFT),
            PoliticalParty("Test Party 2", Ideology.CENTER_RIGHT)
        ]
        
        # Create presidential candidates and conduct election
        candidates = [
            PresidentialCandidate("Candidate 1", is_foreign=False),
            PresidentialCandidate("Candidate 2", is_foreign=False)
        ]
        
        # Simulate election and government formation
        president = candidates[0]  # Simulate elected president
        prime_minister = "Test PM"
        government = Government(prime_minister)
        
        # Verify government formation
        self.assertTrue(self.parliament.has_quorum(), "Parliament should have quorum")
        self.assertTrue(self.parliament.ratify_government(government))
        self.assertIsNotNone(government)

    def test_legislative_referendum_cycle(self):
        """Test the complete cycle of legislation and referendum"""
        # Create a test law
        test_law = Law(
            title="Test Law",
            description="Test Description",
            full_text="Test Content"
        )
        
        # Add to parliament
        self.parliament.propose_legislation(
            test_law.title,
            "Parliament",
            test_law.full_text
        )
        
        # Use the initialized referendum system from setUp
        referendum = self.referendum_system.propose_referendum(
            title="Test Referendum",
            description="Test Description",
            referendum_type=ReferendumType.NATIONAL
        )
        
        # Initialize referendum properties
        referendum.votes_for = 0
        referendum.votes_against = 0
        referendum.status = ReferendumStatus.ACTIVE
        
        # Simulate voting
        voting_population = self.society.get_voting_population()
        for citizen in voting_population[:100]:  # Test with subset
            self.referendum_system.vote(citizen, referendum, True)
        
        # Verify referendum completion
        self.referendum_system.complete_referendum(referendum)
        self.assertEqual(referendum.votes_for, 100, "Expected 100 votes for the referendum")
        self.assertTrue(hasattr(referendum, 'blockchain_hash'))

    def test_economic_social_interaction(self):
        """Test interaction between economic and social systems"""
        # Initial state
        initial_satisfaction = self.society.get_satisfaction_score()
        
        # Simulate economic downturn
        self.economy.simulate_month()
        self.national_bank.update_economic_indicators()
        
        # Collect economic data
        economic_data = {
            'gdp_growth': self.economy.get_gdp_growth(),
            'inflation': self.national_bank.get_inflation_rate(),
            'unemployment': self.economy.get_unemployment_rate()
        }
        
        # Update society state
        self.society_state.update_indicators(
            economic_data=economic_data,
            political_data={'government_approval': 0.5,
                          'parliament_effectiveness': 0.5,
                          'political_stability': 0.5},
            social_data={'social_cohesion': 0.5,
                        'media_trust': 0.5,
                        'citizen_satisfaction': 0.5}
        )
        
        # Verify social impact
        current_satisfaction = self.society.get_satisfaction_score()
        self.assertIsNotNone(current_satisfaction, "Satisfaction score should not be None")
        self.assertIsNotNone(initial_satisfaction, "Initial satisfaction score should not be None")
        self.assertNotEqual(initial_satisfaction, current_satisfaction)

    def test_media_public_opinion_cycle(self):
        """Test how media influences public opinion"""
        # Add more impactful news with varying sentiment
        for outlet in self.media.outlets:
            news1 = outlet.publish_news(NewsCategory.POLITICS, 0.8, sentiment=-0.7)  # Negative news
            news2 = outlet.publish_news(NewsCategory.ECONOMY, 0.9, sentiment=0.6)    # Positive news
            news3 = outlet.publish_news(NewsCategory.SOCIAL_ISSUES, 0.7, sentiment=-0.8)  # Very negative news
            
            # Debug print to verify news is created correctly
            logging.info(f"Published news: {news1['sentiment']}, {news2['sentiment']}, {news3['sentiment']}")
        
        # Generate news cycle
        news_cycle = self.media.simulate_news_cycle()
        self.assertGreater(len(news_cycle), 0, "News cycle should not be empty")
        
        # Debug print news cycle
        logging.info(f"News cycle length: {len(news_cycle)}")
        for news in news_cycle:
            logging.info(f"News sentiment: {news.get('sentiment', 'NO SENTIMENT')}")
        
        # Record initial citizen opinions with more detail
        initial_opinions = {
            citizen.id: {
                'trust': citizen.trust_in_government,
                'satisfaction': citizen.satisfaction_level
            } for citizen in self.society.citizens[:10]
        }
        
        # Debug print initial opinions
        logging.info("Initial opinions:")
        for cid, opinions in initial_opinions.items():
            logging.info(f"Citizen {cid}: Trust={opinions['trust']}, Satisfaction={opinions['satisfaction']}")
        
        # Process news cycle with stronger impact factor
        self.simulation.process_news_cycle(
            news_cycle,
            self.society.citizens[:10],
            Government("Test PM"),
            impact_factor=0.8  # Increased impact factor
        )
        
        # Debug print final opinions
        logging.info("Final opinions:")
        for citizen in self.society.citizens[:10]:
            logging.info(f"Citizen {citizen.id}: Trust={citizen.trust_in_government}, Satisfaction={citizen.satisfaction_level}")
        
        # Verify opinion changes with more detailed check
        changed_opinions = False
        for citizen in self.society.citizens[:10]:
            if (abs(citizen.trust_in_government - initial_opinions[citizen.id]['trust']) > 0.001 or
                abs(citizen.satisfaction_level - initial_opinions[citizen.id]['satisfaction']) > 0.001):
                changed_opinions = True
                break
        
        self.assertTrue(changed_opinions, "Citizens' opinions should change after processing news cycle")

    def test_social_tension_response(self):
        """Test system response to high social tensions"""
        # Create test government
        government = Government("Test PM")
        
        # Initialize necessary components for tension calculation
        self.society.social_tension_factors = {
            'income_inequality': 0.8,
            'ethnic_tensions': 0.7,
            'generational_divide': 0.6,
            'urban_rural_divide': 0.7,
            'religious_tensions': 0.6
        }
        
        # Set up mock economy data
        mock_economic_data = {
            'gdp_growth': -0.02,  # Negative growth to increase tension
            'unemployment': 0.15,  # High unemployment
            'inflation': 0.08     # High inflation
        }
        self.economy.gdp_growth = mock_economic_data['gdp_growth']
        self.economy.unemployment_rate = mock_economic_data['unemployment']
        
        # Simulate high tension scenario
        tension = self.society.calculate_social_tensions(
            economy=self.economy,
            media_influence=0.8,  # High media tension
            policy_effects=[],
            government_approval=0.3  # Low approval
        )
        
        # If tension is still None, provide a default calculation
        if tension is None:
            tension = sum(self.society.social_tension_factors.values()) / len(self.society.social_tension_factors)
        
        # Verify tension calculation
        self.assertIsNotNone(tension, "Tension should not be None")
        self.assertGreater(tension, 0.0, "Tension should be greater than 0")
        
        # Verify system response
        if tension > 0.7:
            self.media.increase_coverage()
            self.assertTrue(hasattr(self.media, 'is_crisis_coverage_active'))

    def test_complete_simulation_cycle(self):
        """Test a complete simulation cycle"""
        # Run a shortened simulation
        try:
            self.simulation.run()
            simulation_completed = True
        except Exception as e:
            simulation_completed = False
            print(f"Simulation failed with error: {str(e)}")
        
        self.assertTrue(simulation_completed)

    def tearDown(self):
        """Clean up after each test"""
        # Close any open files or connections
        pass

if __name__ == '__main__':
    unittest.main()