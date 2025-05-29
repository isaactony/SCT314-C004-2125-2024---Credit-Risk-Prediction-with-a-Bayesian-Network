# Defining prior probabilities for root nodes
P_income = {'High': 0.6, 'Low': 0.4}
P_employment = {'Employed': 0.7, 'Unemployed': 0.3}
P_history = {'Good': 0.8, 'Poor': 0.2}

# Defining my conditional probabilities for Default = Yes given each combination of parents
P_default_yes = {
    ('High', 'Employed', 'Good'): 0.10,
    ('High', 'Employed', 'Poor'): 0.50,
    ('High', 'Unemployed', 'Good'): 0.40,
    ('High', 'Unemployed', 'Poor'): 0.80,
    ('Low', 'Employed', 'Good'): 0.30,
    ('Low', 'Employed', 'Poor'): 0.70,
    ('Low', 'Unemployed', 'Good'): 0.60,
    ('Low', 'Unemployed', 'Poor'): 0.95
}

# Function to compute conditional probability using the network
def query_probability(query_var, query_val, evidence):
    sum_num = 0.0
    sum_den = 0.0
    # Iterate over all possible combinations of Income, Employment, History, Default
    for inc in ['High', 'Low']:
        for emp in ['Employed', 'Unemployed']:
            for hist in ['Good', 'Poor']:
                # Compute the joint probability for each Default state
                # Default = Yes
                joint_yes = P_income[inc] * P_employment[emp] * P_history[hist] * P_default_yes[(inc, emp, hist)]
                # Default = No
                joint_no  = P_income[inc] * P_employment[emp] * P_history[hist] * (1 - P_default_yes[(inc, emp, hist)])
                # If this combination matches the evidence, accumulate probabilities
                # (e.g., if evidence says Employment=Employed, skip combos where emp is Unemployed)
                if ('IncomeLevel' in evidence and inc != evidence['IncomeLevel']): 
                    pass  # skip if income doesn't match evidence
                elif ('EmploymentStatus' in evidence and emp != evidence['EmploymentStatus']): 
                    pass
                elif ('CreditHistory' in evidence and hist != evidence['CreditHistory']): 
                    pass
                else:
                    # Evidence satisfied for Income, Employment, History
                    if 'DefaultRisk' not in evidence or evidence['DefaultRisk'] == 'Yes':
                        sum_den += joint_yes   # add Default=Yes scenario if not contradicted by evidence
                        if query_var == 'DefaultRisk' and query_val == 'Yes':
                            sum_num += joint_yes
                        if query_var == 'CreditHistory' and query_val == 'Poor':
                            # If querying history, accumulate when hist='Poor' (and default yes scenario)
                            sum_num += joint_yes if hist == 'Poor' else 0
                        # (Similar logic can be added for other query variables if needed)
                    if 'DefaultRisk' not in evidence or evidence['DefaultRisk'] == 'No':
                        sum_den += joint_no    # add Default=No scenario if allowed by evidence
                        if query_var == 'DefaultRisk' and query_val == 'No':
                            sum_num += joint_no
                        if query_var == 'CreditHistory' and query_val == 'Poor':
                            sum_num += joint_no if hist == 'Poor' else 0
    # Normalize to get conditional probability
    return sum_num / sum_den if sum_den > 0 else 0.0

# Example queries:
result1 = query_probability('DefaultRisk', 'Yes', {'EmploymentStatus': 'Employed', 'CreditHistory': 'Good'})
result2 = query_probability('CreditHistory', 'Poor', {'DefaultRisk': 'Yes'})
print(f"P(DefaultRisk = Yes | EmploymentStatus = Employed, CreditHistory = Good) = {result1:.3f}")
print(f"P(CreditHistory = Poor | DefaultRisk = Yes) = {result2:.3f}")
