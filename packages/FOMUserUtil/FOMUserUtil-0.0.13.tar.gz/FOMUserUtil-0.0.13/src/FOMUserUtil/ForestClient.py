""" interface to provision of forest client data.  For now its going to
parse / the data in the fom github repo...

Eventually will interface with the forest client api to get this information
"""

import logging
import operator
import re

import requests
try:
    from . import constants
except ImportError:
    import constants

LOGGER = logging.getLogger(__name__)


class ForestClientFromGit:

    def __init__(self):
        self.fcTable = constants.FOREST_CLIENT_IN_GIT
        self.forestClientData = {}
        self.fcUtil = ForestClientUtil()
        self.parseMultiple()

    def parseMultiple(self):
        files2Parse = constants.FOREST_CLIENT_IN_GIT.split("||")
        LOGGER.debug(f"files2Parse:{files2Parse}")
        for file2Parse in files2Parse:
            LOGGER.debug(f"parsing the file: {file2Parse}")
            self.parse(file2Parse)

    def parse(self, file2Parse):
        """pulls down the js migration file, parses out the forest clients from
        it and adds them to the 'forestClientData' property

        :param file2Parse: url to the migrations js file that has the forest
                           clients in it
        :type file2Parse: str
        """
        # pulling the data down from the git repo
        LOGGER.debug(f"file2Parse: {file2Parse}")
        response = requests.get(file2Parse)
        response.raise_for_status()
        # response.raise_for_status()
        LOGGER.debug(f"status_code: {response.status_code}")
        jsFCFile = response.text
        # the insert line marks the start of the data.  This regex detects
        # the insert line
        # sample line that shows the pattern that the next line does.
        #  ('189974', 'LUXOR-SPUR DEVELOPMENTS LTD.', CURRENT_USER),
        dataLine_regex = re.compile(
            "^\s+\('[0-9]{4,8}'\,\s+'.+'\,\s+CURRENT_USER\)\,\s*$")  # noqa
        LOGGER.debug(f"jsFCFile {type(jsFCFile)}")
        cnt = 0
        for line in jsFCFile.split('\n'):
            if dataLine_regex.match(line):
                line = line.replace(', CURRENT_USER),', '')
                line = line.replace('(', '').replace(')', '').strip()
                line = line.replace(', ', ',').replace("'", '')
                lineList = line.split(',')
                forestClientId = self.fcUtil.getPaddedForestClientID(
                    lineList[0])
                self.forestClientData[lineList[1]] = forestClientId
                if not cnt % 1000:
                    LOGGER.debug(f"read and matched: {cnt}")
                cnt += 1
        LOGGER.debug(f"number forest clients = {len(self.forestClientData)}")

    def getForestClientDescription(self, clientId):
        clientId = self.fcUtil.getPaddedForestClientID(clientId)
        returnVal = None
        for fc in self.forestClientData:
            if clientId == self.forestClientData[fc]:
                returnVal = fc
                break
        return returnVal

    def getMatchingClient(self, characters):
        values = []
        for fc in self.forestClientData:
            if characters.lower() in fc.lower():
                values.append([fc, self.forestClientData[fc]])
        values = (sorted(values, key=operator.itemgetter(0)))
        return values

    def forestClientIdExists(self, clientId):
        # remove any padding characters
        clientIdPadded = self.fcUtil.getPaddedForestClientID(clientId)
        clientExists = False
        if clientIdPadded in self.forestClientData.values():
            clientExists = True
        return clientExists


class ForestClientUtil:
    def __init__(self):
        self.rolePrefix = 'fom_forest_client_'

    def getPaddedForestClientID(self, clientId):
        """Forest clients are an 8 digit field that is stored as a string.
        This method will pad the forestclient id with leading 0's to meet
        the expected 8 character length

        :param clientId: input forest client
        :type clientId: str, int
        """
        clientId_str = str(clientId)
        numChars = len(clientId_str)

        if numChars < 8:
            padding = 8 - numChars
            clientId_str = ('0' * padding) + clientId_str
        return clientId_str

    def getRoleName(self, clientID):
        fcPadded = self.getPaddedForestClientID(clientID)
        roleName = f'{self.rolePrefix}{fcPadded}'
        return roleName


class ForestClient(ForestClientFromGit):
    # TODO: should defined an abstract class that standardizes the function
    #       calls so can pivot to new data source for forest client when
    #       it becomes available

    def __init__(self):
        ForestClientFromGit.__init__(self)

    # def getMatchingClient(self, searchCharacters):
    #     return self.fc_git.getMatchingClient(searchCharacters)

    # def forestClientIdExists(self, clientId):
    #     return self.fc_git.forestClientIdExists(clientId)

    # def getForestClientDescription(self, clientId):
    #     """Returns the description for a matching forest client id"""
    #     return self.fc_git.getForestClientDescription(clientId)
