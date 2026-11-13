# NIST 800-53 mapping

What each piece produces as evidence. This is a mapping, not an ATO or a claim of compliance.

| Control | Evidence from this repo |
|---|---|
| SI-2 Flaw remediation | `patchsla` report: time from detection to patch, per host, against the 48 hour critical window |
| CM-3 Change control | `patch.yml` runs `serial: 1`, stops on the first failure, skips hosts with a run in progress |
| CM-6 Configuration settings | `rt_check` role and `scripts/rt-check.sh` assert kernel, CPU isolation, and tuned profile |
| CM-2 Baseline | Inventory and roles in git, reviewed through pull requests |
| AU-12 Audit generation | `/var/lib/patchsla.last` records the patch time on each host |
