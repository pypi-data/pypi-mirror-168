URL = "https://docs.google.com/spreadsheets/d/"
EXCEL_EXPORT = "/export?format=xlsx"


class GoogleSheetsUrlBuilder:
    def __init__(self, sheet_id):
        self.sheet_id = sheet_id

    def xlsx(self):
        return f"{URL}{self.sheet_id}{EXCEL_EXPORT}"
