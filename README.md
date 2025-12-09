# Factorio-Style Data Pipeline Simulator

**Status:** In Development
**Timeline:** Dec 6 - Dec 20, 2025
**Current Phase:** Dashboard & Visualization Complete

## Project Overview

A learning project to master modern data engineering patterns through building a manufacturing data pipeline with controlled chaos.

### Learning Goals
- Medallion architecture (Bronze → Silver → Gold)
- Incremental data loading
- Dimensional modeling
- Data quality debugging
- Working with AI coding assistants (Claude Code)

### Tech Stack
- **Data Generation:** Python
- **Storage:** DuckDB
- **Transformation:** dbt-core (dbt-duckdb)
- **Orchestration:** Python scripts
- **Visualization:** Streamlit

## Manufacturing Scenario

**1 Factory | 3 Machines | 3 Products | 7 Days of Data**

- **Raw Material:** Iron Ore
- **Intermediate:** Iron Plates (smelted)
- **Final Product:** Gear Wheels (assembled)

**Machines:**
- Smelter #1 (Iron Plates)
- Smelter #2 (Iron Plates) - degrading performance
- Assembler #1 (Gear Wheels)

## Project Structure

```
factory-simulation/
├── data_generators/       # Python scripts to generate chaotic data
├── raw_data/             # Daily data dumps (gitignored)
├── dbt_project/          # dbt models (bronze/silver/gold)
├── streamlit_app/        # Dashboard
├── orchestration/        # Pipeline execution scripts
├── tests/                # Ground truth validation
├── duckdb/              # DuckDB warehouse file (gitignored)
└── README.md
```

## Setup Instructions

### Prerequisites
- Python 3.9+
- pip

### Installation

```bash
# Clone repository
git clone https://github.com/pc1493/factory-simulation.git
cd factory-simulation

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Initialize Database

```bash
python orchestration/init_database.py
```

### Generate Data

```bash
# Generate all 7 days of historical data
python -m data_generators.generate_data --all

# Generate specific date
python -m data_generators.generate_data --date 2025-12-01

# Verify generated data
python verify_data.py
```

### Sample Output

7 days of data generated (2025-12-01 to 2025-12-07):
- 212 total production batches
- 14,483 units produced
- 178 defective units (1.23%)
- 1,567 kWh energy consumed

See [DATA_SAMPLES.md](DATA_SAMPLES.md) for detailed examples.

### Run Dashboard

```bash
# Launch interactive dashboard
streamlit run streamlit_app/dashboard.py
```

Dashboard features:
- 🏭 Live machine status monitoring
- 📈 Efficiency degradation tracking
- 🔄 Product flow visualization
- 🚨 Real-time data quality alerts
- ⏯️ Time-travel through 7 days of data

See [streamlit_app/README.md](streamlit_app/README.md) for dashboard details.

## Architecture Decisions

### Data Generation Layer

**Decision**: Use Python with Faker for data generation instead of mock data libraries
- **Rationale**: Full control over chaos injection patterns and ground truth tracking
- **Trade-off**: More code to maintain vs. flexibility in simulating real-world issues

**Decision**: Generate ground truth separately from chaotic data
- **Rationale**: Enables validation that pipeline correctly cleans and aggregates data
- **Validation**: Pipeline output must match ground truth within 2% margin

**Decision**: Make chaos configurable via Python config instead of YAML
- **Rationale**: Simpler for Phase 1, easier to adjust programmatically
- **Future**: Could move to YAML if needed for non-technical users

### Controlled Chaos Patterns

Implemented chaos types:
1. **Product name variations**: 10 different spellings/casings
2. **Machine ID inconsistencies**: 5+ variations per machine in operator logs
3. **Null values**: 7.5% in sensor readings
4. **Timestamp drift**: ±5 minutes between systems
5. **Duplicates**: 3% of production batches
6. **Late-arriving data**: 10% chance, 1-2 day delay
7. **Timezone chaos**: 30% in local time (MST) vs UTC
8. **Performance degradation**: Smelter #2 loses 2% efficiency per day

### Dashboard Visualization Layer

**Decision**: Build 4-quadrant "factory control center" layout
- **Rationale**: Mental model of standing in a control room watching factory floor
- **Visual Design**: Industrial dark theme (#1e293b) with color-coded machine status

**Quadrants:**
1. **Production Floor** (Top-Left): Live machine cards with status, progress bars, efficiency metrics
2. **Machine Health Monitor** (Top-Right): Plotly line charts showing degradation over time, sensor gauges
3. **Product Flow Pipeline** (Bottom-Left): Sankey diagram visualizing ore → plates → gears
4. **Data Quality Alerts** (Bottom-Right): Real-time chaos detection with severity indicators

**Time Controls:**
- Play/Pause simulation with auto-advance
- Speed control: 1x, 10x, 100x, 1000x (watch 7 days in ~10 seconds at max speed)
- Day selection: Jump to any specific day
- Progress bar showing current position in timeline

**Color System:**
- 🟢 Healthy: >90% efficiency
- 🟡 Warning: 70-90% efficiency
- 🔴 Critical: <70% efficiency

## Progress Tracker

### Week 1: Foundation (Dec 6-13)
- [x] Project setup
- [x] Data generation scripts with controlled chaos
- [x] DuckDB initialization with bronze/silver/gold schemas
- [ ] Bronze layer ingestion
- [ ] Silver layer cleaning and standardization
- [ ] Gold layer dimensional model

### Week 2: Analytics & Polish (Dec 14-20)
- [x] Streamlit dashboard with 4-quadrant layout
- [x] Interactive time-travel controls
- [x] Real-time chaos visualization
- [ ] Ground truth validation testing
- [ ] End-to-end pipeline orchestration
- [ ] Documentation and examples

## Ground Truth Validation

Pipeline output must match generator's ground truth within 2% margin of error.

## Phase 2 Ideas (Post-December 20)
- Multiple factories
- Schema evolution
- Advanced chaos patterns
- ML predictions
- Cloud deployment

---

**Last Updated:** 2025-12-08
**Current Sprint:** Dashboard Complete - Interactive factory floor visualization with time-travel controls!
