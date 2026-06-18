#!/usr/bin/env bash
set -u

check_tool() {
  name="$1"
  if command -v "$name" >/dev/null 2>&1; then
    printf "%-28s %s\n" "$name" "$(command -v "$name")"
  else
    printf "%-28s %s\n" "$name" "missing"
  fi
}

echo "Core build and scripting"
for tool in cc gcc clang make cmake ninja python3 node java javac go rustc cargo; do
  check_tool "$tool"
done

echo
echo "POSIX, tracing, and real-time Linux"
for tool in taskset chrt perf trace-cmd ftrace dtrace ltrace strace cyclictest stress-ng; do
  check_tool "$tool"
done

echo
echo "MPI and distributed execution"
for tool in mpicc mpicxx mpirun mpiexec ompi_info; do
  check_tool "$tool"
done

echo
echo "Containers and orchestration"
for tool in docker podman nerdctl kubectl helm kind k3d; do
  check_tool "$tool"
done

echo
echo "Bare-metal and hardware"
for tool in qemu-system-x86_64 qemu-system-arm openocd minicom picocom stty screen; do
  check_tool "$tool"
done

echo
echo "FPGA, silicon, and Wasm/edge"
for tool in verilator yosys nextpnr iverilog gtkwave wasmtime wasmedge wasm-tools; do
  check_tool "$tool"
done
