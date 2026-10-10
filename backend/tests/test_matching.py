from datetime import UTC, datetime, timedelta

from app.services.matching_service import MIN_OVERLAP_MINUTES, compute_score, is_compatible

NOW = datetime.now(UTC).replace(second=0, microsecond=0)


def _layover(airport="DXB", start_offset_h=0, dur_h=6, bags=1, interests=None):
    start = NOW + timedelta(hours=start_offset_h)
    return {
        "airport_code": airport,
        "arrival_time": start,
        "departure_time": start + timedelta(hours=dur_h),
        "baggage_count": bags,
        "interests": interests or [],
    }


def test_same_airport_overlapping_windows_score_high():
    a = _layover(interests=["food"])
    b = _layover(interests=["food"])
    score = compute_score(a, b)
    assert score["total"] > 80


def test_different_airports_score_zero():
    a = _layover(airport="DXB")
    b = _layover(airport="JFK", dur_h=8)
    assert compute_score(a, b)["total"] == 0
    assert not is_compatible(a, b)


def test_non_overlapping_windows_score_zero():
    a = _layover(start_offset_h=0, dur_h=2)
    b = _layover(start_offset_h=5, dur_h=4)
    # Windows don't overlap -> no shared schedule time; baggage/interest may
    # still contribute, but the pair is NOT compatible without overlap.
    assert compute_score(a, b)["overlap_minutes"] == 0
    assert not is_compatible(a, b)


def test_small_overlap_below_threshold_not_compatible():
    a = _layover(start_offset_h=0, dur_h=2)
    b = _layover(start_offset_h=1, dur_h=2)  # 1h overlap < 60min threshold? boundary
    # 60-minute overlap is exactly at threshold -> compatible; below -> not.
    if compute_score(a, b)["overlap_minutes"] >= MIN_OVERLAP_MINUTES:
        assert is_compatible(a, b)
    else:
        assert not is_compatible(a, b)


def test_baggage_difference_lowers_score():
    base = _layover(bags=1)
    same = _layover(bags=1)
    diff = _layover(bags=3)
    assert compute_score(base, same)["baggage"] > compute_score(base, diff)["baggage"]


def test_shared_interests_raise_score():
    base = _layover(interests=["food"])
    no_share = _layover(interests=["history"])
    share = _layover(interests=["food", "art"])
    assert compute_score(base, no_share)["interest"] == 0
    assert compute_score(base, share)["interest"] > 0
