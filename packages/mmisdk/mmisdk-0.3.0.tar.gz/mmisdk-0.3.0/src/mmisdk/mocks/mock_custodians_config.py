MOCK_CUSTODIANS_CONFIG = {
    "portfolio": {
        "enabled": True,
        "url": "https://metamask-institutional.io/",
        "cookieSetUrls": [
            "https://mmi-portfolio-poc.codefi.network/api/update-dashboard-cookie",
            "https://metamask-institutional.io/api/update-dashboard-cookie"
        ]
    },
    "custodians": [
        {
            "refreshTokenUrl": None,
            "name": "cactus",
            "displayName": None,
            "enabled": None,
            "mmiApiUrl": "https://mmi.codefi.network/v1",
            "apiBaseUrl": None,
            "iconUrl": None,
            "isNoteToTraderSupported": False
        },
        {
            "refreshTokenUrl": None,
            "name": "qredo",
            "displayName": None,
            "enabled": None,
            "mmiApiUrl": "https://mmi.codefi.network/v1",
            "apiBaseUrl": None,
            "iconUrl": None,
            "isNoteToTraderSupported": True
        },
    ]
}
