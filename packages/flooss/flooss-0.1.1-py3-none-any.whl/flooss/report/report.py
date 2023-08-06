import pandas as pd
from bokeh.io import output_file, save
from bokeh.layouts import column

from ..aggregation import AggregationEngine
from ..dataframe import AMOUNT, CAT, DATE, STEP, SUBCAT, WHO
from ..plot import pie, vbar, vbar_grouped, vbar_grouped_stack, vbar_stack
from ._display import *


class Report:
    SECTION_TEMPLATE = {}
    PLOT_STRATEGY = {}

    def __init__(self, name, df, template=None):
        self.name = name
        self.df = df
        self.summary = self._summary()
        self.sections = self._sections(template)

    def _sections(self, template):
        template = template or self.SECTION_TEMPLATE
        return {name: engine.apply(self.df) for name, engine in template.items()}

    def to_string(self):
        data = self.to_string_summary()
        data += "\n\n"
        data += self.to_string_sections()
        return data

    def to_string_summary(self):
        data = SUMMARY
        data += "\n"
        data += self.summary.to_string()
        return data

    def to_string_sections(self):
        data = ""
        for name in self.sections:
            data += self.to_string_section(name)
            data += "\n\n"
        return data

    def to_string_section(self, name):
        data = name
        data += "\n"
        data += self.sections[name].to_string()
        return data

    def to_excel(self, path):
        with pd.ExcelWriter(path, mode="w") as writer:
            self.summary.to_excel(writer, sheet_name="Summary")
        with pd.ExcelWriter(path, mode="a") as writer:
            for name, section in self.sections.items():
                section.to_excel(writer, sheet_name=name)

    def to_html(self, path):
        output_file(path)
        figures = []
        for name, plot_callable in self.PLOT_STRATEGY.items():
            section = self.sections[name]
            fig = plot_callable(section, title=name)
            figures.append(fig)
        save(column(figures))

    def _summary_as_dict(self):
        data = {
            SUMMARY_SUM: self.df[AMOUNT].sum(),
            SUMMARY_DAYS: self.df[DATE].nunique(),
        }
        data[SUMMARY_AVG] = data[SUMMARY_SUM] / data[SUMMARY_DAYS]
        return data

    def _summary(self):
        return pd.Series(data=self._summary_as_dict())

    def __eq__(self, other):
        return (
            self.name == other.name
            and pd.DataFrame.equals(self.df, other.df)
            and pd.Series.equals(self.summary, other.summary)
            and self.sections == self.sections
        )


class SingleStepReport(Report):
    SECTION_TEMPLATE = {
        BY_CATEGORY: AggregationEngine(by=[CAT], values=[AMOUNT]),
        BY_CONTRIBUTOR: AggregationEngine(by=[WHO], values=[AMOUNT]),
        BY_CONTRIBUTOR_CATEGORY: AggregationEngine(by=[WHO, CAT], values=[AMOUNT]),
        BY_CATEGORY_SUBCATEGORY: AggregationEngine(by=[CAT, SUBCAT], values=[AMOUNT]),
        BY_CONTRIBUTOR_CATEGORY_SUBCATEGORY: AggregationEngine(
            by=[WHO, CAT, SUBCAT], values=[AMOUNT]
        ),
    }

    PLOT_STRATEGY = {
        BY_CATEGORY: pie,
        BY_CONTRIBUTOR: vbar,
        BY_CATEGORY_SUBCATEGORY: vbar_stack,
        BY_CONTRIBUTOR_CATEGORY: vbar_grouped,
        BY_CONTRIBUTOR_CATEGORY_SUBCATEGORY: vbar_grouped_stack,
    }

    def to_string(self):
        data = f" Expenses report for {self.name}. ".center(100, "*") + "\n"
        data += super().to_string()
        return data


class MultiStepReport(Report):
    SECTION_TEMPLATE = {
        BY_STEP: AggregationEngine(by=[STEP], values=[AMOUNT]),
        BY_CONTRIBUTOR: AggregationEngine(by=[WHO], values=[AMOUNT]),
        BY_CATEGORY: AggregationEngine(by=[CAT], values=[AMOUNT]),
        BY_CONTRIBUTOR_STEP: AggregationEngine(by=[WHO, STEP], values=[AMOUNT]),
        BY_CONTRIBUTOR_CATEGORY: AggregationEngine(by=[WHO, CAT], values=[AMOUNT]),
        BY_CONTRIBUTOR_STEP_CATEGORY: AggregationEngine(
            by=[WHO, STEP, CAT], values=[AMOUNT]
        ),
    }

    PLOT_STRATEGY = {
        BY_STEP: pie,
        BY_CATEGORY: vbar,
        BY_CONTRIBUTOR: vbar,
        BY_CONTRIBUTOR_CATEGORY: vbar_grouped,
        BY_CONTRIBUTOR_STEP: vbar_grouped,
        BY_CONTRIBUTOR_STEP_CATEGORY: vbar_grouped_stack,
    }

    def __init__(self, name, reports, template=None):
        self.name = name
        self.df = self._df(reports)
        self.summary = self._summary()
        self.sections = self._sections(template)

    @staticmethod
    def _df(reports):
        all_steps_df = pd.DataFrame()
        for report in reports:
            step_df = report.df
            step_df[STEP] = report.name
            all_steps_df = pd.concat([all_steps_df, step_df])
        return all_steps_df

    def to_string(self):
        data = f" Global expenses report. ".center(100, "*") + "\n"
        data += super().to_string()
        return data
