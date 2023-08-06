from mmisdk import CustodianFactory

factory = CustodianFactory()
custodian = factory.create_for("cactus-dev", "YOUR-REFRESH-TOKEN-CACTUS-DEV")
transaction = custodian.get_transaction("5CM05NCLMRD888888000800", 5)

print(type(transaction))
# <class 'mmisdk.common.transaction.Transaction'>

print(transaction)
# id='5CM05NCLMRD888888000800'
# type='1'
# from_='0xFA42B2eCf59abD6d6BD4BF07021D870E2FC0eF20'
# to=None
# value=None
# gas='133997'
# gasPrice='2151'
# maxPriorityFeePerGas=None
# maxFeePerGas=None
# nonce=''
# data=None
# hash=None
# status=TransactionStatus(finished=False, submitted=False, signed=False, success=False, displayText='Created', reason='Unknown')
