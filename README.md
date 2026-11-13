# patch-sla-ansible

Security patching with Ansible that checks itself against a remediation window, for hosts that cannot be patched in the middle of a run (lab, control, and real-time systems).

- `patchsla/sla.py`: reads findings (detected and patched times) and reports which are open, breached, or late against an SLA. Critical is 48 hours. Exits 1 on a breach, so a pipeline can fail on it.
- `ansible/roles/patch`: security updates one host at a time, skips any host with a run in progress (a flag file), reboots only when allowed.
- `ansible/roles/rt_check`, `scripts/rt-check.sh`: assert a PREEMPT_RT kernel, `isolcpus`, and the realtime tuned profile.
- `ansible/playbooks/proxmox_vm.yml`: clone a VM from a template on a Proxmox VE cluster.
- `Containerfile`, `Jenkinsfile`: reproducible runner and a pipeline that runs tests, syntax checks, and the SLA report.
- `docs/NIST_MAPPING.md`: which control each output is evidence for.

```bash
python -m pytest -q tests
python -m patchsla.sla tests/findings.json
```

## Verified

- 5 pytest tests pass. The sample report exits 1 on the breached finding.
- All three playbooks pass `ansible-playbook --syntax-check`. `shellcheck` is clean.

## Not verified

- Nothing ran against real hosts, a Proxmox cluster, or a real-time kernel. The reboot path and `needs-restarting` handling are untested.
- The Containerfile and Jenkinsfile were not run.
