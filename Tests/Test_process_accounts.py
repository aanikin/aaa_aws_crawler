import sys, os

testdir = os.path.dirname(__file__)
srcdir = '../'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

import unittest
from unittest import TestCase
from unittest.mock import patch, Mock, mock_open, call
import process_accounts


class ProcessAccounts(TestCase):

    @patch('importlib.import_module')
    def test_get_module_for_function(self, ImportLib):
        self.assertRaises(Exception, process_accounts.get_module_for_function, "wrongname")

        process_accounts.get_module_for_function("module.function")

        ImportLib.assert_called_once_with("module")

    @patch('importlib.import_module')
    def test_audit_process_run_2_functions(self, ImportLib):
        rootAccount = "root"
        accounts = ['123']
        process_accounts.process_accounts(rootAccount, accounts, worker_function="worker.function",
                                          before_run_function="worker.before", after_run_function="worker.after")

        self.assertEqual(ImportLib.call_count, 3)

    @patch('importlib.import_module')
    @patch("ClientProvider.ClientProvider", autospec=True)
    def test_audit_process_parameters_check(self, provider, ImportLib):
        process_accounts.process_accounts(rootAccountNumber="rootAccountNumber", accounts=["someaccount"],
                                          worker_function="worker.function",
                                          before_run_function="worker.before", after_run_function="worker.after",
                                          assumeRoleName="SomeRole")

        provider.assert_called_once_with(assumeRole='SomeRole', rootAccount='rootAccountNumber', accessKey='',
                                         secretKey='')

    @patch('importlib.import_module')
    @patch("ClientProvider.ClientProvider", autospec=True)
    def test_audit_process_parameters_check_keys(self, provider, ImportLib):
        process_accounts.process_accounts(rootAccountNumber="rootAccountNumber", accounts=["someaccount"],
                                          worker_function="worker.function",
                                          before_run_function="worker.before", after_run_function="worker.after",
                                          access_key='akey', secret_key='skey',
                                          assumeRoleName="SomeRole")

        provider.assert_called_once_with(accessKey='akey', assumeRole='SomeRole',
                                         rootAccount='rootAccountNumber', secretKey='skey')


if __name__ == '__main__':
    unittest.main()
