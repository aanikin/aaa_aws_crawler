import boto3


def get_accounts(aws_ou_parent_id):
    #
    session = boto3.Session()

    client = session.client('organizations')
    response = client.describe_organization()

    # response = client.list_accounts_for_parent(ParentId=response["Organization"]["Arn"])
    response = client.list_accounts_for_parent(ParentId=aws_ou_parent_id)

    accounts = []
    for acc in response['Accounts']:
        accounts.append(acc)
    return accounts


def get_accounts_with_paginator(aws_ou_parent_id):
    #
    session = boto3.Session()

    client = session.client('organizations')

    paginator = client.get_paginator('list_accounts_for_parent')
    response_iterator = paginator.paginate(ParentId=aws_ou_parent_id)
    accounts = []
    for response in response_iterator:
        for acc in response['Accounts']:
            accounts.append(acc)
    return accounts


if __name__ == "__main__":
    print(get_accounts("o-c6qo9ge780-r-34iw"))
