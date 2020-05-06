import time
import inspect
import Utilites
from IAM import IAM


class IAM_Reports(IAM):
    def __init__(self, client, accountId, reportFolder='Reports'):
        super(IAM_Reports, self).__init__(client, accountId, reportFolder)
        self.reportType = "IAM"

    def run(self):
        self.generate_credential_report()
        self.list_groups()
        self.list_roles()
        self.list_groups_for_user()
        self.get_group()
        self.list_attached_user_policies()
        self.list_attached_group_policies()
        self.list_attached_role_policies()

    def generate_credential_report(self):
        reportName = self.reportType + "_" + inspect.stack()[0][3]
        filePrefix = self.reportFilenamePrefix + reportName

        response = self._client.generate_credential_report()
        if response['State'] != 'COMPLETE':
            time.sleep(5)

        # Save metadata to file
        response = self._client.get_credential_report()

        metaData = {"GeneratedTime": str(response['GeneratedTime']),
                    "ReportFormat": str(response['ReportFormat']),
                    "ResponseMetadata": str(response['ResponseMetadata'])}

        # Save reports
        self.save_reports(filePrefix, metaData, bytes(response['Content']).decode('ascii'), "csv")

        print(self._accountId + ": " + reportName + " сomplete")

    def list_groups(self):
        reportName = self.reportType + "_" + inspect.stack()[0][3]
        filePrefix = self.reportFilenamePrefix + reportName

        response = self._client.list_groups()
        metaData = {"ResponseMetadata": str(response['ResponseMetadata'])}

        # Save reports
        self.save_reports(filePrefix, metaData, str(response['Groups']))

        print(self._accountId + ": " + reportName + " сomplete")

    def list_roles(self):
        reportName = self.reportType + "_" + inspect.stack()[0][3]
        filePrefix = self.reportFilenamePrefix + reportName

        response = self._client.list_roles()

        # Save reports
        metaData = {"ResponseMetadata": str(response['ResponseMetadata'])}
        self.save_reports(filePrefix, metaData, str(response['Roles']))

        print(self._accountId + ": " + reportName + " сomplete")

    def list_groups_for_user(self):
        reportName = self.reportType + "_" + inspect.stack()[0][3]

        response = self._client.list_users()
        for user in response['Users']:
            filePrefix = self.reportFilenamePrefix + reportName + '_' + user['UserName']

            response = self._client.list_groups_for_user(UserName=str(user['UserName']))

            # Save report to file
            metaData = {"IsTruncated": str(response['IsTruncated']),
                        "ResponseMetadata": str(response['ResponseMetadata'])}
            self.save_reports(filePrefix, metaData, str(response['Groups']))

        print(self._accountId + ": " + reportName + " сomplete")

    def get_group(self):
        reportName = self.reportType + "_" + inspect.stack()[0][3]

        response = self._client.list_groups()
        for group in response['Groups']:
            groupName = group['GroupName']
            filePrefix = self.reportFilenamePrefix + reportName + '_' + groupName

            response = self._client.get_group(GroupName=groupName)

            # Save reports
            metaData = {"Group": str(response["Group"]),
                        "IsTruncated": str(response['IsTruncated']),
                        "ResponseMetadata": str(response['ResponseMetadata'])}

            self.save_reports(filePrefix, metaData, str(response['Users']))

        print(self._accountId + ": " + reportName + " сomplete")

    def list_attached_user_policies(self):
        reportName = self.reportType + "_" + inspect.stack()[0][3]

        response = self._client.list_users()
        for user in response['Users']:
            userName = user['UserName']
            filePrefix = self.reportFilenamePrefix + reportName + '_' + userName

            response = self._client.list_attached_user_policies(UserName=userName)
            # Save metadata to file
            metaData = {"IsTruncated": str(response['IsTruncated']),
                        "ResponseMetadata": str(response['ResponseMetadata'])}

            # Save reports
            self.save_reports(filePrefix, metaData, str(response['AttachedPolicies']))

        print(self._accountId + ": " + reportName + " сomplete")

    def list_attached_group_policies(self):
        reportName = self.reportType + "_" + inspect.stack()[0][3]

        response = self._client.list_groups()
        for group in response['Groups']:
            groupName = group['GroupName']
            filePrefix = self.reportFilenamePrefix + reportName + '_' + groupName

            response = self._client.list_attached_group_policies(GroupName=groupName)

            metaData = {"IsTruncated": str(response['IsTruncated']),
                        "ResponseMetadata": str(response['ResponseMetadata'])}

            # Save reports
            self.save_reports(filePrefix, metaData, str(response['AttachedPolicies']))

        print(self._accountId + ": " + reportName + " сomplete")

    def list_attached_role_policies(self):
        reportName = self.reportType + "_" + inspect.stack()[0][3]

        response = self._client.list_roles()
        for group in response['Roles']:
            roleName = group['RoleName']
            filePrefix = self.reportFilenamePrefix + reportName + '_' + roleName

            response = self._client.list_attached_role_policies(RoleName=roleName)

            # Save metadata to file
            metaData = {"IsTruncated": str(response['IsTruncated']),
                        "ResponseMetadata": str(response['ResponseMetadata'])}

            self.save_reports(filePrefix, metaData, str(response['AttachedPolicies']))

        print(self._accountId + ": " + reportName + " сomplete")
