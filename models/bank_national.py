from enum import Enum
from typing import List, Dict
import random

class MonetaryPolicy(Enum):
    EXPANSIONARY = "Expansionary"
    NEUTRAL = "Neutral"
    CONTRACTIONARY = "Contractionary"

class EconomicIndicator(Enum):
    INFLATION_RATE = "Inflation Rate"
    UNEMPLOYMENT_RATE = "Unemployment Rate"
    GDP_GROWTH = "GDP Growth"
    INTEREST_RATE = "Interest Rate"
    EXCHANGE_RATE = "Exchange Rate"

class NationalBank:
    def __init__(self, name: str):
        self.name = name
        self.monetary_policy = MonetaryPolicy.NEUTRAL
        self.interest_rate = 2.0  # Starting interest rate (%)
        self.reserve_requirement = 10.0  # Starting reserve requirement (%)
        self.foreign_exchange_reserves = 1_000_000_000  # Starting forex reserves ($)
        self.economic_indicators: Dict[EconomicIndicator, float] = {
            EconomicIndicator.INFLATION_RATE: 2.0,
            EconomicIndicator.UNEMPLOYMENT_RATE: 5.0,
            EconomicIndicator.GDP_GROWTH: 2.5,
            EconomicIndicator.INTEREST_RATE: self.interest_rate,
            EconomicIndicator.EXCHANGE_RATE: 1.0  # Assuming 1:1 exchange rate with a reference currency
        }

    def set_monetary_policy(self, policy: MonetaryPolicy) -> None:
        self.monetary_policy = policy
        self._adjust_interest_rate()

    def _adjust_interest_rate(self) -> None:
        if self.monetary_policy == MonetaryPolicy.EXPANSIONARY:
            self.interest_rate = max(0, self.interest_rate - 0.25)
        elif self.monetary_policy == MonetaryPolicy.CONTRACTIONARY:
            self.interest_rate += 0.25
        self.economic_indicators[EconomicIndicator.INTEREST_RATE] = self.interest_rate

    def set_reserve_requirement(self, requirement: float) -> None:
        self.reserve_requirement = max(0, min(100, requirement))

    def conduct_open_market_operations(self, amount: float) -> None:
        # Positive amount means buying securities (expansionary)
        # Negative amount means selling securities (contractionary)
        self.foreign_exchange_reserves += amount
        if amount > 0:
            self.monetary_policy = MonetaryPolicy.EXPANSIONARY
        elif amount < 0:
            self.monetary_policy = MonetaryPolicy.CONTRACTIONARY
        self._adjust_interest_rate()

    def intervene_in_forex_market(self, amount: float) -> None:
        # Positive amount means buying foreign currency
        # Negative amount means selling foreign currency
        if abs(amount) <= self.foreign_exchange_reserves:
            self.foreign_exchange_reserves -= amount
            self._adjust_exchange_rate(amount)

    def _adjust_exchange_rate(self, intervention_amount: float) -> None:
        # Simplified model: intervention affects exchange rate
        current_rate = self.economic_indicators[EconomicIndicator.EXCHANGE_RATE]
        adjustment = intervention_amount / self.foreign_exchange_reserves
        new_rate = current_rate * (1 + adjustment)
        self.economic_indicators[EconomicIndicator.EXCHANGE_RATE] = max(0.1, new_rate)

    def print_money(self, amount: float) -> None:
        # Simplified model: printing money increases inflation
        self.economic_indicators[EconomicIndicator.INFLATION_RATE] += amount / 1_000_000_000

    def update_economic_indicators(self) -> None:
        # Simplified model for updating economic indicators
        self.economic_indicators[EconomicIndicator.INFLATION_RATE] += random.uniform(-0.5, 0.5)
        self.economic_indicators[EconomicIndicator.UNEMPLOYMENT_RATE] += random.uniform(-0.3, 0.3)
        self.economic_indicators[EconomicIndicator.GDP_GROWTH] += random.uniform(-0.2, 0.2)

        # Ensure indicators stay within realistic bounds
        self.economic_indicators[EconomicIndicator.INFLATION_RATE] = max(0, self.economic_indicators[EconomicIndicator.INFLATION_RATE])
        self.economic_indicators[EconomicIndicator.UNEMPLOYMENT_RATE] = max(1, min(20, self.economic_indicators[EconomicIndicator.UNEMPLOYMENT_RATE]))
        self.economic_indicators[EconomicIndicator.GDP_GROWTH] = max(-5, min(10, self.economic_indicators[EconomicIndicator.GDP_GROWTH]))

    def generate_economic_report(self) -> str:
        report = f"Economic Report for {self.name}:\n"
        report += f"Monetary Policy: {self.monetary_policy.value}\n"
        report += f"Interest Rate: {self.interest_rate:.2f}%\n"
        report += f"Reserve Requirement: {self.reserve_requirement:.2f}%\n"
        report += f"Foreign Exchange Reserves: ${self.foreign_exchange_reserves:,}\n"
        report += "\nEconomic Indicators:\n"
        for indicator, value in self.economic_indicators.items():
            if indicator == EconomicIndicator.EXCHANGE_RATE:
                report += f"  {indicator.value}: {value:.4f}\n"
            else:
                report += f"  {indicator.value}: {value:.2f}%\n"
        return report
    
    def print_economic_indicators(self):
        formatted_indicators = {}
        for indicator, value in self.economic_indicators.items():
            if indicator == EconomicIndicator.EXCHANGE_RATE:
                formatted_indicators[indicator.value] = f"{value:.4f}"
            elif indicator == EconomicIndicator.INTEREST_RATE:
                formatted_indicators[indicator.value] = f"{value:.2f}%"
            else:
                formatted_indicators[indicator.value] = f"{value:.2f}%"
        
        return formatted_indicators
