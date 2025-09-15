# buzzline-03-webb

Consumer Protection Monitoring System using Kafka streaming data pipelines.

This project implements real-time monitoring for consumer protection violations using both JSON and CSV data streaming through Apache Kafka.

## Project Overview

This system monitors two types of consumer protection data:
- **Email Monitoring**: Tracks email interactions to detect unsubscribe violations
- **Billing Monitoring**: Monitors billing transactions to identify complaint patterns

## Prerequisites

- Python 3.11
- Apache Kafka (local installation)
- Completed setup from buzzline-01 and buzzline-02 projects

## Setup

### 1. Environment Setup

```bash
# Create virtual environment
py -3.11 -m venv .venv

# Activate virtual environment
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Mac/Linux

# Install dependencies
py -m pip install --upgrade pip wheel setuptools
py -m pip install -r requirements.txt
```

### 2. Start Kafka

```bash
# Prepare Kafka (first time only)
chmod +x scripts/prepare_kafka.sh
scripts/prepare_kafka.sh

# Start Kafka server
cd ~/kafka
bin/kafka-server-start.sh config/kraft/server.properties
```

## Usage

### JSON: Email Monitoring System

Monitors email interactions and flags companies with multiple unsubscribe violations.

**Producer**: Streams email monitoring data
```bash
py -m producers.json_producer_webb
```

**Consumer**: Detects unsubscribe violations
```bash
py -m consumers.json_consumer_webb
```

**Data Format**:
```json
{
  "company": "MegaCorp",
  "email_type": "promotional",
  "user_action": "unsubscribed"
}
```

### CSV: Billing Monitoring System

Tracks billing transactions and identifies companies with multiple complaints.

**Producer**: Streams billing data
```bash
py -m producers.csv_producer_webb
```

**Consumer**: Flags billing violations
```bash
py -m consumers.csv_consumer_webb
```

**Data Format**:
```csv
timestamp,company,amount,complaint_type
2025-09-14 15:00:00,MegaCorp,29.99,unexpected_charge
```

## Features

- Real-time violation detection
- Automated alert system for consumer protection issues
- Persistent logging of all activities
- Rolling window analysis for trend detection

## Data Files

- `data/email_monitor.json` - Email interaction data
- `data/billing_monitor.csv` - Billing transaction data

## Environment Configuration

Topics and intervals are configured in `.env`:
- JSON topic: `buzzline_json`
- CSV topic: `smoker_csv`
- Configurable message intervals

## License

MIT License - See [LICENSE.txt](LICENSE.txt)