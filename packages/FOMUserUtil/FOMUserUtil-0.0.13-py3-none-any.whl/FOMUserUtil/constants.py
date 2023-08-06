import os
import dotenv
import sys
import logging

LOGGER = logging.getLogger(__name__)

#envFiles = ['.env-prd', '.env-tst', '.env-dev']


envFile = '.env-dev'


# populate the env vars from an .env file if it exists
envPath = os.path.join(os.path.dirname(__file__), '..', '..', envFile)
localEnvPath = os.path.join(os.getcwd(), '.env')
LOGGER.debug(f"envPath: {envPath}")
if os.path.exists(envPath):
    LOGGER.debug(f"loading dot env {envPath}...")
    dotenv.load_dotenv(envPath)

elif os.path.exists(localEnvPath):
    LOGGER.debug(f"loading dot env {localEnvPath}...")
    dotenv.load_dotenv(localEnvPath)

# env vars that should be populated for script to run
ENV_VARS = ['KC_HOST', 'KC_CLIENTID', 'KC_REALM', 'KC_SECRET',
            'KC_FOM_CLIENTID']
# KC_SA_CLIENTID

module = sys.modules[__name__]

envsNotSet = []
for env in ENV_VARS:
    if env not in os.environ:
        envsNotSet.append(env)
    else:
        # transfer env vars to module properties
        setattr(module, env, os.environ[env])

if envsNotSet:
    msg = 'The script expects the following environment variables to ' + \
          f'be set {envsNotSet}'
    raise EnvironmentError(msg)

# default values for the references to the forest clients in the fom repo
FOREST_CLIENT_IN_GIT = \
    'https://raw.githubusercontent.com/bcgov/nr-fom/main/api/src/migrations/main/1616015261635-forestClient.js' + '||' + \
    'https://raw.githubusercontent.com/bcgov/nr-fom/main/api/src/migrations/main/1639180924469-forestClientTypesNonCNonI.js' # noqa


FOM_CLIENT_ID = 'fom'
