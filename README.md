# Factorio-Style Data Pipeline Simulator

**Status:** 🚧 In Development
**Timeline:** Dec 6 - Dec 20, 2025
**Current Phase:** Setup

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

**Coming soon after Week 1 implementation**

## Architecture Decisions

**Coming soon - tracking major design decisions here**

## Progress Tracker

### Week 1: Foundation ✅/❌
- [ ] Project setup
- [ ] Data generation scripts
- [ ] Bronze layer
- [ ] Silver layer
- [ ] Gold layer

### Week 2: Dashboard & Polish ✅/❌
- [ ] Streamlit dashboard
- [ ] Ground truth validation
- [ ] End-to-end testing
- [ ] Documentation

## Ground Truth Validation

Pipeline output must match generator's ground truth within 2% margin of error.

## Phase 2 Ideas (Post-December 20)
- Multiple factories
- Schema evolution
- Advanced chaos patterns
- ML predictions
- Cloud deployment

---

**Last Updated:** 2025-12-06
**Current Sprint:** Week 1 - Setup & Data Generation
