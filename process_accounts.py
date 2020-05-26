import importlib
import argparse
import time
import clientprovider
import config
import organizations
from utilites import log_output, log_error, load_accounts_list
from propagatingthread import PropagatingThread


def process_accounts(
        rootAccountNumber: str,
        accounts,
        worker_function: str, before_run_function: str = "", after_run_function: str = "",
        access_key: str = "", secret_key: str = "",
        assumeRoleName: str = 'OrganizationAccountAccessRole',
        degreeeOfParallelizm: int = 1):
    rootAccountNumber = rootAccountNumber.strip()

    if not rootAccountNumber:
        raise Exception("Root account or accounts file not set. Nothing to process.")

    if len(accounts) == 0:
        raise Exception("Nothing to process.")

    log_output('\033[34mRoot account number: ' + rootAccountNumber + '... \033[0m')
    log_output("Number of accounts to proceed: " + str(len(accounts)))

    if before_run_function:
        enclosure_functions_run(rootAccountNumber, before_run_function, access_key, secret_key, assumeRoleName)

    func_name, module = get_module_for_function(worker_function)
    f = getattr(module, func_name)
    log_output("\033[32mWorker function: " + worker_function + "\033[0m")

    if degreeeOfParallelizm > 1:
        parallel_run(rootAccountNumber, accounts, f, degreeeOfParallelizm, access_key, secret_key, assumeRoleName)
    else:
        one_worker_run(rootAccountNumber, accounts, f, access_key, secret_key, assumeRoleName)

    if after_run_function:
        enclosure_functions_run(rootAccountNumber, after_run_function, access_key, secret_key, assumeRoleName)


def enclosure_functions_run(rootAccountNumber, function_name, access_key, secret_key, assumeRoleName):
    provider = clientprovider.ClientProvider(rootAccount=rootAccountNumber, assumeRole=assumeRoleName,
                                             accessKey=access_key, secretKey=secret_key)
    func_name, module = get_module_for_function(function_name)
    getattr(module, func_name)(provider)


def parallel_run(rootAccountNumber, accounts, f, degreeeOfParallelizm, accessKey, secretKey, assumeRoleName):
    count = len(accounts)
    i = 0
    while i < count:
        portion = []

        for t in range(degreeeOfParallelizm):
            if i + t >= count:
                break
            portion.append(accounts[i + t])

        i = i + degreeeOfParallelizm
        threads = []
        for account in portion:
            if not account:
                continue

            provider = clientprovider.ClientProvider(rootAccount=rootAccountNumber, assumeRole=assumeRoleName,
                                                     accessKey=accessKey, secretKey=secretKey)

            log_output('\033[34mProcessing account:' + account + '\033[0m ')
            thread = PropagatingThread(name=account, target=f, args=(provider, account))
            threads.append(thread)

        for thread in threads:
            thread.start()
        try:
            for thread in threads:
                thread.join()
        except Exception as e:
            error = str(e)
            log_output('\033[91m' + error + '\033[0m')
            log_error(error)


def one_worker_run(rootAccountNumber, accounts, f, accessKey, secretKey, assumeRoleName):
    provider = clientprovider.ClientProvider(rootAccount=rootAccountNumber, assumeRole=assumeRoleName,
                                             accessKey=accessKey, secretKey=secretKey)
    for account in accounts:
        if not account:
            continue
        log_output('\033[34mProcessing account:' + account + '\033[0m ')
        try:
            f(provider, account)
        except Exception as e:
            error = str(e)
            log_output('\033[91m' + error + '\033[0m')
            log_error(error)


def get_module_for_function(worker_function: str):
    mod_name, func_name = worker_function.rsplit('.', 1)

    if not mod_name or not func_name:
        raise Exception("Wrong worker function name format. Expected: module_name.function_name")
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
        accounts = load_accounts_list(args.file)
    else:
        if args.organizations:
            log_output("Getting accounts list from organization...")
            accounts = organizations.get_all_accounts(config.RootOU)

    if config.ExcludedAccounts is not None:
        accounts = [account for account in accounts if account not in config.ExcludedAccounts]

    t = time.time()
    process_accounts(rootAccountNumber=config.RootAccountNumber, accounts=accounts, worker_function=args.workerfunction,
                     before_run_function=args.beforefunction, after_run_function=args.afterfunction,
                     assumeRoleName=role,
                     degreeeOfParallelizm=114)
