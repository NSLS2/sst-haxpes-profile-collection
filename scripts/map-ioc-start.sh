#!/usr/bin/bash
# Start the beam map IOC. With NBS_MAP_IOC_SRC set (dev mode), install
# nbs-sim from that checkout first. The checkout may be a git worktree whose
# git dir isn't mounted, so give hatch-vcs a version instead of asking git.
set -e
set -o xtrace

export EPICS_CA_AUTO_ADDR_LIST=no
export EPICS_CAS_AUTO_BEACON_ADDR_LIST=no
export EPICS_CAS_BEACON_ADDR_LIST=10.66.51.255
export EPICS_CA_ADDR_LIST=10.66.51.255

# if [[ -n "${NBS_MAP_IOC_SRC:-}" ]]; then
#     SETUPTOOLS_SCM_PRETEND_VERSION=0.2.99 pip install --no-deps -e "$NBS_MAP_IOC_SRC"
# fi
# if ! command -v nbs-map-ioc > /dev/null; then
#     echo "nbs-map-ioc is not installed in this image; start map-ioc with --dev" \
#          "(see README, Beam map IOC). Exiting."
#     exit 0
# fi
nbs-map-ioc --map startup/beam_map.toml --list-pvs
