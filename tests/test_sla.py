from datetime import datetime, timezone

from patchsla.sla import check

NOW = datetime(2026, 11, 13, 12, 0, tzinfo=timezone.utc)


def one(**kw):
    f = {"cve": "CVE-1", "host": "pcs-01", "severity": "critical",
         "detected_at": "2026-11-12T12:00:00Z", "patched_at": None}
    f.update(kw)
    return check([f], NOW)[0]


def test_open_inside_window():
    assert one().status == "open"  # 24h in


def test_open_past_window_is_a_breach():
    assert one(detected_at="2026-11-10T11:00:00Z").status == "breached"  # 49h in


def test_exactly_48h_is_still_inside():
    assert one(detected_at="2026-11-11T12:00:00Z").status == "open"


def test_patched_inside_and_after_window():
    assert one(patched_at="2026-11-13T10:00:00Z").status == "ok"
    assert one(detected_at="2026-11-01T00:00:00Z", patched_at="2026-11-05T00:00:00Z").status == "late"


def test_severity_without_an_sla_is_skipped():
    assert check([{"cve": "x", "host": "h", "severity": "low", "detected_at": "2026-01-01T00:00:00Z"}], NOW) == []
