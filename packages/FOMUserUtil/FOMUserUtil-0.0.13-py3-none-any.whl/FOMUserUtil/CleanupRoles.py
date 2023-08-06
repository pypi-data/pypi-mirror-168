'''
as a proof of concept that roles could be created using a script, created a
bunch of role in the client that was used to gain access to keycloak admin

This script cleans up those roles
'''

import logging

from . import constants
from . import FOMKeyCloak

LOGGER = logging.getLogger(__name__)


class CleanupRoles:

    def __init__(self):
        self.kc = FOMKeyCloak.FomKeycloak()

    def getRoles(self):
        roles = self.kc.getRoles(constants.KC_SA_CLIENTID)
        roleNames = [role['name'] for role in roles]
        roleNames.sort()

        LOGGER.debug(f"Num roles: {len(roleNames)}")
        return roleNames

    def removeRoles(self, roleNames):
        client = self.kc.getClient(constants.KC_SA_CLIENTID)
        for roleName in roleNames:
            self.kc.removeRole(client['id'], roleName)


if __name__ == '__main__':
    LOGGER = logging.getLogger()
    LOGGER.setLevel(logging.DEBUG)
    hndlr = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(message)s')
    hndlr.setFormatter(formatter)
    LOGGER.addHandler(hndlr)

    LOGGER.debug("hello")
    cr = CleanupRoles()
    roles = cr.getRoles()
    cr.removeRoles(roles)
