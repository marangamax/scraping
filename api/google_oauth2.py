"""extracted from sample_tools.py
provided in the src checkout of
the google api python library
"""
import httplib2
import os

from apiclient import discovery

#extracted from sample_tools.py

#provided in the src checkout of
#the google api python library

import httplib2
import os
import json

from apiclient import discovery
from oauth2client import client
from oauth2client import file
from oauth2client.tools import *

here = os.path.dirname(os.path.realpath(__file__))

_CLIENT_SECRETS_MESSAGE = """WARNING: Please configure OAuth 2.0
To make this sample run you will need to populate the client_secrets.json file
found at:
   %s
with information from the APIs Console <https://code.google.com/apis/console>.
"""


def message_if_missing(filename):
    """Helpful message to display if the CLIENT_SECRETS file is missing."""

    return _CLIENT_SECRETS_MESSAGE % filename


def authenticate(name, version, scope=None):
    """getting data to get into it
    authenticate('analytics', 'v3', 'https://www.googleapis.com/auth/analytics.readonly').__class__
    <class 'apiclient.discovery.Resource'>
    data = authenticate('adwords', 'v201302', 'https://adwords.google.com/api/adwords/')
    "access_token" in data
    True
    "client_id" in data
    True
    "client_secret" in data
    True
    "refresh_token" in data
    True
    "token_expiry" in data
    True
    "token_uri" in data
    True
    "user_agent" in data
    True
    """

    if scope is None:
        scope = 'https://www.googleapis.com/auth/' + name

    client_secrets = os.path.join(here, 'analytics.json')
    flow = client.flow_from_clientsecrets(client_secrets, scope=scope,
                                          message=message_if_missing(client_secrets))

    def __auth(storage, flow):
        credentials = storage.get()
        if credentials is None or credentials.invalid:
            credentials = run(flow, storage)
        return credentials.authorize(http=httplib2.Http())


    storage = file.Storage(os.path.join(here, 'analytics.dat'))
    http = __auth(storage, flow)

    if name == "adwords":
        f = open(storage._filename)
        data = json.load(f)
        f.close()
        return data
    # Construct a service object via the discovery service.
    return discovery.build(name, version, http=http)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
