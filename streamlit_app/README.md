# Factory Simulation Dashboard

Interactive Streamlit dashboard for visualizing the factory simulation data pipeline.

## Features

### 🏭 Production Floor
- Live machine status cards for 3 machines
- Real-time efficiency metrics
- Visual status indicators (healthy/warning/critical)
- Production progress bars

### 📈 Machine Health Monitor
- Efficiency degradation tracking over 7 days
- Real-time sensor gauges (temperature, pressure)
- Visual alerts for Smelter #2 performance drop

### 🔄 Product Flow Pipeline
- Sankey diagram showing material flow
- Iron Ore → Iron Plates → Gear Wheels
- Daily production summaries

### 🚨 Data Quality Alerts
- Null value detection and percentages
- Product name variation tracking
- Duplicate batch detection
- Timestamp drift monitoring
- Machine ID inconsistencies

### ⏯️ Time Controls
- Play/Pause simulation
- Speed control (1x, 10x, 100x, 1000x)
- Day selection (jump to any day)
- Progress tracking

## Running the Dashboard

```bash
# From project root
streamlit run streamlit_app/dashboard.py
```

The dashboard will open in your browser at http://localhost:8501

## Usage

1. **Day Selection**: Use the dropdown to jump to any day (1-7)
2. **Play Simulation**: Click "Play" to auto-advance through days
3. **Speed Control**: Adjust simulation speed (1000x = see all 7 days in ~10 seconds)
4. **Monitor Degradation**: Watch Smelter #2 efficiency drop from 100% to 88% over 7 days
5. **Track Chaos**: See data quality issues in real-time in the alerts panel

## Visual Theme

- Industrial dark mode (#1e293b background)
- Color-coded machine status:
  - 🟢 Green: Healthy (>90% efficiency)
  - 🟡 Yellow: Warning (70-90%)
  - 🔴 Red: Critical (<70%)

## Data Sources

Dashboard reads from:
- `ground_truth/{date}/truth.json` - Clean metrics for each day
- `raw_data/{date}/production_batches.csv` - Chaotic batch data
- `raw_data/{date}/sensor_logs.json` - Sensor readings with nulls

## Key Visualizations

1. **Efficiency Line Chart**: Shows all 3 machines' performance over 7 days
2. **Sankey Flow Diagram**: Material transformation pipeline
3. **Machine Cards**: Real-time status with metrics
4. **Chaos Progress Bars**: Visual indicators of data quality issues

## Auto-Play Behavior

When "Play" is active:
- Dashboard auto-advances to next day
- Update frequency based on speed setting
- Auto-pauses at Day 7
- Shows completion message

## Responsive Design

Dashboard adapts to different screen sizes with Streamlit's column system.
