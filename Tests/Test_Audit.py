import sys, os
testdir = os.path.dirname(__file__)
srcdir = '../'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

import unittest
from unittest import TestCase
from unittest.mock import patch, Mock, mock_open
import Audit

class AuditTests(TestCase):
    @patch('IAM_Reports.IAM_Reports')
    @patch('IAM_KeyRoutines.IAM_KeyRoutines')
    def test_audit_process(self, Iam_reports, Iam_keyroutines):
        provider = Mock()

        client = Mock()
        client._endpoint.host = 'https://iam.amazonaws.com'

        iam_reports = Iam_reports()
        iam_keyroutines = Iam_keyroutines()

        accounts = ['123']
        Audit.audit_process(provider, accounts)

        provider.get_client.assert_called_with('123', 'iam')

        iam_reports.run.assert_called_with()
        iam_keyroutines.run.assert_called_with()

    def test_IAMAudit_invalid_parameters(self):
        rootAccount = ''
        accounts = ['someaccount']
        self.assertRaises(Exception, Audit.IAMAudit, rootAccount, accounts)

        rootAccount = 'rootAccount'
        self.assertRaises(Exception, Audit.IAMAudit, rootAccount, [])

    @patch('IAM_Reports.IAM_Reports')
    @patch('IAM_KeyRoutines.IAM_KeyRoutines')
    @patch("ClientProvider.ClientProvider", autospec=True)
    def test_IAMAudit(self, provider, iam_reports, iam_keyroutines):
        with patch('builtins.open', mock_open(read_data='account')) as m:
            Audit.IAMAudit(rootAccountNumber="rootAccountNumber", accounts=["someaccount"])

        provider.assert_called_once_with('rootAccountNumber')


if __name__ == '__main__':
    unittest.main()
