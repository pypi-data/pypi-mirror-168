from pathlib import Path, PurePath

import pandas as pd

from .dataframe import ExpenseDataFrameBuilder
from .google import GoogleSheetsUrlBuilder
from .report import MultiStepReport, SingleStepReport

pd.options.display.float_format = "{:.4f}".format

GOOGLE_SHEET_ID = "14TYhaFNHryi6jfcW43veZBHt4goGNtMTtqUccUGHKV8"
STEPS = [
    "Depenses Diverses",
    "Singapour",
    "Bali",
    "Kuala Lumpur",
    "Sulawesi",
    "USA",
    "Baja California",
    "Perou",
    "Argentine",
]

OUTPUT_DIR = "reports"


def init_excel_file():
    url = GoogleSheetsUrlBuilder(sheet_id=GOOGLE_SHEET_ID).xlsx()
    return pd.ExcelFile(url)


def create_step_report(io, step_name):
    step_df = ExpenseDataFrameBuilder.read_excel(io, sheet_name=step_name)
    step_report = SingleStepReport(name=step_name, df=step_df)
    return step_report


def dump_report(report, directory):
    p = Path(directory)
    if not p.exists() or not p.is_dir():
        p.mkdir()

    html_path = PurePath.joinpath(p, report.name + ".html")
    report.to_html(html_path)
    print(f"{html_path} has been generated.")

    excel_path = PurePath.joinpath(p, report.name + ".xlsx")
    report.to_excel(excel_path)
    print(f"{excel_path} has been generated.")

    txt_path = PurePath.joinpath(p, report.name + ".txt")
    with open(txt_path, "w") as f:
        f.write(report.to_string())
        print(f"{txt_path} has been generated.")


def main():
    excel_file = init_excel_file()
    print(f"* Building expense reports from file {excel_file.io}")

    reports = []
    for step in STEPS:
        print(f"** Building report for step {step}")
        step_report = create_step_report(excel_file, step)
        dump_report(step_report, OUTPUT_DIR)
        reports.append(step_report)

    print("** Building the finale aggregated report.")
    all_steps_report = MultiStepReport(name="ALL", reports=reports)
    dump_report(all_steps_report, OUTPUT_DIR)


if __name__ == "__main__":
    main()
