import ClientProvider
import IAM


# Multiline file with child account numbers
def load_accounts_list(accounsFile):
    accounts = []
    with open(accounsFile, 'r') as f:
        accounts = f.read().splitlines()

    return accounts


def IAMAudit(rootAccountNumber: str, accounsFile: str):
    rootAccountNumber = rootAccountNumber.strip()

    if not rootAccountNumber or not accounsFile:
        print("Root account or accounts file not set. Nothing to process.")
        return

    print("Root account number: " + rootAccountNumber)

    accounts = load_accounts_list(accounsFile)

    if len(accounts) == 0:
        print("Nothing to process.")
        return

    print("Number of child accounts: " + str(len(accounts)))

    provider = ClientProvider.ClientProvider(rootAccountNumber)

    for account in accounts:
        if not account: continue

        if account[0] == "-":
            print("Account " + account[1:-1] + " skipped")
            continue

        try:
            iam = provider.get_client(account, 'iam')
            print(account + ': IAM client created.')

            iam_client = IAM.IAM(iam, account)
            iam_client.generate_credential_report()
            iam_client.list_groups()
            iam_client.list_roles()
            iam_client.list_groups_for_user()
            iam_client.get_group()
            iam_client.list_attached_user_policies()
            iam_client.list_attached_group_policies()
            iam_client.list_attached_role_policies()
            pass
        except Exception as e:
            print('Account: ' + account + ' Exception: ' + str(e))
