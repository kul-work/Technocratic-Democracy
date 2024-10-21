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

class Simulation:
    def __init__(self):
        self.society = SocietySystem(initial_population=100_000)  # Start with 100,000 citizens
        pass

    # Example of how news could affect other parts of the simulation
    def process_news_cycle(news_cycle: List[Dict], citizens: List['Citizen'], government: 'Government'):
        for news in news_cycle:
            if news['category'] == NewsCategory.POLITICS:
                # Affect citizen's trust in government
                for citizen in citizens:
                    citizen.trust_in_government += news['impact'] * 0.01 * (1 if news['bias'] > 0 else -1)
            elif news['category'] == NewsCategory.ECONOMY:
                # Affect government's economic policy
                government.adjust_economic_policy(news['impact'] * 0.1)
            # ... handle other categories
    
    # Main simulation logic
    def run(self):
        # Initialize core components
        political_system = PoliticalSystem()
        civil_society = CivilSociety()
        economy = EconomicModel()
        
        national_bank = NationalBank("Central Bank of Teknos")
        media_landscape = MediaLandscape()
        parliament = Parliament(300)
        
        # Set up political parties and civic organizations
        parties = [
            PoliticalParty("Progressive Alliance", Ideology.CENTER_LEFT),
            PoliticalParty("Conservative Union", Ideology.CENTER_RIGHT),
            PoliticalParty("Green Future", Ideology.LEFT)
        ]
        for party in parties:
            political_system.register_party(party)

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
        print(f"{president.name} has been elected as President.")

        # Simulate parliamentary composition and seat allocation
        political_system.form_parliament(parliament)

        # Form government
        if parliament.has_quorum():
            prime_minister = president.choose_prime_minister(parliament)
            print(f"{prime_minister} has been elected as Prime Minister.")
            government = Government(prime_minister)
            government.form_ministries()
            
            if parliament.ratify_government(government):
                print("Government successfully formed and ratified!")
            else:
                print("Government ratification failed.")
        else:
            print("Parliament lacks quorum. Cannot proceed with government formation.")

        # Main simulation loop (e.g., 4 years / 48 months)
        for month in range(48):
            print(f"\n--- Month {month + 1} ---")

            # Update population
            self.society.update_population()

            # Economic updates
            economy.simulate_month()
            national_bank.update_economic_indicators()

            # Random bank policy decisions
            if random.random() < 0.3:
                national_bank.set_monetary_policy(random.choice(list(MonetaryPolicy)))
            
            if random.random() < 0.2:
                national_bank.conduct_open_market_operations(random.uniform(-1_000_000, 1_000_000))
            
            if random.random() < 0.1:
                national_bank.intervene_in_forex_market(random.uniform(-100_000_000, 100_000_000))
            
            if random.random() < 0.05:
                national_bank.print_money(random.uniform(100_000_000, 1_000_000_000))

            # Government operations
            if 'government' in locals():
                government.update_approval_rating()
                print(f"Government approval rating: {government.approval_rating:.2f}%")

                if government.check_dissolution():
                    print("Government dissolved. New elections needed.")
                    # TODO: Implement new election logic here
                    break

            # Parliamentary activities
            if random.random() < 0.4:
                parliament.propose_legislation(f"Bill {month}", "Parliament", f"Content of bill {month}")
            
            if parliament.proposed_legislation:
                legislation = parliament.proposed_legislation[0]
                if parliament.vote_on_legislation(legislation):
                    print(f"Legislation '{legislation.title}' passed")
                    civil_society.react_to_legislation(legislation)
                else:
                    print(f"Legislation '{legislation.title}' failed")

            # Presidential actions
            if random.random() < 0.1:
                member_to_dismiss = random.choice(parliament.members) if parliament.members else None
                if member_to_dismiss is not None and president.propose_dismissal(member_to_dismiss):
                    print(f"President proposed dismissal of parliamentarian {member_to_dismiss.id}")
                    if not president.veto_dismissal(member_to_dismiss):
                        parliament.remove_member(member_to_dismiss)
                        print(f"Parliamentarian {member_to_dismiss.id} has been dismissed")

            # Referendum (occasional)
            if random.random() < 0.05:
                referendum = parliament.propose_referendum(f"Referendum {month}", f"Description of referendum {month}", ReferendumType.NATIONAL)
                parliament.referendum_system.start_referendum(referendum)
                voting_population = self.society.get_voting_population()
                for citizen in voting_population:
                    parliament.referendum_system.vote(citizen, referendum, random.choice([True, False]))
                parliament.referendum_system.complete_referendum(referendum)
                print(f"Referendum '{referendum.title}' results: For: {referendum.votes_for}, Against: {referendum.votes_against}")

            # Media influence
            news_cycle = media_landscape.simulate_news_cycle()
            # TODO: Apply process_news_cycle() to affect citizens and government

            # Civil society activities
            if random.random() < 0.2:
                civil_society.propose_legislation(parliament)

            # Political party activities
            for party in political_system.parties:
                party.campaign(1000)  # Smaller ongoing campaigns

        # End of simulation reports
        print("\n--- End of Simulation Reports ---")
        print(economy.get_economic_indicators())
        print(national_bank.generate_economic_report())
        print(media_landscape.generate_media_report())
        print(f"Total political system popularity: {political_system.total_popularity()}")
        # for party in political_system.get_most_popular_parties(3):
        #     print(f"{party.name}: Popularity = {party.popularity:.2f}, Members = {len(party.members)}")
        #     print(f"  Key policies: {', '.join(f'{area.value}: {strength:.2f}' for area, strength in party.policies.items() if abs(strength) > 0.5)}")
        print(f"Total civil society influence: {civil_society.total_influence()}")
        # for org in civil_society.get_most_influential_orgs(3):
        #     print(f"{org.name}: Influence = {org.influence:.2f}, Members = {len(org.members)}")

def run_simulation():
    simulation = Simulation()
    simulation.run()
