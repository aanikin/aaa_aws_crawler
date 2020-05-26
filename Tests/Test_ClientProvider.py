import unittest
from unittest.mock import patch, Mock
import clientprovider


class ClientProviderTests(unittest.TestCase):
    @patch("boto3.Session")
    def test_init(self, session):
        provider = clientprovider.ClientProvider("rootAccount")

        session.assert_called_with()
        assert provider._rootSession == session.return_value
        assert provider.rootAccount == "rootAccount"
        assert provider._assumeRole == "OrganizationAccountAccessRole"

    @patch("boto3.Session")
    def test_init_with_keys(self, session):
        provider = clientprovider.ClientProvider("rootAccount", accessKey="accessKey", secretKey="secretKey",
                                                 assumeRole="role")

        session.assert_called_with(aws_access_key_id='accessKey', aws_secret_access_key='secretKey')
        assert provider._rootSession == session.return_value
        assert provider.rootAccount == "rootAccount"
        assert provider._assumeRole == "role"

    @patch("boto3.Session")
    def test_get_client_for_root(self, session):
        provider = clientprovider.ClientProvider("rootAccount")

        provider.get_client("rootAccount", "someService", "someRegion")

        session().client.assert_called_with(region_name='someRegion', service_name='someService', use_ssl=True)

    @patch("boto3.Session")
    def test_get_client_for_another_account(self, session):
        provider = clientprovider.ClientProvider("rootAccount")

        provider.get_client("someAccount", "someService", "someRegion")

        session().client.assert_called_with(region_name='someRegion', service_name='someService', use_ssl=True)

    @patch("boto3.Session")
    def test_assume_role(self, Session):
        provider = clientprovider.ClientProvider("rootAccount")

        assumedSession = provider.assumed_role_session("someAccount")

        provider._rootSession.client.assert_called_with("sts")
        provider._rootSession.client.return_value.assume_role.assert_called_once_with(
            RoleArn='arn:aws:iam::someAccount:role/OrganizationAccountAccessRole', RoleSessionName='newsession')


if __name__ == '__main__':
    unittest.main()
