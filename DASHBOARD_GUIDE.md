# Factory Dashboard - Quick Start Guide

## Launch the Dashboard

```bash
streamlit run streamlit_app/dashboard.py
```

The dashboard will open at: **http://localhost:8501**

## Dashboard Overview

### 🎮 Control Center Layout

```
┌─────────────────────────────────────────────────────────────┐
│  🏭 FACTORY CONTROL CENTER                                  │
│  [Day Selector] [▶ Play] [⏸ Pause] [↻ Reset] [Speed: 100x]│
├─────────────────────────┬───────────────────────────────────┤
│  🏭 PRODUCTION FLOOR    │  📈 MACHINE HEALTH MONITOR        │
│  - Smelter #1 Card      │  - Efficiency Line Chart          │
│  - Smelter #2 Card      │  - Real-Time Sensor Gauges        │
│  - Assembler #1 Card    │  - Temperature/Pressure Readings  │
├─────────────────────────┼───────────────────────────────────┤
│  🔄 PRODUCT FLOW        │  🚨 DATA QUALITY ALERTS           │
│  - Sankey Diagram       │  - Null Values: 7.8%              │
│  - Material Pipeline    │  - Product Variations: 10         │
│  - Production Metrics   │  - Duplicate Batches: 3.2%        │
└─────────────────────────┴───────────────────────────────────┘
```

## How to Use

### 1. Navigate Through Time

**Jump to Specific Day:**
- Use the "Jump to Day" dropdown to select Day 1-7
- Dashboard instantly updates to show that day's data

**Auto-Play Mode:**
- Click **▶ Play** to start auto-advancing through days
- Adjust **Speed** slider: 1x, 10x, 100x, or 1000x
  - **1000x speed** = watch all 7 days in ~10 seconds!
- Click **⏸ Pause** to stop
- Click **↻ Reset** to go back to Day 1

### 2. Monitor Machine Health

**Watch Smelter #2 Degrade:**
- Look at the efficiency line chart (top-right)
- Red line shows Smelter #2 dropping from 100% to 88% over 7 days
- Green line (Smelter #1) stays steady at 98%
- Blue line (Assembler #1) stays at 95%

**Machine Status Colors:**
- 🟢 **Green**: Healthy (>90% efficiency)
- 🟡 **Yellow**: Warning (70-90%)
- 🔴 **Red**: Critical (<70%)

### 3. Track Production

**Machine Cards (Top-Left):**
Each card shows:
- Current status (RUNNING/IDLE)
- Number of batches completed
- Units produced
- Energy consumed (kWh)
- Efficiency percentage

**Product Flow (Bottom-Left):**
- Sankey diagram shows material transformation
- Width of flow = volume of production
- Summary metrics for Ore, Plates, Gears

### 4. Monitor Data Quality

**Chaos Alerts (Bottom-Right):**
- **Null Values**: Percentage of missing sensor readings
- **Product Variations**: Different spellings detected
- **Duplicates**: Percentage of duplicate batches
- **Machine ID Variations**: Inconsistent naming
- **Event Log**: Recent data quality issues

**Progress Bars:**
- Shows severity of each chaos type
- Longer bar = more chaos detected

## What to Look For

### Day 1 (Baseline)
- All machines healthy
- Smelter #2 at 100% efficiency
- ~35 batches total
- ~2,400 units produced

### Day 4 (Mid-Point)
- Smelter #2 drops to ~94% efficiency
- Yellow warning may appear
- Production slightly lower

### Day 7 (End State)
- Smelter #2 at 88% efficiency
- Clear degradation visible in chart
- Production impact observable
- ~27 batches (vs 35 on Day 1)

## Speed Guide

| Speed | 1 Day Takes | Full 7 Days |
|-------|-------------|-------------|
| 1x    | ~2 seconds  | ~14 seconds |
| 10x   | ~0.2 sec    | ~1.4 sec    |
| 100x  | ~0.02 sec   | ~0.14 sec   |
| 1000x | ~0.002 sec  | ~10 sec     |

**Recommended:** Start at **100x** for smooth visualization

## Tips & Tricks

1. **Hover over charts** to see exact values at each point
2. **Watch the event log** in bottom-right for chaos detection
3. **Compare machine cards** to spot degradation
4. **Use Play mode** to see trends over time
5. **Pause at Day 7** to compare with Day 1

## Troubleshooting

**Dashboard won't load?**
- Make sure you ran `python -m data_generators.generate_data --all` first
- Check that `ground_truth/` and `raw_data/` directories exist
- Verify you're in the project root directory

**Charts not showing?**
- Data may still be loading (check console)
- Try refreshing the browser (F5)

**Auto-play not working?**
- Click Pause then Play again
- Try a different speed setting
- Reset and try again

## Advanced Features

### Session State
Dashboard remembers:
- Current day
- Playback state (playing/paused)
- Speed setting

### Data Caching
- Ground truth data cached for performance
- Raw batch/sensor data cached per day
- Chaos metrics calculated on demand

### Interactive Elements
- Click day selector for instant jump
- Adjust speed mid-playback
- Charts are zoomable (Plotly)

## What This Shows You

✅ **Real-time monitoring** - See factory status at any point in time
✅ **Degradation tracking** - Watch Smelter #2 performance drop
✅ **Material flow** - Understand product transformation pipeline
✅ **Data quality** - Identify chaos patterns immediately
✅ **Time-travel** - Jump to any day or auto-play through timeline

## Next Steps

After exploring the dashboard, you can:
1. Build **Bronze layer** to ingest this raw data into DuckDB
2. Build **Silver layer** to clean and standardize the chaos
3. Build **Gold layer** for dimensional modeling
4. Compare dashboard metrics to ground truth for validation

---

**Pro Tip:** Run at 1000x speed and watch the efficiency chart closely. You'll see Smelter #2's red line steadily decline while the others stay flat - this is the degradation pattern you'll need to detect and analyze in your data pipeline!
