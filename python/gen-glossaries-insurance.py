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
    "Insurance Policies Glossary": [
        {'name': 'Policy', 'shortDescription': 'A contract between an insurance company and an individual or entity, providing coverage for specific risks.'},
        {'name': 'Premium', 'shortDescription': 'The amount paid by the policyholder to the insurance company for the coverage provided.'},
        {'name': 'Deductible', 'shortDescription': 'The amount the policyholder must pay out-of-pocket before the insurance coverage kicks in.'},
        {'name': 'Claim', 'shortDescription': 'A request made by the policyholder to the insurance company for reimbursement or payment of covered expenses.'},
        {'name': 'Policy Holder', 'shortDescription': 'An individual or organization that holds the policy.'}
    ],
    "Insurance Plans Glossary": [
        {'name': 'HMO', 'shortDescription': 'Health Maintenance Organization, a type of health insurance plan that typically requires members to receive care from in-network providers.'},
        {'name': 'PPO', 'shortDescription': 'Preferred Provider Organization, a type of health insurance plan that allows members to receive care from both in-network and out-of-network providers, with higher costs for out-of-network care.'},
        {'name': 'Copay', 'shortDescription': 'A fixed amount the policyholder pays for a covered healthcare service, such as a doctor\'s visit or prescription.'},
        {'name': 'Coinsurance', 'shortDescription': 'The percentage of covered healthcare costs the policyholder pays after meeting the deductible.'}
    ],
    "Insurance Providers Glossary": [
        {'name': 'Insurer', 'shortDescription': 'The company that provides insurance coverage and assumes the risk in exchange for premium payments.'},
        {'name': 'Underwriting', 'shortDescription': 'The process of evaluating and assessing the risk of insuring an individual or entity.'},
        {'name': 'Reinsurance', 'shortDescription': 'A practice where an insurance company transfers a portion of its risk to another insurance company to reduce its exposure.'}
    ],
    "Insurance Claims Glossary": [
        {'name': 'Adjuster', 'shortDescription': 'An individual employed by an insurance company to investigate and evaluate insurance claims.'},
        {'name': 'Subrogation', 'shortDescription': 'The process by which an insurance company seeks to recover the amount paid on a claim from a third party who was responsible for the loss.'},
        {'name': 'Fraud', 'shortDescription': 'Intentional deception or misrepresentation made by a policyholder or provider to obtain an unlawful benefit from an insurance company.'}
    ],
    "Insurance Regulations Glossary": [
        {'name': 'Compliance', 'shortDescription': 'Adhering to the laws, regulations, and guidelines governing the insurance industry.'},
        {'name': 'Solvency', 'shortDescription': 'The ability of an insurance company to meet its long-term financial obligations.'},
        {'name': 'Fiduciary Duty', 'shortDescription': 'The legal obligation of an insurance company to act in the best interests of its policyholders.'}
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