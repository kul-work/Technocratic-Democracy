from enum import Enum
from dataclasses import dataclass
from typing import Dict, Any

class SocietyStateType(Enum):
    STABLE = "stable"
    ECONOMIC_CRISIS = "economic_crisis"
    POLITICAL_CRISIS = "political_crisis"
    SOCIAL_UNREST = "social_unrest"
    STATE_OF_EMERGENCY = "state_of_emergency"
    PROSPERITY = "prosperity"

@dataclass
class SocietyIndicators:
    economic_stability: float = 0.0    # -1.0 to 1.0
    political_stability: float = 0.0   # -1.0 to 1.0
    social_cohesion: float = 0.0       # -1.0 to 1.0
    public_trust: float = 0.0          # -1.0 to 1.0  

class SocietyState:
    def __init__(self):
        self.current_state = SocietyStateType.STABLE
        self.indicators = SocietyIndicators()
        self.state_history = []        

    def update_indicators(self, 
                         economic_data: Dict[str, float],
                         political_data: Dict[str, float],
                         social_data: Dict[str, float]) -> None:

        # Update indicators based on various inputs
        self.indicators.economic_stability = self._calculate_economic_stability(economic_data)
        self.indicators.political_stability = self._calculate_political_stability(political_data)
        self.indicators.social_cohesion = self._calculate_social_cohesion(social_data)        

        # Determine if state transition is needed
        self._evaluate_state_transition()

    def _evaluate_state_transition(self) -> None:
        previous_state = self.current_state

        # Example transition rules
        if self.indicators.economic_stability < -0.6:
            self.current_state = SocietyStateType.ECONOMIC_CRISIS
        elif self.indicators.political_stability < -0.5:
            self.current_state = SocietyStateType.POLITICAL_CRISIS
        elif self.indicators.social_cohesion < -0.4:
            self.current_state = SocietyStateType.SOCIAL_UNREST
        elif all(getattr(self.indicators, ind) > 0.7 for ind in self.indicators.__annotations__):
            self.current_state = SocietyStateType.PROSPERITY        

        if self.current_state != previous_state:
            self.state_history.append((previous_state, self.current_state))

    def _calculate_economic_stability(self, economic_data: Dict[str, float]) -> float:
        """
        Calculate economic stability based on key economic indicators
        Returns value between -1.0 and 1.0
        """

        # Weights for different factors
        weights = {
            'gdp_growth': 0.4,
            'inflation': -0.3,  # Higher inflation reduces stability
            'unemployment': -0.3  # Higher unemployment reduces stability
        }
        stability = 0.0
        
        # GDP growth typically ranges from -10% to +10%
        if 'gdp_growth' in economic_data:
            gdp_impact = max(-1.0, min(1.0, economic_data['gdp_growth'] / 0.1))
            stability += weights['gdp_growth'] * gdp_impact
        
        # Inflation impact (assuming healthy inflation is around 2%)
        if 'inflation' in economic_data:
            inflation_deviation = abs(economic_data['inflation'] - 0.02)
            inflation_impact = max(-1.0, min(1.0, -inflation_deviation / 0.1))
            stability += weights['inflation'] * inflation_impact

        # Unemployment impact (assuming natural rate around 5%)
        if 'unemployment' in economic_data:
            unemployment_deviation = economic_data['unemployment'] - 0.05
            unemployment_impact = max(-1.0, min(1.0, -unemployment_deviation / 0.1))
            stability += weights['unemployment'] * unemployment_impact

        return max(-1.0, min(1.0, stability))

    def _calculate_political_stability(self, political_data: Dict[str, float]) -> float:
        """
        Calculate political stability based on government and institutional indicators
        Returns value between -1.0 and 1.0
        """
        weights = {
            'government_approval': 0.4,
            'parliament_effectiveness': 0.3,
            'political_stability': 0.3
        }
        stability = 0.0

        # Government approval (typically 0-100%)
        if 'government_approval' in political_data:
            approval_impact = (political_data['government_approval'] - 50) / 50  # Center at 50%
            stability += weights['government_approval'] * approval_impact        

        # Parliament effectiveness (assumed 0-1 scale)
        if 'parliament_effectiveness' in political_data:
            effectiveness_impact = (political_data['parliament_effectiveness'] - 0.5) * 2
            stability += weights['parliament_effectiveness'] * effectiveness_impact

        # Overall political stability score (assumed 0-1 scale)
        if 'political_stability' in political_data:
            stability_impact = (political_data['political_stability'] - 0.5) * 2
            stability += weights['political_stability'] * stability_impact

        return max(-1.0, min(1.0, stability))

    def _calculate_social_cohesion(self, social_data: Dict[str, float]) -> float:
        """
        Calculate social cohesion based on social indicators
        Returns value between -1.0 and 1.0
        """
        weights = {
            'social_cohesion': 0.4,
            'media_trust': 0.3,
            'citizen_satisfaction': 0.3
        }
        cohesion = 0.0

        # Direct social cohesion measure (assumed 0-1 scale)
        if 'social_cohesion' in social_data:
            cohesion_impact = (social_data['social_cohesion'] - 0.5) * 2
            cohesion += weights['social_cohesion'] * cohesion_impact

        # Media trust impact (assumed 0-1 scale)
        if 'media_trust' in social_data:
            trust_impact = (social_data['media_trust'] - 0.5) * 2
            cohesion += weights['media_trust'] * trust_impact

        # Citizen satisfaction (assumed 0-1 scale)
        if 'citizen_satisfaction' in social_data:
            satisfaction_impact = (social_data['citizen_satisfaction'] - 0.5) * 2
            cohesion += weights['citizen_satisfaction'] * satisfaction_impact

        return max(-1.0, min(1.0, cohesion))

    def get_state_report(self) -> Dict[str, Any]:
        """
        Generate a comprehensive report of the current society state
        """
        return {
            'current_state': self.current_state.value,
            'indicators': {
                'economic_stability': round(self.indicators.economic_stability, 3),
                'political_stability': round(self.indicators.political_stability, 3),
                'social_cohesion': round(self.indicators.social_cohesion, 3),
                'public_trust': round(self.indicators.public_trust, 3)
            },
            'state_history': [(prev.value, curr.value) for prev, curr in self.state_history[-5:]]  # Last 5 transitions
        }

