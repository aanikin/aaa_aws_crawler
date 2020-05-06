import argparse
import ClientProvider
import Config
import Organizations
import Utilites
import IAM_KeyRoutines
import IAM_Reports


def audit_process(provider, accounts):
    for account in accounts:
        if not account: continue
        try:
            process_account(provider, account)
        except Exception as e:
            print('\033[91mAccount: ' + account + ' Exception: ' + str(e))


def process_account(provider, account):
    iam = provider.get_client(account, 'iam')
    iam_reports = IAM_Reports.IAM_Reports(iam, account)
    iam_keys = IAM_KeyRoutines.IAM_KeyRoutines(iam, account)
    iam_reports.run()
    iam_keys.run()


def IAMAudit(rootAccountNumber: str, accounts):
    rootAccountNumber = rootAccountNumber.strip()

    if not rootAccountNumber:
        raise Exception("Root account or accounts file not set. Nothing to process.")

    if len(accounts) == 0:
        raise Exception("Nothing to process.")

    print("Root account number: " + rootAccountNumber)

    print("Number of child accounts: " + str(len(accounts)))

    provider = ClientProvider.ClientProvider(rootAccountNumber)

    audit_process(provider, accounts)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-F", "--file", help="get account list from file")
    parser.add_argument("-O", "--organizations", help="get account list from organizations structure")

    # Read arguments from the command line
    args = parser.parse_args()

    # Check for --version or -V
    if args.file:
        accounts = Utilites.load_accounts_list(args.file)
    else:
        if args.organizations:
            accounts = Organizations.get_all_accounts(Config.RootOU)

    if Config.ExcludedAccounts is not None:
        accounts = [account for account in accounts if account not in Config.ExcludedAccounts]

    IAMAudit(rootAccountNumber=Config.RootAccountNumber, accounts=accounts)
