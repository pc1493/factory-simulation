"""
Daily Data Generation Scheduler using APScheduler.

This script runs as a long-running process to automatically generate
factory simulation data daily at a specified time.

Usage:
    python scheduler.py

To stop: Press Ctrl+C
"""
import logging
from datetime import datetime
from pathlib import Path
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from data_generators.generate_data import generate_day

# Create logs directory if it doesn't exist
LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / 'scheduler.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def daily_generation_job():
    """
    Daily job to generate factory simulation data.

    This runs automatically at the scheduled time and generates
    data for the current date.
    """
    try:
        today = datetime.now()
        logger.info(f"=" * 60)
        logger.info(f"Starting daily data generation for {today.strftime('%Y-%m-%d')}")
        logger.info(f"=" * 60)

        # Generate data for today
        generate_day(today)

        logger.info(f"=" * 60)
        logger.info(f"Successfully completed data generation for {today.strftime('%Y-%m-%d')}")
        logger.info(f"=" * 60)

    except Exception as e:
        logger.error(f"Data generation FAILED: {e}", exc_info=True)
        raise


def main():
    """
    Start the APScheduler with daily data generation job.

    The scheduler will run continuously and execute the job
    daily at 9:00 AM local time.
    """
    logger.info("=" * 70)
    logger.info("FACTORY DATA SCHEDULER STARTING")
    logger.info("=" * 70)

    # Create scheduler
    scheduler = BlockingScheduler()

    # Add daily job at 9:00 AM
    scheduler.add_job(
        daily_generation_job,
        CronTrigger(hour=9, minute=0),  # Run at 9:00 AM daily
        id='daily_factory_data',
        name='Generate Daily Factory Data',
        replace_existing=True
    )

    # Log scheduled jobs
    logger.info("\nScheduled Jobs:")
    for job in scheduler.get_jobs():
        logger.info(f"  - {job.name}")
        logger.info(f"    ID: {job.id}")
        logger.info(f"    Next run: {job.next_run_time}")
        logger.info(f"    Trigger: Daily at 9:00 AM")

    logger.info("\n" + "=" * 70)
    logger.info("Scheduler is running. Press Ctrl+C to stop.")
    logger.info("=" * 70 + "\n")

    try:
        # Start the scheduler (this blocks)
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("\n" + "=" * 70)
        logger.info("Scheduler stopped by user")
        logger.info("=" * 70)


if __name__ == '__main__':
    main()
