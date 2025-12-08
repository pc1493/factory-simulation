"""
Main data generation script - generates all data types for a given date.
"""
import json
import csv
import random
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any
from faker import Faker

from data_generators.config import (
    MACHINES, PRODUCTS, FACTORY, START_DATE, END_DATE,
    OPERATING_HOURS, BATCHES_PER_DAY_RANGE,
    QC_INSPECTION_PROBABILITY, OPERATOR_LOG_PROBABILITY,
    INSPECTORS, OPERATORS
)
from data_generators.chaos_injectors import (
    inject_null, inject_timestamp_drift, inject_product_name_variation,
    inject_machine_id_variation, should_duplicate, inject_timezone_chaos,
    calculate_defect_rate, inject_typo, add_measurement_noise,
    calculate_degraded_efficiency
)

fake = Faker()
Faker.seed(42)  # For reproducibility
random.seed(42)


def generate_batch_id(machine_id: str, date: datetime, batch_num: int) -> str:
    """Generate a unique batch ID."""
    return f"{machine_id}_{date.strftime('%Y%m%d')}_{batch_num:03d}"


def generate_production_batches(date: datetime, machine: Dict, days_elapsed: int) -> List[Dict]:
    """
    Generate production batches for a machine on a given date.

    Args:
        date: Production date
        machine: Machine configuration
        days_elapsed: Days since START_DATE (for degradation calc)

    Returns:
        List of batch dictionaries
    """
    batches = []
    num_batches = random.randint(*BATCHES_PER_DAY_RANGE)

    # Calculate current efficiency (with degradation)
    current_efficiency = calculate_degraded_efficiency(
        machine["base_efficiency"],
        machine["degradation_rate"],
        days_elapsed
    )

    # Distribute batches throughout operating hours
    start_hour = OPERATING_HOURS["start"]
    end_hour = OPERATING_HOURS["end"]
    operating_minutes = (end_hour - start_hour) * 60

    current_time = datetime.combine(date, datetime.min.time()) + timedelta(hours=start_hour)

    for batch_num in range(1, num_batches + 1):
        # Batch duration
        min_duration, max_duration = machine["typical_batch_minutes"]
        duration_minutes = random.randint(min_duration, max_duration)

        batch_start = current_time
        batch_end = batch_start + timedelta(minutes=duration_minutes)

        # Calculate production
        hours = duration_minutes / 60
        expected_units = int(machine["base_output_rate"] * hours * current_efficiency)
        units_produced = max(1, int(expected_units + random.randint(-5, 5)))  # Some variance

        # Calculate defects
        defect_rate = calculate_defect_rate()
        units_defective = int(units_produced * defect_rate)

        batch = {
            "batch_id": generate_batch_id(machine["machine_id"], date, batch_num),
            "machine_id": machine["machine_id"],
            "product_name": machine["output_product"],
            "start_time": batch_start,
            "end_time": batch_end,
            "units_produced": units_produced,
            "units_defective": units_defective,
            "efficiency_actual": round(current_efficiency, 4),
            "energy_consumed_kwh": round(units_produced * machine["energy_per_unit"], 2)
        }

        batches.append(batch)

        # Move to next batch (with some random gap)
        gap_minutes = random.randint(5, 20)
        current_time = batch_end + timedelta(minutes=gap_minutes)

        # Stop if we're past operating hours
        if current_time.hour >= end_hour:
            break

    return batches


def generate_sensor_logs(batches: List[Dict], machine: Dict) -> List[Dict]:
    """
    Generate sensor logs for production batches.

    Args:
        batches: List of production batches
        machine: Machine configuration

    Returns:
        List of sensor log dictionaries
    """
    sensor_logs = []

    for batch in batches:
        # Generate 3-5 sensor readings per batch
        num_readings = random.randint(3, 5)
        batch_duration = (batch["end_time"] - batch["start_time"]).total_seconds() / 60
        interval = batch_duration / num_readings

        for i in range(num_readings):
            reading_time = batch["start_time"] + timedelta(minutes=i * interval)

            # Apply timestamp drift for chaos
            drifted_time = inject_timestamp_drift(reading_time)

            # Generate sensor readings based on machine type
            if machine["machine_type"] == "Smelter":
                temperature = random.uniform(1200, 1400)  # Celsius
                pressure = random.uniform(1.5, 2.5)  # bar
            else:  # Assembler
                temperature = random.uniform(25, 45)  # Celsius (much cooler)
                pressure = random.uniform(0.8, 1.2)  # bar

            # Add measurement noise
            temperature = add_measurement_noise(temperature, 0.03)
            pressure = add_measurement_noise(pressure, 0.02)

            sensor_log = {
                "machine_id": machine["machine_id"],
                "timestamp": drifted_time.isoformat(),
                "temperature": inject_null(round(temperature, 2)),
                "pressure": inject_null(round(pressure, 3)),
                "energy_kwh": inject_null(round(random.uniform(5, 15), 2)),
                "efficiency_percent": inject_null(round(batch["efficiency_actual"] * 100, 2))
            }

            sensor_logs.append(sensor_log)

    return sensor_logs


def generate_qc_checks(batches: List[Dict], date: datetime) -> List[Dict]:
    """
    Generate QC inspection records.

    Args:
        batches: List of production batches
        date: Production date

    Returns:
        List of QC check dictionaries
    """
    qc_checks = []
    check_counter = 1

    for batch in batches:
        # Only inspect some batches
        if random.random() > QC_INSPECTION_PROBABILITY:
            continue

        # Inspection happens shortly after batch ends
        check_time = batch["end_time"] + timedelta(minutes=random.randint(5, 30))
        check_time = inject_timezone_chaos(check_time)

        inspector = random.choice(INSPECTORS)

        # Determine pass/fail
        has_defects = batch["units_defective"] > 0
        if has_defects and random.random() < 0.7:  # 70% chance of catching defects
            pass_fail = "FAIL"
            defect_notes = random.choice([
                "Surface imperfections detected",
                "Dimensional tolerance exceeded",
                "Material discoloration observed",
                "Structural weakness identified"
            ])
        else:
            pass_fail = "PASS"
            defect_notes = ""

        qc_check = {
            "check_id": f"QC_{date.strftime('%Y%m%d')}_{check_counter:04d}",
            "batch_id": batch["batch_id"],
            "check_timestamp": check_time.isoformat(),
            "inspector_id": inspector,
            "pass_fail": pass_fail,
            "defect_notes": defect_notes
        }

        qc_checks.append(qc_check)
        check_counter += 1

    return qc_checks


def generate_operator_logs(batches: List[Dict], machine: Dict, date: datetime) -> List[Dict]:
    """
    Generate operator log entries with intentional inconsistencies.

    Args:
        batches: List of production batches
        machine: Machine configuration
        date: Production date

    Returns:
        List of operator log dictionaries
    """
    operator_logs = []
    log_counter = 1

    for batch in batches:
        # Only log some batches
        if random.random() > OPERATOR_LOG_PROBABILITY:
            continue

        log_time = batch["start_time"] + timedelta(minutes=random.randint(-10, 10))
        log_time = inject_timezone_chaos(log_time)

        operator = random.choice(OPERATORS)

        # Generate action and notes with chaos
        actions = ["START_BATCH", "MONITOR", "ADJUST_PARAMS", "END_BATCH"]
        action = random.choice(actions)

        notes_templates = [
            f"Batch {batch['batch_id']} started normally",
            f"Output looks good, produced ~{batch['units_produced']} units",
            f"Machine running smooth on {inject_machine_id_variation(machine['machine_id'])}",
            f"Temperature stable for {inject_product_name_variation(batch['product_name'])} production",
        ]

        notes = inject_typo(random.choice(notes_templates), typo_probability=0.1)

        operator_log = {
            "log_id": f"LOG_{date.strftime('%Y%m%d')}_{log_counter:04d}",
            "machine_id": inject_machine_id_variation(machine["machine_id"]),
            "operator_id": operator,
            "log_timestamp": log_time.isoformat(),
            "action": action,
            "notes": notes
        }

        operator_logs.append(operator_log)
        log_counter += 1

    return operator_logs


def generate_ground_truth(batches: List[Dict], date: datetime) -> Dict:
    """
    Generate ground truth data (clean, canonical) for validation.

    Args:
        batches: List of production batches (clean versions)
        date: Production date

    Returns:
        Dictionary with ground truth metrics
    """
    truth = {
        "date": date.strftime("%Y-%m-%d"),
        "total_batches": len(batches),
        "by_machine": {},
        "by_product": {},
        "factory_totals": {
            "units_produced": 0,
            "units_defective": 0,
            "energy_consumed_kwh": 0
        }
    }

    for batch in batches:
        machine_id = batch["machine_id"]
        product = batch["product_name"]

        # Initialize if needed
        if machine_id not in truth["by_machine"]:
            truth["by_machine"][machine_id] = {
                "batches": 0,
                "units_produced": 0,
                "units_defective": 0,
                "energy_consumed_kwh": 0
            }

        if product not in truth["by_product"]:
            truth["by_product"][product] = {
                "batches": 0,
                "units_produced": 0,
                "units_defective": 0
            }

        # Accumulate
        truth["by_machine"][machine_id]["batches"] += 1
        truth["by_machine"][machine_id]["units_produced"] += batch["units_produced"]
        truth["by_machine"][machine_id]["units_defective"] += batch["units_defective"]
        truth["by_machine"][machine_id]["energy_consumed_kwh"] += batch["energy_consumed_kwh"]

        truth["by_product"][product]["batches"] += 1
        truth["by_product"][product]["units_produced"] += batch["units_produced"]
        truth["by_product"][product]["units_defective"] += batch["units_defective"]

        truth["factory_totals"]["units_produced"] += batch["units_produced"]
        truth["factory_totals"]["units_defective"] += batch["units_defective"]
        truth["factory_totals"]["energy_consumed_kwh"] += batch["energy_consumed_kwh"]

    return truth


def apply_chaos_to_batches(batches: List[Dict]) -> List[Dict]:
    """
    Apply chaos to production batches (product name variations, duplicates).

    Args:
        batches: Clean batch list

    Returns:
        Chaotic batch list
    """
    chaotic_batches = []

    for batch in batches:
        # Create a copy with chaos
        chaotic_batch = batch.copy()

        # Apply product name variation
        chaotic_batch["product_name"] = inject_product_name_variation(batch["product_name"])

        chaotic_batches.append(chaotic_batch)

        # Maybe duplicate
        if should_duplicate():
            chaotic_batches.append(chaotic_batch.copy())

    return chaotic_batches


def save_data(date: datetime, sensor_logs: List, batches: List, qc_checks: List, operator_logs: List, ground_truth: Dict):
    """
    Save all generated data to files.

    Args:
        date: Production date
        sensor_logs: Sensor log data
        batches: Production batch data
        qc_checks: QC check data
        operator_logs: Operator log data
        ground_truth: Ground truth data
    """
    date_str = date.strftime("%Y-%m-%d")

    # Create directories
    raw_dir = Path(__file__).parent.parent / "raw_data" / date_str
    raw_dir.mkdir(parents=True, exist_ok=True)

    truth_dir = Path(__file__).parent.parent / "ground_truth" / date_str
    truth_dir.mkdir(parents=True, exist_ok=True)

    # Save sensor logs (JSON)
    with open(raw_dir / "sensor_logs.json", "w") as f:
        json.dump(sensor_logs, f, indent=2)

    # Save production batches (CSV)
    with open(raw_dir / "production_batches.csv", "w", newline="") as f:
        if batches:
            fieldnames = ["batch_id", "machine_id", "product_name", "start_time", "end_time", "units_produced", "units_defective"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for batch in batches:
                writer.writerow({
                    "batch_id": batch["batch_id"],
                    "machine_id": batch["machine_id"],
                    "product_name": batch["product_name"],
                    "start_time": batch["start_time"].isoformat(),
                    "end_time": batch["end_time"].isoformat(),
                    "units_produced": batch["units_produced"],
                    "units_defective": batch["units_defective"]
                })

    # Save QC checks (CSV)
    with open(raw_dir / "qc_checks.csv", "w", newline="") as f:
        if qc_checks:
            fieldnames = ["check_id", "batch_id", "check_timestamp", "inspector_id", "pass_fail", "defect_notes"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(qc_checks)

    # Save operator logs (CSV)
    with open(raw_dir / "operator_logs.csv", "w", newline="") as f:
        if operator_logs:
            fieldnames = ["log_id", "machine_id", "operator_id", "log_timestamp", "action", "notes"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(operator_logs)

    # Save ground truth (JSON)
    with open(truth_dir / "truth.json", "w") as f:
        json.dump(ground_truth, f, indent=2)

    print(f"[OK] Generated data for {date_str}:")
    print(f"  - {len(sensor_logs)} sensor readings")
    print(f"  - {len(batches)} production batches")
    print(f"  - {len(qc_checks)} QC inspections")
    print(f"  - {len(operator_logs)} operator logs")


def generate_day(date: datetime):
    """Generate all data for a single day."""
    days_elapsed = (date.date() - START_DATE).days

    all_batches_clean = []
    all_sensor_logs = []
    all_qc_checks = []
    all_operator_logs = []

    # Generate data for each machine
    for machine in MACHINES:
        batches = generate_production_batches(date.date(), machine, days_elapsed)
        all_batches_clean.extend(batches)

        sensors = generate_sensor_logs(batches, machine)
        all_sensor_logs.extend(sensors)

        qc = generate_qc_checks(batches, date.date())
        all_qc_checks.extend(qc)

        ops = generate_operator_logs(batches, machine, date.date())
        all_operator_logs.extend(ops)

    # Generate ground truth from clean batches
    ground_truth = generate_ground_truth(all_batches_clean, date.date())

    # Apply chaos to batches
    chaotic_batches = apply_chaos_to_batches(all_batches_clean)

    # Save all data
    save_data(date, all_sensor_logs, chaotic_batches, all_qc_checks, all_operator_logs, ground_truth)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Generate factory simulation data")
    parser.add_argument("--date", type=str, help="Specific date (YYYY-MM-DD)")
    parser.add_argument("--all", action="store_true", help="Generate all 7 days")
    args = parser.parse_args()

    if args.all:
        print(f"Generating data from {START_DATE} to {END_DATE}...")
        current = datetime.combine(START_DATE, datetime.min.time())
        end = datetime.combine(END_DATE, datetime.min.time())

        while current <= end:
            generate_day(current)
            current += timedelta(days=1)

        print(f"\n[SUCCESS] All historical data generated!")

    elif args.date:
        target_date = datetime.strptime(args.date, "%Y-%m-%d")
        generate_day(target_date)

    else:
        print("Please specify --date YYYY-MM-DD or --all")
        return


if __name__ == "__main__":
    main()
