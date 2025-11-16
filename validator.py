"""
validator.py

Encapsulates all Great Expectations logic using OOP.
"""

from pathlib import Path
import pandas as pd
import great_expectations as gx

from config import (
    CSV_PATH,
    EXPECTATION_SUITE,
    GE_DATASOURCE_NAME,
    GE_DATA_ASSET_NAME
)


class GEValidator:
    def __init__(self, df: pd.DataFrame = None, csv_path: Path = None):
        if df is None and csv_path is None:
            raise ValueError("Provide either a DataFrame or a csv_path.")

        self.df = df
        self.csv_path = csv_path
        self.context = gx.get_context()
        self.validator = None

    # ---------------------
    # GE Setup
    # ---------------------
    def _prepare_batch_from_df(self, df: pd.DataFrame):
        datasource = self.context.data_sources.add_pandas(
            name=GE_DATASOURCE_NAME
        )

        asset = datasource.add_dataframe_asset(name=GE_DATA_ASSET_NAME)

        batch_def = asset.add_batch_definition_whole_dataframe("batch_whole")
        batch = batch_def.get_batch(batch_parameters={"dataframe": df})

        self.validator = self.context.get_validator(
            batch=batch,
            create_expectation_suite_with_name=EXPECTATION_SUITE
        )

        return self.validator

    def _prepare_batch_from_csv(self, csv_path: Path):
        df = pd.read_csv(csv_path)
        return self._prepare_batch_from_df(df)

    def setup(self):
        """Build GE validator from DataFrame or CSV."""
        if self.df is not None:
            return self._prepare_batch_from_df(self.df)
        else:
            return self._prepare_batch_from_csv(self.csv_path)

    # ---------------------
    # Expectations
    # ---------------------
    def add_expectations(self):
        if self.validator is None:
            raise RuntimeError("Call setup() before add_expectations().")

        v = self.validator

        v.expect_column_values_to_not_be_null("employee_id")
        v.expect_column_values_to_be_between("age", 18, 65)
        v.expect_column_values_to_match_regex("email", r"[^@]+@[^@]+\.[^@]+")
        v.expect_column_values_to_be_in_set(
            "department", ["HR", "Finance", "Engineering", "Marketing", "Sales"]
        )
        v.expect_column_values_to_match_strftime_format("join_date", "%Y-%m-%d")

        return v

    # ---------------------
    # Validation execution
    # ---------------------
    def run_validation(self):
        if self.validator is None:
            raise RuntimeError("Call setup() first.")

        return self.validator.validate()
