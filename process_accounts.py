import importlib
import argparse

import ClientProvider
import Config
import Organizations
import Utilites


def process_accounts(
        rootAccountNumber: str,
        accounts,
        worker_function: str, before_run_function: str = "", after_run_function: str = "",
        access_key: str = "", secret_key: str = "",
        assumeRoleName: str = 'OrganizationAccountAccessRole'):
    rootAccountNumber = rootAccountNumber.strip()

    if not rootAccountNumber:
        raise Exception("Root account or accounts file not set. Nothing to process.")

    if len(accounts) == 0:
        raise Exception("Nothing to process.")

    print('\033[34mRoot account number: ' + rootAccountNumber + '... \033[0m')
    print("Number of accounts to proceed: " + str(len(accounts)))

    provider = ClientProvider.ClientProvider(rootAccount=rootAccountNumber, assumeRole=assumeRoleName,
                                             accessKey=access_key, secretKey=secret_key)

    if before_run_function:
        func_name, module = get_module_for_function(before_run_function)
        getattr(module, func_name)(provider)

    func_name, module = get_module_for_function(worker_function)
    for account in accounts:
        if not account:
            continue

        try:
            print('\033[34mProcessing account:' + account + '\033[0m ')
            getattr(module, func_name)(provider, account)

        except Exception as e:
            print('\033[91mAccount: ' + account + ' Exception: ' + str(e) + '\033[0m')

    if after_run_function:
        func_name, module = get_module_for_function(after_run_function)
        getattr(module, func_name)(provider)


def get_module_for_function(worker_function: str):
    mod_name, func_name = worker_function.rsplit('.', 1)

    if not mod_name or not func_name:
        raise Exception("Wrong worker function name format. Expectred: module_name.function_name")
    module = importlib.import_module(mod_name)

    if not module:
        raise Exception("Couldn't find a module for worker function!")

    return func_name, module


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-F", "--file", help="get account list from file")
    parser.add_argument("-O", "--organizations", action='store_true',
                        help="get account list from organizations structure")
    parser.add_argument("-W", "--workerfunction", help="worker function name")
    parser.add_argument("-B", "--beforefunction", help="function name to be run before run")
    parser.add_argument("-A", "--afterfunction", help="function name to be run after run")
    parser.add_argument("-R", "--assumeRoleName", default="OrganizationAccountAccessRole",
                        help="name of the role to assume")
    parser.add_argument("-AK", "--accessKey", help="function name to be run before run")
    parser.add_argument("-Sk", "--secretKey", help="function name to be run after run")

    # Read arguments from the command line
    args = parser.parse_args()

    if not args.workerfunction:
        raise Exception("Worker function name is not set!")

    if args.assumeRoleName:
        role = args.assumeRoleName

    if not role:
        raise Exception("Worker function name is not set!")

    if args.file:
        accounts = Utilites.load_accounts_list(args.file)
    else:
        if args.organizations:
            accounts = Organizations.get_all_accounts(Config.RootOU)

    if Config.ExcludedAccounts is not None:
        accounts = [account for account in accounts if account not in Config.ExcludedAccounts]

    process_accounts(rootAccountNumber=Config.RootAccountNumber, accounts=accounts, worker_function=args.workerfunction,
                     before_run_function=args.beforefunction, after_run_function=args.afterfunction,
                     assumeRoleName=role)
