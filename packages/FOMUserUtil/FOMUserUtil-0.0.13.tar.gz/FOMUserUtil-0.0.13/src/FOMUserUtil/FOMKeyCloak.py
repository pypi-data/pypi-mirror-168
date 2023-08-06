import logging

import keycloak_wrapper
# TODO: not happy with the way this wrapper is implemented... Should provide
#       errors when api call fails, among other things.  Connecting to api
#       end points in KC is actually pretty easy.  Move to wrapping my self.
import requests

try:
    from . import constants
    from . import ForestClient
except ImportError:
    import constants
    import ForestClient

LOGGER = logging.getLogger(__name__)


class FomKeycloak:

    def __init__(self):
        self.getAccessToken()
        self.defaultheaders = {"Authorization": "Bearer " + self.access_token}

        self.fcUtil = ForestClient.ForestClientUtil()

    def getAccessToken(self):
        """using client id and secret queries keycloak for access token
        """
        uri = f"{constants.KC_HOST}/auth/realms/{constants.KC_REALM}" + \
              "/protocol/openid-connect/token"
        header = {'Accept': 'application/json'}
        params = {
                "client_id": constants.KC_CLIENTID,
                "client_secret": constants.KC_SECRET,
                "grant_type": "client_credentials"}
        LOGGER.debug(f'uri: {uri}')
        r = requests.post(uri, data=params, headers=header)
        r.raise_for_status()
        access_key = r.json()
        self.access_token = access_key['access_token']
        LOGGER.debug(f'response as json string {self.access_token}')

    def getMatchingUsers(self, userId, usrAndEmailOnly=True):
        """ Keycloak contains a lot of information about users.  This method
        determines if a userid exists in keycloak.  The method will do its own
        search of all the users in keycloak.  (not efficient)

        Looks for either <userid>@<identity provider>, or looks for any user id
        that matches the identity provider.

        If more than one user is found then a warning message will be logged.

            user@dir
            user@bceid
            <email address>

        Will get a list of the users in the realm and search for

        :param userId: [description]
        :type userId: [type]
        :return: [description]
        :rtype: [type]
        """
        users = self.getAllUsers()
        matchedUsers = []
        LOGGER.debug(f"userId: {userId}")
        for user in users:
            if userId.lower() in user['username'].lower():
                matchedUsers.append(user)
            elif ('email' in user) and userId.lower() in user['email'].lower():
                matchedUsers.append(user)

            elif (('attributes' in user) and
                  'idir_username' in user['attributes']) and \
                    userId.lower() in \
                    user['attributes']['idir_username'][0].lower():
                matchedUsers.append(user)
        if usrAndEmailOnly:
            matchedUsers = self.extractUsernameEmailFromuUserList(matchedUsers)
        LOGGER.debug(f"matchedUsers: {matchedUsers}")
        return matchedUsers

    def getMatchingUsersWithRoleMapping(self, userId):
        """For a given string searches all the users and related roles and
        returns a data structure like:
        [ <username>, <email>, [<roles>...]]

        :param userId: the input userid
        :type userId: str
        :return: list of users and the roles they belong to
        :rtype: list
        """
        users = self.getMatchingUsers(userId, usrAndEmailOnly=False)
        LOGGER.debug(f"users: {users}")
        roleMappings = []
        usrCnt = 0
        #print("", end='\x1b[1K\r', flush=True)
        for user in users:
            print(f'user {usrCnt} of {len(users)}', end='\r', flush=True)
            #print('.', end='', flush=True) # noqa
            roleMapping = self.getFOMUserRoleMappings(user['id'])
            usernameAndEmail = self.extractUsernameEmailFromuUser(user)
            usernameAndEmail.append(roleMapping)
            LOGGER.debug(f'rolemaps: {roleMapping}')
            roleMappings.append(usernameAndEmail)
            usrCnt += 1

        return roleMappings

    def extractUsernameEmailFromuUserList(self, users):
        userNameAndEmailList = []
        for user in users:
            userNameAndEmail = self.extractUsernameEmailFromuUser(user)
            userNameAndEmailList.append(userNameAndEmail)
        return userNameAndEmailList

    def extractUsernameEmailFromuUser(self, user):
        LOGGER.debug(f"extract email from user : {user}")
        email = ''
        username = ''
        if 'email' in user:
            email = user['email']

        # if the user is an idir user the user object will have the following
        # properties:
        #     attributes:
        #         idir_user_guild list(str)
        #         idir_userid list(str)
        #         idir_username list(str)
        #         idir_username list(str)
        #         displayName list(str)
        # if (('attributes' in user) and
        #         'idir_username' in user['attributes']):
        username = user['username']

        if not email and not user:
            msg = f'unable to extract email and username from this user: {user}'
            raise ValueError(msg)

        retVal = [username, email]

        return retVal

    def getUserProfile(self, userId):
        # GET /{realm}/users/{id}

        url = f"{constants.KC_HOST}/auth/admin/realms/{constants.KC_REALM}/users/{userId}"  # noqa
        params = {"realm-name": constants.KC_HOST}
        response = requests.get(url=url, params=params,
                                headers=self.defaultheaders)
        data = response.json()
        return data

    def getFOMUserRoleMappings(self, userId, nameonly=True):
        """for a given userId returns the rolemappings for that user id.  This
        is the userid from keycloak, not the username.

        :param userId: input userid
        :type userId: str
        :param nameonly: if set to true returns a list of only role names,
                         defaults to True
        :type nameonly: bool, optional
        :return: list of role mapping for the given userid
        :rtype: list
        """
        fomClient = self.getFomClientId()
        LOGGER.debug(f"fomClient: {fomClient}")
        url = f"{constants.KC_HOST}/auth/admin/realms/{constants.KC_REALM}/users/{userId}/role-mappings/clients/{fomClient}"  # noqa
        LOGGER.debug(f"url: {url}")

        params = {"realm-name": constants.KC_HOST}
        LOGGER.debug(f"params: {params}")
        response = requests.get(url=url, params=params,
                                headers=self.defaultheaders)
        data = response.json()
        returnData = data
        if nameonly:
            returnData = []
            for mapping in data:
                returnData.append(mapping['name'])
        return returnData

    def getUserCount(self):
        """ returns the number of users that are currently configured in
        keycloak

        :return: the number of users in keycloak
        :rtype: int
        """
        url = f"{constants.KC_HOST}/auth/admin/realms/{constants.KC_REALM}/users/count"  # noqa
        headers = {"Authorization": "Bearer " + self.access_token}
        params = {"realm-name": constants.KC_HOST}
        response = requests.get(url=url, params=params, headers=headers)
        data = response.json()
        return data

    def getAllUsers(self):
        """ Returns all the users currently configured in Keycloak

        :return: a list of objects from json describing all the users in
                 keycloak
        :rtype: list(dict)
        """

        # TODO: this is quick and dirty, could consider implementing a search
        #      in the api call for a specific user instead of returning all the
        #      users and then parsing that list

        userCnt = self.getUserCount()
        LOGGER.debug(f"userCnt: {userCnt}")

        max = 100
        first = 0

        userData = []

        while len(userData) < userCnt:
            respData = self.getUserPage(first, max)
            userData.extend(respData)
            LOGGER.debug(f"first: {first}, userdata cnt: {len(userData)} " +
                         f"usercount: {userCnt}")
            first = first + max

        LOGGER.debug(f"users returned: {len(userData)}")
        return userData

    def getUserPage(self, first, max):
        url = f"{constants.KC_HOST}/auth/admin/realms/{constants.KC_REALM}/users"  # noqa
        params = {"realm-name": constants.KC_HOST, 'max': max,
                    'first': first}
        response = requests.get(url=url, params=params,
                                headers=self.defaultheaders)
        respData = response.json()
        LOGGER.debug(f"status code: {response.status_code}")
        return respData

    def isValidUser(self, userid):
        """validates that the user provided exists in keycloak, and that the
        id is unique

        :param userid: input user id to be validated
        :type userid: str
        """
        isValid = False
        users = self.getAllUsers()
        LOGGER.debug(f"users: {users}")
        matches = []
        for user in users:
            if user['username'] == userid:
                matches.append(user)
        if len(matches) == 1:
            isValid = True
        return isValid

    def getRoles(self, clientID):
        """returns a list of roles that exist within the provided client id"""
        roles = keycloak_wrapper.client_roles(
            f"{constants.KC_HOST}/auth/",
            constants.KC_REALM,
            self.access_token,
            clientID)
        return roles

    def getFOMRoles(self, forestClientNumber: int):
        """_summary_

        :param forestClientNumber: _description_
        :type forestClientNumber: int
        :param clientID: _description_, defaults to 'fom'
        :type clientID: str, optional
        :return: _description_
        :rtype: _type_
        """
        roles = self.getRoles(constants.FOM_CLIENT_ID)
        roleName = self.fcUtil.getRoleName(forestClientNumber)

        filteredRoles = [role for role in roles if roleName == role['name']]
        return filteredRoles

    def roleExists(self, forestClientNumber: int):
        """ Checks to see if the forest client exists in keycloak

        :param forestClientNumber: [description]
        :type forestClientNumber: int
        """
        roleName = self.fcUtil.getRoleName(forestClientNumber)

        roles = self.getFOMRoles(forestClientNumber)
        roleExists = False
        if roleName in [role['name'] for role in roles]:
            roleExists = True
        return roleExists

    def getFomClientId(self):
        """Looks up the FOM client 'id' using the 'clientid'

        the client 'id' is usually what is required to create / modify objects
        in / for / on behalf of the client
        """
        clients = keycloak_wrapper.realm_clients(
            f"{constants.KC_HOST}/auth/", constants.KC_REALM,
            self.access_token)
        fomClient = None
        for client in clients:
            if client['clientId'] == constants.KC_FOM_CLIENTID:
                fomClient = client['id']
        return fomClient

    def createRole(self, forestClientId, description):
        """Creates the role for the forest client id if it doesn't already
        exist.

        * send payload/body where {"name":"role name to create"}
        * end point /auth/admin/realms/$REALM/clients/$CLIENTID/roles
        * method POST
        """
        # self.fcUtil.
        if not self.roleExists(forestClientId):
            roleName = self.fcUtil.getRoleName(forestClientId)
            LOGGER.debug(f'rolename: {roleName}')

            clientid = self.getFomClientId()
            Url = f"{constants.KC_HOST}/auth/admin/realms/{constants.KC_REALM}/clients/{clientid}/roles"  # noqa
            data = {"name": roleName,
                    "description":  description}
            headers = {
                "Authorization": "Bearer " + self.access_token,
                'Content-type': 'application/json',
                'Accept': 'application/json'}
            response = requests.post(url=Url,
                                     headers=headers,
                                     json=data)
            response.raise_for_status()

    def removeRole(self, clientID, roleName):
        """_summary_

        :param clientID: _description_
        :type clientID: _type_
        :param roleName: _description_
        :type roleName: _type_

        https://$KC_URL/auth/admin/realms/$REALM/clients/{id}/roles/{role-name}

        """
        LOGGER.debug(f'clientID: {clientID}')
        LOGGER.debug(f'roleName: {roleName}')
        Url = f"{constants.KC_HOST}/auth/admin/realms/{constants.KC_REALM}/clients/{clientID}/roles/{roleName}"  # noqa
        headers = {
            "Authorization": "Bearer " + self.access_token,
            'Content-type': 'application/json',
            'Accept': 'application/json'}
        LOGGER.debug(f"deleting the role: {roleName}")
        response = requests.delete(url=Url,
                                   headers=headers
                                   )
        response.raise_for_status()
        LOGGER.debug(f"response: {response.status_code}")

    def getClients(self):
        '''
        GET /{realm}/clients
        '''
        Url = f"{constants.KC_HOST}/auth/admin/realms/{constants.KC_REALM}/clients"  # noqa
        headers = {
            "Authorization": "Bearer " + self.access_token,
            'Content-type': 'application/json',
            'Accept': 'application/json'}
        response = requests.get(url=Url,
                                headers=headers
                                )
        response.raise_for_status()
        LOGGER.debug(f"response: {response.status_code}")

        data = response.json()
        return data

    def getClient(self, clientID):
        """gets a list of all the clients in the realm and returns only the
        client that matches the clientID provided
        """
        clients = self.getClients()
        client = None
        for client in clients:
            if client['clientId'].lower() == clientID.lower():
                break
        return client

    def addRoleToUser(self, userid, forestClientId):
        """This is the role mapping exercise...

        /auth/admin/realms/$REALM/users/$USERID/role-mappings/clients/$CLIENTID
        USERID - comes from user['id']

        assumes that the forestclientid and the userid have been
        validated then does the role mapping

        https://$KC_URL/auth/admin/realms/$REALM/users/$userid/role-mappings/clients/$fom_client_id

        1. get user id
        1. get client id
        1. get role
        """
        users = self.getAllUsers()
        matchUsers = []
        for user in users:
            if user['username'] == userid:
                matchUsers.append(user)

        # TODO: make sure only one user
        LOGGER.debug(f"users length {len(matchUsers)}")

        roles = self.getFOMRoles(forestClientId)
        LOGGER.debug(f"roles length {len(roles)}")
        LOGGER.debug(f"role length {roles}")

        clientid = self.getFomClientId()

        Url = f"{constants.KC_HOST}/auth/admin/realms/{constants.KC_REALM}/users/{matchUsers[0]['id']}/role-mappings/clients/{clientid}"  # noqa
        headers = {
            "Authorization": "Bearer " + self.access_token,
            'Content-type': 'application/json',
            'Accept': 'application/json'}

        response = requests.post(url=Url,
                                 headers=headers,
                                 json=roles)
        response.raise_for_status()
