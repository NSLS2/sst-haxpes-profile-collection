import nslsii
import haxpes
from haxpes.startup import *

nslsii.configure_base(get_ipython().user_ns, "haxpes", publish_documents_with_kafka=True)
