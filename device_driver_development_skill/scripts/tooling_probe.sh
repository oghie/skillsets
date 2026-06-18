#!/usr/bin/env sh
set -eu

have() {
	if command -v "$1" >/dev/null 2>&1; then
		printf 'ok      %s -> %s\n' "$1" "$(command -v "$1")"
	else
		printf 'missing %s\n' "$1"
	fi
}

printf '%s\n' "Driver tooling probe"
printf 'kernel  %s\n' "$(uname -r)"

if [ -d "/lib/modules/$(uname -r)/build" ]; then
	printf 'ok      kernel build dir -> %s\n' "/lib/modules/$(uname -r)/build"
else
	printf 'missing kernel build dir -> /lib/modules/%s/build\n' "$(uname -r)"
	printf 'hint    Debian/Ubuntu: sudo apt install build-essential linux-headers-$(uname -r)\n'
fi

for tool in make cc gcc clang sparse smatch spatch bpftrace qemu-system-x86_64 gdb syz-manager syz-execprog; do
	have "$tool"
done
