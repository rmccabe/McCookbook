#!/usr/bin/env python3
"""
A demo script showcasing breadth of Python knowledge via multiple libraries
commonly used in a production support context in large financial institutions.

Libraries used and demonstrated:
  1) logging (Standard Library)
  2) requests
  3) paramiko
  4) psycopg2
  5) yaml (PyYAML)
  6) cryptography (Fernet)
  7) pandas
  8) multiprocessing (Standard Library)

Note: 
  - You may need to `pip install requests paramiko psycopg2-binary pyyaml cryptography pandas`
    and possibly `pip install psycopg2` or `apt-get install libpq-dev python3-dev` for full DB support.
  - Replace sample credentials, server IPs, database details, etc. for real usage.
"""

import logging
import sys
import os
import time
import requests
import paramiko
import psycopg2
import yaml
from cryptography.fernet import Fernet
import pandas as pd
from multiprocessing import Process, Queue


# ------------------------------------------------------------------------------
# 1) LOGGING SETUP
# ------------------------------------------------------------------------------

# Basic logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        # You could add a FileHandler or SysLogHandler for production
    ]
)
logger = logging.getLogger("ProdSupportDemo")


# ------------------------------------------------------------------------------
# 2) REQUESTS EXAMPLE
# ------------------------------------------------------------------------------

def fetch_data_from_api(api_url):
    """
    Demonstrates fetching JSON data from an external API.
    For production usage, handle exceptions, timeouts, authentication, etc.
    """
    try:
        logger.info(f"Fetching data from {api_url}")
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()  # raise an HTTPError if the status is >= 400
        data = response.json()
        logger.info("Data fetched successfully!")
        return data
    except requests.RequestException as e:
        logger.error(f"API request failed: {e}")
        return {}


# ------------------------------------------------------------------------------
# 3) PARAMIKO (SSH) EXAMPLE
# ------------------------------------------------------------------------------

def ssh_demo(server_ip, username, password):
    """
    Demonstrates creating an SSH client, executing a command on a remote server,
    and retrieving output.
    NOTE: For secure production usage, consider more secure credential handling (keys).
    """
    client = paramiko.SSHClient()
    # Auto-accept unknown host keys (NOT recommended in production without caution)
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        logger.info(f"Connecting to SSH server at {server_ip}")
        client.connect(server_ip, username=username, password=password, timeout=5)

        stdin, stdout, stderr = client.exec_command("echo 'Hello from Paramiko!'")
        logger.info("Command executed on remote server.")
        
        output = stdout.read().decode().strip()
        err = stderr.read().decode().strip()

        logger.info(f"STDOUT: {output}")
        if err:
            logger.warning(f"STDERR: {err}")

    except Exception as e:
        logger.error(f"SSH connection failed: {e}")
    finally:
        client.close()


# ------------------------------------------------------------------------------
# 4) PSYCOPG2 (PostgreSQL) EXAMPLE
# ------------------------------------------------------------------------------

def query_database(db_config):
    """
    Demonstrates connecting to a PostgreSQL database using psycopg2
    and executing a basic SELECT query.
    'db_config' should be a dict with keys: dbname, user, password, host, port
    """
    conn = None
    try:
        logger.info("Connecting to PostgreSQL database...")
        conn = psycopg2.connect(**db_config)  # e.g., dbname='testdb', user='dbuser', etc.
        cur = conn.cursor()

        # Simple query: get current date/time from DB
        cur.execute("SELECT NOW();")
        row = cur.fetchone()
        logger.info(f"Database current time: {row[0]}")

        cur.close()
    except Exception as e:
        logger.error(f"Database operation failed: {e}")
    finally:
        if conn:
            conn.close()


# ------------------------------------------------------------------------------
# 5) YAML (CONFIG) EXAMPLE
# ------------------------------------------------------------------------------

def load_config(config_path):
    """
    Demonstrates reading a YAML config file and returning its contents as a dict.
    """
    if not os.path.exists(config_path):
        logger.warning(f"Config file '{config_path}' not found.")
        return {}

    logger.info(f"Loading YAML config from {config_path}")
    with open(config_path, "r") as f:
        config_data = yaml.safe_load(f)
    logger.info(f"Config loaded: {config_data}")
    return config_data


# ------------------------------------------------------------------------------
# 6) CRYPTOGRAPHY (FERNET) EXAMPLE
# ------------------------------------------------------------------------------

def encrypt_decrypt_demo(message):
    """
    Demonstrates encrypting and decrypting a message with the Fernet symmetric key.
    """
    # Generate a key (in real usage, store/retrieve securely)
    key = Fernet.generate_key()
    cipher = Fernet(key)

    logger.info(f"Original message: {message}")
    encrypted = cipher.encrypt(message.encode('utf-8'))
    logger.info(f"Encrypted message: {encrypted}")

    decrypted = cipher.decrypt(encrypted).decode('utf-8')
    logger.info(f"Decrypted message: {decrypted}")


# ------------------------------------------------------------------------------
# 7) PANDAS EXAMPLE
# ------------------------------------------------------------------------------

def analyze_data_with_pandas(data):
    """
    Demonstrates using pandas to turn a list of dicts into a DataFrame
    and performing some basic analysis.
    'data' can be any list of dictionaries. We'll do a trivial example.
    """
    if not data:
        logger.warning("No data provided to analyze.")
        return

    df = pd.DataFrame(data)
    logger.info(f"DataFrame created:\n{df}")

    # Example: show descriptive stats if numeric columns exist
    try:
        stats = df.describe()
        logger.info(f"Descriptive statistics:\n{stats}")
    except ValueError as e:
        logger.info("No numeric data to describe.")


# ------------------------------------------------------------------------------
# 8) MULTIPROCESSING EXAMPLE
# ------------------------------------------------------------------------------

def worker_process(queue, idx):
    """Simple worker that reads data from a queue, 'processes' it, and logs results."""
    while not queue.empty():
        item = queue.get()
        logger.info(f"[Worker {idx}] Processing item: {item}")
        time.sleep(0.5)  # Simulate some work


def run_multiprocessing_demo(data_items):
    """
    Demonstrates the multiprocessing library by creating multiple worker processes
    that pull tasks from a shared queue.
    """
    queue = Queue()
    for item in data_items:
        queue.put(item)

    processes = []
    num_workers = 2  # For example
    for i in range(num_workers):
        p = Process(target=worker_process, args=(queue, i))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()


# ------------------------------------------------------------------------------
# MAIN ENTRY POINT
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    logger.info("=== Production Support Demo Script Start ===")

    # 1) logging - already configured above.

    # 2) requests
    sample_api_url = "https://jsonplaceholder.typicode.com/posts?_limit=5"
    api_data = fetch_data_from_api(sample_api_url)

    # 3) paramiko (SSH)
    # For demonstration, these credentials/host are placeholders
    # Replace with valid ones for a real environment
    # ssh_demo("192.168.1.10", "myuser", "mypassword")

    # 4) psycopg2 (DB)
    # db_config = {
    #     "dbname": "testdb",
    #     "user": "dbuser",
    #     "password": "dbpass",
    #     "host": "127.0.0.1",
    #     "port": 5432,
    # }
    # query_database(db_config)

    # 5) YAML config
    # config = load_config("app_config.yaml")

    # 6) cryptography
    encrypt_decrypt_demo("Secret message!")

    # 7) pandas
    # We'll use the data fetched from the API (which is a list of dicts) as a simple example
    analyze_data_with_pandas(api_data)

    # 8) multiprocessing
    # We'll just demonstrate parallel processing on some test data
    run_multiprocessing_demo(["task1", "task2", "task3", "task4"])

    logger.info("=== Production Support Demo Script End ===")
