import boto3
from threading import Lock

lock = Lock()


def get_organizations_client():
    with lock:
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


def get_root_account():
    client = get_organizations_client()
    response = client.describe_organization()

    return response["Organization"]["MasterAccountId"]


def get_root_ou(client):
    response = client.list_roots()
    return response["Roots"]


def get_all_accounts():
    allAccounts = []
    client = get_organizations_client()

    for root in get_root_ou(client):
        id = root["Id"]
        accounts = get_accounts(client, id)
        allAccounts.extend(accounts)

        # get from child OU
        for ou in list_organizational_units_for_parent(client, id):
            accounts = get_accounts(client, ou)
            allAccounts.extend(accounts)

    return allAccounts


if __name__ == "__main__":
    print(get_all_accounts())
