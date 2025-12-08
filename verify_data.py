"""
Quick verification script to check generated data quality.
"""
import json
from pathlib import Path
from datetime import datetime, timedelta

# Get date range
end_date = datetime.now().date()
start_date = end_date - timedelta(days=6)

print("=" * 60)
print("FACTORY SIMULATION DATA VERIFICATION")
print("=" * 60)
print(f"\nDate range: {start_date} to {end_date}\n")

# Check each day
total_batches = 0
total_units = 0
total_defects = 0
total_energy = 0

current = start_date
while current <= end_date:
    date_str = current.strftime("%Y-%m-%d")
    truth_file = Path(f"ground_truth/{date_str}/truth.json")

    if truth_file.exists():
        with open(truth_file) as f:
            truth = json.load(f)

        print(f"{date_str}:")
        print(f"  Batches: {truth['total_batches']}")
        print(f"  Units produced: {truth['factory_totals']['units_produced']}")
        print(f"  Defective: {truth['factory_totals']['units_defective']}")
        print(f"  Energy (kWh): {truth['factory_totals']['energy_consumed_kwh']:.2f}")

        total_batches += truth['total_batches']
        total_units += truth['factory_totals']['units_produced']
        total_defects += truth['factory_totals']['units_defective']
        total_energy += truth['factory_totals']['energy_consumed_kwh']

    current += timedelta(days=1)

print("\n" + "=" * 60)
print("7-DAY TOTALS:")
print("=" * 60)
print(f"Total batches: {total_batches}")
print(f"Total units produced: {total_units}")
print(f"Total defective: {total_defects} ({total_defects/total_units*100:.2f}%)")
print(f"Total energy consumed: {total_energy:.2f} kWh")
print(f"Average batches/day: {total_batches/7:.1f}")
print(f"Average units/day: {total_units/7:.1f}")

print("\n" + "=" * 60)
print("SMELTER #2 DEGRADATION TRACKING")
print("=" * 60)

current = start_date
day_num = 1
while current <= end_date:
    date_str = current.strftime("%Y-%m-%d")
    truth_file = Path(f"ground_truth/{date_str}/truth.json")

    if truth_file.exists():
        with open(truth_file) as f:
            truth = json.load(f)

        smelter2 = truth['by_machine'].get('SMELTER-02', {})
        if smelter2:
            batches = smelter2['batches']
            units = smelter2['units_produced']
            avg_output = units / batches if batches > 0 else 0

            print(f"Day {day_num} ({date_str}): {batches} batches, {units} units ({avg_output:.1f} avg/batch)")

    current += timedelta(days=1)
    day_num += 1

print("\n" + "=" * 60)
print("DATA CHAOS VERIFICATION")
print("=" * 60)

# Check first day's production batches for chaos
first_day = start_date.strftime("%Y-%m-%d")
batch_file = Path(f"raw_data/{first_day}/production_batches.csv")

if batch_file.exists():
    with open(batch_file) as f:
        lines = f.readlines()

    product_names = set()
    for line in lines[1:]:  # Skip header
        parts = line.split(',')
        if len(parts) >= 3:
            product_names.add(parts[2])

    print(f"\nProduct name variations found: {len(product_names)}")
    for name in sorted(product_names):
        print(f"  - '{name}'")

# Check operator logs for machine ID variations
op_log_file = Path(f"raw_data/{first_day}/operator_logs.csv")

if op_log_file.exists():
    with open(op_log_file) as f:
        lines = f.readlines()

    machine_ids = set()
    for line in lines[1:]:  # Skip header
        parts = line.split(',')
        if len(parts) >= 2:
            machine_ids.add(parts[1])

    print(f"\nMachine ID variations found: {len(machine_ids)}")
    for mid in sorted(machine_ids):
        print(f"  - '{mid}'")

print("\n" + "=" * 60)
print("[SUCCESS] Data verification complete!")
print("=" * 60)
