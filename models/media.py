from enum import Enum
from typing import List, Dict
import random

from citizen import Citizen
from government import Government 

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

    def publish_news(self, category: NewsCategory, factuality: float) -> Dict:
        perceived_factuality = factuality * (1 - self.sensationalism)
        impact = self.audience_reach * (self.credibility / 100)
        
        return {
            "outlet": self.name,
            "category": category,
            "factuality": perceived_factuality,
            "impact": impact,
            "bias": self.bias
        }

    def update_credibility(self, factuality: float) -> None:
        credibility_change = (factuality - 0.5) * 10  # -5 to +5
        self.credibility = max(0, min(100, self.credibility + credibility_change))

    def update_audience_reach(self) -> None:
        # Audience reach changes based on credibility and media type
        change = random.uniform(-0.1, 0.1) * self.audience_reach
        if self.media_type in [MediaType.ONLINE_NEWS_PORTAL, MediaType.SOCIAL_MEDIA_PLATFORM]:
            change *= 2  # Digital media can grow/shrink faster
        self.audience_reach = max(100, self.audience_reach + change)

class MediaLandscape:
    def __init__(self):
        self.outlets: List[MediaOutlet] = []
        self.public_trust = 50.0  # Scale of 0-100

    def add_outlet(self, outlet: MediaOutlet) -> None:
        self.outlets.append(outlet)

    def simulate_news_cycle(self) -> List[Dict]:
        news_cycle = []
        for outlet in self.outlets:
            category = random.choice(list(NewsCategory))
            factuality = random.uniform(0.5, 1.0)  # Simplified: news are more often true than false
            news = outlet.publish_news(category, factuality)
            news_cycle.append(news)
            outlet.update_credibility(factuality)
            outlet.update_audience_reach()
        self.update_public_trust(news_cycle)
        return news_cycle

    def update_public_trust(self, news_cycle: List[Dict]) -> None:
        avg_factuality = sum(news["factuality"] for news in news_cycle) / len(news_cycle)
        trust_change = (avg_factuality - 0.5) * 10  # -5 to +5
        self.public_trust = max(0, min(100, self.public_trust + trust_change))

    def get_most_influential_outlets(self, n: int) -> List[MediaOutlet]:
        return sorted(self.outlets, key=lambda x: x.audience_reach * (x.credibility / 100), reverse=True)[:n]

    def generate_media_report(self) -> str:
        report = "Media Landscape Report:\n"
        report += f"Public Trust in Media: {self.public_trust:.2f}%\n\n"
        report += "Top 5 Most Influential Outlets:\n"
        for outlet in self.get_most_influential_outlets(5):
            report += f"  {outlet.name} ({outlet.media_type.value}):\n"
            report += f"    Credibility: {outlet.credibility:.2f}%\n"
            report += f"    Audience Reach: {outlet.audience_reach:,}\n"
            report += f"    Bias: {outlet.bias:.2f} ({self.bias_to_string(outlet.bias)})\n"
            report += f"    Sensationalism: {outlet.sensationalism:.2f}\n"
        return report

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

# Example usage
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
