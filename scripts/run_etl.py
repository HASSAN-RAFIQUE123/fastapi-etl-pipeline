"""Run the ETL pipeline from the command line."""

from etl.pipeline import run_pipeline


if __name__ == "__main__":
    run_pipeline()
    print("ETL pipeline completed")
