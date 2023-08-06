def group_and_aggregate(df, by, values, func, sort=True):
    result_df = df.groupby(by).agg(func)[values]
    if sort:
        result_df = result_df.reset_index()
        result_df = result_df.sort_values(by=by[:-1] + values)
        result_df = result_df.set_index(by)
    return result_df


class AggregationEngine:
    def __init__(self, by, values, agg_func="sum", sort=True):
        self.by = by
        self.values = values
        self.agg_func = agg_func
        self.sort = sort

    def apply(self, df):
        return group_and_aggregate(
            df=df, by=self.by, values=self.values, func=self.agg_func, sort=self.sort
        )

    def __eq__(self, other):
        return (
            self.by == other.by
            and self.values == other.values
            and self.agg_func == other.agg_func
            and self.sort == other.sort
        )
