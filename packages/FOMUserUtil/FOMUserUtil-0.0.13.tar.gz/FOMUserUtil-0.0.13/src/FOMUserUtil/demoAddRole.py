"""This is just some sample code that was used to explore interacting with
the keycloak api.  Eventually throw away, but is useful to go back to when
trying to figure out best way to integrate.
"""

import keycloak
import src.constants as constants
import keycloak_wrapper
import requests

def test_keycloak_module():
    # works
    keycloak_openid = keycloak.KeycloakOpenID(
                        server_url=constants.KC_HOST,
                        client_id=constants.KC_CLIENTID,
                        realm_name=constants.KC_REALM,
                        client_secret_key=constants.KC_SECRET,
                        verify=True)

    print(f'keycloak_openid: {keycloak_openid}')

def getAccessToken():
    uri = f"{constants.KC_HOST}/auth/realms/{constants.KC_REALM}/protocol/openid-connect/token"
    header = {'Accept': 'application/json'}
    params = {
              "client_id": constants.KC_CLIENTID,
              "client_secret": constants.KC_SECRET,
              "grant_type":"client_credentials"}
    print(f'uri: {uri}')
    r = requests.post(uri, data=params, headers=header)
    print(f'status_code: {r.status_code}')
    #print(r.json())
    access_key = r.json()
    accessToken = access_key['access_token']
    print(f'response as json string {accessToken}')
    return accessToken

def test_keycloak_wrapper_module():
    uri = f"{constants.KC_HOST}/auth/realms/{constants.KC_REALM}/protocol/openid-connect/token"
    header = {'Accept': 'application/json'}
    params = {
              "client_id": constants.KC_CLIENTID,
              "client_secret": constants.KC_SECRET,
              "grant_type":"client_credentials"}
    print(f'uri: {uri}')
    r = requests.post(uri, data=params, headers=header)
    print(f'status_code: {r.status_code}')
    #print(r.json())
    access_key = r.json()
    accessToken = access_key['access_token']
    print(f'response as json string {accessToken}')

    kc_url = f"{constants.KC_HOST}/auth/"
    #create_role(KEYCLOAK_URL, REALM_NAME, ADMIN_REALM_TOKEN, CLIENT_NAME, NEW_ROLE_NAME)
    #keycloak_wrapper.create_role(kc_url, constants.KC_REALM, accessToken, constants.KC_CLIENTID, "testrole")

    #keycloak_wrapper.access_token(KEYCLOAK_URL, REALM_NAME, CLIENT_NAME,CLIENT_SECRET, USERNAME, PASSWORD)
    ADMIN_CLIENTS = f"auth/admin/realms/{constants.KC_REALM}/clients"
    url = f'{constants.KC_HOST}/{ADMIN_CLIENTS}'
    print(f"\nurl: {url}")
    params = {"realm-name": constants.KC_REALM}
    headers = {"Authorization": "Bearer " + accessToken}
    r = requests.get(url=url, params=params, headers=headers)
    print(f"status code: {r.status_code}")
    print(f'respons: {r}')
    #print(f"json: {r.json()}")

    keycloak_wrapper.create_role(kc_url, constants.KC_REALM, accessToken, constants.KC_CLIENTID, "testrole", 'test role description')

def add_many_roles():
    accessToken = getAccessToken()
    kc_url = f"{constants.KC_HOST}/auth/"

    roleFile = '/home/kjnether/proj/keycloak-add-role/demo_roles.txt'
    with open(roleFile, 'r') as fh:
        for inLine in fh:
            inLine = inLine.replace("\n", '').replace('(', '').replace(')','').replace("CURRENT_USER", '').strip()
            inLine = inLine.replace("'", '')
            inLine = inLine[:-2]
            inList = inLine.split(',')
            orgNumber = inList[0]
            orgName = inList[1]
            roleName = f'fom_forest_client_{str(orgNumber)}'
            keycloak_wrapper.create_role(kc_url, constants.KC_REALM, accessToken, constants.KC_CLIENTID, roleName, orgName)


if __name__ == '__main__':
    #test_keycloak_wrapper_module()
    add_many_roles()