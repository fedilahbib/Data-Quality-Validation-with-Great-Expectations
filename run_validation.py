from pathlib import Path
from config import DATA_PATH, CSV_PATH
from dataset import EmployeeDataset
from validator import GEValidator


def main(generate_data=True, n_rows=10):

    # Ensure data/ exists
    DATA_PATH.mkdir(parents=True, exist_ok=True)

    # Step 1 — Generate dataset
    if generate_data:
        dataset = EmployeeDataset(n_rows=n_rows)
        csv_path = dataset.save_csv(CSV_PATH)
        print(f"Dataset generated → {csv_path}")
    else:
        csv_path = CSV_PATH

    # Step 2 — Setup GE
    ge = GEValidator(csv_path=csv_path)
    ge.setup()
    ge.add_expectations()
    results = ge.run_validation()

    # Step 3 — Summary
    print("\n========== VALIDATION SUMMARY ==========")
    print(f"Success: {results.success}")
    print(f"Expectations Run: {len(results.results)}")
    failed = [r for r in results.results if not r.success]
    print(f"Failed Expectations: {len(failed)}")
    print("========================================\n")


if __name__ == "__main__":
    main()
