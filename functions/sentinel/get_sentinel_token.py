from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

def get_sentinel_token(client_id, client_secret):
    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)

    token = oauth.fetch_token(token_url='https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token',
                              client_secret=client_secret, include_client_id=True)

    return oauth
