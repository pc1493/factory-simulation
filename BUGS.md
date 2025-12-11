# Bug Tracker - Factory Simulation

**Last Updated:** 2025-12-10

---

## 🔴 CRITICAL (Must Fix Immediately)

### BUG-001: Division by Zero in verify_data.py
- **File:** `verify_data.py:50`
- **Severity:** Critical
- **Status:** 🔴 Open
- **Description:** Script crashes if no production data exists
- **Code:**
  ```python
  print(f"Total defective: {total_defects} ({total_defects/total_units*100:.2f}%)")
  ```
- **Fix:**
  ```python
  defect_pct = (total_defects/total_units*100) if total_units > 0 else 0
  print(f"Total defective: {total_defects} ({defect_pct:.2f}%)")
  ```

### BUG-002: Incorrect Timezone Conversion Logic
- **File:** `data_generators/chaos_injectors.py:107`
- **Severity:** Critical
- **Status:** 🔴 Open
- **Description:** Timezone conversion subtracts hours when it should add (or vice versa)
- **Code:**
  ```python
  return timestamp - timedelta(hours=7)  # Convert to MST (UTC-7)
  ```
- **Issue:** Comment says "convert to local time" but direction is unclear. MST is UTC-7, so:
  - FROM UTC TO MST: subtract 7 hours ✅ (current code)
  - FROM MST TO UTC: add 7 hours ❌ (not implemented)
- **Fix:** Clarify intent and ensure correct direction

### BUG-003: Division by Zero in Dashboard
- **File:** `streamlit_app/dashboard.py:506`
- **Severity:** Critical
- **Status:** 🔴 Open
- **Description:** Shows 0% defect rate when no production (misleading)
- **Code:**
  ```python
  defect_rate = (totals.get('units_defective', 0) / totals.get('units_produced', 1)) * 100
  ```
- **Fix:**
  ```python
  units = totals.get('units_produced', 0)
  defect_rate = (totals.get('units_defective', 0) / units * 100) if units > 0 else 0
  ```

### BUG-004: Hardcoded Start Date in Dashboard
- **File:** `streamlit_app/dashboard.py:90, 106, 118`
- **Severity:** Critical
- **Status:** 🔴 Open
- **Description:** Dashboard hardcodes Dec 1, 2025 as start date
- **Code:**
  ```python
  start_date = datetime(2025, 12, 1).date()
  ```
- **Impact:** Dashboard can't load data from different date ranges
- **Fix:**
  ```python
  from data_generators.config import START_DATE, END_DATE
  start_date = START_DATE
  ```

---

## 🟠 HIGH SEVERITY

### BUG-005: Null Sensor Data Crashes Dashboard
- **File:** `streamlit_app/dashboard.py:362, 367`
- **Severity:** High
- **Status:** 🟠 Open
- **Description:** Dashboard crashes if ALL sensor values are null
- **Code:**
  ```python
  avg_temp = sensor_data['temperature'].dropna().mean()
  st.metric("Avg Temperature", f"{avg_temp:.0f}°C")
  ```
- **Fix:**
  ```python
  avg_temp = sensor_data['temperature'].dropna().mean()
  if pd.isna(avg_temp):
      st.metric("Avg Temperature", "No Data")
  else:
      st.metric("Avg Temperature", f"{avg_temp:.0f}°C")
  ```

### BUG-006: Hardcoded Efficiency Calculation
- **File:** `streamlit_app/dashboard.py:262-264`
- **Severity:** High
- **Status:** 🟠 Open
- **Description:** Dashboard calculates efficiency instead of using actual data
- **Impact:** Dashboard efficiency doesn't match generated data (has ±1% variance)
- **Fix:** Load actual efficiency from ground_truth data

### BUG-007: Timestamp Type Mismatch
- **File:** `data_generators/generate_data.py:146`
- **Severity:** High
- **Status:** 🟠 Open
- **Description:** Sensor logs store timestamps as ISO strings, DB expects TIMESTAMP
- **Fix:** Standardize timestamp handling

### BUG-008: Confusing Date Indexing
- **File:** `streamlit_app/dashboard.py:107`
- **Severity:** High
- **Status:** 🟠 Open
- **Description:** Day selector uses 1-indexed days, but calculation uses `day - 1`
- **Fix:** Add clear documentation and verify indexing

---

## 🟡 MEDIUM SEVERITY

### BUG-009: Incomplete Chaos Injection
- **File:** `data_generators/generate_data.py:325-350`
- **Severity:** Medium
- **Status:** 🟡 Open
- **Description:** Production batches only get product name and duplicate chaos, missing machine ID and timestamp chaos
- **Fix:** Apply full chaos suite

### BUG-010: Energy Sensor Values Don't Match Batches
- **File:** `data_generators/generate_data.py:149`
- **Severity:** Medium
- **Status:** 🟡 Open
- **Description:** Sensor energy values are random (5-15 kWh), not proportional to batch energy
- **Fix:** Calculate based on batch energy

### BUG-011: Inconsistent Timezone Chaos Application
- **File:** `data_generators/generate_data.py:179, 233`
- **Severity:** Medium
- **Status:** 🟡 Open
- **Description:** Timezone chaos applied to QC and operator logs but not sensor logs
- **Fix:** Apply consistently or document rationale

### BUG-012: Operating Hours Boundary Issue
- **File:** `data_generators/generate_data.py:100-102`
- **Severity:** Medium
- **Status:** 🟡 Open
- **Description:** Batches can extend past 10 PM closing time
- **Fix:** Check batch_end time, not just current_time

---

## 🟢 LOW SEVERITY

### BUG-013: Hardcoded Sensor Ranges
- **File:** `data_generators/generate_data.py:134-138`
- **Severity:** Low
- **Status:** 🟢 Open
- **Description:** Temperature/pressure ranges hardcoded in function
- **Fix:** Move to config.py

### BUG-014: Magic Numbers in Dashboard
- **File:** `streamlit_app/dashboard.py` (multiple lines)
- **Severity:** Low
- **Status:** 🟢 Open
- **Description:** Threshold values scattered throughout code
- **Fix:** Define constants

### BUG-015: No Config Validation
- **File:** `data_generators/config.py`
- **Severity:** Low
- **Status:** 🟢 Open
- **Description:** No validation for invalid machine configs
- **Fix:** Add validation function

### BUG-016: Silent Data Loading Failures
- **File:** `streamlit_app/dashboard.py:95, 109, 121`
- **Severity:** Low
- **Status:** 🟢 Open
- **Description:** Functions return empty DataFrames silently when data missing
- **Fix:** Add warnings or logging

### BUG-017: Incorrect Sankey Flow Logic
- **File:** `streamlit_app/dashboard.py:391-403`
- **Severity:** Low
- **Status:** 🟢 Open
- **Description:** Sankey diagram shows incorrect product dependencies
- **Fix:** Build dynamically based on config

---

## 📊 Bug Summary

- **Critical:** 4 bugs
- **High:** 4 bugs
- **Medium:** 4 bugs
- **Low:** 5 bugs
- **Total:** 17 bugs

---

## 🎯 Priority Fix Order

1. BUG-001: Division by zero (verify_data.py)
2. BUG-003: Division by zero (dashboard.py)
3. BUG-004: Hardcoded dates (dashboard.py)
4. BUG-002: Timezone logic (chaos_injectors.py)
5. BUG-005: Null sensor data (dashboard.py)
6. BUG-006: Hardcoded efficiency (dashboard.py)
7. BUG-009: Incomplete chaos (generate_data.py)
8. BUG-010: Energy mismatch (generate_data.py)

Fix first 4 before continuing development.
