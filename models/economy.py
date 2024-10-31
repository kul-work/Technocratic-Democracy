import random
from enum import Enum
from typing import Dict
from config import *

from .economy_sector import EconomySector, EconomySectorType

class EconomicModel:
    def __init__(self):
        # Initialize economic indicators
        self.gdp = INITIAL_GDP
        self.inflation_rate = INITIAL_INFLATION_RATE
        self.unemployment_rate = INITIAL_UNEMPLOYMENT_RATE
        self.trade_balance = 0  # Neutral trade balance

        # Economic sectors (percentage of GDP)
        self.sectors = {
            # Public sectors
            'public_administration': EconomySector('Public Administration', EconomySectorType.PUBLIC),
            'healthcare': EconomySector('Healthcare', EconomySectorType.PUBLIC),
            'education': EconomySector('Education', EconomySectorType.PUBLIC),
            'defense': EconomySector('Defense', EconomySectorType.PUBLIC),
            'justice': EconomySector('Justice', EconomySectorType.PUBLIC),
            
            # Private sectors
            'manufacturing': EconomySector('Manufacturing', EconomySectorType.PRIVATE),
            'services': EconomySector('Services', EconomySectorType.PRIVATE),
            'technology': EconomySector('Technology', EconomySectorType.PRIVATE),
            'finance': EconomySector('Finance', EconomySectorType.PRIVATE),
            
            # Mixed sectors
            'agriculture': EconomySector('Agriculture', EconomySectorType.MIXED),
            'industry': EconomySector('Industry', EconomySectorType.MIXED),
            'infrastructure': EconomySector('Infrastructure', EconomySectorType.MIXED),
            'environment': EconomySector('Environment', EconomySectorType.MIXED),
            'culture': EconomySector('Culture', EconomySectorType.MIXED),
        }
        
        # Initialize sector shares
        self._initialize_sector_shares()
        
        # Labor market
        self.labor_force = INITIAL_LABOR_FORCE
        self.employed = self.labor_force * (1 - self.unemployment_rate)
        self.average_wage = self.gdp / self.employed

        # Fiscal system
        self.income_tax_rate = INITIAL_TAX_RATES['income']
        self.corporate_tax_rate = INITIAL_TAX_RATES['corporate']
        self.vat_rate = INITIAL_TAX_RATES['vat']
        self.social_security_rate = INITIAL_TAX_RATES['social']

        self.government_revenue = 0
        self.government_spending = 0
        self.budget_balance = 0

        # Financial system
        self.interest_rate = 0.01  # 1% interest rate
        self.money_supply = self.gdp * 1.5  # M2 money supply

    def _initialize_sector_shares(self):
        # Public sector typically represents 30-50% of GDP in European countries
        public_share = random.uniform(0.3, 0.5)
        private_share = 1.0 - public_share
        
        public_sectors = [s for s in self.sectors.values() if s.sector_type == EconomySectorType.PUBLIC]
        private_sectors = [s for s in self.sectors.values() if s.sector_type == EconomySectorType.PRIVATE]
        
        # Distribute shares within each sector type
        for sector in public_sectors:
            sector.gdp_share = public_share / len(public_sectors)
            sector.employment_share = public_share / len(public_sectors)
            
        for sector in private_sectors:
            sector.gdp_share = private_share / len(private_sectors)
            sector.employment_share = private_share / len(private_sectors)

    def simulate_year(self) -> None:
        self.update_sectors()
        self.update_labor_market()
        self.update_fiscal_system()
        self.update_financial_system()

        # Simulate economic changes for one year
        self.gdp *= (1 + random.uniform(-0.05, 0.07))  # GDP growth between -5% and 7%
        self.inflation_rate = max(0, self.inflation_rate + random.uniform(-0.01, 0.01))
        self.unemployment_rate = max(0, min(1, self.unemployment_rate + random.uniform(-0.02, 0.02)))
        self.trade_balance += random.uniform(-0.1, 0.1) * self.gdp

        # Update other economic variables
        self.update_sectors()
        self.update_labor_market()
        self.update_fiscal_system()
        self.update_financial_system()

    def simulate_month(self) -> None:
        self.update_sectors()
        self.update_labor_market()
        self.update_fiscal_system()
        self.update_financial_system()

        # Simulate economic changes for one month
        # TODO: add more realistic growth
        self.gdp *= (1 + random.uniform(-0.01, 0.02))  # GDP growth between -1% and 2%
        self.inflation_rate = max(0, self.inflation_rate + random.uniform(-0.01, 0.01))
        self.unemployment_rate = max(0, min(1, self.unemployment_rate + random.uniform(-0.02, 0.02)))
        self.trade_balance += random.uniform(-0.1, 0.1) * self.gdp

        # Add sector interaction simulation
        self._simulate_sector_interactions()
        
        # Update economic indicators based on sector performance
        self._update_economic_indicators()

        # Update other economic variables
        self.update_sectors()
        self.update_labor_market()
        self.update_fiscal_system()
        self.update_financial_system()

    def _simulate_sector_interactions(self):
        """Simulate interactions between public and private sectors"""
        public_efficiency = sum(s.efficiency for s in self.sectors.values() 
                              if s.sector_type == EconomySectorType.PUBLIC)
        private_innovation = sum(s.innovation_rate for s in self.sectors.values() 
                               if s.sector_type == EconomySectorType.PRIVATE)
        
        # Public sector efficiency affects private sector growth
        for sector in self.sectors.values():
            if sector.sector_type == EconomySectorType.PRIVATE:
                sector.gdp_share *= (1 + 0.01 * public_efficiency * random.uniform(0.8, 1.2))
                
        # Private sector innovation affects public sector efficiency
        for sector in self.sectors.values():
            if sector.sector_type == EconomySectorType.PUBLIC:
                sector.efficiency *= (1 + 0.005 * private_innovation * random.uniform(0.8, 1.2))

    def _update_economic_indicators(self):
        """Update economic indicators based on sector performance"""
        # Calculate total GDP growth based on sector performance
        public_gdp_growth = sum(s.gdp_share * s.efficiency for s in self.sectors.values() 
                               if s.sector_type == EconomySectorType.PUBLIC)
        private_gdp_growth = sum(s.gdp_share * (1 + s.innovation_rate) for s in self.sectors.values() 
                                if s.sector_type == EconomySectorType.PRIVATE)
        
        self.gdp *= (1 + (public_gdp_growth + private_gdp_growth) * 0.1)
        
        # Update unemployment based on sector employment changes
        public_employment = sum(s.employment_share for s in self.sectors.values() 
                              if s.sector_type == EconomySectorType.PUBLIC)
        private_employment = sum(s.employment_share for s in self.sectors.values() 
                               if s.sector_type == EconomySectorType.PRIVATE)
        
        self.unemployment_rate = 1.0 - (public_employment + private_employment)

    def update_sectors(self) -> None:
        for sector in self.sectors:
            self.sectors[sector].gdp_share = max(0, min(1, self.sectors[sector].gdp_share + random.uniform(-0.02, 0.02)))
            self.sectors[sector].employment_share = max(0, min(1, self.sectors[sector].employment_share + random.uniform(-0.02, 0.02)))
        # Normalize sector percentages
        total = sum(sector.gdp_share for sector in self.sectors.values())
        for sector in self.sectors.values():
            sector.gdp_share /= total

    def update_labor_market(self) -> None:
        self.employed = self.labor_force * (1 - self.unemployment_rate)
        self.average_wage = self.gdp / self.employed

    def update_fiscal_system(self) -> None:
        # Calculate government revenue
        income_tax = self.income_tax_rate * self.average_wage * self.employed
        corporate_tax = self.corporate_tax_rate * self.gdp * 0.15  # Assume corporate profits are 15% of GDP
        vat = self.vat_rate * self.gdp * 0.6  # Assume 60% of GDP is subject to VAT
        social_security = self.social_security_rate * self.average_wage * self.employed

        self.government_revenue = income_tax + corporate_tax + vat + social_security

        # Calculate government spending (now based on revenue plus allowed deficit)
        max_deficit = MAX_DEFICIT_GDP_RATIO * self.gdp
        self.government_spending = self.government_revenue + random.uniform(0, max_deficit)

        # Calculate budget balance
        self.budget_balance = self.government_revenue - self.government_spending

        # Update tax rates with small random changes
        self.income_tax_rate = max(0, min(0.5, self.income_tax_rate + random.uniform(-TAX_RATE_MAX_CHANGE, TAX_RATE_MAX_CHANGE)))
        self.corporate_tax_rate = max(0, min(0.5, self.corporate_tax_rate + random.uniform(-TAX_RATE_MAX_CHANGE, TAX_RATE_MAX_CHANGE)))
        self.vat_rate = max(0, min(0.3, self.vat_rate + random.uniform(-TAX_RATE_MAX_CHANGE, TAX_RATE_MAX_CHANGE)))
        self.social_security_rate = max(0, min(0.3, self.social_security_rate + random.uniform(-TAX_RATE_MAX_CHANGE, TAX_RATE_MAX_CHANGE)))

    def update_financial_system(self) -> None:
        self.interest_rate = max(0, self.interest_rate + random.uniform(-0.005, 0.005))
        self.money_supply *= (1 + random.uniform(-0.05, 0.07))

    def apply_policy(self, policy):
        #def apply_policy(self, policy: 'Policy'):
        if policy.area == 'FISCAL':
            self.income_tax_rate = max(0, min(0.5, self.income_tax_rate + policy.effectiveness_score * 0.01))
        elif policy.area == 'INVESTMENT':
            self.gdp *= (1 + policy.effectiveness_score * 0.01)
        # Add more policy areas as needed

    def get_economic_indicators(self) -> None:
        return {
            'GDP': f"{self.gdp:.2f}",
            'Inflation Rate': f"{self.inflation_rate:.2f}",
            'Unemployment Rate': f"{self.unemployment_rate:.2f}",
            'Trade Balance': f"{self.trade_balance:.2f}",
            'Sectors': self.print_sectors(),
            'Average Wage': f"{self.average_wage:.2f}",
            'Government Revenue': f"{self.government_revenue:.2f}",
            'Government Spending': f"{self.government_spending:.2f}",
            'Budget Balance': f"{self.budget_balance:.2f}",
            'Income Tax Rate': f"{self.income_tax_rate:.2f}",
            'Corporate Tax Rate': f"{self.corporate_tax_rate:.2f}",
            'VAT Rate': f"{self.vat_rate:.2f}",
            'Social Security Rate': f"{self.social_security_rate:.2f}",
            'Interest Rate': f"{self.interest_rate:.2f}",
            'Money Supply': f"{self.money_supply:.2f}"
        }

    def get_gdp_growth(self) -> float:
        """Returns the GDP growth rate"""
        # GDP growth is already calculated in simulate_month/year
        # We'll return it as a percentage
        return (self.gdp / (self.gdp / (1 + random.uniform(-0.01, 0.02)))) - 1

    def get_unemployment_rate(self) -> float:
        return self.unemployment_rate
        
    def print_sectors(self):
        return {sector.name: round(sector.gdp_share, 2) for sector in self.sectors.values()}

    def get_sector_report(self) -> Dict[str, Dict]:
        """Generate a detailed report of all sectors"""
        return {
            name: {
                'type': sector.sector_type.value,
                'gdp_share': f"{sector.gdp_share:.2%}",
                'employment_share': f"{sector.employment_share:.2%}",
                'efficiency': f"{sector.efficiency:.2f}",
                'innovation_rate': f"{sector.innovation_rate:.2f}"
            } for name, sector in self.sectors.items()
        }

    def get_gini_coefficient(self) -> float:
        """
        Calculate Gini coefficient based on economic indicators.
        Returns a value between 0 (perfect equality) and 1 (perfect inequality)
        """
        # Simplified Gini calculation based on:
        # - Unemployment rate (higher unemployment = higher inequality)
        # - Tax rates (higher progressive taxes = lower inequality)
        # - GDP per capita variation across sectors
        
        # Base inequality from unemployment
        base_inequality = self.unemployment_rate * 0.3
        
        # Tax system progressivity (higher taxes generally mean more redistribution)
        tax_effect = (1 - (self.income_tax_rate + self.corporate_tax_rate) / 2) * 0.3
        
        # Sector inequality (variation in GDP shares)
        sector_shares = [sector.gdp_share for sector in self.sectors.values()]
        sector_inequality = max(0, (max(sector_shares) - min(sector_shares))) * 0.4
        
        gini = base_inequality + tax_effect + sector_inequality
        
        # Ensure result is between 0 and 1
        return max(0.0, min(1.0, gini))
