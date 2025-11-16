from pathlib import Path


PROJECT_ROOT = Path(__file__).parent
DATA_PATH = PROJECT_ROOT / "data"
CSV_NAME = "synthetic_employees.csv"
CSV_PATH = DATA_PATH / CSV_NAME


# Great Expectations expectation suite name
EXPECTATION_SUITE = "employees_suite"


# Data source / asset names used in the GE context
GE_DATASOURCE_NAME = "employees_src"
GE_DATA_ASSET_NAME = "employees_asset"