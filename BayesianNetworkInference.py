from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

# Define the Bayesian Network structure
model = DiscreteBayesianNetwork([
    ('IncomeLevel', 'DefaultRisk'),
    ('EmploymentStatus', 'DefaultRisk'),
    ('CreditHistory', 'DefaultRisk')
])

# Define CPDs
cpd_income = TabularCPD('IncomeLevel', 2, [[0.6], [0.4]])  # 0 = High, 1 = Low
cpd_employment = TabularCPD('EmploymentStatus', 2, [[0.7], [0.3]])  # 0 = Employed, 1 = Unemployed
cpd_history = TabularCPD('CreditHistory', 2, [[0.8], [0.2]])  # 0 = Good, 1 = Poor

cpd_default = TabularCPD(
    'DefaultRisk', 2,
    [
        [0.90, 0.50, 0.60, 0.20, 0.70, 0.30, 0.40, 0.05],  # Default = No
        [0.10, 0.50, 0.40, 0.80, 0.30, 0.70, 0.60, 0.95]   # Default = Yes
    ],
    evidence=['IncomeLevel', 'EmploymentStatus', 'CreditHistory'],
    evidence_card=[2, 2, 2]
)

# Add CPDs
model.add_cpds(cpd_income, cpd_employment, cpd_history, cpd_default)
assert model.check_model()

# Perform inference
infer = VariableElimination(model)
result1 = infer.query(['DefaultRisk'], evidence={'EmploymentStatus': 0, 'CreditHistory': 0})
print(result1)

result2 = infer.query(['CreditHistory'], evidence={'DefaultRisk': 1})
print(result2)
