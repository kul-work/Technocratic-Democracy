# Debug mode
DEBUG_MODE = False

# Simulation Control
SIMULATION_MONTHS = 48  # 4 years default
RANDOM_SEED = None  # For reproducible results

# Population Settings
INITIAL_POPULATION = 10_000
MAX_POPULATION = 1_000_000
BIRTH_RATE = 0.011  # Annual rate
DEATH_RATE = 0.009  # Annual rate
POPULATION_GROWTH_CHANCE = 0.2  # 20% chance for population growth
POPULATION_DECLINE_CHANCE = 0.1  # 10% chance for population decline
POPULATION_GROWTH_FACTOR = 0.1  # 10% growth batch
POPULATION_DECLINE_FACTOR = 0.05  # 5% decline batch

# Political System
PARLIAMENT_TOTAL_SEATS = 300
DEPUTIES_PROPORTION = 0.6  # 60% Deputies
SENATE_PROPORTION = 0.4  # 40% Senate
PARLIAMENT_QUORUM = 0.51  # 51% for valid session
INITIAL_PARTY_FUNDS = 10_000.0
MAX_PARTY_MEMBERS = 100
CAMPAIGN_POPULARITY_FACTOR = 0.1
CAMPAIGN_COST_FACTOR = 1000

# Government
MAX_ADVISORS = 12
EMERGENCY_DURATION = 120  # days
GOVERNMENT_APPROVAL_DECAY = 0.5  # Factor for approval rating updates
MIN_MINISTRY_EFFICIENCY = 0.5
MAX_MINISTRY_EFFICIENCY = 1.0
AUSTERITY_BUDGET_CUT = 0.2  # 20% budget reduction
AUSTERITY_APPROVAL_PENALTY = 15.0

# Economic Parameters
INITIAL_GDP = 1_000_000_000_000  # 1 trillion
INITIAL_LABOR_FORCE = 50_000_000
INITIAL_INFLATION_RATE = 0.02  # 2%
INITIAL_UNEMPLOYMENT_RATE = 0.05  # 5%
MAX_DEFICIT_GDP_RATIO = 0.03  # 3% of GDP
INITIAL_TAX_RATES = {
    'income': 0.20,
    'corporate': 0.25,
    'vat': 0.20,
    'social': 0.15
}
TAX_RATE_MAX_CHANGE = 0.01  # Maximum tax rate change per update

# Society State Thresholds
ECONOMIC_CRISIS_THRESHOLD = -0.6
POLITICAL_CRISIS_THRESHOLD = -0.5
SOCIAL_UNREST_THRESHOLD = -0.4
PROSPERITY_THRESHOLD = 0.7