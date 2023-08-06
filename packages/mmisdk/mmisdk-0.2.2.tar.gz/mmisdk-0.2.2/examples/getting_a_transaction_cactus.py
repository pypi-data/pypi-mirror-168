from mmisdk import CustodianFactory

factory = CustodianFactory()
custodian = factory.create_for("cactus-dev", "YOUR-REFRESH-TOKEN-CACTUS-DEV")
transaction = custodian.get_transaction("JTQMNHSSTID888888000792", 42)

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
