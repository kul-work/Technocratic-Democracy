import random
from enum import Enum
from datetime import datetime, timedelta
from typing import List, Optional

from .citizen import *
from .legislative import *
from .referendum import *

class President:
    def __init__(self, name):
        self.name = name
        self.term_start_date = datetime.now()
        self.term_end_date = self.term_start_date + timedelta(days=5*365)  # 5 years term
        self.referendum_system = ReferendumSystem(Parliament) #TODO: will fail, current parlament ??
        self.vetoed_laws = []
        self.sent_to_referendum = []

    def is_term_expired(self) -> bool:
        return datetime.now() > self.term_end_date

    def propose_dismissal(self, parliamentarian: Parliamentarian) -> bool:
        # Simplified logic for proposing dismissal
        return random.random() > 0.7

    def veto_dismissal(self, parliamentarian: Parliamentarian) -> bool:
        # Simplified logic for vetoing dismissal
        return random.random() > 0.6

    #TODO: use it
    def call_referendum(self, law: Legislation) -> bool:
        # Simplified logic for calling a referendum
        return random.random() > 0.8
    
    def propose_referendum(self, title: str, description: str, referendum_type: ReferendumType) -> Referendum:
        return self.referendum_system.propose_referendum(title, description, referendum_type)
    
    def choose_prime_minister(self, parliament: Parliament) -> Parliamentarian:
        while True:
            # Create a random parliamentarian first
            random_parliamentarian = Parliamentarian(random.choice([Chamber.DEPUTIES, Chamber.SENATE]))
            candidate = self.nominate_candidate(random_parliamentarian.name, parliament)
            
            # Continue loop if no candidate was found
            if not candidate:
                continue
                
            if parliament.has_quorum() and parliament.propose_legislation('New Prime Minister', "President", f'Appointment of {candidate.name} as Prime Minister', ignore_quorum=True):
                legislation = parliament.proposed_legislation[-1]  # Get the last proposed legislation
                if parliament.vote_on_legislation(legislation, ignore_quorum=True):
                    return candidate
                    
    def nominate_candidate(self, name: str, parliament: Parliament) -> Optional[Parliamentarian]:
        # Search for parliamentarian with that name
        parliamentarian = parliament.find_member_by_name(name)
        if parliamentarian:
            return parliamentarian
        else:
            return None
        
    def send_law_to_referendum(self, law: 'Law', referendum_system: ReferendumSystem) -> bool:
        """
        Sends an already promulgated law to a national referendum for a vote of confidence.
        
        Args:
            law: The promulgated law to review
            referendum_system: The referendum system to use
            
        Returns:
            bool: True if the referendum was created successfully
        """
        # Check if law is actually promulgated
        if not law.is_promulgated:
            return False
            
        # Check if law was already sent to referendum
        if law in self.sent_to_referendum:
            return False
            
        # Create the presidential review referendum
        referendum = referendum_system.create_presidential_review_referendum(law, self)
        
        if referendum:
            self.sent_to_referendum.append(law)
            return True
            
        return False

    def handle_referendum_result(self, law: 'Law', referendum_system: ReferendumSystem) -> None:
        """
        Handles the result of a presidential review referendum.
        
        Args:
            law: The law that was reviewed
            referendum_system: The referendum system used
        """
        # Find the corresponding referendum
        referendum = next(
            (ref for ref in referendum_system.referendums 
             if ref.type == ReferendumType.PRESIDENTIAL_REVIEW 
             and law.title in ref.title),
            None
        )
        
        if not referendum:
            return
            
        # Check the result
        if referendum_system.handle_presidential_review_result(referendum):
            # Law is confirmed by the people - nothing more to do
            pass
        else:
            # Law failed the referendum - return it to Parliament
            law.is_promulgated = False
            law.promulgation_date = None
            # The law should be returned to Parliament for revision or repeal
            self.vetoed_laws.append(law)
    
    def evaluate_dismissal_cause(self, parliamentarian):
        # Add a safer check that doesn't rely on the ethics_violations attribute
        if getattr(parliamentarian, 'ethics_violations', 0) > 3:
            return "Multiple ethics violations"
        
        # Add other dismissal conditions here
        if random.random() < 0.1:  # 10% chance of finding other violations
            return "Violation of parliamentary duties"
            
        return None

## Presidential Candidates and Elections
class ExamType(Enum):
    FOREIGN_POLICY = "Foreign Policy"
    HISTORY = "History"
    ECONOMY = "Economy"
    INTERNAL_LEGISLATION = "Internal Legislation"
    MEDICAL = "Medical"
    LANGUAGE = "Language"

class ExamResult:
    def __init__(self, exam_type, score):
        self.exam_type = exam_type
        self.score = score

class PresidentialCandidate:
    def __init__(self, name: str, is_foreign: bool):
        self.name = name
        self.is_foreign = is_foreign
        self.exam_results = []

    def take_exam(self, exam_type: ExamType) -> None:
        score = 0.7 + (0.3 * random.random())  # Simplified exam scoring
        self.exam_results.append(ExamResult(exam_type, score))

    def has_passed_exams(self) -> bool:
        required_exams = [ExamType.FOREIGN_POLICY, ExamType.HISTORY, ExamType.ECONOMY, 
                          ExamType.INTERNAL_LEGISLATION, ExamType.MEDICAL]
        if self.is_foreign:
            required_exams.append(ExamType.LANGUAGE)

        for exam in required_exams:
            if not any(result.exam_type == exam and result.score >= 0.7 for result in self.exam_results):
                return False
        return True
    
class PresidentialElection:
    def __init__(self):
        self.candidates = []

    def register_candidate(self, candidate: 'Citizen') -> Citizen:
        if candidate.has_passed_exams():
            self.candidates.append(candidate)

    def conduct_election(self) -> President:
        if not self.candidates:
            return None
        winner = random.choice(self.candidates)
        return President(winner.name)
## END Presidential Candidates and Elections


