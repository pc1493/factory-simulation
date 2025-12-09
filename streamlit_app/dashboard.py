"""
Factory Simulation Dashboard - Main Streamlit App
"""
import streamlit as st
import pandas as pd
import json
from pathlib import Path
from datetime import datetime, timedelta
import time
import plotly.graph_objects as go
import plotly.express as px

# Page config
st.set_page_config(
    page_title="Factory Control Center",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for industrial theme
st.markdown("""
<style>
    .main {
        background-color: #1e293b;
    }
    .stApp {
        background-color: #1e293b;
    }
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: bold;
        font-family: 'Courier New', monospace;
    }
    .metric-card {
        background-color: #0f172a;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #3b82f6;
    }
    .machine-card {
        background-color: #0f172a;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border: 2px solid #334155;
    }
    .machine-healthy {
        border-left: 6px solid #10b981;
    }
    .machine-warning {
        border-left: 6px solid #f59e0b;
    }
    .machine-critical {
        border-left: 6px solid #ef4444;
    }
    .alert-item {
        background-color: #1e293b;
        padding: 10px;
        margin: 5px 0;
        border-radius: 5px;
        border-left: 3px solid #f59e0b;
    }
    h1, h2, h3 {
        color: #e2e8f0;
    }
    p, span {
        color: #cbd5e1;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_day' not in st.session_state:
    st.session_state.current_day = 1
if 'current_time_offset' not in st.session_state:
    st.session_state.current_time_offset = 0
if 'is_playing' not in st.session_state:
    st.session_state.is_playing = False
if 'speed' not in st.session_state:
    st.session_state.speed = 100  # 100x speed
if 'last_update' not in st.session_state:
    st.session_state.last_update = time.time()

# Data loading functions
@st.cache_data
def load_all_data():
    """Load all 7 days of ground truth data."""
    data_by_day = {}
    start_date = datetime(2025, 12, 1).date()

    for day in range(7):
        date = start_date + timedelta(days=day)
        date_str = date.strftime("%Y-%m-%d")
        truth_file = Path(f"ground_truth/{date_str}/truth.json")

        if truth_file.exists():
            with open(truth_file) as f:
                data_by_day[day + 1] = json.load(f)

    return data_by_day

@st.cache_data
def load_raw_batches(day):
    """Load raw production batches for a specific day."""
    start_date = datetime(2025, 12, 1).date()
    date = start_date + timedelta(days=day - 1)
    date_str = date.strftime("%Y-%m-%d")
    batch_file = Path(f"raw_data/{date_str}/production_batches.csv")

    if batch_file.exists():
        return pd.read_csv(batch_file)
    return pd.DataFrame()

@st.cache_data
def load_sensor_logs(day):
    """Load sensor logs for a specific day."""
    start_date = datetime(2025, 12, 1).date()
    date = start_date + timedelta(days=day - 1)
    date_str = date.strftime("%Y-%m-%d")
    sensor_file = Path(f"raw_data/{date_str}/sensor_logs.json")

    if sensor_file.exists():
        with open(sensor_file) as f:
            data = json.load(f)
        return pd.DataFrame(data)
    return pd.DataFrame()

def get_machine_status(efficiency):
    """Determine machine status based on efficiency."""
    if efficiency >= 0.90:
        return "healthy", "🟢", "#10b981"
    elif efficiency >= 0.70:
        return "warning", "🟡", "#f59e0b"
    else:
        return "critical", "🔴", "#ef4444"

def calculate_chaos_metrics(day):
    """Calculate data quality chaos metrics."""
    batches = load_raw_batches(day)
    sensors = load_sensor_logs(day)

    chaos = {
        "null_count": 0,
        "null_percent": 0,
        "product_variations": 0,
        "duplicates": 0,
        "duplicate_percent": 0
    }

    if not sensors.empty:
        null_count = sensors.isnull().sum().sum()
        total_values = sensors.shape[0] * sensors.shape[1]
        chaos["null_count"] = int(null_count)
        chaos["null_percent"] = (null_count / total_values * 100) if total_values > 0 else 0

    if not batches.empty:
        chaos["product_variations"] = batches['product_name'].nunique()
        chaos["duplicates"] = batches['batch_id'].duplicated().sum()
        chaos["duplicate_percent"] = (chaos["duplicates"] / len(batches) * 100) if len(batches) > 0 else 0

    return chaos

# Load data
all_data = load_all_data()

# ============================================================================
# HEADER - Factory Control Center
# ============================================================================
st.title("🏭 FACTORY CONTROL CENTER")
st.markdown(f"### Dec 1-7, 2025 | Currently viewing: **Day {st.session_state.current_day}**")

# ============================================================================
# TOP CONTROL BAR
# ============================================================================
st.markdown("---")
col1, col2, col3, col4 = st.columns([2, 2, 2, 2])

with col1:
    st.markdown("#### 📅 Day Selection")
    day_select = st.selectbox(
        "Jump to Day:",
        options=[1, 2, 3, 4, 5, 6, 7],
        index=st.session_state.current_day - 1,
        key="day_selector"
    )
    if day_select != st.session_state.current_day:
        st.session_state.current_day = day_select
        st.rerun()

with col2:
    st.markdown("#### ⏯️ Playback Controls")
    play_col, pause_col, reset_col = st.columns(3)
    with play_col:
        if st.button("▶ Play", use_container_width=True):
            st.session_state.is_playing = True
    with pause_col:
        if st.button("⏸ Pause", use_container_width=True):
            st.session_state.is_playing = False
    with reset_col:
        if st.button("↻ Reset", use_container_width=True):
            st.session_state.current_day = 1
            st.session_state.current_time_offset = 0
            st.rerun()

with col3:
    st.markdown("#### ⚡ Speed Control")
    speed = st.select_slider(
        "Simulation Speed:",
        options=[1, 10, 100, 1000],
        value=st.session_state.speed,
        format_func=lambda x: f"{x}x",
        key="speed_selector"
    )
    if speed != st.session_state.speed:
        st.session_state.speed = speed

with col4:
    st.markdown("#### 📊 Progress")
    progress = (st.session_state.current_day - 1) / 6
    st.progress(progress, text=f"Day {st.session_state.current_day} of 7")

st.markdown("---")

# Get current day data
current_data = all_data.get(st.session_state.current_day, {})

# ============================================================================
# MAIN DASHBOARD - 4 QUADRANTS
# ============================================================================

# Top row
top_left, top_right = st.columns([6, 4])

# ============================================================================
# QUADRANT 1: PRODUCTION FLOOR (Top Left)
# ============================================================================
with top_left:
    st.markdown("### 🏭 PRODUCTION FLOOR")

    if current_data:
        machines_data = current_data.get('by_machine', {})

        # Display 3 machine cards
        machine_cols = st.columns(3)

        machine_configs = [
            ("SMELTER-01", "🔥", machines_data.get("SMELTER-01", {})),
            ("SMELTER-02", "🔥", machines_data.get("SMELTER-02", {})),
            ("ASSEMBLER-01", "⚙️", machines_data.get("ASSEMBLER-01", {}))
        ]

        for idx, (machine_id, icon, data) in enumerate(machine_configs):
            with machine_cols[idx]:
                if data:
                    batches = data.get('batches', 0)
                    units = data.get('units_produced', 0)
                    energy = data.get('energy_consumed_kwh', 0)

                    # Calculate efficiency (degradation for SMELTER-02)
                    if machine_id == "SMELTER-02":
                        base_efficiency = 1.0 - (0.02 * (st.session_state.current_day - 1))
                    else:
                        base_efficiency = 0.98 if machine_id == "SMELTER-01" else 0.95

                    status, status_icon, color = get_machine_status(base_efficiency)

                    # Machine card
                    st.markdown(f"""
                    <div class="machine-card machine-{status}">
                        <h3>{icon} {machine_id}</h3>
                        <p><strong>Status:</strong> {status_icon} {status.upper()}</p>
                        <p><strong>Batches:</strong> {batches}</p>
                        <p><strong>Units:</strong> {units:,}</p>
                        <p><strong>Energy:</strong> {energy:.2f} kWh</p>
                    </div>
                    """, unsafe_allow_html=True)

                    # Efficiency meter
                    st.metric(
                        "Efficiency",
                        f"{base_efficiency*100:.1f}%",
                        delta=f"{-2.0 if machine_id == 'SMELTER-02' else 0}%" if st.session_state.current_day > 1 else None,
                        delta_color="inverse"
                    )

                    # Progress bar
                    avg_per_batch = units / batches if batches > 0 else 0
                    progress_val = min(avg_per_batch / 100, 1.0)
                    st.progress(progress_val, text=f"{avg_per_batch:.0f} units/batch")

# ============================================================================
# QUADRANT 2: MACHINE HEALTH MONITOR (Top Right)
# ============================================================================
with top_right:
    st.markdown("### 📈 MACHINE HEALTH MONITOR")

    # Build efficiency over time chart
    days = list(range(1, 8))
    smelter1_eff = [0.98] * 7
    smelter2_eff = [1.0 - (0.02 * (d-1)) for d in days]
    assembler_eff = [0.95] * 7

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=days, y=smelter1_eff,
        mode='lines+markers',
        name='Smelter #1',
        line=dict(color='#10b981', width=3),
        marker=dict(size=8)
    ))

    fig.add_trace(go.Scatter(
        x=days, y=smelter2_eff,
        mode='lines+markers',
        name='Smelter #2 (Degrading)',
        line=dict(color='#ef4444', width=3),
        marker=dict(size=8)
    ))

    fig.add_trace(go.Scatter(
        x=days, y=assembler_eff,
        mode='lines+markers',
        name='Assembler #1',
        line=dict(color='#3b82f6', width=3),
        marker=dict(size=8)
    ))

    # Add vertical line for current day
    fig.add_vline(
        x=st.session_state.current_day,
        line_dash="dash",
        line_color="#f59e0b",
        line_width=2,
        annotation_text="Current Day"
    )

    fig.update_layout(
        title="Efficiency Over Time",
        xaxis_title="Day",
        yaxis_title="Efficiency",
        yaxis=dict(range=[0.5, 1.05], tickformat='.0%'),
        plot_bgcolor='#0f172a',
        paper_bgcolor='#0f172a',
        font=dict(color='#e2e8f0'),
        hovermode='x unified',
        height=350
    )

    st.plotly_chart(fig, use_container_width=True)

    # Real-time sensor gauges
    st.markdown("#### 🌡️ Real-Time Sensors (Latest Readings)")
    sensor_data = load_sensor_logs(st.session_state.current_day)

    if not sensor_data.empty:
        gauge_cols = st.columns(2)

        # Temperature gauge
        with gauge_cols[0]:
            avg_temp = sensor_data['temperature'].dropna().mean()
            st.metric("Avg Temperature", f"{avg_temp:.0f}°C", delta="±25°C variance")

        # Pressure gauge
        with gauge_cols[1]:
            avg_pressure = sensor_data['pressure'].dropna().mean()
            st.metric("Avg Pressure", f"{avg_pressure:.2f} bar", delta="±0.3 variance")

# Bottom row
bottom_left, bottom_right = st.columns([6, 4])

# ============================================================================
# QUADRANT 3: PRODUCT FLOW PIPELINE (Bottom Left)
# ============================================================================
with bottom_left:
    st.markdown("### 🔄 PRODUCT FLOW PIPELINE")

    if current_data:
        products = current_data.get('by_product', {})

        # Create Sankey diagram
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=["Iron Ore", "Smelter #1", "Smelter #2", "Iron Plates", "Assembler #1", "Gear Wheels"],
                color=["#92400e", "#ef4444", "#ef4444", "#94a3b8", "#3b82f6", "#fbbf24"]
            ),
            link=dict(
                source=[0, 0, 1, 2, 3, 4],
                target=[1, 2, 3, 3, 4, 5],
                value=[
                    machines_data.get("SMELTER-01", {}).get('units_produced', 0),
                    machines_data.get("SMELTER-02", {}).get('units_produced', 0),
                    machines_data.get("SMELTER-01", {}).get('units_produced', 0),
                    machines_data.get("SMELTER-02", {}).get('units_produced', 0),
                    products.get("Iron Plate", {}).get('units_produced', 0),
                    products.get("Gear Wheel", {}).get('units_produced', 0)
                ],
                color=["rgba(239, 68, 68, 0.4)"] * 6
            )
        )])

        fig.update_layout(
            title="Material Flow",
            plot_bgcolor='#0f172a',
            paper_bgcolor='#0f172a',
            font=dict(size=12, color='#e2e8f0'),
            height=300
        )

        st.plotly_chart(fig, use_container_width=True)

        # Daily production summary
        st.markdown("#### 📦 Daily Production Summary")
        prod_cols = st.columns(3)

        with prod_cols[0]:
            iron_ore = machines_data.get("SMELTER-01", {}).get('units_produced', 0) + \
                       machines_data.get("SMELTER-02", {}).get('units_produced', 0)
            st.metric("🟤 Iron Ore Consumed", f"{iron_ore:,}")

        with prod_cols[1]:
            plates = products.get("Iron Plate", {}).get('units_produced', 0)
            st.metric("⬜ Iron Plates", f"{plates:,}")

        with prod_cols[2]:
            gears = products.get("Gear Wheel", {}).get('units_produced', 0)
            st.metric("⚙️ Gear Wheels", f"{gears:,}")

# ============================================================================
# QUADRANT 4: DATA QUALITY ALERTS (Bottom Right)
# ============================================================================
with bottom_right:
    st.markdown("### 🚨 DATA QUALITY ALERTS")

    chaos = calculate_chaos_metrics(st.session_state.current_day)

    # Chaos metrics
    st.markdown("#### Chaos Detected:")

    # Null values
    null_severity = "🔴" if chaos['null_percent'] > 10 else "🟡" if chaos['null_percent'] > 5 else "🟢"
    st.markdown(f"{null_severity} **Null Values:** {chaos['null_count']} ({chaos['null_percent']:.1f}%)")
    st.progress(min(chaos['null_percent'] / 20, 1.0))

    # Product variations
    var_severity = "🔴" if chaos['product_variations'] > 8 else "🟡" if chaos['product_variations'] > 5 else "🟢"
    st.markdown(f"{var_severity} **Product Name Variations:** {chaos['product_variations']} found")
    st.progress(min(chaos['product_variations'] / 10, 1.0))

    # Duplicates
    dup_severity = "🔴" if chaos['duplicate_percent'] > 5 else "🟡" if chaos['duplicate_percent'] > 2 else "🟢"
    st.markdown(f"{dup_severity} **Duplicate Batches:** {chaos['duplicates']} ({chaos['duplicate_percent']:.1f}%)")
    st.progress(min(chaos['duplicate_percent'] / 10, 1.0))

    # Machine ID variations
    st.markdown("🟡 **Machine ID Variations:** 5+ detected")
    st.progress(0.5)

    # Timestamp drift
    st.markdown("🟠 **Timestamp Drift:** ±5 min variance")
    st.progress(0.4)

    st.markdown("---")
    st.markdown("#### 📋 Recent Events:")

    # Sample event log
    events = [
        ("⚠️", "Null temperature detected on SMELTER-01"),
        ("📝", f"Product name variation: found {chaos['product_variations']} spellings"),
        ("🔁", f"{chaos['duplicates']} duplicate batches detected"),
        ("⏰", "Timestamp drift: +4 minutes detected"),
        ("🔧", "Machine ID variation: 'Smelter-2' vs 'SMELTER-02'")
    ]

    for icon, event in events[:5]:
        st.markdown(f"""
        <div class="alert-item">
            {icon} {event}
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# BOTTOM STATS BAR
# ============================================================================
st.markdown("---")
st.markdown("### 📊 Factory Totals (Current Day)")

if current_data:
    totals = current_data.get('factory_totals', {})
    stat_cols = st.columns(5)

    with stat_cols[0]:
        st.metric("Total Batches", current_data.get('total_batches', 0))

    with stat_cols[1]:
        st.metric("Units Produced", f"{totals.get('units_produced', 0):,}")

    with stat_cols[2]:
        st.metric("Defective Units", totals.get('units_defective', 0))

    with stat_cols[3]:
        defect_rate = (totals.get('units_defective', 0) / totals.get('units_produced', 1)) * 100
        st.metric("Defect Rate", f"{defect_rate:.2f}%")

    with stat_cols[4]:
        st.metric("Energy Consumed", f"{totals.get('energy_consumed_kwh', 0):.2f} kWh")

# ============================================================================
# AUTO-PLAY LOGIC
# ============================================================================
if st.session_state.is_playing:
    time.sleep(2 / st.session_state.speed)  # Update based on speed

    # Advance to next day
    if st.session_state.current_day < 7:
        st.session_state.current_day += 1
        st.rerun()
    else:
        st.session_state.is_playing = False
        st.info("🎬 Simulation complete! Press Reset to start over.")
