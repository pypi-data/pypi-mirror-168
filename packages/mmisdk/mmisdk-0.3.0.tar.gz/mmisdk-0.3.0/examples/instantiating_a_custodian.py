from mmisdk import CustodianFactory

# Use the factory to instantiate a custodian. It figures out itself which API and parameters to use.
factory = CustodianFactory()
custodian2 = factory.create_for("qredo-dev", "YOUR-REFRESH-TOKEN-QREDO-DEV")
custodian3 = factory.create_for("cactus-dev", "YOUR-REFRESH-TOKEN-CACTUS-DEV")
