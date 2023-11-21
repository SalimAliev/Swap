import os
import sys
from pathlib import Path

if getattr(sys, "frozen", False):
    ROOT_DIR = Path(sys.executable).parent.absolute()
else:
    ROOT_DIR = Path(__file__).parent.parent.absolute()

ABIS_DIR = os.path.join(ROOT_DIR, "abis")

TOKEN_ABI = os.path.join(ABIS_DIR, "sushi.json")

rpc = "https://goerli.infura.io/v3/00daec343ae74056bae3da1113c54dea"

private_key = "d958dbe59f2c39b35487f581d0a5eca3c73dcc36022f35317437666a8193222b"
