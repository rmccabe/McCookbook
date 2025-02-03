# 4_production_support_example.py
#
# Demonstrates a typical production support script that connects
# to remote servers, fetches logs, and checks for errors.

import paramiko
import re

def check_logs_for_errors(host, username, password, log_path):
    """
    SSH into a remote host, read the log file,
    search for critical errors, and print them.
    """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(host, username=username, password=password, timeout=5)
        sftp = client.open_sftp()
        remote_file = sftp.open(log_path, "r")

        error_pattern = re.compile(r"ERROR|CRITICAL")
        for line in remote_file:
            if error_pattern.search(line):
                print(f"[{host}] {line.strip()}")

        remote_file.close()
        sftp.close()
    except Exception as e:
        print(f"Error connecting to {host} or reading file: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    # Example usage:
    servers = [
        {"host": "192.168.1.101", "user": "devops", "pass": "secret123", "log": "/var/log/trading_app.log"},
        {"host": "192.168.1.102", "user": "devops", "pass": "secret123", "log": "/var/log/trading_app.log"},
    ]

    for srv in servers:
        print(f"Checking logs on {srv['host']}...")
        check_logs_for_errors(
            host=srv["host"],
            username=srv["user"],
            password=srv["pass"],
            log_path=srv["log"]
        )
