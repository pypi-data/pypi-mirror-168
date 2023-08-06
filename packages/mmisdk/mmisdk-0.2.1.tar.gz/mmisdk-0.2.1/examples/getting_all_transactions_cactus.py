from mmisdk import CustodianFactory

factory = CustodianFactory()
custodian = factory.create_for("cactus-dev", "YOUR-REFRESH-TOKEN-CACTUS-DEV")
transactions = custodian.get_transactions(42)

print(transactions)
# [
#     Transaction(id='VURKJPZ2JVD888888000277', type='1', from_='0xA7f5D02E141c5DF8A987833E01E4f0922A91cF29', to=None, value=None, gas='180549', gasPrice='1000000007', maxPriorityFeePerGas='1000000008', maxFeePerGas='1400000012', nonce='0', data=None, hash='0x27a8aa70a501c20c7614aac084add4482482b51447804ff23275b1fb21e63927', status=TransactionStatus(finished=True, submitted=True, signed=True, success=False, displayText='Completed', reason='Unknown')),
#     Transaction(id='VHV3LIBLVND888888000431', type='1', from_='0xA7f5D02E141c5DF8A987833E01E4f0922A91cF29', to=None, value=None, gas='1500000', gasPrice='1000000008', maxPriorityFeePerGas='1000000000', maxFeePerGas='3500000012', nonce='4', data=None, hash='0xc062e8e89fa6447b59fc981fa6be352d012bd8bf92bb6833626bcb34c89ce455', status=TransactionStatus(finished=True, submitted=True, signed=True, success=False, displayText='Completed', reason='Unknown')),
#     Transaction(id='HJRW4ZQNRHD888888000441', type='1', from_='0xA7f5D02E141c5DF8A987833E01E4f0922A91cF29', to=None, value=None, gas='201060', gasPrice='1000000008', maxPriorityFeePerGas='1000000000', maxFeePerGas='3500000012', nonce='5', data=None, hash='0xf706b11023c6a443d6b3fffb350aea88909e1bccafa836addb0081b99052fa91', status=TransactionStatus(finished=True, submitted=True, signed=True, success=False, displayText='Completed', reason='Unknown')),
#     ...
# ]
