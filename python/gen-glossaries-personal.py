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
    "Personal Banking Glossary": [
        {'name': 'Account', 'shortDescription': 'A financial record that tracks an individual\'s transactions and balances.'},
        {'name': 'Checking Account', 'shortDescription': 'A type of account that allows frequent deposits and withdrawals.'},
        {'name': 'Savings Account', 'shortDescription': 'A type of account designed for storing and accumulating money over time.'},
        {'name': 'Loan', 'shortDescription': 'A sum of money borrowed from a lender that must be repaid with interest.'},
        {'name': 'Transaction', 'shortDescription': 'A withdrawl or payment'}
    ],
    "Personal Banking Credit Glossary": [
        {'name': 'Credit Card', 'shortDescription': 'A card issued by a financial institution that allows the holder to borrow money for purchases.'},
        {'name': 'Credit Limit', 'shortDescription': 'The maximum amount of credit a lender will extend to a borrower.'},
        {'name': 'Credit Score', 'shortDescription': 'A numerical representation of an individual\'s creditworthiness.'},
        {'name': 'Interest Rate', 'shortDescription': 'The percentage charged by a lender for the use of borrowed money.'}
    ],
    "Personal BankingInvestment Glossary": [
        {'name': 'Stock', 'shortDescription': 'A type of security that represents ownership in a company.'},
        {'name': 'Bond', 'shortDescription': 'A debt security that represents a loan made by an investor to a borrower.'},
        {'name': 'Mutual Fund', 'shortDescription': 'A professionally managed investment fund that pools money from many investors.'},
        {'name': 'Portfolio', 'shortDescription': 'A collection of investments owned by an individual or organization.'}
    ],
    "Personal Banking Customer Glossary": [
        {'name': 'Customer', 'shortDescription': 'An individual or organization that purchases goods or services from a bank.'},
        {'name': 'Customer Relationship Management (CRM)', 'shortDescription': 'A strategy for managing interactions with customers and potential customers.'},
        {'name': 'Know Your Customer (KYC)', 'shortDescription': 'A process of verifying the identity of customers and assessing potential risks.'}
    ],
    "Personal Banking Operations Glossary": [
        {'name': 'Automated Teller Machine (ATM)', 'shortDescription': 'An electronic banking outlet that allows customers to perform financial transactions.'},
        {'name': 'Branch', 'shortDescription': 'A physical location where a bank offers its services to customers.'},
        {'name': 'Online Banking', 'shortDescription': 'A service that allows customers to conduct financial transactions over the internet.'},
        {'name': 'Mobile Banking', 'shortDescription': 'A service that allows customers to conduct financial transactions through a mobile app.'}
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