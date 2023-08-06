from mmisdk import CustodianFactory

# Instantiate the factory
factory = CustodianFactory()

# Create the custodian, using the factory
custodian = factory.create_for("cactus-dev", "YOUR-REFRESH-TOKEN-CACTUS-DEV")

# Build tx details
tx_params = {
    "from": "0xFA42B2eCf59abD6d6BD4BF07021D870E2FC0eF20",
    "to": "0x7dc55e5C19c43FF6f027d0CeF656B2E1513916e6",
    "gasLimit": "133997",
    "value": "0.1",
    "gasPrice": "200000000000",
}
cactus_extra_params = {
    "chainId": 42,  # Kovan
    "note": "Some information"
}

# Create the tx from details and send it to the custodian
transaction = custodian.create_transaction(tx_params, cactus_extra_params)

print(type(transaction))
# <class 'mmisdk.common.transaction.Transaction'>

print(transaction)
# id='JTQMNHSSTID888888000792'
# type='1'
# from_='0xFA42B2eCf59abD6d6BD4BF07021D870E2FC0eF20'
# to=None
# value=None
# gas='133997'
# gasPrice='2774'
# maxPriorityFeePerGas=None
# maxFeePerGas=None
# nonce=''
# data=None
# hash=None
# status=TransactionStatus(finished=False, submitted=False, signed=False, success=False, displayText='Created', reason='Unknown')
