import sys, os
testdir = os.path.dirname(__file__)
srcdir = '../'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

import unittest
from unittest import TestCase
from unittest.mock import patch, Mock, mock_open, call
import Audit

class AuditTests(TestCase):
    @patch('ClientProvider.ClientProvider')
    @patch('IAM_Reports.IAM_Reports')
    @patch('Organizations_Reports.Organizations_Reports')
    def test_audit_process(self, Organizations, Iam_reports, Provider):
        provider = Provider()

        client = Mock()
        client._endpoint.host = 'https://iam.amazonaws.com'

        iam_reports = Iam_reports()
        Organizations = Organizations()

        rootAccount = "root"
        accounts = ['123']
        Audit.audit_process(provider, rootAccount, accounts, Audit.audit_worker)
        calls = [call.get_client('123', 'iam'),
                 call.get_client('root', 'organizations')]
        provider.get_client.assert_has_calls(calls, any_order=True)

        iam_reports.run.assert_called_with()
        Organizations.run.assert_called_with()

    def test_IAMAudit_invalid_parameters(self):
        rootAccount = ''
        accounts = ['someaccount']
        self.assertRaises(Exception, Audit.SOC_audit, rootAccount, accounts)

        rootAccount = 'rootAccount'
        self.assertRaises(Exception, Audit.SOC_audit, rootAccount, [])

    @patch('IAM_Reports.IAM_Reports')
    @patch('Organizations_Reports.Organizations_Reports')
    @patch("ClientProvider.ClientProvider", autospec=True)
    def test_IAMAudit(self, provider, Organizations, Iam_reports):
        with patch('builtins.open', mock_open(read_data='account')) as m:
            Audit.SOC_audit(rootAccountNumber="rootAccountNumber", accounts=["someaccount"],
                            worker_function=Audit.audit_worker)

        provider.assert_called_once_with('rootAccountNumber')


if __name__ == '__main__':
    unittest.main()
