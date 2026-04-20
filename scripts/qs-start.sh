#!/usr/bin/bash
set -e
set -o xtrace

pip install -e /home/xf07id1/collection_packages/haxpes
if [ -f /nsls2/data/sst/legacy/HAXPES/PeakSDK/peak_sdk-1.5.27-py3-none-any.whl ]; then
    pip install /nsls2/data/sst/legacy/HAXPES/PeakSDK/peak_sdk-1.5.27-py3-none-any.whl
fi

start-re-manager --redis-addr ${QS_REDIS_ADDR:-localhost}:6379 --zmq-publish-console ON --use-ipython-kernel ON --ipython-kernel-ip auto --startup-profile collection
