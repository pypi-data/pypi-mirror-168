# MMI Custodian SDK

A Python library to create and submit EVM transactions to custodians connected with MetaMask Institutional.

## Installing

```sh
pip3 install mmisdk
```

## Getting started

```python
from mmisdk import CustodianFactory

factory = CustodianFactory()

# Instiate a Qredo client with a refresh token
custodian = factory.create_for(
    "qredo", "YOUR-REFRESH-TOKEN")
```

You can see a list of supported custodians and API URLs here
https://mmi-configuration-api.codefi.network/v1/configuration/default. Use the custodian's field `name` in the code below to instantiate a client for the right custodian.

| Custodian  | Supported | As of version | Factory name param |
| ---------- | --------- | ------------- | ------------------ |
| Qredo      | ✅        | 0.0.0         | `"qredo"`          |
| Qredo Dev  | ✅        | 0.0.0         | `"qredo-dev"`      |
| Cactus     | ✅        | 0.0.0         | `"cactus"`         |
| Cactus Dev | ✅        | 0.0.0         | `"cactus-dev"`     |
| All others | ❌        |               |                    |

## Creating a transaction

```python
tx_params = {
  "data" : "0x031E223FabC1Da031E223FabC1Da031E223FabC1Da031E223FabC1Da031E223FabC1Da",
  "from": "0xb2c77973279baaaf48c295145802695631d50c01",
  "to": "0x57f36031E223FabC1DaF93B401eD9F4F1Acc6904",
  "type": "0x2",
  "value": "0x1",
  "gas": "0x5208",
  "maxFeePerGas": "0x59682f0e",
  "maxPriorityFeePerGas": "0x59682f0e"
}

qredo_tx_details = {
  "chainId": "0x4",
  "originUrl": "https://www.example.com"
}

transaction = custodian.create_transaction(qredo_tx_details, tx_params)

print(transaction)

# {
#   "id": "ef8cb7af-1a00-4687-9f82-1f1c82fbef54",
#   "type": "0x2",
#   "from": "0xCD2a3d9F938E13CD947Ec05AbC7FE734Df8DD826",
#   "to": "0xB8c77482e45F1F44dE1745F52C74426C631bDD52",
#   "value": "0x0",
#   "gas": "0x5208",
#   "gasPrice": "0x4A817C800",
#   "nonce": "0x1",
#   "data": "0x",
#   "hash": "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
#   "status": {
#     "finished": true,
#     "submitted": true,
#     "signed": true,
#     "success": true,
#     "displayText": "Mined"
#   }
# }
```

## Getting a transaction

```python
from mmisdk import CustodianFactory

factory = CustodianFactory()
custodian0 = factory.create_for("cactus-dev", "YOUR-REFRESH-TOKEN-CACTUS")
response0 = custodian0.get_transaction("VURKJPZ2JVD888888000277", 42)
print(response0.json())

# {
#     "chain_id": "42",
#     "nonce": "",
#     "from": "0x14228088b52b245FfC932a9228624E08951f11af",
#     "signature": None,
#     "transactionStatus": "rejected",
#     "transactionHash": None,
#     "custodian_transactionId": "J6WVLRC0TMD888888000352",
#     "gasPrice": "2000000000",
#     "maxFeePerGas": "2000000000",
#     "maxPriorityFeePerGas": "2000000000",
#     "gasLimit": "161420"
# }
```

## Subscribing to transaction events

🚨 NOT IMPLEMENTED YET

```python
def log_event(event, *args, **kwargs):
    log.debug('%s %s %s', event, args, kwargs)

custodian.on('transaction-update', log_event)
```

## MVP Scope

-   Works with one custodian type (either Qredo or JSON-RPC)
-   Library published on pypi for python3 only

## Developer documentation

For instructions about development, testing, building and release, check the [developer documentation](https://gitlab.com/ConsenSys/codefi/products/mmi/mmi-sdk-py).
