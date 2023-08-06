import requests

from mmisdk.adapters.cactus_adapter import CactusAdapter
from mmisdk.adapters.qredo_adapter import QredoAdapter
from mmisdk.cactus.cactus_client import CactusClient
from mmisdk.common.custodian import Custodian
from mmisdk.qredo.qredo_client import QredoClient

MMI_CONFIGURATION_API = "https://mmi-configuration-api.codefi.network/v1/configuration/default"

CUSTODIAN_CONFIGS = [
    {
        "name": "qredo",
        "apiBaseUrl": "https://api.qredo.network",
        "client": QredoClient,
        "adapter": QredoAdapter
    },
    {
        "name": "qredo-dev",
        "apiBaseUrl": "https://7ba211-api.qredo.net",
        "client": QredoClient,
        "adapter": QredoAdapter
    },
    {
        "name": "cactus",
        "apiBaseUrl": "https://api.mycactus.com/custody/v1/mmi-api",
        "client": CactusClient,
        "adapter": CactusAdapter
    },
    {
        "name": "cactus-dev",
        "apiBaseUrl": "https://api.mycactus.dev/custody/v1/mmi-api",
        "client": CactusClient,
        "adapter": CactusAdapter
    },
]


class CustodianFactory:
    """Utility class to instantiate custodians."""

    def __init__(self) -> None:
        try:
            response = requests.get(MMI_CONFIGURATION_API, timeout=1)
            custodians_config = response.json()["custodians"]
        except TimeoutError:
            print('The request timed out')
        else:
            # self.custodians_config = custodians_config  # TODO Restore this
            self.custodians_config = CUSTODIAN_CONFIGS

    def get_supported_custodians(self):
        """Lists the names of custodians supported by the library. Use this name in the method "create_for" to instantiate a custodian object.

        Returns:
            The names of supported custodians, as a list of strings
        """
        return list(map(lambda config: config["name"], self.custodians_config))

    def create_for(self, custodian_name, refresh_token) -> Custodian:
        """Creates an custodian instance for the passed custodian name.

        Args:
            custodian_name: The custodian name. Call the method "get_supported_custodians" to check the avaialble values.
            refresh_token: A refresh, provided to you by the custodian.

        Returns:
            The custodian instance.
        """
        configs_with_name = list(filter(
            lambda config: config["name"] == custodian_name, self.custodians_config))

        assert len(
            configs_with_name) > 0, f"Could not find a custodian with name {custodian_name}"
        assert len(
            configs_with_name) < 2, f"Found multiple custodians with name {custodian_name}"

        config = configs_with_name[0]

        # Instantiate the client
        client = config["client"](config["apiBaseUrl"], refresh_token)

        # Adapt the client into the class Custodian
        return config["adapter"](client)
