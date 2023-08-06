

class AbstractClient:
    """Abstract class that each custodian client inherits from."""

    def __init__(self, api_url, refresh_token):
        self.api_url = api_url
        self.refresh_token = refresh_token
