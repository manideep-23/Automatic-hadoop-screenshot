import os
import subprocess
import json
from datetime import datetime

from utils.logger import setup_logger
from utils.screenshot_taker import take_screenshot
from utils.app_status_checker import get_latest_app_id_and_status
from utils.report_generator import generate_word_report, generate_csv_report

# Load config
with open("config/config.json") as f:
    config = json.load(f)

logger = setup_logger(config['log_file'])

with open("config/job_order.txt") as f:
    job_scripts = [line.strip() for line in f if line.strip()]

job_records = []

for script in job_scripts:
    script_path = os.path.join("scripts", script)

    if not os.path.exists(script_path):
        logger.error(f"Script not found: {script_path}")
        continue

    logger.info(f"Starting job: {script}")
    start_time = datetime.now()

    os.chmod(script_path, 0o755)  # Ensure executable
    result = subprocess.run([f"./{script_path}"], shell=True, capture_output=True, text=True)

    end_time = datetime.now()

    app_id, status = get_latest_app_id_and_status(config['resourcemanager_url'])
    screenshot_path = take_screenshot(app_id, config) if app_id else "N/A"

    record = {
        "script": script,
        "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S"),
        "app_id": app_id or "N/A",
        "status": status,
        "command": f"./{script_path}",
        "screenshot": screenshot_path
    }

    job_records.append(record)

    logger.info(f"Completed job: {script} with status {status}")

# Save reports
os.makedirs(config['output_folder'], exist_ok=True)
generate_word_report(job_records, os.path.join(config['output_folder'], "job_report.docx"))
generate_csv_report(job_records, os.path.join(config['output_folder'], "job_report.csv"))

logger.info("All jobs completed.")
