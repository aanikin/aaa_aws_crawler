from BaseReport import BaseReport
import inspect


class Organizations_Reports(BaseReport):
    def __init__(self, client, accountId, reportFolder='Reports', shortAlias=""):
        BaseReport.__init__(self, client, accountId, reportFolder, shortAlias)

        if "organizations" not in self._client._endpoint.host:
            raise Exception('Provided client is not Organizations client!')

    def run(self):
        self.describe_account()

    def describe_account(self):
        reportName = inspect.stack()[0][3]

        response = self._client.describe_account(
            AccountId=self._accountId
        )

        metaData = {"ResponseMetadata": response['ResponseMetadata']}

        self.save_reports(reportName, metaData, response["Account"])
        print(self._accountId + ": " + reportName + " сomplete")
