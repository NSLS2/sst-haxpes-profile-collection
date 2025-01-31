import sys
from pathlib import Path
"""
paths = [
    path
    for path in Path(
        "/nsls2/data/sst/haxpes/shared/config/bluesky/collection_packages"
    ).glob("*")
    if path.is_dir()
]
for path in paths:
    sys.path.append(str(path))
"""
import atexit
import nslsii
import haxpes
import os
import redis
import time as ttime
from databroker import Broker
#from haxpes.startup import *
from nbs_bl.configuration import load_and_configure_everything
from nslsii import configure_kafka_publisher
from redis_json_dict import RedisJSONDict
from tiled.client import from_profile

from bluesky.plan_stubs import mv as _mv, mvr as _mvr

load_and_configure_everything()

class TiledInserter:
    def insert(self, name, doc):
        ATTEMPTS = 20
        error = None
        for attempt in range(ATTEMPTS):
            try:
                tiled_writing_client.post_document(name, doc)
            except Exception as exc:
                print("Document saving failure:", repr(exc))
                error = exc
            else:
                break
            ttime.sleep(2)
        else:
            # Out of attempts
            raise error

print("making writing client")

tiled_writing_client = from_profile(
    "nsls2", api_key=os.environ["TILED_BLUESKY_WRITING_API_KEY_HAXPES"]
)["haxpes"]["raw"]
tiled_inserter = TiledInserter()
#c = tiled_reading_client = from_profile("nsls2")["haxpes"]["raw"]
#db = Broker(c)

print("Before nslsii.configure_base")

# nslsii.configure_base(get_ipython().user_ns, "haxpes", publish_documents_with_kafka=True)
nslsii.configure_base(
    get_ipython().user_ns, tiled_inserter, publish_documents_with_kafka=False
)

configure_kafka_publisher(RE, beamline_name="haxpes")

#RE.md = RedisJSONDict(redis.Redis("info.sst.nsls2.bnl.gov"), prefix="haxpes-")

print("After configure_base")

#from haxpes.xpswriter import catalog as xpswriter_catalog
#from haxpes.xaswriter import catalog as xaswriter_catalog

print("Got to end of 00-startup")
"""
def whoami():
    try:
        print(f"\nLogged in to Tiled as: {c.context.whoami()['identities'][0]['id']}\n")
    except TypeError as e:
        print("Not authenticated with Tiled! Please login...")


whoami()

def logout():
    c.logout(clear_default=True)


def login():
    haxpes_username = input("Please enter your username: ")
    haxpes_unauthenticated = (
        c.context.api_key is None and c.context.http_client.auth is None
    )
    if not haxpes_unauthenticated:
        haxpes_current_user = c.context.whoami()["identities"][0]["id"]
        if haxpes_username != haxpes_current_user:
            logout()

    c.login(username=haxpes_username)

    # temporarily manage imported clients from WIP helpers
    imports_with_clients = [
        "haxpes.xpswriter",
        "haxpes.xaswriter",
    ]
    for module in imports_with_clients:
        if module in sys.modules:
            try:
                imported_clients = [
                    xpswriter_catalog,
                    xaswriter_catalog,
                ]
                for client in imported_clients:
                    client.login(username=haxpes_username)
            except NameError:
                print(
                    f"Client from '{module}' was not imported as expected - could not login"
                )
    # above is a temporary code block
    print(f"Logged in to Tiled as {haxpes_username}!")


# separate logout function to feed to atexit, bypassing
# problems that ipython early deallocation would cause
def logout_on_exit(c=c):
    c.logout(clear_default=True)


# need to pass kwargs to deal with ipython early deallocation
# therefore, cannot user the atexit.register decorator
atexit.register(logout_on_exit, c=c)
"""

# A bug in bluesky 1.13 causes QueueServer validation to fail
# for mv and mvr due to an unserializable type annotation (NamedMovable)
# Redefine without type annotation to fix temporarily
def mv(*args, group=None, **kwargs):
    yield from _mv(*args, group=group, **kwargs)

def mvr(*args, group=None, **kwargs):
    yield from _mvr(*args, group=group, **kwargs)
