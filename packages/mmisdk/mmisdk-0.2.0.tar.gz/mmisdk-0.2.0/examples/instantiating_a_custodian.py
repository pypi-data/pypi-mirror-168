from mmisdk import CustodianFactory
from mmisdk import Qredo
from mmisdk import Cactus

# You can instantiate a custodian directly like so:
custodian0 = Qredo("https://7ba211-api.qredo.net", "YOUR-REFRESH-TOKEN-QREDO-DEV")
custodian1 = Cactus("https://api.mycactus.dev/custody/v1/mmi-api", "YOUR-REFRESH-TOKEN-CACTUS-DEV")

# However it's simpler to rely on the factory as it figures out itself which api URL to use
factory = CustodianFactory()
custodian2 = factory.create_for("qredo-dev", "YOUR-REFRESH-TOKEN-QREDO-DEV")
custodian3 = factory.create_for("cactus-dev", "YOUR-REFRESH-TOKEN-CACTUS-DEV")
