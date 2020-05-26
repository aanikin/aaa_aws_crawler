import sys, os

testdir = os.path.dirname(__file__)
srcdir = '../'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

import unittest
from unittest import TestCase
from unittest.mock import patch, Mock, mock_open, call
import threading
import process_accounts



class ProcessAccounts(TestCase):

    @patch('importlib.import_module')
    def test_get_module_for_function(self, ImportLib):
        self.assertRaises(Exception, process_accounts.get_module_for_function, "wrongname")

        process_accounts.get_module_for_function("module.function")

        ImportLib.assert_called_once_with("module")

    # @patch('propagatingthread.PropagatingThread', autospec=True)
    @patch('importlib.import_module')
    def test_audit_process_run_2_functions(self, ImportLib):
        rootAccount = "root"
        accounts = ['123', '456']
        process_accounts.process_accounts(rootAccount, accounts, worker_function="worker.function",
                                          before_run_function="worker.before", after_run_function="worker.after",
                                          degreeeOfParallelizm=2)
        self.assertEqual(ImportLib.call_count, 3)

    @patch("clientprovider.ClientProvider", autospec=True)
    def test_number_of_started_threads(self, provider):
        def worker(provider, account):
            print("Run from thread for account/thread name: " + threading.current_thread().name)
            worker.counter += 1

        worker.counter = 0

        accounts = ['789', '012']
        process_accounts.parallel_run("root", accounts, worker, degreeeOfParallelizm=len(accounts),
                                      accessKey="", secretKey="", assumeRoleName="")

        self.assertEqual(worker.counter, len(accounts))

    @patch('importlib.import_module')
    @patch("clientprovider.ClientProvider", autospec=True)
    def test_audit_process_parameters_check(self, provider, ImportLib):
        process_accounts.process_accounts(rootAccountNumber="rootAccountNumber", accounts=["someaccount"],
                                          worker_function="worker.function",
                                          before_run_function="worker.before", after_run_function="worker.after",
                                          assumeRoleName="SomeRole")
        self.assertEqual(provider.call_count, 3)
        provider.assert_called_with(assumeRole='SomeRole', rootAccount='rootAccountNumber', accessKey='', secretKey='')

    @patch('importlib.import_module')
    @patch("clientprovider.ClientProvider", autospec=True)
    def test_audit_process_parameters_check_keys(self, provider, ImportLib):
        process_accounts.process_accounts(rootAccountNumber="rootAccountNumber", accounts=["someaccount"],
                                          worker_function="worker.function",
                                          before_run_function="worker.before", after_run_function="worker.after",
                                          access_key='akey', secret_key='skey',
                                          assumeRoleName="SomeRole")
        self.assertEqual(provider.call_count, 3)
        provider.assert_called_with(accessKey='akey', assumeRole='SomeRole', rootAccount='rootAccountNumber',
                                    secretKey='skey')


if __name__ == '__main__':
    unittest.main()
