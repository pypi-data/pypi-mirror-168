import logging

import pytest

from . import FOMKeyCloak

LOGGER = logging.getLogger(__name__)
LOGGER.debug("message test")


class Test_FOMKeyCloak:

    def test_getFOMRoles(self, fomKeyCloak_fixture):
        clientRoleExists = fomKeyCloak_fixture.roleExists('234234')
        assert not clientRoleExists

        clientRoleExists = fomKeyCloak_fixture.roleExists('1011')
        assert clientRoleExists

    def test_getRoles(self, fomKeyCloak_fixture):
        roles = fomKeyCloak_fixture.getRoles('99999999')
        # should error but doesn't
        LOGGER.debug(f"roles: {roles}")

    def test_userIDExists(self, fomKeyCloak_fixture):
        userData = fomKeyCloak_fixture.isValidUser('kjnether@idir')
        LOGGER.debug(f"userData: {userData}")
        assert userData is True

    def test_getMatchingUsers(self, fomKeyCloak_fixture, userNames_fixtures):
        for userString in userNames_fixtures:
            users = fomKeyCloak_fixture.getMatchingUsers(userString, False)
            users = fomKeyCloak_fixture.getMatchingUsers(userString, True)
            LOGGER.debug(f"userData: {users[0]}")

    def test_getUserProfile(self, fomKeyCloak_fixture):
        #users = fomKeyCloak_fixture.getMatchingUsers('huhs', False)
        #LOGGER.debug(f"userData: {users}")
        id = 'a8646348-24f7-4222-ad48-1e201be124bd'
        profile = fomKeyCloak_fixture.getUserProfile(id)
        LOGGER.debug(f"profile: {profile}")

    def test_getFOMUserRoleMappings(self, fomKeyCloak_fixture):
        id = 'a8646348-24f7-4222-ad48-1e201be124bd'
        mappings = fomKeyCloak_fixture.getFOMUserRoleMappings(id)
        LOGGER.debug(f"profile: {mappings}")

    def test_getMatchingUsersWithRoleMapping(self, fomKeyCloak_fixture, userNames_fixtures):
        #testStrings = ['huh', 'ath', 'kjn', 'md', 'a']
        for testString in userNames_fixtures:
            retVal = fomKeyCloak_fixture.getMatchingUsersWithRoleMapping(testString)
            LOGGER.debug(f"userroles: {retVal}")

    def test_addRoleToUser(self, fomKeyCloak_fixture):
        fomKeyCloak_fixture.addRoleToUser('kjnether@idir', '99999999')

    def test_createRole(self, fomKeyCloak_fixture):
        testfcid = '99999999'
        description = "test dummy role"
        fomKeyCloak_fixture.createRole(testfcid, description)

    def test_getFomClientId(self, fomKeyCloak_fixture):
        client = fomKeyCloak_fixture.getFomClientId()
        LOGGER.debug(f"clientid: {client}")
        assert client is not None

    def test_isValidUser(self, fomKeyCloak_fixture):
        users = fomKeyCloak_fixture.getAllUsers()
        valid = fomKeyCloak_fixture.isValidUser(users[0]['username'])
        LOGGER.debug(f"users total: {len(users)}")
        LOGGER.debug(f"isvalid: {valid}")

    def test_getAllUsers(self, fomKeyCloak_fixture):
        users = fomKeyCloak_fixture.getAllUsers()
        LOGGER.debug(f"first user: {users[0]}")
        assert users is not None

    def test_getUserCount(self, fomKeyCloak_fixture):
        usersCnt = fomKeyCloak_fixture.getUserCount()
        LOGGER.debug(f"total users in sys: {usersCnt}")

    def test_getUserPage(self, fomKeyCloak_fixture):
        users = fomKeyCloak_fixture.getUserPage(230, 20)
        usersCnt = len(users)
        LOGGER.debug(f"returned: {usersCnt}")



@pytest.fixture
def fomKeyCloak_fixture():
    return FOMKeyCloak.FomKeycloak()

@pytest.fixture
def userNames_fixtures():
    return ['huh', 'ath', 'kjn', 'md', 'a']
