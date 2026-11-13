"""Check patch findings against a remediation SLA (default: critical within 48 hours)."""
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

SLA_HOURS = {"critical": 48, "high": 168, "medium": 720}


@dataclass
class Result:
    cve: str
    host: str
    severity: str
    status: str  # "ok", "open", "breached", "late"
    hours: float


def parse(ts):
    d = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    return d if d.tzinfo else d.replace(tzinfo=timezone.utc)


def check(findings, now, sla_hours=None):
    """Each finding: cve, host, severity, detected_at, patched_at (null while open).

    ok: patched inside the SLA. late: patched after it. open: not patched, still inside it.
    breached: not patched and past it. Severities with no SLA are skipped.
    """
    sla = sla_hours or SLA_HOURS
    out = []
    for f in findings:
        limit = sla.get(f["severity"].lower())
        if limit is None:
            continue
        start = parse(f["detected_at"])
        end = parse(f["patched_at"]) if f.get("patched_at") else None
        elapsed = ((end or now) - start) / timedelta(hours=1)
        if end:
            status = "ok" if elapsed <= limit else "late"
        else:
            status = "open" if elapsed <= limit else "breached"
        out.append(Result(f["cve"], f["host"], f["severity"].lower(), status, round(elapsed, 1)))
    return out


def main(argv):
    if len(argv) != 2:
        sys.exit("usage: python -m patchsla.sla findings.json")
    with open(argv[1]) as fh:
        results = check(json.load(fh), datetime.now(timezone.utc))
    for r in results:
        print(f"{r.status:9} {r.severity:9} {r.cve:16} {r.host:14} {r.hours}h")
    bad = [r for r in results if r.status in ("breached", "late")]
    print(f"{len(bad)} of {len(results)} outside SLA")
    return 1 if any(r.status == "breached" for r in results) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
