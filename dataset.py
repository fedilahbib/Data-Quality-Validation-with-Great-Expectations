"""
dataset.py

Generates synthetic employee data using a clean OOP class.
"""

from pathlib import Path
from datetime import datetime, timedelta
import numpy as np
import random
import pandas as pd


class EmployeeDataset:
    def __init__(self, n_rows: int = 10, seed: int = 42):
        self.n_rows = n_rows
        self.seed = seed
        self.departments = ["Engineering", "Marketing", "HR", "Finance", "Sales"]

    def generate(self) -> pd.DataFrame:
        np.random.seed(self.seed)
        random.seed(self.seed)

        df = pd.DataFrame({
            "employee_id": [f"E{random.randint(1000, 9999)}" for _ in range(self.n_rows)],
            "age": np.random.randint(18, 70, self.n_rows).astype(float),
            "salary": np.round(np.random.uniform(45_000, 120_000, self.n_rows), 2),
            "department": random.choices(self.departments, k=self.n_rows),
            "is_active": random.choices([True, False], k=self.n_rows),
            "email": [f"user{i}@example.com" for i in range(self.n_rows)],
            "join_date": [
                (datetime(2024, 12, 1) +
                 timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d")
                for _ in range(self.n_rows)
            ]
        })

        return df

    def save_csv(self, path: Path, index: bool = False) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        df = self.generate()
        df.to_csv(path, index=index)
        return path

    def get_dataframe(self) -> pd.DataFrame:
        return self.generate()
