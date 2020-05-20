from BaseReport import BaseReport
import inspect
from datetime import datetime, timezone


class IAM_KeyRoutines(BaseReport):
    def __init__(self, client, accountId, reportFolder='Reports', shortAlias=""):
        BaseReport.__init__(self, client, accountId, reportFolder, shortAlias)

        if self._client._endpoint.host != 'https://iam.amazonaws.com':
            raise Exception('Provided client is not IAM client!')

    def run(self):
        self.old_access_keys()

    def old_access_keys(self):
        reportName = inspect.stack()[0][3]
        now = datetime.now(timezone.utc)
        users = self._client.list_users()

        keys = []
        for user in users["Users"]:
            accessKeys = self._client.list_access_keys(UserName=user['UserName'])

            for key in accessKeys['AccessKeyMetadata']:
                timeSpan = now - key["CreateDate"]
                if timeSpan.days >= 90:
                    keys.append(key)

        self.save_reports(reportName, "", keys)
        print(self._accountId + ": " + reportName + " сomplete")
