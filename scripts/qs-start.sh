#!/usr/bin/bash
set -e
set -o xtrace

pip install -e /home/xf07id1/collection_packages/haxpes

start-re-manager --zmq-publish-console ON --use-ipython-kernel ON --ipython-kernel-ip auto --startup-profile collection
