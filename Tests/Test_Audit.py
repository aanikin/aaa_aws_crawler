import sys, os
testdir = os.path.dirname(__file__)
srcdir = '../'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

import unittest
from unittest import TestCase
from unittest.mock import patch, Mock, mock_open
import Audit


# pragma: no cover
class AuditTests(TestCase):
    @patch('IAM.IAM')
    def test_audit_process(self, Iam):
        provider = Mock()

        client = Mock()
        client._endpoint.host = 'https://iam.amazonaws.com'

        iam = Iam()

        accounts = ['123', '-234']
        Audit.audit_process(provider, accounts)

        provider.get_client.assert_called_with('123', 'iam')
        iam.generate_credential_report.assert_called_with()
        iam.generate_credential_report.assert_called_with()
        iam.list_groups.assert_called_with()
        iam.list_roles.assert_called_with()
        iam.list_groups_for_user.assert_called_with()
        iam.get_group.assert_called_with()
        iam.list_attached_user_policies.assert_called_with()
        iam.list_attached_group_policies.assert_called_with()
        iam.list_attached_role_policies.assert_called_with()


    def test_IAMAudit_invalid_parameters(self):
        rootAccount = ''
        accountsFile = 'file_path'
        self.assertRaises(Exception, Audit.IAMAudit, rootAccount, accountsFile)

        rootAccount = 'rootAccount'
        accountsFile = ''
        self.assertRaises(Exception, Audit.IAMAudit, rootAccount, accountsFile)

    def test_loadload_accounts_list(self):
        with patch('builtins.open', mock_open(read_data='account')) as m:
            r = Audit.load_accounts_list("test")

        m.assert_called_once_with("test", "r")
        assert r == ['account']

    @patch("ClientProvider.ClientProvider", autospec=True)
    def test_IAMAudit_accounts_list_is_empty(self, provider):
        with patch('builtins.open', mock_open(read_data='')) as m:
            self.assertRaises(Exception, Audit.IAMAudit, "rootAccount", "data_file")

    @patch("ClientProvider.ClientProvider", autospec=True)
    def test_IAMAudit_without_provider(self, provider):
        with patch('builtins.open', mock_open(read_data='account')) as m:
            Audit.IAMAudit("rootAccountNumber", "data_file")

        provider.assert_called_once_with('rootAccountNumber')


if __name__ == '__main__':
    unittest.main()
