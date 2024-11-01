import logging
from config import *

from models.citizen import *
from models.society import *
from models.legislative import *
from models.government import *
from models.president import *
from models.referendum import *
from models.political_party import *
from models.civil_society import *
from models.economy import *
from models.bank_national import *
from models.media import *

from models.society_state import SocietyState, SocietyStateType

class Simulation:
    def __init__(self, debug_mode=False):
        global DEBUG_MODE
        DEBUG_MODE = debug_mode

        # Set up logging to both console and file
        logging.basicConfig(
            level=logging.DEBUG if DEBUG_MODE else logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),  # Console handler
                logging.FileHandler('output/output.txt', mode='w')  # 'w' mode overwrites
            ]
        )
        self.logger = logging.getLogger(__name__)

        self.interim_government = None  # Track interim government during transitions

    def process_news_cycle(self, news_cycle: List[Dict], citizens: List['Citizen'], government: 'Government'):
        # Example of how news could affect other parts of the simulation
        for news in news_cycle:
            if news['category'] == NewsCategory.POLITICS:
                # Affect citizen's trust in government
                for citizen in citizens:
                    citizen.trust_in_government += news['impact'] * 0.01 * (1 if news['bias'] > 0 else -1)
            elif news['category'] == NewsCategory.ECONOMY:
                # Affect government's economic policy
                government.adjust_economic_policy(news['impact'] * 0.1)
            # ... handle other categories

    def update_public_trust(self, society_data):
        """Calculate and return the public trust score"""
        # Add weights to make calculation more nuanced
        weights = {
            'citizen_satisfaction': 0.4,
            'media_trust': 0.3,
            'social_cohesion': 0.3  # Added social_cohesion as a factor
        }
        
        trust = (
            society_data['citizen_satisfaction'] * weights['citizen_satisfaction'] +
            society_data['media_trust'] * weights['media_trust'] +
            society_data['social_cohesion'] * weights['social_cohesion']
        )
        
        # Add some random monthly variation
        variation = random.uniform(-0.03, 0.03)  # +/- 3% monthly variation
        trust += variation
        
        # Ensure trust stays within 0-1 range
        return max(0.0, min(1.0, trust))

    # Main simulation logic
    def run(self):
        self.logger.debug("Starting simulation...")
    
        # Initialize core components
        society = SocietySystem(initial_population=10_000)  # Start with 10K citizens
        society_state = SocietyState()

        political_system = PoliticalSystem()
        civil_society = CivilSociety()
        parliament = Parliament(300)

        national_bank = NationalBank("Central Bank of Technocratia")
        economy = EconomicModel()

        media_landscape = MediaLandscape()

        # Track demographic factors
        demographics = {
            'age_groups': {'young': 0.3, 'middle': 0.5, 'elderly': 0.2},
            'urban_rural_ratio': 0.7,  # 70% urban
            'education_levels': {'low': 0.2, 'medium': 0.5, 'high': 0.3},
            'income_brackets': {'low': 0.4, 'middle': 0.4, 'high': 0.2}
        }
        
        # Set up political parties and civic organizations
        parties = [
            PoliticalParty("Progressive Alliance", Ideology.CENTER_LEFT),
            PoliticalParty("Conservative Union", Ideology.CENTER_RIGHT),
            PoliticalParty("Green Future", Ideology.LEFT)
        ]
        for party in parties:
            political_system.register_party(party)
            self.logger.debug(f"Registered party: {party.name}")
            
            # Recruit some members
            for _ in range(100):  
                party.recruit_member(random.randint(1, 10_000))

            # Conduct a campaign                
            party.campaign(5000)

            # Propose some policies
            for _ in range(3):  
                area = random.choice(list(PolicyArea))
                strength = random.uniform(-1, 1)
                party.propose_policy(area, strength)

        civic_orgs = [
            CivicOrganization("Green Earth", CauseType.ENVIRONMENTAL),
            CivicOrganization("Education for All", CauseType.EDUCATION),
            CivicOrganization("Health First", CauseType.HEALTHCARE)
        ]
        for org in civic_orgs:
            civil_society.register_organization(org)

            # Recruit some members
            for _ in range(10):  # Recruit some members
                org.recruit_member(random.randint(1, 1000))

            # Organize some activities
            for _ in range(5):
                activity = random.choice(list(ActivityType))
                org.organize_activity(activity)

        # Set up media outlets
        media_outlets = [
            ("Daily Chronicle", MediaType.TRADITIONAL_NEWSPAPER),
            ("Global News Network", MediaType.TV_NETWORK),
            ("TechTruth", MediaType.ONLINE_NEWS_PORTAL),
            ("SocialPulse", MediaType.SOCIAL_MEDIA_PLATFORM),
            ("Independent Voice", MediaType.INDEPENDENT_JOURNALIST)
        ]
        for name, type in media_outlets:
            media_landscape.add_outlet(MediaOutlet(name, type))

        # Simulate presidential election
        presidential_candidates = [
            PresidentialCandidate("Ion Iliescu", is_foreign=False),
            PresidentialCandidate("Ion Ratiu", is_foreign=True)
        ]
        for candidate in presidential_candidates:
            for exam_type in ExamType:
                candidate.take_exam(exam_type)

        presidential_election = PresidentialElection()
        for candidate in presidential_candidates:
            presidential_election.register_candidate(candidate)

        president = presidential_election.conduct_election()
        self.logger.info(f"{president.name} has been elected as President.")

        # Fill the parliament with active members
        for i in range(300):
            if i <= 180:
                chamber = Chamber.DEPUTIES
            else:
                chamber = Chamber.SENATE
            member = Parliamentarian(chamber)  # No need to pass ID anymore
            member.status = ParliamentaryStatus.ACTIVE
            parliament.add_member(member)

        # Simulate parliamentary composition and seat allocation
        political_system.form_parliament(parliament)

        # Initialize government as None
        government = None
       
        # Try to form government
        if parliament.has_quorum():
            prime_minister = president.choose_prime_minister(parliament)
            self.logger.info(f"{prime_minister} has been elected as Prime Minister.")
            government = Government(prime_minister)
            
            if parliament.ratify_government(government):
                self.logger.info("Government successfully formed and ratified!")
                government.update_budget(economy.government_revenue, economy.government_spending)
            else:
                self.logger.info("Government ratification failed.")
                government = None
        else:
            self.logger.info("Parliament lacks quorum. Cannot proceed with government formation.")

        # Simulate presidential review of laws
        if random.random() < 0.9:  # 10% chance each month
            # Create a sample law
            test_law = Law(
                title="Healthcare Reform Act",
                description="A comprehensive reform of the national healthcare system to improve accessibility and quality of care.",
                full_text="This law aims to overhaul the national healthcare system by increasing funding, improving infrastructure, and ensuring universal healthcare coverage for all citizens. The key provisions include: 1) Increased budget allocation for healthcare services, 2) Construction of new hospitals and clinics in underserved areas, 3) Implementation of a universal healthcare insurance program, 4) Recruitment and training of additional healthcare professionals, 5) Introduction of preventive care programs to reduce the incidence of chronic diseases."
            )
            test_law.is_promulgated = True
            test_law.promulgation_date = datetime.now()
            
            # President sends law to referendum
            if president.send_law_to_referendum(test_law, parliament.referendum_system):
                self.logger.info(f"President {president.name} sent law '{test_law.title}' to referendum")
                
                # Assign the referendum before voting
                referendum = parliament.referendum_system.referendums[-1]
                
                # Simulate voting
                voting_population = society.get_voting_population()
                for citizen in voting_population:
                    parliament.referendum_system.vote(citizen, referendum, random.choice([True, False]))
                    
                # Complete the referendum
                parliament.referendum_system.complete_referendum(referendum)
                
                # Handle the results
                president.handle_referendum_result(test_law, parliament.referendum_system)
                
                self.logger.info(
                    f"Presidential review referendum for '{test_law.title}' completed. "
                    f"Results: For: {referendum.votes_for}, Against: {referendum.votes_against}"
                )

        # Main loop simulation
        for month in range(12 if DEBUG_MODE else SIMULATION_MONTHS):
            self.logger.debug(f"\n--- Month {month + 1} ---")

            # Update population
            society.update_population()
            self.logger.debug(f"Updated population. Current size: {len(society.citizens)}")

            # Collect data from various society systems
            economic_data = {
                'gdp_growth': economy.get_gdp_growth(),
                'inflation': national_bank.get_inflation_rate(),
                'unemployment': economy.get_unemployment_rate()
            }          

            political_data = {
                'government_approval': government.approval_rating if government else 0.0,
                'parliament_effectiveness': parliament.get_effectiveness_score(),
                'political_stability': political_system.get_stability_score()
            }          

            social_data = {
                'social_cohesion': civil_society.get_cohesion_score(),
                'media_trust': media_landscape.get_trust_score(),
                'citizen_satisfaction': society.get_satisfaction_score()
            }            

            # Calculate public trust
            public_trust = self.update_public_trust(social_data)

            # Update society state with all indicators including public trust
            society_state.update_indicators(
                economic_data, 
                political_data,
                {**social_data, 'public_trust': public_trust}  # Include public trust in social data
            )

            # Update public trust
            self.logger.debug(f"Updated public trust: {public_trust}")

            # Economic updates
            economy.simulate_month()
            national_bank.update_economic_indicators()
            self.logger.debug(f"Updated economic indicators: {national_bank.print_economic_indicators()}")

            # Update government budget based on economic model
            if government is not None:
                government.update_budget(economy.government_revenue, economy.government_spending)

            # Random bank policy decisions
            if random.random() < 0.3:
                national_bank.set_monetary_policy(random.choice(list(MonetaryPolicy)))
            if random.random() < 0.2:
                national_bank.conduct_open_market_operations(random.uniform(-1_000_000, 1_000_000))
            if random.random() < 0.1:
                national_bank.intervene_in_forex_market(random.uniform(-100_000_000, 100_000_000))            
            if random.random() < 0.05:
                national_bank.print_money(random.uniform(100_000_000, 1_000_000_000))

            # Government operations with proper transition handling
            if government is not None:
                government.update_approval_rating()
                self.logger.info(f"Government approval rating: {government.approval_rating:.2f}%")

                if government.check_dissolution():
                    self.logger.info("Government dissolved. Initiating transition period.")
                    self.interim_government = government
                    government = None
                    # Trigger emergency measures during transition
                    national_bank.emergency_measures()
                    political_system.initiate_emergency_election()
                    continue  # Skip to next month instead of breaking

            # Handle interim government if regular government is dissolved
            if government is None and self.interim_government is not None:
                self.interim_government.run_emergency_operations()
                if political_system.can_form_government():
                    government = political_system.form_new_government()
                    self.interim_government = None
                    self.logger.info("New government formed after transition period.")

            # Parliamentary activities
            if random.random() < 0.4:
                parliament.propose_legislation(f"Bill {month}", "Parliament", f"Content of bill {month}")           

            if parliament.proposed_legislation:
                legislation = parliament.proposed_legislation[0]
                if parliament.vote_on_legislation(legislation):
                    self.logger.info(f"Legislation '{legislation.title}' passed")
                    if random.choice([True, False, False, False]):
                        civil_society.react_to_legislation(legislation)
                else:
                    self.logger.info(f"Legislation '{legislation.title}' failed")

            # Presidential actions with proper checks
            if random.random() < 0.1:
                member_to_dismiss = random.choice(parliament.members) if parliament.members else None
                if member_to_dismiss is not None:
                    dismissal_reason = president.evaluate_dismissal_cause(member_to_dismiss)
                    if dismissal_reason:
                        self.logger.info(f"President attempting to dismiss parliamentarian for: {dismissal_reason}")
                        if president.propose_dismissal(member_to_dismiss, dismissal_reason):
                            self.logger.info(f"President proposed dismissal of parliamentarian {member_to_dismiss.id}")
                            if parliament.vote_on_dismissal(member_to_dismiss):
                                parliament.remove_member(member_to_dismiss)
                                self.logger.info(f"Parliamentarian {member_to_dismiss.id} dismissed after parliamentary approval")
                        else:
                            self.logger.info("Dismissal proposal failed")

            # Media influence implementation
            news_cycle = media_landscape.simulate_news_cycle()
            self.process_news_cycle(news_cycle, society.citizens, government if government else self.interim_government)
            
            # Update citizen opinions based on media coverage
            for citizen in society.citizens:
                citizen.process_media_influence(news_cycle)

            # Enhanced referendum implementation
            if random.random() < 0.05:
                referendum = parliament.propose_referendum(
                    f"Referendum {month}",
                    f"Description of referendum {month}",
                    ReferendumType.NATIONAL
                )
                
                # Proper campaign period
                media_landscape.cover_referendum(referendum)
                for party in political_system.parties:
                    party.campaign_for_referendum(referendum)
                
                # Citizens vote based on their attributes and campaign influence
                parliament.referendum_system.start_referendum(referendum)
                voting_population = society.get_voting_population()
                for citizen in voting_population:
                    vote_choice = citizen.decide_referendum_vote(
                        referendum,
                        media_landscape.get_referendum_coverage(referendum),
                        political_system.get_party_positions(referendum)
                    )
                    parliament.referendum_system.vote(citizen, referendum, vote_choice)
                
                parliament.referendum_system.complete_referendum(referendum)
                self.logger.info(f"Referendum '{referendum.title}' results: For: {referendum.votes_for}, Against: {referendum.votes_against}")

            # Enhanced social tension calculation
            social_tension = society.calculate_social_tensions(
                economy=economy,
                media_influence=media_landscape.get_tension_impact(),
                policy_effects=parliament.get_active_legislation(),
                government_approval=government.approval_rating if government else 0
            ) or 0.0  # Provide default value of 0.0 if None is returned
            
            self.logger.debug(f"Calculated social tensions: {social_tension:.2f}")

            if month % 3 == 0:  # Every 3 months
                tension_level = society.calculate_social_tensions(economy) or 0.0  # Added default value
                self.logger.info(f"Social Tension Level: {tension_level:.2f}")
                
                if tension_level > 0.7:
                    self.logger.warning("High social tensions detected!")
                    civil_society.organize_protests()
                    media_landscape.increase_coverage()
                    government.implement_social_measures()

        # Simulation reports
        self.logger.info("\n--- Simulation Reports ---")
        self.logger.info(f"Economic indicators: {economy.get_economic_indicators()}")
        self.logger.info("\n--")
        self.logger.info(national_bank.generate_economic_report())
        self.logger.info("\n--")
        if not DEBUG_MODE:
            self.logger.info(media_landscape.generate_media_report())
            self.logger.info("\n--")
        self.logger.info(f"Total political system popularity: {political_system.total_popularity():.2f}")
        self.logger.info(f"Total civil society influence: {civil_society.total_influence():.2f}")

        # Add to the simulation reports section
        self.logger.info("\n--- Society State Report ---")
        self.logger.info(society_state.get_state_report())
    
def run_simulation(debug_mode=False):
    global DEBUG_MODE
    DEBUG_MODE = debug_mode
    simulation = Simulation(debug_mode)
    simulation.run()

if __name__ == "__main__":
    simulation = Simulation(debug_mode=True)
    simulation.run()
