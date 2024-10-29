from enum import Enum
from typing import Dict, Optional
from datetime import datetime

class PolicyStatus(Enum):
    PROPOSED = "Proposed"
    ACTIVE = "Active"
    EXPIRED = "Expired"
    REJECTED = "Rejected"

class PolicyArea(Enum):
    ECONOMY = "Economy"
    HEALTHCARE = "Healthcare"
    EDUCATION = "Education"
    ENVIRONMENT = "Environment"
    FOREIGN_POLICY = "Foreign Policy"
    SOCIAL_WELFARE = "Social Welfare"
    INFRASTRUCTURE = "Infrastructure"
    TECHNOLOGY = "Technology"
    DEFENSE = "Defense"
    JUSTICE = "Justice"
    CULTURE = "Culture"
    AGRICULTURE = "Agriculture"
    ENERGY = "Energy"
    TRANSPORTATION = "Transportation"
    HOUSING = "Housing"
    IMMIGRATION = "Immigration"

class Policy:
    def __init__(self, 
                 title: str,
                 area: PolicyArea,
                 strength: float,
                 proposer: str,
                 description: Optional[str] = None):
        self.title = title
        self.area = area
        self.strength = max(-1, min(1, strength))  # Ensure policy strength is between -1 and 1
        self.proposer = proposer
        self.description = description
        self.status = PolicyStatus.PROPOSED
        self.creation_date = datetime.now()
        self.implementation_date: Optional[datetime] = None
        self.expiration_date: Optional[datetime] = None
        
        # Track policy effects
        self.economic_impact: float = 0.0
        self.social_impact: float = 0.0
        self.environmental_impact: float = 0.0
        
        # Cost and resource allocation
        self.implementation_cost: float = 0.0
        self.annual_budget: float = 0.0
        
        # Policy effectiveness metrics
        self.effectiveness_score: float = 0.0
        self.public_approval: float = 0.0
        
    def implement(self) -> None:
        """Activate the policy and set implementation date"""
        self.status = PolicyStatus.ACTIVE
        self.implementation_date = datetime.now()
        
    def expire(self) -> None:
        """Mark policy as expired"""
        self.status = PolicyStatus.EXPIRED
        self.expiration_date = datetime.now()
        
    def reject(self) -> None:
        """Mark policy as rejected"""
        self.status = PolicyStatus.REJECTED
        
    def calculate_impacts(self, economic_model, society_model) -> Dict[str, float]:
        """Calculate various impact scores based on policy strength and area"""
        impacts = {
            'economic': 0.0,
            'social': 0.0,
            'environmental': 0.0
        }
        
        # Different calculations based on policy area
        if self.area == PolicyArea.ECONOMY:
            impacts['economic'] = self.strength * 0.8
            impacts['social'] = self.strength * 0.4
        elif self.area == PolicyArea.HEALTHCARE:
            impacts['social'] = self.strength * 0.7
            impacts['economic'] = self.strength * 0.3
        elif self.area == PolicyArea.EDUCATION:
            impacts['social'] = self.strength * 0.6
            impacts['economic'] = self.strength * 0.4
        elif self.area == PolicyArea.ENVIRONMENT:
            impacts['environmental'] = self.strength * 0.9
            impacts['economic'] = self.strength * -0.2
        elif self.area == PolicyArea.SOCIAL_WELFARE:
            impacts['social'] = self.strength * 0.8
            impacts['economic'] = self.strength * -0.3
        elif self.area == PolicyArea.INFRASTRUCTURE:
            impacts['economic'] = self.strength * 0.6
            impacts['social'] = self.strength * 0.3
            impacts['environmental'] = self.strength * -0.2
        elif self.area == PolicyArea.TECHNOLOGY:
            impacts['economic'] = self.strength * 0.7
            impacts['social'] = self.strength * 0.4
            impacts['environmental'] = self.strength * 0.2
        elif self.area == PolicyArea.DEFENSE:
            impacts['economic'] = self.strength * -0.4
            impacts['social'] = self.strength * 0.3
        elif self.area == PolicyArea.JUSTICE:
            impacts['social'] = self.strength * 0.8
            impacts['economic'] = self.strength * 0.2
        elif self.area == PolicyArea.CULTURE:
            impacts['social'] = self.strength * 0.9
            impacts['economic'] = self.strength * 0.1
        elif self.area == PolicyArea.AGRICULTURE:
            impacts['economic'] = self.strength * 0.5
            impacts['environmental'] = self.strength * -0.3
            impacts['social'] = self.strength * 0.2
        elif self.area == PolicyArea.ENERGY:
            impacts['economic'] = self.strength * 0.6
            impacts['environmental'] = self.strength * self.strength  # Quadratic impact
        elif self.area == PolicyArea.TRANSPORTATION:
            impacts['economic'] = self.strength * 0.5
            impacts['environmental'] = self.strength * -0.4
            impacts['social'] = self.strength * 0.3
        elif self.area == PolicyArea.HOUSING:
            impacts['social'] = self.strength * 0.7
            impacts['economic'] = self.strength * 0.4
        elif self.area == PolicyArea.IMMIGRATION:
            impacts['social'] = self.strength * 0.6
            impacts['economic'] = self.strength * 0.5
        
        self.economic_impact = impacts['economic']
        self.social_impact = impacts['social']
        self.environmental_impact = impacts['environmental']
        
        return impacts
        
    def update_effectiveness(self, economic_indicators: Dict, social_indicators: Dict) -> None:
        """Update policy effectiveness based on various indicators"""
        # Calculate effectiveness based on policy area and relevant indicators
        if self.area == PolicyArea.ECONOMY:
            self.effectiveness_score = (
                economic_indicators.get('gdp_growth', 0) * 0.4 +
                economic_indicators.get('unemployment_rate', 0) * -0.3 +
                economic_indicators.get('inflation_rate', 0) * -0.3
            )
        elif self.area == PolicyArea.SOCIAL_WELFARE:
            self.effectiveness_score = (
                social_indicators.get('social_cohesion', 0) * 0.5 +
                social_indicators.get('public_trust', 0) * 0.3 +
                economic_indicators.get('unemployment_rate', 0) * -0.2
            )
        elif self.area == PolicyArea.INFRASTRUCTURE:
            self.effectiveness_score = (
                economic_indicators.get('gdp_growth', 0) * 0.3 +
                social_indicators.get('public_satisfaction', 0) * 0.4 +
                economic_indicators.get('investment_rate', 0) * 0.3
            )
        elif self.area == PolicyArea.TECHNOLOGY:
            self.effectiveness_score = (
                economic_indicators.get('innovation_index', 0) * 0.5 +
                economic_indicators.get('productivity_growth', 0) * 0.3 +
                social_indicators.get('digital_literacy', 0) * 0.2
            )
        # Add similar calculations for other policy areas 