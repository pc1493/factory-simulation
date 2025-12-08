# Generated Data Samples

This document shows examples of the generated factory simulation data with controlled chaos.

## Summary Statistics (2025-12-01)

**From Ground Truth:**
- Total batches: 35
- Total units produced: 2,420
- Total defective units: 27
- Total energy consumed: 263.49 kWh

### By Machine:
- **SMELTER-01**: 13 batches, 1,037 iron plates (13 defective)
- **SMELTER-02**: 12 batches, 947 iron plates (11 defective) - *degrading*
- **ASSEMBLER-01**: 10 batches, 436 gear wheels (3 defective)

## Data Files Generated Per Day

Each day produces 4 raw data files:

1. `sensor_logs.json` - Machine sensor readings
2. `production_batches.csv` - Production batch records
3. `qc_checks.csv` - Quality control inspections
4. `operator_logs.csv` - Manual operator notes

Plus ground truth: `truth.json`

## Sample: Sensor Logs (JSON)

```json
{
  "machine_id": "SMELTER-01",
  "timestamp": "2025-12-01T06:25:40",
  "temperature": 1209.3,
  "pressure": 2.218,
  "energy_kwh": 10.57,
  "efficiency_percent": 97.22
}
```

**Chaos injected:**
- Null values (~7.5% of readings)
- Timestamp drift (±5 minutes)
- Measurement noise

## Sample: Production Batches (CSV)

```csv
batch_id,machine_id,product_name,start_time,end_time,units_produced,units_defective
SMELTER-01_20251201_001,SMELTER-01,IronPlate,2025-12-01T06:00:00,2025-12-01T07:02:00,73,1
SMELTER-01_20251201_002,SMELTER-01,iron_plate,2025-12-01T07:10:00,2025-12-01T08:38:00,109,1
SMELTER-01_20251201_003,SMELTER-01,Iron Plates,2025-12-01T08:56:00,2025-12-01T09:43:00,52,0
```

**Chaos injected:**
- Product name variations: "IronPlate", "iron_plate", "Iron Plates", "Iron Plate", "IRON_PLATE"
- 3% duplicate records (same batch_id)

## Sample: Operator Logs (CSV)

```csv
log_id,machine_id,operator_id,log_timestamp,action,notes
LOG_20251201_0001,SMELTER_01,OP-102,2025-12-01T11:20:00,ADJUST_PARAMS,Temperature stable for IronPlate production
LOG_20251201_0002,Smelter #1,OP-102,2025-12-01T19:44:00,MONITOR,Temperature stable for iron plate production
LOG_20251201_0003,Smelter-2,OP-104,2025-12-01T02:06:00,START_BATCH,Machine running smooth on smelter2
```

**Chaos injected:**
- Machine ID variations: "SMELTER_01", "Smelter #1", "Smelter-2", "smelter2"
- Timezone chaos (some UTC, some MST)
- Occasional typos in notes

## Sample: QC Checks (CSV)

```csv
check_id,batch_id,check_timestamp,inspector_id,pass_fail,defect_notes
QC_20251201_0001,SMELTER-01_20251201_002,2025-12-01T08:52:00,QC-002,FAIL,Surface imperfections detected
QC_20251201_0002,SMELTER-01_20251201_003,2025-12-01T10:06:00,QC-001,PASS,
```

**Features:**
- 40% of batches get inspected
- 70% chance of catching defects if present

## Controlled Chaos Configuration

All chaos parameters are configurable in `data_generators/config.py`:

- **Null probability**: 7.5%
- **Timestamp drift**: ±5 minutes
- **Duplicate probability**: 3%
- **Late arrival**: 10% chance, 1-2 day delay
- **Timezone chaos**: 30% in local time (MST)
- **Defect rate**: 2% ± 1%
- **Smelter #2 degradation**: 2% efficiency loss per day

## Machine Performance Tracking

**Smelter #2 Degradation Over 7 Days:**
- Day 1: 100% efficiency
- Day 2: 98% efficiency
- Day 3: 96% efficiency
- Day 4: 94% efficiency
- Day 5: 92% efficiency
- Day 6: 90% efficiency
- Day 7: 88% efficiency

This degradation should be detectable in the Silver/Gold layer analysis!

## Next Steps

The Bronze layer will ingest this raw data as-is (immutable).
The Silver layer will clean and standardize it.
The Gold layer will build a dimensional model for analytics.
