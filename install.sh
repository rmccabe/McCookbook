#!/usr/bin/env bash
#
# install_libraries.sh
#
# Installs Python libraries frequently mentioned in our discussions, suitable
# for a production support engineer or advanced usage scenarios in Python.
#
# Usage:
#   chmod +x install_libraries.sh
#   ./install_libraries.sh
#
# Or, on Windows (Git Bash / WSL), simply:
#   bash install_libraries.sh
#
# NOTE: This script assumes you have 'pip' available on PATH and that
#       you are installing into the desired Python environment (e.g., venv).

# 1. Upgrade pip to avoid any compatibility issues
echo "Upgrading pip to the latest version..."
pip install --upgrade pip

# 2. Install external libraries
echo "Installing Python libraries..."

# If you're using a requirements.txt, you could place these entries in the file and run:
#   pip install -r requirements.txt
# But here, we'll install them inline.

pip install \
  requests \              # HTTP requests
  paramiko \              # SSH/SFTP
  psycopg2-binary \       # PostgreSQL DB driver (binary variant)
  SQLAlchemy \            # ORM for databases
  PyYAML \                # YAML parsing
  pandas \                # Data analysis library
  numpy \                 # Array computing
  cryptography \          # Encryption & secure communications
  APScheduler \           # Advanced Python Scheduler
  celery \                # Distributed task queue (more complex usage)
  boto3 \                 # AWS SDK
  pytest \                # Testing framework
  docker \                # Control Docker containers/services from Python
  kafka-python \          # Apache Kafka client
  matplotlib \            # Data visualization
  plotly \                # Interactive plots & dashboards
  sentry-sdk \            # Error monitoring / alerting
  cx_Oracle \             # Oracle DB driver (requires Oracle client libs)
  PyMySQL \               # MySQL/MariaDB driver
  pandas-datareader \     #FRED
  bls-api \               #Bureau of Labor Statistics (BLS)
  wbdata \                #World Bank, IMF
  alpha_vantage \         #FOREX
  ccxt \                  #Crypto/Binance
  pandasdmx \             #IMF
  glassnode \             #Crypto market data
  tk \                    #Not sure?
  pyinstaller \           #This will let us create executable python scripts
  pyshortcuts \           #Create windows shortcuts

# 3. Post-install notes / system dependencies:
echo ""
echo "================================================="
echo "Installation completed (if no errors appeared)."
echo "Some libraries may require extra system dependencies or setup:"
echo "  - cx_Oracle: Requires Oracle Instant Client (https://www.oracle.com/database/technologies/instant-client.html)"
echo "  - psycopg2-binary: For production, consider 'psycopg2' + system packages like libpq-dev (Linux) or Postgres tools."
echo "  - docker: Requires Docker Engine installed & running."
echo "  - cryptography: May require development headers (e.g., libssl-dev)."
echo "  - Others (Paramiko, etc.) may also require system libs depending on your OS."
echo "================================================="

#pyinstaller --onefile --windowed macroMarketData.py

