import os

import utilites


class BaseReport(object):
    def __init__(self, client, accountId, reportFolder='Reports', shortAlias=""):
        self._client = client

        self._accountId = accountId
        self._folder = reportFolder + '/' + accountId
        if not os.path.exists(self._folder):
            os.mkdir(self._folder)

        self.reportFilenamePrefix = self._folder + '/' + accountId + "_"

        if not shortAlias:
            self.reportClass = self.__class__.__name__
        else:
            self.reportClass = shortAlias

    def save_reports(self, reportName, metaData, content, contentType="json"):

        filePrefix = self.reportFilenamePrefix + self.reportClass + "_" + reportName

        if metaData:
            utilites.write_meta(filePrefix, metaData)

        utilites.write_data(filePrefix, content, contentType)
