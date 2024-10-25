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
            candidate = self.nominate_candidate('')
            if parliament.has_quorum() and parliament.propose_legislation('New Prime Minister', "President", f'Appointment of {candidate.name} as Prime Minister', ignore_quorum=True):
                legislation = parliament.proposed_legislation[-1]  # Get the last proposed legislation
                if parliament.vote_on_legislation(legislation, ignore_quorum=True):
                    return candidate
                    
    def nominate_candidate(self, name: str) -> Parliamentarian:
        # Simplified simulation of nomination
        # TODO: link param 'name' to Parliament
        return Parliamentarian(random.choice([Chamber.DEPUTIES, Chamber.SENATE]))
    
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

