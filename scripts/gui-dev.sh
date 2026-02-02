#!/usr/bin/bash
set -e
set -o xtrace

pip install -e /home/xf07id1/collection_packages/nbs-bl
pip install -e /home/xf07id1/collection_packages/nbs-gui
pip install -e /home/xf07id1/collection_packages/sst_base
pip install git+https://github.com/cjtitus/bluesky-widgets@worker_weakref
# haxpes is always installed by gui-start
$(dirname "$0")/gui-start.sh
