#!/usr/bin/env sh
set -eu

usage() {
	printf '%s\n' "usage: $0 <module-dir> [kernel-build-dir]"
	printf '%s\n' "env: ARCH=... CROSS_COMPILE=... EXTRA_MAKE_ARGS='...'"
}

if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
	usage
	exit 0
fi

if [ $# -lt 1 ] || [ $# -gt 2 ]; then
	usage >&2
	exit 2
fi

MODULE_DIR=$1
KDIR=${2:-/lib/modules/$(uname -r)/build}

if [ ! -d "$MODULE_DIR" ]; then
	printf '%s\n' "module directory not found: $MODULE_DIR" >&2
	exit 1
fi

if [ ! -d "$KDIR" ]; then
	printf '%s\n' "kernel build directory not found: $KDIR" >&2
	exit 1
fi

MAKE_ARGS="W=1"
if [ "${SPARSE:-0}" = "1" ]; then
	MAKE_ARGS="$MAKE_ARGS C=1"
fi

printf '%s\n' "Building external module:"
printf '  %s\n' "module: $MODULE_DIR"
printf '  %s\n' "kernel: $KDIR"
make -C "$KDIR" M="$(cd "$MODULE_DIR" && pwd)" $MAKE_ARGS ${EXTRA_MAKE_ARGS:-} modules
