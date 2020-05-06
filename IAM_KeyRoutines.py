import os
from IAM import IAM


class IAM_KeyRoutines(IAM):
    def run(self):
        self.not_used_keys()

    def not_used_keys(self):
        reportName = self.reportType + "_" + inspect.stack()[0][3]
        filePrefix = self.reportFilenamePrefix + reportName

        # response = self._client.generate_credential_report()

        print(self._accountId + ": " + reportName + " сomplete")
