import requests
from mmisdk.cactus.cactus import Cactus

from mmisdk.common.custodian import Custodian
from mmisdk.qredo.qredo import Qredo

MMI_CONFIGURATION_API = "https://mmi-configuration-api.codefi.network/v1/configuration/default"

CUSTODIAN_CONFIGS = [
    {
        "name": "qredo",
        "apiBaseUrl": "https://api.qredo.network",
        "class": Qredo,
    },
    {
        "name": "qredo-dev",
        "apiBaseUrl": "https://7ba211-api.qredo.net",
        "class": Qredo,
    },
    {
        "name": "cactus",
        "apiBaseUrl": "https://api.mycactus.com/custody/v1/mmi-api",
        "class": Cactus,
    },
    {
        "name": "cactus-dev",
        "apiBaseUrl": "https://api.mycactus.dev/custody/v1/mmi-api",
        "class": Cactus,
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

        return config["class"](config["apiBaseUrl"], refresh_token)
