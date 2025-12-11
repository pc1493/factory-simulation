# Factory Simulation - Comprehensive Project Status

**Last Updated:** 2025-12-10
**Current Phase:** Data Generation + Dashboard Complete
**Days of Data:** 10 days (Dec 1-10, 2025)

---

## 🎯 PROJECT COMPONENTS

### ✅ 1. Data Generation Layer (COMPLETE)

**Files:**
- `data_generators/config.py` - Configuration for machines, products, chaos settings
- `data_generators/chaos_injectors.py` - Functions to inject controlled chaos
- `data_generators/generate_data.py` - Main data generation script

**Capabilities:**
- Generates 4 data files per day:
  - `sensor_logs.json` - Machine sensor readings (temperature, pressure, energy)
  - `production_batches.csv` - Production batch records
  - `qc_checks.csv` - Quality control inspections
  - `operator_logs.csv` - Manual operator notes
- Ground truth file: `truth.json` - Clean metrics for validation
- Configurable chaos patterns (8 types)
- Date range: Dynamic (currently Dec 1-10, 2025)

**Current Data Stats (10 days):**
- ~300+ production batches
- ~20,000+ units produced
- ~250+ defective units
- ~2,200+ kWh energy consumed

---

### ✅ 2. Database Infrastructure (COMPLETE)

**Files:**
- `orchestration/init_database.py` - DuckDB initialization

**Capabilities:**
- Creates DuckDB warehouse (`duckdb/warehouse.db`)
- 3 schemas: bronze, silver, gold
- 4 bronze tables ready for ingestion:
  - `bronze.sensor_logs`
  - `bronze.production_batches`
  - `bronze.qc_checks`
  - `bronze.operator_logs`

---

### ✅ 3. Interactive Dashboard (COMPLETE)

**Files:**
- `streamlit_app/dashboard.py` - Main dashboard application
- `streamlit_app/README.md` - Dashboard documentation

**Features:**

#### Quadrant 1: Production Floor
- 3 machine status cards (Smelter #1, #2, Assembler #1)
- Real-time efficiency metrics
- Color-coded health indicators (🟢🟡🔴)
- Production progress bars

#### Quadrant 2: Machine Health Monitor
- Plotly line chart showing efficiency over time
- Visual tracking of Smelter #2 degradation (100% → 88%)
- Real-time sensor gauges (temperature, pressure)

#### Quadrant 3: Product Flow Pipeline
- Sankey diagram showing material transformation
- Iron Ore → Iron Plates → Gear Wheels
- Daily production summaries

#### Quadrant 4: Data Quality Alerts
- Real-time chaos detection
- Null value tracking (~7.8%)
- Product name variations (10 spellings)
- Duplicate batch detection (~3%)
- Event log

#### Time Controls
- Day selector (1-10)
- Play/Pause auto-advance
- Speed control: 1x, 10x, 100x, 1000x
- Progress bar

---

### ✅ 4. Utilities & Documentation (COMPLETE)

**Files:**
- `verify_data.py` - Data quality verification script
- `README.md` - Main project documentation
- `DATA_SAMPLES.md` - Sample data examples
- `DASHBOARD_GUIDE.md` - Dashboard user guide
- `requirements.txt` - Python dependencies

---

## 🔧 SCHEDULER RESEARCH SUMMARY

### Recommended Approach: **APScheduler**

**Why APScheduler:**
- ✅ Pure Python (no external dependencies)
- ✅ Low complexity (beginner-friendly)
- ✅ Portable (runs on Windows/Linux/Cloud)
- ✅ Professional scheduler patterns
- ✅ 1-2 hour setup time

**Implementation Plan:**
```python
# scheduler.py
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from data_generators.generate_data import generate_day

def daily_job():
    generate_day(datetime.now())

scheduler = BlockingScheduler()
scheduler.add_job(
    daily_job,
    CronTrigger(hour=9, minute=0),
    id='daily_factory_data'
)
scheduler.start()
```

**Alternative Options (for later):**
- **Prefect** - When you have 3+ pipeline stages (Bronze → Silver → Gold)
- **Airflow** - For production-grade learning experience
- **GitHub Actions** - For CI/CD + cloud execution

---

## 🐛 CODE AUDIT FINDINGS

### **CRITICAL ISSUES (4)**

#### 1. Division by Zero - verify_data.py:50
```python
# CURRENT (BROKEN):
print(f"Total defective: {total_defects} ({total_defects/total_units*100:.2f}%)")

# FIX:
defect_pct = (total_defects/total_units*100) if total_units > 0 else 0
print(f"Total defective: {total_defects} ({defect_pct:.2f}%)")
```
**Impact:** Script crashes if no production data

#### 2. Incorrect Timezone Logic - chaos_injectors.py:107
```python
# CURRENT (WRONG):
return timestamp - timedelta(hours=7)  # Subtracts when should add

# FIX:
# MST is UTC-7, so to convert FROM UTC TO MST, subtract 7 hours (correct)
# But to convert FROM MST TO UTC, add 7 hours
# Clarify the intent and fix direction
```
**Impact:** All timezone-affected timestamps are backwards

#### 3. Division by Zero - dashboard.py:506
```python
# CURRENT (MISLEADING):
defect_rate = (totals.get('units_defective', 0) / totals.get('units_produced', 1)) * 100

# FIX:
units = totals.get('units_produced', 0)
defect_rate = (totals.get('units_defective', 0) / units * 100) if units > 0 else 0
```
**Impact:** Shows 0% defect rate when no data (misleading)

#### 4. Hardcoded Dates - dashboard.py:90,106,118
```python
# CURRENT (WRONG):
start_date = datetime(2025, 12, 1).date()

# FIX:
from data_generators.config import START_DATE, END_DATE
start_date = START_DATE  # Use dynamic config
```
**Impact:** Dashboard breaks when data range changes

---

### **HIGH SEVERITY ISSUES (5)**

5. **Null data crashes dashboard gauges** (dashboard.py:362,367)
6. **Hardcoded efficiency calculation** (dashboard.py:262-264)
7. **Timestamp type mismatch** (generate_data.py:146)
8. **Date indexing confusion** (dashboard.py:107)
9. **Incomplete chaos injection** (generate_data.py:325-350)

---

### **MEDIUM SEVERITY ISSUES (7)**

10. Energy sensor values not proportional to batch energy
11. Typo function edge case handling
12. Timezone chaos inconsistently applied
13. Date range config mismatch
14. Operating hours boundary check
15. Defect rate can be negative (before clamping)
16. Sensor data energy disconnect

---

### **LOW SEVERITY ISSUES (5)**

17. Hardcoded sensor temperature ranges
18. Magic numbers in dashboard
19. No machine config validation
20. Silent failures on missing data
21. Incorrect Sankey diagram logic

---

## 📊 CURRENT DATA STRUCTURE

### Raw Data Files (per day)
```
raw_data/YYYY-MM-DD/
├── sensor_logs.json          # 140-145 readings/day
├── production_batches.csv    # 27-36 batches/day
├── qc_checks.csv             # 10-16 inspections/day
└── operator_logs.csv         # 4-11 logs/day
```

### Ground Truth Files
```
ground_truth/YYYY-MM-DD/
└── truth.json                # Clean aggregated metrics
    ├── date
    ├── total_batches
    ├── by_machine (SMELTER-01, SMELTER-02, ASSEMBLER-01)
    ├── by_product (Iron Plate, Gear Wheel)
    └── factory_totals
```

### Database Schema
```
bronze/
├── sensor_logs
├── production_batches
├── qc_checks
└── operator_logs

silver/   (NOT YET IMPLEMENTED)
gold/     (NOT YET IMPLEMENTED)
```

---

## 🎯 CONTROLLED CHAOS PATTERNS

### Implemented Chaos (8 types)

1. **Product Name Variations** - 10 different spellings
   - "Iron Plate", "iron_plate", "IronPlate", "Iron Plates", etc.

2. **Machine ID Inconsistencies** - 5+ variations per machine
   - "SMELTER-01", "Smelter-1", "SMELTER_01", "smelter1", etc.

3. **Null Values** - 7.5% in sensor readings
   - Random nulls in temperature, pressure, energy, efficiency

4. **Timestamp Drift** - ±5 minutes variance
   - Sensor readings drift from batch times

5. **Duplicate Records** - 3% of production batches
   - Same batch_id appears multiple times

6. **Late-Arriving Data** - 10% chance, 1-2 day delay
   - (Configured but not yet simulated in practice)

7. **Timezone Chaos** - 30% local time (MST) vs UTC
   - Some timestamps in MST, others in UTC

8. **Performance Degradation** - Smelter #2 loses 2% efficiency/day
   - Linear degradation from 100% to 88% over 7 days

---

## 🚀 WHAT'S WORKING

✅ **Data Generation:**
- Generates realistic manufacturing data
- Controlled chaos injection
- Ground truth for validation
- Configurable parameters
- 10 days of data (Dec 1-10, 2025)

✅ **Dashboard:**
- 4-quadrant factory control center
- Interactive time-travel controls
- Real-time chaos visualization
- Efficiency degradation tracking
- Beautiful Plotly charts
- Industrial dark theme

✅ **Infrastructure:**
- DuckDB warehouse initialized
- Bronze schema ready
- Git repository with good commit history
- Comprehensive documentation

---

## ❌ WHAT'S NOT WORKING (Critical Bugs)

1. **verify_data.py crashes** on division by zero
2. **Timezone math is backwards** (subtracts when should add)
3. **Dashboard shows 0% defects** when no data (misleading)
4. **Dashboard hardcoded Dec 1 start** (breaks with new data)
5. **Dashboard can crash** if all sensor values are null
6. **Efficiency calculation** doesn't match actual data

---

## 🔄 WHAT'S MISSING

### Bronze Layer
- ❌ Ingestion scripts to load CSV/JSON into DuckDB
- ❌ Metadata tracking (_loaded_at, _source_file)
- ❌ Incremental load logic

### Silver Layer
- ❌ dbt project initialization
- ❌ Deduplication models
- ❌ Product name standardization
- ❌ Timestamp normalization to UTC
- ❌ Null value handling

### Gold Layer
- ❌ Dimensional model (fact_production, dim_*)
- ❌ SCD Type 2 for dim_machines
- ❌ Incremental fact table loading

### Orchestration
- ❌ Daily data generation scheduler (APScheduler)
- ❌ End-to-end pipeline orchestration
- ❌ Bronze → Silver → Gold execution flow

### Validation
- ❌ Ground truth comparison tests
- ❌ Data quality metrics calculation
- ❌ 2% accuracy validation

---

## 📅 IMPLEMENTATION ROADMAP

### IMMEDIATE (Next 1-2 hours)
1. Fix critical bugs (4 issues)
2. Implement APScheduler for daily generation
3. Test scheduler with manual runs

### THIS WEEK (Next 3-5 days)
1. Bronze layer ingestion scripts
2. Basic dbt project setup
3. Silver layer cleaning models
4. Update dashboard to use Silver data

### NEXT WEEK (Next 7-10 days)
1. Gold dimensional model
2. Ground truth validation tests
3. End-to-end orchestration
4. Documentation polish

---

## 🏆 PROJECT STRENGTHS

1. **Well-structured codebase** with clear separation of concerns
2. **Comprehensive documentation** (README, samples, guides)
3. **Realistic data patterns** with controlled chaos
4. **Beautiful visualization** with industrial theme
5. **Good git hygiene** with descriptive commits
6. **Configurable architecture** easy to extend

---

## ⚠️ PROJECT WEAKNESSES

1. **Critical bugs** blocking production use
2. **No automated testing** (pytest framework unused)
3. **Hardcoded values** scattered throughout
4. **No data pipeline** (Bronze/Silver/Gold not implemented)
5. **No scheduler** (manual data generation only)
6. **Type inconsistencies** between generation and storage

---

## 📈 METRICS SUMMARY (10 Days)

### Data Volume
- **Production batches:** ~300
- **Sensor readings:** ~1,430
- **QC inspections:** ~130
- **Operator logs:** ~60

### Production Output
- **Total units:** ~20,000+
- **Defective units:** ~250
- **Defect rate:** ~1.2%
- **Energy consumed:** ~2,200 kWh

### Data Quality (Chaos)
- **Null values:** 7.5% of sensor readings
- **Product variations:** 10 different spellings
- **Duplicate batches:** ~3% rate
- **Machine ID variations:** 5+ per machine
- **Timestamp drift:** ±5 minutes

---

## 🎓 LEARNING OUTCOMES SO FAR

### Skills Demonstrated
- ✅ Python data generation with Faker
- ✅ Controlled chaos injection patterns
- ✅ Streamlit dashboard development
- ✅ Plotly interactive visualizations
- ✅ DuckDB database setup
- ✅ Git version control
- ✅ Documentation writing

### Skills To Practice
- ⏳ dbt modeling and transformations
- ⏳ Incremental data loading
- ⏳ Dimensional modeling (Kimball)
- ⏳ Data quality testing
- ⏳ Workflow orchestration
- ⏳ Bronze/Silver/Gold architecture

---

## 💡 RECOMMENDATIONS

### Priority 1: Fix Critical Bugs
- Division by zero errors
- Timezone logic reversal
- Hardcoded dashboard dates
- Null value handling

### Priority 2: Implement Scheduler
- Install APScheduler
- Create scheduler.py
- Test daily generation
- Set up as Windows service (optional)

### Priority 3: Build Data Pipeline
- Bronze layer ingestion
- Silver layer dbt models
- Basic transformation testing

### Priority 4: Validation
- Ground truth comparison
- Accuracy metrics
- Data quality dashboard

---

## 📞 NEXT STEPS

**Ask yourself:**
1. Should I fix bugs first or continue building features?
2. Is scheduler more important than Bronze layer?
3. Do I want to learn Airflow now or stick with APScheduler?
4. Should I pause and write tests before continuing?

**Recommendation:**
1. Fix critical bugs (1 hour)
2. Implement APScheduler (1 hour)
3. Build Bronze layer (2-3 hours)
4. Then decide: dbt vs. testing vs. Airflow

---

**Total Project Status: 40% Complete**
- ✅ Data Generation: 100%
- ✅ Dashboard: 100%
- ✅ Database Setup: 100%
- ❌ Data Pipeline: 0%
- ❌ Validation: 0%
- ❌ Orchestration: 0%
