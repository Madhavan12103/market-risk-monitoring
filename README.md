# Market Risk Monitoring Pipeline

A comprehensive data pipeline for monitoring market risks using dbt, Apache Airflow, and Snowflake.

## Architecture

This project implements a modern data stack with:

- **dbt (Data Build Tool)**: For data transformation and modeling
- **Apache Airflow**: For workflow orchestration
- **Snowflake**: As the data warehouse

## Project Structure

```
market-risk-monitoring/
├── dags/                          # Airflow DAGs
│   └── market_risk_monitoring.py  # Main orchestration DAG
├── telecom_risk_pipeline/         # dbt project
│   ├── models/                    # dbt models
│   │   ├── staging/              # Raw data staging models
│   │   ├── intermediate/          # Business logic models
│   │   └── mart/                  # Final presentation layer
│   ├── sources.yml               # Data source definitions
│   ├── dbt_project.yml           # dbt configuration
│   └── profiles.yml              # dbt connection profiles
├── generate_data.py              # Data generation script
├── market_assets.csv            # Sample market assets data
├── price_tickers.csv            # Sample price ticker data
└── supply_chain_impact.csv      # Sample supply chain data
```

## Data Flow

1. **Raw Data**: Market assets, price tickers, and supply chain impact data
2. **Staging Layer**: Clean and standardize raw data
3. **Intermediate Layer**: Business logic and calculations (price drop analysis)
4. **Mart Layer**: Final risk alerts and reporting

## Key Features

- **Automated Risk Detection**: Identifies critical market events based on price drops > 10% AND high risk levels
- **Daily Monitoring**: Scheduled to run every day at midnight
- **Modular Architecture**: Clear separation of concerns across layers
- **Snowflake Integration**: Optimized for cloud data warehousing

## Setup Instructions

### Prerequisites

- Python 3.9+
- dbt-core
- Apache Airflow 2.10.2
- Snowflake account with appropriate permissions

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd market-risk-monitoring
   ```

2. **Set up Python environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Install additional dependencies**
   ```bash
   pip install apache-airflow==2.10.2 snowflake-connector-python
   ```

4. **Configure Snowflake credentials**
   - Update `telecom_risk_pipeline/profiles.yml` with your Snowflake credentials
   - Update `dags/market_risk_monitoring.py` with your connection details

5. **Initialize Airflow**
   ```bash
   export AIRFLOW_HOME=$(pwd)
   airflow db init
   ```

### Usage

1. **Generate sample data** (optional)
   ```bash
   python generate_data.py
   ```

2. **Run dbt models**
   ```bash
   cd telecom_risk_pipeline
   dbt run
   ```

3. **Run Airflow DAG**
   ```bash
   airflow dags unpause market_risk_monitoring
   airflow dags trigger market_risk_monitoring
   ```

## Models Overview

### Staging Models
- `stg_market_assets`: Clean market asset data
- `stg_price_tickers`: Price data with timestamp casting
- `stg_supply_chain_impact`: Supply chain risk data

### Intermediate Models
- `int_asset_price_analysis`: Price drop calculations and volatility filtering

### Mart Models
- `fct_risk_alerts`: Critical risk alerts with business logic

## Monitoring

The Airflow DAG provides:
- Automated daily execution
- Risk alert notifications
- Comprehensive logging
- Error handling and retries

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
