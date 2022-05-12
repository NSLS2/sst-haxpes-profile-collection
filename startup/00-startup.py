import sys
from pathlib import Path

paths = [
    path
    for path in Path(
        "/nsls2/data/sst1/ucal/shared/config/bluesky/collection_packages"
    ).glob("*")
    if path.is_dir()
]
for path in paths:
    sys.path.append(str(path))

import nslsii
import haxpes
# from haxpes.startup import *

nslsii.configure_base(get_ipython().user_ns, "haxpes", publish_documents_with_kafka=True)
