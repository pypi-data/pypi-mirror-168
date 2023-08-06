from mmisdk import CustodianFactory

# Instantiate the factory
factory = CustodianFactory()

supported_custodians = factory.get_supported_custodians()
print(supported_custodians)

# [ "qredo", "qredo-dev", "cactus", ... ]
