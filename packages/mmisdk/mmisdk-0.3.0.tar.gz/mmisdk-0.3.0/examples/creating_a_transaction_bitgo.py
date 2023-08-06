from mmisdk import CustodianFactory

# Instantiate the factory
factory = CustodianFactory()

# Create the custodian, using the factory
custodian = factory.create_for("bitgo-test", "YOUR-TOKEN-BITGO-TEST")

# Build tx details
tx_params = {
    "from_": "0xeddb59689e4ec3931b8d42d615c0d4a7a3a208e7",
    "to": "0xb22505ee2aac7d52d4a218f5877cdbae3bbeec75",
    "value": "999000000",  # in Wei
    "gas": "123456",
    "gasPrice": "900000",
    "data": "0x00000"
}
bitgo_extra_params = {
    "walletId": "614a2a61df1332000686516a6dbee90a",
}

# Create the tx from details and send it to the custodian
transaction = custodian.create_transaction(tx_params, bitgo_extra_params)

print(type(transaction))
# <class 'mmisdk.common.transaction.Transaction'>

print(transaction)
# id='84236067-9962-49af-a2df-e635847289bd'
# type='1'
# from_='0xeddb59689e4ec3931b8d42d615c0d4a7a3a208e7'
# to='0xb22505ee2aac7d52d4a218f5877cdbae3bbeec75'
# value='999000000'
# gas='123456'
# gasPrice=None
# maxPriorityFeePerGas=None
# maxFeePerGas=None
# nonce=None
# data='0x00000'
# hash=None
# status=TransactionStatus(finished=False, submitted=False, signed=False, success=False, displayText='Created', reason='Unknown')
