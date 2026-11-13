#!/usr/bin/env bash
# Report whether this host looks ready for low-latency work. Exit 1 if anything is off.
set -u
fail=0
check() { if eval "$2"; then echo "ok   $1"; else echo "FAIL $1"; fail=1; fi; }

check "PREEMPT_RT kernel"    "uname -v | grep -q PREEMPT_RT"
check "isolcpus set"         "grep -q isolcpus /proc/cmdline"
check "performance governor" "! grep -qv performance /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor 2>/dev/null"
check "swap off"             "[ -z \"\$(swapon --show --noheadings 2>/dev/null)\" ]"
exit "$fail"
