"""
Chaos injection functions to simulate real-world data quality issues.
"""
import random
from datetime import datetime, timedelta
from typing import Any, Optional
from data_generators.config import CHAOS_CONFIG


def inject_null(value: Any, probability: Optional[float] = None) -> Any:
    """
    Randomly return None instead of the value.

    Args:
        value: The original value
        probability: Override default null probability

    Returns:
        None or the original value
    """
    prob = probability if probability is not None else CHAOS_CONFIG["null_probability"]
    return None if random.random() < prob else value


def inject_timestamp_drift(timestamp: datetime, drift_range: Optional[tuple] = None) -> datetime:
    """
    Add random drift to a timestamp.

    Args:
        timestamp: Original timestamp
        drift_range: (min_minutes, max_minutes) tuple

    Returns:
        Drifted timestamp
    """
    if drift_range is None:
        drift_range = CHAOS_CONFIG["timestamp_drift_range"]

    drift_minutes = random.randint(drift_range[0], drift_range[1])
    return timestamp + timedelta(minutes=drift_minutes)


def inject_product_name_variation(canonical_name: str) -> str:
    """
    Return a random variation of a product name.

    Args:
        canonical_name: The canonical product name

    Returns:
        A variation of the product name (or canonical if not found)
    """
    variations = CHAOS_CONFIG["product_name_variations"].get(canonical_name, [canonical_name])
    return random.choice(variations)


def inject_machine_id_variation(canonical_id: str) -> str:
    """
    Return a random variation of a machine ID.

    Args:
        canonical_id: The canonical machine ID

    Returns:
        A variation of the machine ID (or canonical if not found)
    """
    variations = CHAOS_CONFIG["machine_id_variations"].get(canonical_id, [canonical_id])
    return random.choice(variations)


def should_duplicate() -> bool:
    """
    Determine if a record should be duplicated.

    Returns:
        True if record should be duplicated
    """
    return random.random() < CHAOS_CONFIG["duplicate_probability"]


def should_arrive_late() -> tuple[bool, int]:
    """
    Determine if data should arrive late and by how many days.

    Returns:
        Tuple of (should_be_late, days_delayed)
    """
    if random.random() < CHAOS_CONFIG["late_arrival_probability"]:
        days = random.randint(*CHAOS_CONFIG["late_arrival_days"])
        return True, days
    return False, 0


def inject_timezone_chaos(timestamp: datetime, use_utc: bool = True) -> datetime:
    """
    Randomly convert timestamp to local time instead of UTC.

    Args:
        timestamp: Original timestamp (assumed to be UTC)
        use_utc: If True, sometimes convert to local time

    Returns:
        Timestamp (possibly in local time)
    """
    if use_utc and random.random() < CHAOS_CONFIG["timezone_chaos_probability"]:
        # Convert to MST (UTC-7)
        return timestamp - timedelta(hours=7)
    return timestamp


def calculate_defect_rate(base_rate: Optional[float] = None) -> float:
    """
    Calculate defect rate with random variance.

    Args:
        base_rate: Override default base defect rate

    Returns:
        Defect rate (between 0 and 1)
    """
    if base_rate is None:
        base_rate = CHAOS_CONFIG["base_defect_rate"]

    variance = CHAOS_CONFIG["defect_rate_variance"]
    rate = base_rate + random.uniform(-variance, variance)

    # Clamp between 0 and 1
    return max(0.0, min(1.0, rate))


def inject_typo(text: str, typo_probability: float = 0.05) -> str:
    """
    Randomly introduce a typo into text.

    Args:
        text: Original text
        typo_probability: Probability of introducing a typo

    Returns:
        Text with possible typo
    """
    if random.random() > typo_probability or len(text) < 3:
        return text

    # Simple typo: swap two adjacent characters
    pos = random.randint(0, len(text) - 2)
    chars = list(text)
    chars[pos], chars[pos + 1] = chars[pos + 1], chars[pos]
    return ''.join(chars)


def add_measurement_noise(value: float, noise_percent: float = 0.02) -> float:
    """
    Add random measurement noise to a numeric value.

    Args:
        value: Original value
        noise_percent: Noise as percentage of value (e.g., 0.02 = ±2%)

    Returns:
        Value with noise added
    """
    noise = value * noise_percent * random.uniform(-1, 1)
    return value + noise


def calculate_degraded_efficiency(base_efficiency: float, degradation_rate: float, days_elapsed: int) -> float:
    """
    Calculate efficiency after degradation over time.

    Args:
        base_efficiency: Starting efficiency (0-1)
        degradation_rate: Daily degradation rate (e.g., 0.02 = 2% per day)
        days_elapsed: Number of days since start

    Returns:
        Degraded efficiency (clamped to 0.5 minimum)
    """
    # Linear degradation with some random variance
    degradation = degradation_rate * days_elapsed
    variance = random.uniform(-0.01, 0.01)  # ±1% random variance

    efficiency = base_efficiency - degradation + variance

    # Don't go below 50% efficiency (machines would be shut down)
    return max(0.5, min(1.0, efficiency))
