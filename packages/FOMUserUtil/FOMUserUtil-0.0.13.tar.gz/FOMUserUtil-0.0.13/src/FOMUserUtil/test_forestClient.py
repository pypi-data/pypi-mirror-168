import logging

import pytest

from . import ForestClient

LOGGER = logging.getLogger(__name__)
LOGGER.debug("message test")


class Test_ForestClientFromGit:

    def test_forestClientFromGitParse(self, forestClient_fixture):
        forestClient_fixture.parseMultiple()
        LOGGER.debug(
            "number of forest clients: " +
            f"{len(forestClient_fixture.forestClientData)}")
        assert len(forestClient_fixture.forestClientData) >= 22408

    def test_getMatchingClient(self, forestClientParsed_fixture):
        values = forestClientParsed_fixture.getMatchingClient('arm')
        LOGGER.debug(f"values: {values}")

    def test_getPaddedForestClientID(self, forestClientUtil_fixture):
        fc = forestClientUtil_fixture
        sampleData = [['33', '00000033'], ['2234', '00002234']]
        for data in sampleData:
            padded = fc.getPaddedForestClientID(data[0])
            assert padded == data[1]

    def test_getForestClientDescription(self, forestClientParsed_fixture):
        client = 187347
        desc = forestClientParsed_fixture.getForestClientDescription(client)
        LOGGER.debug(f"desc: {desc}")
        assert desc is not None
        assert desc == 'LANDING HV DEVELOPMENT LTD'

    def test_forestClientIdExists(self, forestClientParsed_fixture):
        fc = forestClientParsed_fixture
        clientsThatExist = ['188736', '187347', '186040', '181461', '177380',
                            '62911', '23530', '2884', '1011']
        clientsThatDontExist = ['88348', '88978', '90125']
        for clExist in clientsThatExist:
            LOGGER.debug(f"fcExists: {clExist}")

            assert fc.forestClientIdExists(clExist) is True

        for clExist in clientsThatDontExist:
            fcExists = fc.forestClientIdExists(clExist)
            LOGGER.debug(f"fcExists: {clExist}  :  {fcExists}")
            assert fcExists is False


@pytest.fixture
def forestClient_fixture():
    return ForestClient.ForestClientFromGit()


@pytest.fixture
def forestClientParsed_fixture(forestClient_fixture):
    forestClient_fixture.parseMultiple()
    return forestClient_fixture


@pytest.fixture
def forestClientUtil_fixture():
    fcUtil = ForestClient.ForestClientUtil()
    return fcUtil


@pytest.fixture
def forestClientCsv_fixture():
    fcUtil = ForestClient.ForestClientFromCsv()
    return fcUtil
