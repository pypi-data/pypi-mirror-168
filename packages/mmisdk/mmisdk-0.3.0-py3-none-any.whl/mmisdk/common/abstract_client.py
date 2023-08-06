

class AbstractClient:
    """Abstract class that each custodian client inherits from."""

    def __init__(self, api_url, token):
        """
        Args:
            api_url: The custodian's API base URL.
            token: A token provided to you by the custodian. Depending on the custodian, it could be either a refresh token
            or an access token. Regardless of which, the library takes care of the authentication flow.
        """
        self.api_url = api_url
        self.token = token
