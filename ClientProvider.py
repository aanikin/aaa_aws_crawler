import boto3


class ClientProvider(object):

    def __init__(self, rootAccount, accessKey: str = None, secretKey: str = None,
                 assumeRole='OrganizationAccountAccessRole'):
        if accessKey is None or secretKey is None:
            self._rootSession = boto3.Session()
        else:
            self._rootSession = boto3.Session(aws_access_key_id=accessKey,
                                              aws_secret_access_key=secretKey)

        self._rootAccount = rootAccount
        self._assumeRole = assumeRole

    def assumed_role_session(self, accountId):
        client = self._rootSession.client('sts')
        stsresponse = client.assume_role(
            RoleArn='arn:aws:iam::' + accountId + ':role/' + self._assumeRole,
            RoleSessionName='newsession'
        )

        # Save the details from assumed role into vars
        newsession_id = stsresponse["Credentials"]["AccessKeyId"]
        newsession_key = stsresponse["Credentials"]["SecretAccessKey"]
        newsession_token = stsresponse["Credentials"]["SessionToken"]

        return boto3.Session(aws_access_key_id=newsession_id,
                             aws_secret_access_key=newsession_key,
                             aws_session_token=newsession_token)

    def get_client(self, accountId, serviceName, region='us-east-1'):
        session = self._rootSession
        if (accountId != self._rootAccount):
            session = self.assumed_role_session(accountId)

        print(accountId + ": " + serviceName + " client created.")
        return session.client(service_name=serviceName, region_name=region, use_ssl=True)
