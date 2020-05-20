import argparse
import ClientProvider
import Config
import Organizations
import Utilites
import IAM_KeyRoutines
import IAM_Reports
import Organizations_Reports


def audit_process(provider, rootAccount, accounts, process_account):
    for account in accounts:
        if not account: continue
        try:
            process_account(provider, rootAccount, account)
        except Exception as e:
            print('\033[91mAccount: ' + account + ' Exception: ' + str(e) + '\033[0m')


def audit_worker(provider, rootAccount, account):
    iam = provider.get_client(account, 'iam')
    iam_reports = IAM_Reports.IAM_Reports(iam, account)
    iam_reports.run()

    org = provider.get_client(rootAccount, 'organizations')  # must have root account session
    org_reports = Organizations_Reports.Organizations_Reports(org, account)
    org_reports.run()


def security_worker(provider, rootAccount, account):
    iam = provider.get_client(account, 'iam')
    iam_keys = IAM_KeyRoutines.IAM_KeyRoutines(iam, account)
    iam_keys.run()


def SOC_audit(rootAccountNumber: str, accounts, worker_function):
    rootAccountNumber = rootAccountNumber.strip()

    if not rootAccountNumber:
        raise Exception("Root account or accounts file not set. Nothing to process.")

    if len(accounts) == 0:
        raise Exception("Nothing to process.")

    print("Root account number: " + rootAccountNumber)

    print("Number of child accounts: " + str(len(accounts)))

    provider = ClientProvider.ClientProvider(rootAccountNumber)

    audit_process(provider, rootAccountNumber, accounts, worker_function)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-F", "--file", help="get account list from file")
    parser.add_argument("-O", "--organizations", action='store_true',
                        help="get account list from organizations structure")
    parser.add_argument("-W", "--workerfunction", help="worker function name")

    # Read arguments from the command line
    args = parser.parse_args()

    if args.file:
        accounts = Utilites.load_accounts_list(args.file)
    else:
        if args.organizations:
            accounts = Organizations.get_all_accounts(Config.RootOU)

    if Config.ExcludedAccounts is not None:
        accounts = [account for account in accounts if account not in Config.ExcludedAccounts]

    worker = globals()[args.workerfunction]
    if not worker:
        raise Exception("No such worker found!")
    # method_to_call = getattr(Audit, 'audit_worker')

    SOC_audit(rootAccountNumber=Config.RootAccountNumber, accounts=accounts, worker_function=worker)
