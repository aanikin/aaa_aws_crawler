import boto3


class ClientProvider(object):

    def __init__(self, rootAccount, accessKey: str = "", secretKey: str = "",
                 assumeRole='OrganizationAccountAccessRole'):
        if not accessKey or not secretKey:
            self._rootSession = boto3.Session()
        else:
            self._rootSession = boto3.Session(aws_access_key_id=accessKey,
                                              aws_secret_access_key=secretKey)

        self.rootAccount = rootAccount
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
        if (accountId != self.rootAccount):
            session = self.assumed_role_session(accountId)

        print("\033[90m" + accountId + ": client for service " + serviceName + " created.\033[0m")
        return session.client(service_name=serviceName, region_name=region, use_ssl=True)

    def get_client_for_root(self, serviceName, region='us-east-1'):
        session = self._rootSession

        print("\033[90mROOT: client for " + serviceName + " created.\033[0m")
        return session.client(service_name=serviceName, region_name=region, use_ssl=True)

    def get_clients_for_all_regions(self, accountId, serviceName):
        session = self._rootSession
        if (accountId != self.rootAccount):
            session = self.assumed_role_session(accountId)

        client = session.client('ec2')
        regions = [region['RegionName'] for region in client.describe_regions()['Regions']]

        for region in regions:
            print(
                "\033[90m" + accountId + ": client for service " + serviceName + " in region " + region + " created.\033[0m")
            yield (region, session.client(service_name=serviceName, region_name=region, use_ssl=True))
