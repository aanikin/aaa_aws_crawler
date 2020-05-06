import boto3
import Config

def get_accounts(aws_ou_parent_id):
    #
    session = boto3.Session()

    client = session.client('organizations')

    paginator = client.get_paginator('list_accounts_for_parent')
    response_iterator = paginator.paginate(ParentId=aws_ou_parent_id)
    accounts = []
    for response in response_iterator:
        for acc in response['Accounts']:
            accounts.append(acc["Id"])
    return accounts


def list_organizational_units_for_parent(rootOU):
    session = boto3.Session()

    client = session.client('organizations')

    paginator = client.get_paginator('list_organizational_units_for_parent')
    response_iterator = paginator.paginate(ParentId=rootOU)

    OUs = []
    for response in response_iterator:
        for ou in response["OrganizationalUnits"]:
            OUs.append(ou["Id"])

    return OUs


def get_all_accounts(rootOU):
    allAccounts = []

    # get from root OU first
    accounts = get_accounts(rootOU)
    allAccounts.extend(accounts)

    # get from child OU
    for ou in list_organizational_units_for_parent(rootOU):
        accounts = get_accounts(ou)
        allAccounts.extend(accounts)

    return allAccounts


if __name__ == "__main__":
    allAccounts = get_all_accounts(Config.RootOU)

    print(len(allAccounts))
    print(allAccounts)
