"""
Initialize DuckDB warehouse with bronze, silver, and gold schemas.
"""
import duckdb
from pathlib import Path

# Database path
DB_PATH = Path(__file__).parent.parent / "duckdb" / "warehouse.db"

def init_database():
    """Create DuckDB database and initialize schemas."""

    # Ensure duckdb directory exists
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Connect to DuckDB
    con = duckdb.connect(str(DB_PATH))

    print(f"Initializing database at: {DB_PATH}")

    # Create schemas
    con.execute("CREATE SCHEMA IF NOT EXISTS bronze")
    con.execute("CREATE SCHEMA IF NOT EXISTS silver")
    con.execute("CREATE SCHEMA IF NOT EXISTS gold")

    print("[OK] Created schemas: bronze, silver, gold")

    # Create bronze tables (will be populated by ingestion scripts)
    # These are raw, immutable tables with metadata

    con.execute("""
        CREATE TABLE IF NOT EXISTS bronze.sensor_logs (
            machine_id VARCHAR,
            timestamp TIMESTAMP,
            temperature DOUBLE,
            pressure DOUBLE,
            energy_kwh DOUBLE,
            efficiency_percent DOUBLE,
            _loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            _source_file VARCHAR
        )
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS bronze.production_batches (
            batch_id VARCHAR,
            machine_id VARCHAR,
            product_name VARCHAR,
            start_time TIMESTAMP,
            end_time TIMESTAMP,
            units_produced INTEGER,
            units_defective INTEGER,
            _loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            _source_file VARCHAR
        )
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS bronze.qc_checks (
            check_id VARCHAR,
            batch_id VARCHAR,
            check_timestamp TIMESTAMP,
            inspector_id VARCHAR,
            pass_fail VARCHAR,
            defect_notes VARCHAR,
            _loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            _source_file VARCHAR
        )
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS bronze.operator_logs (
            log_id VARCHAR,
            machine_id VARCHAR,
            operator_id VARCHAR,
            log_timestamp TIMESTAMP,
            action VARCHAR,
            notes VARCHAR,
            _loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            _source_file VARCHAR
        )
    """)

    print("[OK] Created bronze tables:")
    print("  - bronze.sensor_logs")
    print("  - bronze.production_batches")
    print("  - bronze.qc_checks")
    print("  - bronze.operator_logs")

    # Verify schemas
    schemas = con.execute("SELECT schema_name FROM information_schema.schemata WHERE schema_name IN ('bronze', 'silver', 'gold')").fetchall()
    print(f"\n[OK] Verified {len(schemas)} schemas created")

    # Verify tables
    tables = con.execute("SELECT table_schema, table_name FROM information_schema.tables WHERE table_schema = 'bronze'").fetchall()
    print(f"[OK] Verified {len(tables)} bronze tables created")

    con.close()
    print("\n[SUCCESS] Database initialization complete!")

if __name__ == "__main__":
    init_database()
