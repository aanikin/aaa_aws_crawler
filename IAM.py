import os
import Utilites

class IAM(object):
    def __init__(self, client, accountId, reportFolder='Reports'):
        self._client = client
        if self._client._endpoint.host != 'https://iam.amazonaws.com':
            raise Exception('Provided client is not IAM client!')

        self._accountId = accountId
        self._folder = reportFolder + '/' + accountId
        if not os.path.exists(self._folder):
            os.mkdir(self._folder)

        self.reportFilenamePrefix = self._folder + "_"

        self.reportType = self.__class__.__name__

    def save_reports(self, filePrefix, metaData, content, contentType="json"):
        Utilites.write_meta(filePrefix, metaData)
        Utilites.write_data(filePrefix, content, contentType)
