"""
Configuration for factory data generation.
Defines machines, products, chaos levels, and simulation parameters.
"""
from datetime import datetime, timedelta

# ============================================================================
# FACTORY CONFIGURATION
# ============================================================================

FACTORY = {
    "name": "Factory Alpha",
    "location": "Phoenix, AZ",
    "timezone": "MST"
}

# ============================================================================
# MACHINES CONFIGURATION
# ============================================================================

MACHINES = [
    {
        "machine_id": "SMELTER-01",
        "machine_name": "Smelter #1",
        "machine_type": "Smelter",
        "installation_date": "2024-01-15",
        "input_product": "Iron Ore",
        "output_product": "Iron Plate",
        "base_output_rate": 75,  # units per hour
        "base_efficiency": 0.98,  # 98%
        "degradation_rate": 0.0,  # No degradation
        "typical_batch_minutes": (45, 90),  # min, max
        "energy_per_unit": 0.12  # kWh per unit
    },
    {
        "machine_id": "SMELTER-02",
        "machine_name": "Smelter #2",
        "machine_type": "Smelter",
        "installation_date": "2024-02-10",
        "input_product": "Iron Ore",
        "output_product": "Iron Plate",
        "base_output_rate": 80,  # units per hour
        "base_efficiency": 1.00,  # 100% on day 1
        "degradation_rate": 0.02,  # 2% loss per day
        "typical_batch_minutes": (40, 85),
        "energy_per_unit": 0.11
    },
    {
        "machine_id": "ASSEMBLER-01",
        "machine_name": "Assembler #1",
        "machine_type": "Assembler",
        "installation_date": "2024-03-01",
        "input_product": "Iron Plate",
        "output_product": "Gear Wheel",
        "base_output_rate": 30,  # units per hour
        "base_efficiency": 0.95,  # 95%
        "degradation_rate": 0.0,
        "typical_batch_minutes": (60, 120),
        "energy_per_unit": 0.08
    }
]

# ============================================================================
# PRODUCTS CONFIGURATION
# ============================================================================

PRODUCTS = [
    {
        "product_id": "IRON_ORE",
        "canonical_name": "Iron Ore",
        "product_tier": "Raw",
        "recipe_version": "1.0"
    },
    {
        "product_id": "IRON_PLATE",
        "canonical_name": "Iron Plate",
        "product_tier": "Intermediate",
        "recipe_version": "1.0",
        "input_ratio": 1  # 1 ore -> 1 plate
    },
    {
        "product_id": "GEAR_WHEEL",
        "canonical_name": "Gear Wheel",
        "product_tier": "Final",
        "recipe_version": "1.0",
        "input_ratio": 2  # 2 plates -> 1 gear
    }
]

# ============================================================================
# CHAOS CONFIGURATION
# ============================================================================

CHAOS_CONFIG = {
    # Null values in sensor data
    "null_probability": 0.075,  # 7.5% chance of null

    # Timestamp drift (in minutes)
    "timestamp_drift_range": (-5, 5),  # ±5 minutes

    # Product name variations (chaos!)
    "product_name_variations": {
        "Iron Plate": [
            "Iron Plate",
            "iron_plate",
            "IronPlate",
            "Iron Plates",
            "IRON_PLATE",
            "iron plate"
        ],
        "Gear Wheel": [
            "Gear Wheel",
            "gear_wheel",
            "GearWheel",
            "Gear Wheels",
            "GEAR_WHEEL"
        ],
        "Iron Ore": [
            "Iron Ore",
            "iron_ore",
            "IronOre",
            "IRON_ORE"
        ]
    },

    # Machine ID variations (operator logs)
    "machine_id_variations": {
        "SMELTER-01": ["SMELTER-01", "Smelter-1", "SMELTER_01", "smelter1", "Smelter #1"],
        "SMELTER-02": ["SMELTER-02", "Smelter-2", "SMELTER_02", "smelter2", "Smelter #2"],
        "ASSEMBLER-01": ["ASSEMBLER-01", "Assembler-1", "ASSEMBLER_01", "assembler1", "Asm-1"]
    },

    # Duplicate records
    "duplicate_probability": 0.03,  # 3% chance

    # Late-arriving data
    "late_arrival_probability": 0.10,  # 10% chance
    "late_arrival_days": (1, 2),  # 1-2 day delay

    # Timezone chaos (some logs in local time, some UTC)
    "timezone_chaos_probability": 0.30,  # 30% in local time

    # Defect rate
    "base_defect_rate": 0.02,  # 2% defective units
    "defect_rate_variance": 0.01  # ±1% variance
}

# ============================================================================
# SIMULATION PARAMETERS
# ============================================================================

# Date range for historical data generation
# Using today's date as the end date
END_DATE = datetime.now().date()
START_DATE = END_DATE - timedelta(days=6)  # 7 days total (inclusive)

# Operating hours
OPERATING_HOURS = {
    "start": 6,  # 6 AM
    "end": 22    # 10 PM (16 hour operation day)
}

# Batches per machine per day
BATCHES_PER_DAY_RANGE = (8, 14)  # Random between 8-14 batches

# QC inspection frequency
QC_INSPECTION_PROBABILITY = 0.40  # 40% of batches get inspected

# Operator log frequency
OPERATOR_LOG_PROBABILITY = 0.25  # 25% of batches have operator notes

# Inspector and operator IDs
INSPECTORS = ["QC-001", "QC-002", "QC-003"]
OPERATORS = ["OP-101", "OP-102", "OP-103", "OP-104"]
