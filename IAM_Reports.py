import time
import inspect
from BaseReport import BaseReport


class IAM_Reports(BaseReport):

    def __init__(self, client, accountId, reportFolder='Reports', shortAlias="IAM"):
        BaseReport.__init__(self, client, accountId, reportFolder, shortAlias)

        if self._client._endpoint.host != 'https://iam.amazonaws.com':
            raise Exception('Provided client is not IAM client!')

    def run(self):
        self.generate_credential_report()
        self.list_groups()
        self.list_roles()
        self.list_groups_for_user()
        self.get_group()
        self.list_attached_user_policies()
        self.list_attached_group_policies()
        self.list_attached_role_policies()
        self.get_account_summary()

    def generate_credential_report(self):
        reportName = inspect.stack()[0][3]

        response = self._client.generate_credential_report()
        if response['State'] != 'COMPLETE':
            time.sleep(5)

        # Save metadata to file
        response = self._client.get_credential_report()

        metaData = {"GeneratedTime": response['GeneratedTime'],
                    "ReportFormat": response['ReportFormat'],
                    "ResponseMetadata": response['ResponseMetadata']}

        # Save reports
        self.save_reports(reportName, metaData, bytes(response['Content']).decode('ascii'), "csv")

        print(self._accountId + ": " + reportName + " сomplete")

    def list_groups(self):
        reportName = inspect.stack()[0][3]

        response = self._client.list_groups()
        metaData = {"ResponseMetadata": response['ResponseMetadata']}

        # Save reports
        self.save_reports(reportName, metaData, response['Groups'])

        print(self._accountId + ": " + reportName + " сomplete")

    def list_roles(self):
        reportName = inspect.stack()[0][3]

        response = self._client.list_roles()

        # Save reports
        metaData = {"ResponseMetadata": response['ResponseMetadata']}
        self.save_reports(reportName, metaData, response['Roles'])

        print(self._accountId + ": " + reportName + " сomplete")

    def list_groups_for_user(self):
        reportName = inspect.stack()[0][3]

        response = self._client.list_users()
        for user in response['Users']:
            response = self._client.list_groups_for_user(UserName=str(user['UserName']))

            # Save report to file
            metaData = {"IsTruncated": response['IsTruncated'],
                        "ResponseMetadata": response['ResponseMetadata']}
            self.save_reports(reportName + '_' + user['UserName'], metaData, response['Groups'])

        print(self._accountId + ": " + reportName + " сomplete")

    def get_group(self):
        reportName = inspect.stack()[0][3]

        response = self._client.list_groups()
        for group in response['Groups']:
            groupName = group['GroupName']

            response = self._client.get_group(GroupName=groupName)

            # Save reports
            metaData = {"Group": response["Group"],
                        "IsTruncated": response['IsTruncated'],
                        "ResponseMetadata": response['ResponseMetadata']}

            self.save_reports(reportName + '_' + group['GroupName'], metaData, response['Users'])

        print(self._accountId + ": " + reportName + " сomplete")

    def list_attached_user_policies(self):
        reportName = inspect.stack()[0][3]

        response = self._client.list_users()
        for user in response['Users']:
            userName = user['UserName']

            response = self._client.list_attached_user_policies(UserName=userName)
            # Save metadata to file
            metaData = {"IsTruncated": response['IsTruncated'],
                        "ResponseMetadata": response['ResponseMetadata']}

            # Save reports
            self.save_reports(reportName + '_' + user['UserName'], metaData, response['AttachedPolicies'])

        print(self._accountId + ": " + reportName + " сomplete")

    def list_attached_group_policies(self):
        reportName = inspect.stack()[0][3]

        response = self._client.list_groups()
        for group in response['Groups']:
            groupName = group['GroupName']
            response = self._client.list_attached_group_policies(GroupName=groupName)

            metaData = {"IsTruncated": response['IsTruncated'],
                        "ResponseMetadata": response['ResponseMetadata']}

            # Save reports
            self.save_reports(reportName + '_' + groupName, metaData, response['AttachedPolicies'])

        print(self._accountId + ": " + reportName + " сomplete")

    def list_attached_role_policies(self):
        reportName = inspect.stack()[0][3]

        response = self._client.list_roles()
        for group in response['Roles']:
            roleName = group['RoleName']

            response = self._client.list_attached_role_policies(RoleName=roleName)

            # Save metadata to file
            metaData = {"IsTruncated": response['IsTruncated'],
                        "ResponseMetadata": response['ResponseMetadata']}

            self.save_reports(reportName + '_' + roleName, metaData, response['AttachedPolicies'])

        print(self._accountId + ": " + reportName + " сomplete")

    def get_account_summary(self):
        reportName = inspect.stack()[0][3]

        response = self._client.get_account_summary()

        metaData = {"ResponseMetadata": response['ResponseMetadata']}

        self.save_reports(reportName, metaData, response["SummaryMap"])

        print(self._accountId + ": " + reportName + " сomplete")
