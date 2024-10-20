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

        #legislative
        if (True):
            parliament = Parliament(300)  # 300 total seats

            # Create a civic organization
            org = CivicOrganization("Social Equality Group")

            # Propose and add a candidate (scholarship and regular)
            for is_scholarship in [True, False]:
                candidate = org.propose_candidate(Chamber.DEPUTIES)
                candidate.is_scholarship = is_scholarship
                if parliament.conduct_admission_interview(candidate):
                    parliament.add_member(candidate)
                    print(f"New {'scholarship' if is_scholarship else 'regular'} member admitted")

            # Simulate a year passing # TODO : where's the time param??
            parliament.update_all_members()

            # Nominate a member for the admission committee
            for member in parliament.members:
                if parliament.nominate_for_admission_committee(member):
                    if parliament.vote_for_admission_committee(member):
                        member.admission_committee_member = True
                        parliament.admission_committee.append(member)
                        print(f"Member {member.id} added to the admission committee")
                        break

            # Simulate internal legislation proposal
            if parliament.propose_internal_legislation():
                print("Internal legislation proposed successfully")

            # Simulate external legislation proposal
            if parliament.process_external_legislation(org):
                print("External legislation from civic organization processed successfully")

            # Simulate legislation proposal
            if parliament.propose_legislation("Economic Reform", "Parliament", "Content of the economic reform..."):
                print("Legislation proposed successfully")

            legislation = parliament.proposed_legislation[0]
            if parliament.vote_on_legislation(legislation):
                print(f"Legislation '{legislation.title}' passed")
            else:
                print(f"Legislation '{legislation.title}' failed")

            # Simulate no-confidence vote
            if parliament.has_quorum():
                if parliament.vote_no_confidence():
                    print("No-confidence vote succeeded")
            else:
                print("Cannot hold no-confidence vote: No quorum")

        #government
        if (True):
            president = President()
            parliament = Parliament(300)  # Using the Parliament class from legislative.py

            # Add some parliamentarians
            for _ in range(100):
                citizen = Citizen(random.randint(25, 70), random.choice(["Male", "Female"]), "Region1")
                citizen.citizenship_status = CitizenshipStatus.CITIZEN
                parliamentarian = Parliamentarian(parliament.total_seats + 1, random.choice(list(Chamber)))
                parliament.add_member(parliamentarian)

            # Simulate prime minister selection
            if parliament.has_quorum():
                prime_minister = president.choose_prime_minister(parliament)
                print(f"{prime_minister} has been elected as Prime Minister.")
                government = Government(prime_minister)

                for ministry in government.ministries.values():
                    for _ in range(random.randint(3, MAX_ADVISORS)):
                        advisor = Advisor(f"Advisor {random.randint(1000, 9999)}")
                        ministry.add_advisor(advisor)
                    ministry.set_minister(random.choice(ministry.advisors))

                # Ratify the government
                if parliament.has_quorum() and parliament.propose_internal_legislation():
                    government.total_budget = 1_000_000_000  # Example budget
                    government.allocate_budget()
                    print("Government successfully formed and ratified!")
                else:
                    print("Government ratification failed.")
            else:
                print("Parliament lacks quorum. Cannot proceed with government formation.")

            # Simulate time passage and government operations
            if 'government' in locals():
                government.formation_date = datetime.now() - timedelta(days=1095)

                for _ in range(12):  # Simulate 12 months # TODO: test & improve this
                    if government.check_dissolution():
                        print("Government automatically dissolved after 3 years.")
                        break

                    government.update_approval_rating() # Monthly updates
                    print(f"Government approval rating: {government.approval_rating:.2f}%")

                    # Simulate state of emergency
                    if random.random() > 0.9:  # 10% chance of emergency each month
                        if government.declare_emergency():
                            print("State of emergency declared for 4 months.")
                            government.formation_date = datetime.now() - timedelta(days=1155)  # 3 years and 2 months

                            if government.check_emergency_status():
                                print("State of emergency expired.")
                            if government.check_dissolution():
                                print("Government dissolved after the expiration of the state of emergency.")
                                # TODO: - new government here

                # Output a checkup status
                if government.status == GovernmentStatus.ACTIVE:
                    print("Government completed its term.")
                elif government.status == GovernmentStatus.DISSOLVED:
                    print("Government was dissolved.")
                elif government.status == GovernmentStatus.EMERGENCY:
                    print("Government ended its term in a state of emergency.")

        #president
        if (True):
            candidate1 = PresidentialCandidate("John Doe", is_foreign=False)
            candidate2 = PresidentialCandidate("Jane Smith", is_foreign=True)

            for exam_type in ExamType:
                candidate1.take_exam(exam_type)
                candidate2.take_exam(exam_type)

            election = PresidentialElection()
            election.register_candidate(candidate1)
            election.register_candidate(candidate2)

            president = election.conduct_election()

            if president:
                print(f"{president.name} has been elected as President.")
                
                # Simulate presidential actions
                parliament = Parliament(300)  # Assuming we have a Parliament instance
                
                for member in parliament.members[:5]:  # Try to dismiss first 5 members
                    if president.propose_dismissal(member):
                        print(f"President proposed dismissal of parliamentarian {member.id}")
                        if not president.veto_dismissal(member):
                            parliament.remove_member(member)
                            print(f"Parliamentarian {member.id} has been dismissed")

                # Simulate calling a referendum on a law
                if parliament.proposed_legislation:
                    law = parliament.proposed_legislation[0]
                    if president.call_referendum(law):
                        print(f"President called a referendum on '{law.title}'")

                # Simulate Senate initiating suspension procedure
                if parliament.initiate_presidential_suspension():
                    print("Senate has initiated the presidential suspension procedure")
                    if parliament.conduct_suspension_referendum():
                        print("Referendum passed. The President has been suspended.")
                    else:
                        print("Referendum failed. The President remains in office.")
            else:
                print("No President was elected.")
        
        #referendum
        if (True):
            parliament = Parliament(300)
            citizens = [Citizen(random.randint(16, 80), f"Region_{i}") for i in range(10)]

            # Propose and start a referendum
            referendum = parliament.propose_referendum("New Economic Policy", "Description of the policy", ReferendumType.NATIONAL)
            parliament.referendum_system.start_referendum(referendum)

            # Simulate voting
            for citizen in citizens:
                parliament.referendum_system.vote(citizen, referendum, random.choice([True, False]))

            # Complete the referendum
            parliament.referendum_system.complete_referendum(referendum)

            # Check results
            print(f"Referendum '{referendum.title}' results:")
            print(f"Votes For: {referendum.votes_for}")
            print(f"Votes Against: {referendum.votes_against}")
            print(f"Total Votes: {referendum.total_votes}")
            print(f"Status: {referendum.status}")
            print(f"Blockchain Hash: {referendum.blockchain_hash}")

            # Monitor referendums
            print("\nReferendum Monitoring:")
            monitoring_results = parliament.referendum_system.monitor_referendums()
            for key, value in monitoring_results.items():
                print(f"{key.capitalize()}: {value}")

        #political_party
            political_system = PoliticalSystem()

            party1 = PoliticalParty("Progressive Alliance", Ideology.CENTER_LEFT)
            party2 = PoliticalParty("Conservative Union", Ideology.CENTER_RIGHT)
            party3 = PoliticalParty("Green Future", Ideology.LEFT)

            political_system.register_party(party1)
            political_system.register_party(party2)
            political_system.register_party(party3)

            # Simulate some activities
            for party in political_system.parties:
                for _ in range(100):  # Recruit some members
                    party.recruit_member(random.randint(1, 10_000))
                
                party.campaign(5000)  # Conduct a campaign

                for _ in range(3):  # Propose some policies
                    area = random.choice(list(PolicyArea))
                    strength = random.uniform(-1, 1)
                    party.propose_policy(area, strength)

            # Simulate an election
            parliament = Parliament(300)
            political_system.conduct_election(parliament)

            # Simulate proposing legislation
            political_system.propose_legislation(parliament)

            print(f"Total political system popularity: {political_system.total_popularity()}")
            for party in political_system.get_most_popular_parties(3):
                print(f"{party.name}: Popularity = {party.popularity:.2f}, Members = {len(party.members)}")
                print(f"  Key policies: {', '.join(f'{area.value}: {strength:.2f}' for area, strength in party.policies.items() if abs(strength) > 0.5)}")

        #civil_society
        if (True):
            civil_society = CivilSociety()

            org1 = CivicOrganization("Green Earth", CauseType.ENVIRONMENTAL)
            org2 = CivicOrganization("Education for All", CauseType.EDUCATION)
            org3 = CivicOrganization("Health First", CauseType.HEALTHCARE)

            civil_society.register_organization(org1)
            civil_society.register_organization(org2)
            civil_society.register_organization(org3)

            # Simulate some activities
            for org in civil_society.organizations:
                for _ in range(10):  # Recruit some members
                    org.recruit_member(random.randint(1, 1000))
                
                for _ in range(5):  # Organize some activities
                    activity = random.choice(list(ActivityType))
                    org.organize_activity(activity)

            # Simulate proposing legislation
            parliament = Parliament(300)  # Assuming we have a Parliament instance
            civil_society.propose_legislation(parliament)

            # Simulate reacting to legislation
            if parliament.proposed_legislation:
                civil_society.react_to_legislation(parliament.proposed_legislation[0])

            print(f"Total civil society influence: {civil_society.total_influence()}")
            for org in civil_society.get_most_influential_orgs(3):
                print(f"{org.name}: Influence = {org.influence:.2f}, Members = {len(org.members)}")

        #economy
        if (True):
            economy = EconomicModel()
            for year in range(5):
                economy.simulate_year()
                print(f"Year {year + 1} Economic Indicators:")
                print(economy.get_economic_indicators())
                print("\n")

        #bank_national
        if (True):
            national_bank = NationalBank("Central Bank of Technocratia")

            # Simulate some economic activities
            for _ in range(12):  # Simulate 12 months
                national_bank.update_economic_indicators()
                
                # Random policy decisions
                if random.random() < 0.3:
                    national_bank.set_monetary_policy(random.choice(list(MonetaryPolicy)))
                
                if random.random() < 0.2:
                    national_bank.conduct_open_market_operations(random.uniform(-1_000_000, 1_000_000))
                
                if random.random() < 0.1:
                    national_bank.intervene_in_forex_market(random.uniform(-100_000_000, 100_000_000))
                
                if random.random() < 0.05:
                    national_bank.print_money(random.uniform(100_000_000, 1_000_000_000))

            print(national_bank.generate_economic_report())

        #media
        if (True):
            media_landscape = MediaLandscape()

            # Add various media outlets
            media_landscape.add_outlet(MediaOutlet("Daily Chronicle", MediaType.TRADITIONAL_NEWSPAPER))
            media_landscape.add_outlet(MediaOutlet("Global News Network", MediaType.TV_NETWORK))
            media_landscape.add_outlet(MediaOutlet("TechTruth", MediaType.ONLINE_NEWS_PORTAL))
            media_landscape.add_outlet(MediaOutlet("SocialPulse", MediaType.SOCIAL_MEDIA_PLATFORM))
            media_landscape.add_outlet(MediaOutlet("Independent Voice", MediaType.INDEPENDENT_JOURNALIST))

            # Simulate several news cycles
            for _ in range(10):
                news_cycle = media_landscape.simulate_news_cycle()

            print(media_landscape.generate_media_report())

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

def run_simulation():
    simulation = Simulation()
    simulation.run()