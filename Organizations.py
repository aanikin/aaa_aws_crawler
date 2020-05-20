import boto3
import Config


def get_organizations_client():
    session = boto3.Session()
    client = session.client('organizations')
    return client


def get_accounts(client, aws_ou_parent_id):
    paginator = client.get_paginator('list_accounts_for_parent')
    response_iterator = paginator.paginate(ParentId=aws_ou_parent_id)
    accounts = []
    for response in response_iterator:
        for acc in response['Accounts']:
            accounts.append(acc["Id"])
    return accounts


def list_organizational_units_for_parent(client, rootOU):
    paginator = client.get_paginator('list_organizational_units_for_parent')
    response_iterator = paginator.paginate(ParentId=rootOU)

    OUs = []
    for response in response_iterator:
        for ou in response["OrganizationalUnits"]:
            OUs.append(ou["Id"])

    return OUs


def get_all_accounts(rootOU):
    allAccounts = []
    client = get_organizations_client()
    accounts = get_accounts(client, rootOU)
    allAccounts.extend(accounts)

    # get from child OU
    for ou in list_organizational_units_for_parent(client, rootOU):
        accounts = get_accounts(client, ou)
        allAccounts.extend(accounts)

    return allAccounts


if __name__ == "__main__":
    allAccounts = get_all_accounts(Config.RootOU)

    print(len(allAccounts))
    print(allAccounts)
