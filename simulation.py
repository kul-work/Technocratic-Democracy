from models.citizen import *
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
        pass
    
    # Main simulation logic
    def run(self):
        # Initialize core components
        political_system = PoliticalSystem()
        civil_society = CivilSociety()
        economy = EconomicModel()
        national_bank = NationalBank("Central Bank of Technokratia")
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
            party.recruit_members(100)
            party.campaign(5000)
            party.propose_policies(3)

        civic_orgs = [
            CivicOrganization("Green Earth", CauseType.ENVIRONMENTAL),
            CivicOrganization("Education for All", CauseType.EDUCATION),
            CivicOrganization("Health First", CauseType.HEALTHCARE)
        ]
        for org in civic_orgs:
            civil_society.register_organization(org)
            org.recruit_members(50)
            org.organize_activities(3)

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
            PresidentialCandidate("John Doe", is_foreign=False),
            PresidentialCandidate("Jane Smith", is_foreign=True)
        ]
        for candidate in presidential_candidates:
            for exam_type in ExamType:
                candidate.take_exam(exam_type)

        presidential_election = PresidentialElection()
        for candidate in presidential_candidates:
            presidential_election.register_candidate(candidate)

        president = presidential_election.conduct_election()
        print(f"{president.name} has been elected as President.")

        # Simulate parliamentary election
        political_system.conduct_election(parliament)

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

            # Economic updates
            economy.simulate_month()
            national_bank.update_economic_indicators()
            if random.random() < 0.3:
                national_bank.set_monetary_policy(random.choice(list(MonetaryPolicy)))

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
                member_to_dismiss = random.choice(parliament.members)
                if president.propose_dismissal(member_to_dismiss):
                    print(f"President proposed dismissal of parliamentarian {member_to_dismiss.id}")
                    if not president.veto_dismissal(member_to_dismiss):
                        parliament.remove_member(member_to_dismiss)
                        print(f"Parliamentarian {member_to_dismiss.id} has been dismissed")

            # Referendum (occasional)
            if random.random() < 0.05:
                referendum = parliament.propose_referendum(f"Referendum {month}", f"Description of referendum {month}", ReferendumType.NATIONAL)
                parliament.referendum_system.start_referendum(referendum)
                for citizen in range(1000):  # Simulate 1000 citizens voting
                    parliament.referendum_system.vote(Citizen(random.randint(18, 80), f"Region_{random.randint(1,10)}"), referendum, random.choice([True, False]))
                parliament.referendum_system.complete_referendum(referendum)
                print(f"Referendum '{referendum.title}' results: For: {referendum.votes_for}, Against: {referendum.votes_against}")

            # Media influence
            news_cycle = media_landscape.simulate_news_cycle()
            # TODO: Implement process_news_cycle to affect citizens and government

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
        print(f"Total civil society influence: {civil_society.total_influence()}")

def run_simulation():
    simulation = Simulation()
    simulation.run()
