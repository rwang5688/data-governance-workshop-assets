import boto3
import sys

# Create a DataZone client
datazone_client = boto3.client('datazone')

# Domain and project IDs
# domain_id = input("Enter the Domain Identifier: ")
# project_id = input("Enter the Project Identifier: ")
domain_id = sys.argv[1] 
project_id = sys.argv[2]

# Define multiple glossaries with their terms
glossaries = {
    "Wealth Management Glossary": [
        {'name': 'Portfolio', 'shortDescription': 'A collection of investments owned by an individual or organization.'},
        {'name': 'Asset Allocation', 'shortDescription': 'The strategy of dividing an investment portfolio across different asset categories.'},
        {'name': 'Risk Tolerance', 'shortDescription': 'The degree of variability in returns that an investor is willing to withstand.'},
        {'name': 'Client', 'shortDescription': 'An individual or organization that owns the investment portfolio.'}
    ],
    "Wealth Management Investment Glossary": [
        {'name': 'Stocks', 'shortDescription': 'Shares of ownership in a publicly-traded company.'},
        {'name': 'Bonds', 'shortDescription': 'Debt securities issued by governments or corporations.'},
        {'name': 'Mutual Funds', 'shortDescription': 'A pooled investment vehicle that invests in a diversified portfolio of securities.'}
    ],
    "Wealth Management Financial Planning Glossary": [
        {'name': 'Retirement Planning', 'shortDescription': 'The process of determining retirement income goals and the actions necessary to achieve those goals.'},
        {'name': 'Estate Planning', 'shortDescription': 'The process of anticipating and arranging for the disposal of an estate during a person\'s life.'},
        {'name': 'Tax Planning', 'shortDescription': 'The analysis of a financial situation or plan from a tax perspective.'}
    ],
    "Wealth Management Banking Glossary": [
        {'name': 'Checking Account', 'shortDescription': 'A bank account that allows easy access to funds for daily transactions.'},
        {'name': 'Savings Account', 'shortDescription': 'A bank account that earns interest on deposited funds.'},
        {'name': 'Loan', 'shortDescription': 'A sum of money borrowed from a lender that must be repaid with interest.'}
    ]
}

# Function to create a glossary and its terms
def create_glossary_and_terms(glossary_name, terms):
    # Create the glossary
    glossary_response = datazone_client.create_glossary(
        description=f'Glossary for {glossary_name.lower()} terms',
        domainIdentifier=domain_id,
        name=glossary_name,
        owningProjectIdentifier=project_id,
        status='ENABLED'
    )
    glossary_identifier = glossary_response['id']
    print(f"{glossary_name} created:", glossary_response)

    # Create terms for the glossary
    for term in terms:
        term_params = {
            'domainIdentifier': domain_id,
            'glossaryIdentifier': glossary_identifier,
            'name': term['name'],
            'shortDescription': term['shortDescription']
        }
        term_response = datazone_client.create_glossary_term(**term_params)
        print(f"Glossary Term '{term['name']}' created:", term_response)

# Create each glossary and its terms
for glossary_name, terms in glossaries.items():
    create_glossary_and_terms(glossary_name, terms)