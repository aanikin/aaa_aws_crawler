import time
import inspect
import Utilites
import os


class IAM(object):
    def __init__(self, client, accountId, reportFolder='Reports'):
        self._client = client
        if self._client._endpoint.host != 'https://iam.amazonaws.com':
            raise Exception('Provided client is not IAM client!')

        self._accountId = accountId
        self._folder = reportFolder + '/' + accountId
        if not os.path.exists(self._folder):
            os.mkdir(self._folder)

        self.reportFilenamePrefix = self._folder + "/" + accountId + "_"

    def generate_credential_report(self):
        reportName = self.__class__.__name__ + "_" + inspect.stack()[0][3]
        filePrefix = self.reportFilenamePrefix + reportName

        response = self._client.generate_credential_report()
        if response['State'] != 'COMPLETE':
            time.sleep(5)

        # Save metadata to file
        response = self._client.get_credential_report()

        metaData = {"GeneratedTime": str(response['GeneratedTime']),
                    "ReportFormat": str(response['ReportFormat']),
                    "ResponseMetadata": str(response['ResponseMetadata'])}
        Utilites.write_meta(filePrefix, metaData)

        # Save report to file
        Utilites.write_data(filePrefix, bytes(response['Content']).decode('ascii'), "csv")

        print(self._accountId + ": " + reportName + " сomplete")

    def list_groups(self):
        reportName = self.__class__.__name__ + "_" + inspect.stack()[0][3]
        filePrefix = self.reportFilenamePrefix + reportName

        response = self._client.list_groups()
        # Save metadata to file
        metaData = {"ResponseMetadata": str(response['ResponseMetadata'])}
        Utilites.write_meta(filePrefix, metaData)

        # Save report to file
        Utilites.write_data(filePrefix, str(response['Groups']))

        print(self._accountId + ": " + reportName + " сomplete")

    def list_roles(self):
        reportName = self.__class__.__name__ + "_" + inspect.stack()[0][3]
        filePrefix = self.reportFilenamePrefix + reportName

        response = self._client.list_roles()
        # Save metadata to file
        metaData = {"ResponseMetadata": str(response['ResponseMetadata'])}
        Utilites.write_meta(filePrefix, metaData)

        # Save report to file
        Utilites.write_data(filePrefix, str(response['Roles']))

        print(self._accountId + ": " + reportName + " сomplete")

    def list_groups_for_user(self):
        reportName = self.__class__.__name__ + "_" + inspect.stack()[0][3]

        response = self._client.list_users()
        for user in response['Users']:
            filePrefix = self.reportFilenamePrefix + reportName + '_' + user['UserName']

            response = self._client.list_groups_for_user(UserName=str(user['UserName']))
            # Save metadata to file
            metaData = {"IsTruncated": str(response['IsTruncated']),
                        "ResponseMetadata": str(response['ResponseMetadata'])}
            Utilites.write_meta(filePrefix, metaData)

            # Save report to file
            Utilites.write_data(filePrefix, str(response['Groups']))

        print(self._accountId + ": " + reportName + " сomplete")

    def get_group(self):
        reportName = self.__class__.__name__ + "_" + inspect.stack()[0][3]

        response = self._client.list_groups()
        for group in response['Groups']:
            groupName = group['GroupName']
            filePrefix = self.reportFilenamePrefix + reportName + '_' + groupName

            response = self._client.get_group(GroupName=groupName)

            # Save metadata to file
            metaData = {"Group": str(response["Group"]),
                        "IsTruncated": str(response['IsTruncated']),
                        "ResponseMetadata": str(response['ResponseMetadata'])}
            Utilites.write_meta(filePrefix, metaData)

            Utilites.write_data(filePrefix, str(response['Users']))

        print(self._accountId + ": " + reportName + " сomplete")

    def list_attached_user_policies(self):
        reportName = self.__class__.__name__ + "_" + inspect.stack()[0][3]

        response = self._client.list_users()
        for user in response['Users']:
            userName = user['UserName']
            filePrefix = self.reportFilenamePrefix + reportName + '_' + userName

            response = self._client.list_attached_user_policies(UserName=userName)
            # Save metadata to file
            metaData = {"IsTruncated": str(response['IsTruncated']),
                        "ResponseMetadata": str(response['ResponseMetadata'])}
            Utilites.write_meta(filePrefix, metaData)

            # Save report to file
            Utilites.write_data(filePrefix, str(response['AttachedPolicies']))

        print(self._accountId + ": " + reportName + " сomplete")

    def list_attached_group_policies(self):
        reportName = self.__class__.__name__ + "_" + inspect.stack()[0][3]

        response = self._client.list_groups()
        for group in response['Groups']:
            groupName = group['GroupName']
            filePrefix = self.reportFilenamePrefix + reportName + '_' + groupName

            response = self._client.list_attached_group_policies(GroupName=groupName)

            # Save metadata to file
            metaData = {"IsTruncated": str(response['IsTruncated']),
                        "ResponseMetadata": str(response['ResponseMetadata'])}
            Utilites.write_meta(filePrefix, metaData)

            Utilites.write_data(filePrefix, str(response['AttachedPolicies']))

        print(self._accountId + ": " + reportName + " сomplete")

    def list_attached_role_policies(self):
        reportName = self.__class__.__name__ + "_" + inspect.stack()[0][3]

        response = self._client.list_roles()
        for group in response['Roles']:
            roleName = group['RoleName']
            filePrefix = self.reportFilenamePrefix + reportName + '_' + roleName

            response = self._client.list_attached_role_policies(RoleName=roleName)

            # Save metadata to file
            metaData = {"IsTruncated": str(response['IsTruncated']),
                        "ResponseMetadata": str(response['ResponseMetadata'])}
            Utilites.write_meta(filePrefix, metaData)

            Utilites.write_data(filePrefix, str(response['AttachedPolicies']))

        print(self._accountId + ": " + reportName + " сomplete")
