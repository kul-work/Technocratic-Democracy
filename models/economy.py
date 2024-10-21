import random

class EconomicModel:
    def __init__(self):
        # Initialize economic indicators
        self.gdp = 1_000_000_000_000  # Initial GDP (trillion)
        self.inflation_rate = 0.02  # 2% initial inflation
        self.unemployment_rate = 0.05  # 5% initial unemployment
        self.trade_balance = 0  # Neutral trade balance

        # Economic sectors (percentage of GDP)
        self.sectors = {
            'industry': 0.3,
            'services': 0.6,
            'agriculture': 0.05,
            'technology': 0.05,
            'finance': 0.05
        }

        # Labor market
        self.labor_force = 50_000_000  # Total labor force
        self.employed = self.labor_force * (1 - self.unemployment_rate)
        self.average_wage = self.gdp / self.employed

        # Fiscal system
        self.income_tax_rate = 0.2  # 20% income tax
        self.corporate_tax_rate = 0.25  # 25% corporate tax
        self.vat_rate = 0.2  # 20% VAT
        self.social_security_rate = 0.15  # 15% social security contributions

        self.government_revenue = 0
        self.government_spending = 0
        self.budget_balance = 0

        # Financial system
        self.interest_rate = 0.01  # 1% interest rate
        self.money_supply = self.gdp * 1.5  # M2 money supply

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

        # Update other economic variables
        self.update_sectors()
        self.update_labor_market()
        self.update_fiscal_system()
        self.update_financial_system()

    def update_sectors(self) -> None:
        for sector in self.sectors:
            self.sectors[sector] = max(0, min(1, self.sectors[sector] + random.uniform(-0.02, 0.02)))
        # Normalize sector percentages
        total = sum(self.sectors.values())
        self.sectors = {k: v / total for k, v in self.sectors.items()}

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
        max_deficit = 0.03 * self.gdp  # 3% of GDP max deficit (example constraint)
        self.government_spending = self.government_revenue + random.uniform(0, max_deficit)

        # Calculate budget balance
        self.budget_balance = self.government_revenue - self.government_spending

        # Update tax rates with small random changes
        self.income_tax_rate = max(0, min(0.5, self.income_tax_rate + random.uniform(-0.01, 0.01)))
        self.corporate_tax_rate = max(0, min(0.5, self.corporate_tax_rate + random.uniform(-0.01, 0.01)))
        self.vat_rate = max(0, min(0.3, self.vat_rate + random.uniform(-0.01, 0.01)))
        self.social_security_rate = max(0, min(0.3, self.social_security_rate + random.uniform(-0.01, 0.01)))

    def update_financial_system(self) -> None:
        self.interest_rate = max(0, self.interest_rate + random.uniform(-0.005, 0.005))
        self.money_supply *= (1 + random.uniform(-0.05, 0.07))

    def apply_policy(self, policy):
    #def apply_policy(self, policy: 'Policy'):
        # Method to apply economic policies
        pass

    def get_economic_indicators(self) -> None:
        return {
            'GDP': self.gdp,
            'Inflation Rate': self.inflation_rate,
            'Unemployment Rate': self.unemployment_rate,
            'Trade Balance': self.trade_balance,
            'Sectors': self.sectors,
            'Average Wage': self.average_wage,
            'Government Revenue': self.government_revenue,
            'Government Spending': self.government_spending,
            'Budget Balance': self.budget_balance,
            'Income Tax Rate': self.income_tax_rate,
            'Corporate Tax Rate': self.corporate_tax_rate,
            'VAT Rate': self.vat_rate,
            'Social Security Rate': self.social_security_rate,
            'Interest Rate': self.interest_rate,
            'Money Supply': self.money_supply
        }
