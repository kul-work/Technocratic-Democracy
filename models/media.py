from enum import Enum
from typing import List, Dict, TYPE_CHECKING
import random
from datetime import datetime

if TYPE_CHECKING:
    from .citizen import Citizen
from .government import Government 
from .economy_sector import EconomySectorType

class MediaType(Enum):
    TRADITIONAL_NEWSPAPER = "Traditional Newspaper"
    TV_NETWORK = "TV Network"
    ONLINE_NEWS_PORTAL = "Online News Portal"
    SOCIAL_MEDIA_PLATFORM = "Social Media Platform"
    INDEPENDENT_JOURNALIST = "Independent Journalist"

class NewsCategory(Enum):
    POLITICS = "Politics"
    ECONOMY = "Economy"
    SOCIAL_ISSUES = "Social Issues"
    INTERNATIONAL = "International"
    TECHNOLOGY = "Technology"
    ENVIRONMENT = "Environment"

class MediaOutlet:
    def __init__(self, name: str, media_type: MediaType):
        self.name = name
        self.media_type = media_type
        self.credibility = 50.0  # Scale of 0-100
        self.audience_reach = 1000  # Number of people reached
        self.bias = random.uniform(-1, 1)  # -1 (left) to 1 (right)
        self.sensationalism = random.uniform(0, 1)  # 0 (factual) to 1 (sensational)
        self.sector_coverage = {
            EconomySectorType.PUBLIC: random.uniform(0.3, 0.7),   # Coverage balance between sectors
            EconomySectorType.PRIVATE: random.uniform(0.3, 0.7)
        }
        self.reach = random.uniform(0.1, 0.8)  # Add this line: Percentage of population reached
        

    # def publish_news(self, category: NewsCategory, factuality: float) -> Dict:
    #     perceived_factuality = factuality * (1 - self.sensationalism)
    #     impact = self.audience_reach * (self.credibility / 100)

    #     result = {
    #         'outlet_name': self.name,
    #         'media_type': self.media_type.value,
    #         'category': category.value,
    #         'factuality': perceived_factuality,
    #         'credibility': self.credibility,
    #         "impact": impact,
    #         'bias': self.bias,
    #         'sensationalism': self.sensationalism
    #     }
        
    #     # Add sector-specific reporting
    #     focused_sector = random.choices(
    #         [EconomySectorType.PUBLIC, EconomySectorType.PRIVATE],
    #         weights=[self.sector_coverage[EconomySectorType.PUBLIC], 
    #                 self.sector_coverage[EconomySectorType.PRIVATE]]
    #     )[0]
        
    #     result.update({
    #         'sector_focus': focused_sector.value,
    #         'sector_coverage': self.sector_coverage[focused_sector]
    #     })
        
    #     return result

    #TODO: Check why the simplified version below is better
    def publish_news(self, category: NewsCategory, factuality: float, sentiment=0.0) -> Dict:
        """Publish a news item with the given properties"""
        news = {
            'outlet': self,
            'category': category,
            'factuality': factuality,
            'sentiment': sentiment,
            'timestamp': datetime.now()
        }
        return news

    def update_credibility(self, factuality: float) -> None:
        credibility_change = (factuality - 0.5) * 10  # -5 to +5
        self.credibility = max(0, min(100, self.credibility + credibility_change))

    def update_audience_reach(self) -> None:
        # Audience reach changes based on credibility and media type
        change = random.uniform(-0.1, 0.1) * self.audience_reach
        if self.media_type in [MediaType.ONLINE_NEWS_PORTAL, MediaType.SOCIAL_MEDIA_PLATFORM]:
            change *= 2  # Digital media can grow/shrink faster
        self.audience_reach = max(100, self.audience_reach + change)

    def affect_citizens(self, citizens: List['Citizen']):
        # Method implementation
        pass

    def get_tension_contribution(self) -> float:
        """
        Calculate how much this media outlet contributes to social tension
        Returns a value between -1 (reducing tension) and 1 (increasing tension)
        """
        # Media outlets with extreme bias tend to increase tension more
        bias_factor = abs(self.bias)
        # Less credible outlets might cause more tension
        credibility_impact = (1 - self.credibility) * 0.5
        
        return bias_factor + credibility_impact

    def publish_referendum_coverage(self, referendum, coverage):
        """
        Publishes coverage about a referendum
        Args:
            referendum: The referendum being covered
            coverage: The coverage details/stance
        """
        coverage_stance = coverage.get('stance', 0.0)
        coverage_bias = coverage_stance * self.bias
        
        return {
            'outlet_name': self.name,
            'referendum_id': referendum.id,
            'coverage_stance': coverage_bias,
            'reach': self.reach,
            'credibility': self.credibility
        }

class MediaLandscape:
    def __init__(self):
        self.outlets: List[MediaOutlet] = []
        self.media_trust_score = random.uniform(40, 60)  # Start with 40-60% trust
        self.referendum_coverage: Dict[int, Dict] = {}

    def add_outlet(self, outlet: MediaOutlet) -> None:
        self.outlets.append(outlet)

    def get_most_influential_outlets(self, n: int) -> List[MediaOutlet]:
        return sorted(self.outlets, key=lambda x: x.audience_reach * (x.credibility / 100), reverse=True)[:n]

    def simulate_news_cycle(self) -> List[Dict]:
        """Generate a news cycle from all published news"""
        news_cycle = []
        for outlet in self.outlets:
            category = random.choice(list(NewsCategory))
            factuality = random.uniform(0.5, 1.0)
            sentiment = random.uniform(-0.8, 0.8)  # Add sentiment
            news = outlet.publish_news(
                category=category,
                factuality=factuality,
                sentiment=sentiment
            )
            news_cycle.append(news)
            outlet.update_credibility(factuality)
            outlet.update_audience_reach()
        self.update_public_trust(news_cycle)
        return news_cycle

    def update_public_trust(self, news_cycle: List[Dict]) -> None:
        avg_factuality = sum(news["factuality"] for news in news_cycle) / len(news_cycle)
        trust_change = (avg_factuality - 0.5) * 10  # -5 to +5
        self.media_trust_score = max(0, min(100, self.media_trust_score + trust_change))
    
    def increase_coverage(self) -> None:
        """
        Increases media coverage during social unrest:
        - Intensifies news cycle
        - Increases audience reach
        - Adjusts credibility based on coverage quality
        """
        for outlet in self.outlets:
            # Increase audience reach during crisis coverage
            outlet.audience_reach *= 1.2
            
            # More sensational coverage during unrest
            original_sensationalism = outlet.sensationalism
            outlet.sensationalism = min(1.0, outlet.sensationalism * 1.5)
            
            # Publish additional crisis-related news
            crisis_news = outlet.publish_news(
                category=random.choice([
                    NewsCategory.POLITICS,
                    NewsCategory.SOCIAL_ISSUES
                ]),
                factuality=0.8  # Maintain relatively high factuality during crisis
            )
            
            # Adjust credibility based on crisis coverage quality
            credibility_change = (0.8 - outlet.sensationalism) * 10
            outlet.credibility = max(0, min(100, outlet.credibility + credibility_change))
            
            # Reset sensationalism after crisis coverage
            outlet.sensationalism = original_sensationalism

    @staticmethod
    def bias_to_string(bias: float) -> str:
        if bias < -0.6:
            return "Far Left"
        elif bias < -0.2:
            return "Left"
        elif bias < 0.2:
            return "Center"
        elif bias < 0.6:
            return "Right"
        else:
            return "Far Right"

    def get_trust_score(self) -> float:
        """
        Returns the current public trust in media
        Scale of 0-1 (converted from 0-100 internal scale)
        """
        # Add some random variation to make it more dynamic
        base_trust = self.media_trust_score / 100
        variation = random.uniform(-0.05, 0.05)  # +/- 5% variation
        return max(0.0, min(1.0, base_trust + variation))

    def generate_media_report(self) -> str:
        report = "Media Landscape Report:\n"
        report += f"Public Trust in Media: {self.media_trust_score:.2f}%\n\n"
        report += "Top 5 Most Influential Outlets:\n"
        for outlet in self.get_most_influential_outlets(5):
            report += f"  {outlet.name} ({outlet.media_type.value}):\n"
            report += f"    Credibility: {outlet.credibility:.2f}%\n"
            report += f"    Audience Reach: {outlet.audience_reach:.2f}\n"
            report += f"    Bias: {outlet.bias:.2f} ({self.bias_to_string(outlet.bias)})\n"
            report += f"    Sensationalism: {outlet.sensationalism:.2f}\n"
        return report

    def cover_referendum(self, referendum) -> None:
    #def cover_referendum(self, referendum: 'Referendum') -> None:
        """Generate media coverage for referendum"""
        coverage = {
            #'support_ratio': random.uniform(0.3, 0.7),  # Ratio of positive coverage
            #'intensity': random.uniform(0.5, 1.0),      # How much coverage
            #'bias': random.uniform(-0.2, 0.2),          # Media bias
            'stance': random.uniform(-1, 1),  # Basic stance from -1 to 1
            'intensity': random.uniform(0, 1)  # How much coverage to give
        }
        
        self.referendum_coverage[referendum.id] = coverage
        
        # Generate news articles about referendum
        for outlet in self.outlets:
            outlet.publish_referendum_coverage(referendum, coverage)

    def get_referendum_coverage(self, referendum) -> Dict:
    #def get_referendum_coverage(self, referendum: 'Referendum') -> Dict:
        """Get aggregated media coverage for referendum"""
        return self.referendum_coverage.get(referendum.id, {
            'support_ratio': 0.5,
            'intensity': 0.5,
            'bias': 0.0
        })

    def get_tension_impact(self) -> float:
        """Calculate media's impact on social tensions"""
        tension_impact = 0.0
        for outlet in self.outlets:
            # Consider factors like sensationalism, polarization
            tension_impact += outlet.get_tension_contribution()
        return min(1.0, tension_impact / len(self.outlets))
