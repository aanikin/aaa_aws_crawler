import unittest
from unittest.mock import patch, Mock, mock_open
import IAM
import os


class IAMTests(unittest.TestCase):
    def setUp(self):
        self.iam_client = Mock()
        self.iam_client._endpoint.host = 'https://iam.amazonaws.com'

        self.iam = IAM.IAM(self.iam_client, "someAccount")

    def test_enerate_credential_report(self):
        filePrefix = self.iam.reportFilenamePrefix + "IAM_generate_credential_report"

        self.iam_client.generate_credential_report.return_value = {"State": "COMPLETE"}
        self.iam_client.get_credential_report.return_value = {"GeneratedTime": "time",
                                                              "ReportFormat": "format",
                                                              "ResponseMetadata": "responseMetadata",
                                                              "Content": "someContent".encode("ascii")}

        self.iam.generate_credential_report()

        self.iam_client.generate_credential_report.assert_called_once_with()
        self.iam_client.get_credential_report.assert_called_once_with()

        assert os.path.exists(filePrefix + "_meta") is True
        assert os.path.exists(filePrefix + ".csv") is True


if __name__ == '__main__':
    unittest.main()
