import pandas as pd

STEP = "Etape"
WHO = "Bénéficiaire"
SUBCAT = "Sous-catégorie"
CAT = "Catégorie"
DESC = "Dépense"
DATE = "Date"
AMOUNT = "Montant (Euro)"
COLUMNS = [DATE, DESC, CAT, SUBCAT, AMOUNT, WHO]
PARTYSEP = "/"


class ExpenseDataFrameBuilder:
    @staticmethod
    def read_excel(io, *args, **kwargs):
        df = pd.read_excel(
            io, header=1, usecols=COLUMNS, parse_dates=[DATE], *args, **kwargs
        )
        df = df.dropna()
        df[DATE] = pd.to_datetime(df[DATE])
        return ExpenseDataFrameBuilder._explode_rows_with_multi_contributors(df)

    @staticmethod
    def _explode_rows_with_multi_contributors(df):
        df[AMOUNT] = df[AMOUNT] / (df[WHO].str.count(PARTYSEP) + 1)
        df[WHO] = df[WHO].str.split(PARTYSEP)
        df = df.explode(WHO)
        df = df.reset_index(drop=True)
        return df
