from math import pi

from bokeh.models import ColumnDataSource, FactorRange
from bokeh.palettes import Category20_20
from bokeh.plotting import figure
from bokeh.transform import cumsum

DEFAULT_WIDTH = 1000
DEFAULT_HEIGHT = 500


def _customize_vbar_fig(fig):
    fig.y_range.start = 0
    fig.x_range.range_padding = 0.1
    fig.xgrid.grid_line_color = None
    fig.ygrid.grid_line_color = "grey"
    fig.ygrid.grid_line_alpha = 0.2
    fig.ygrid.minor_grid_line_color = "grey"
    fig.ygrid.minor_grid_line_alpha = 0.1
    fig.xaxis.major_label_orientation = 1
    return fig


def vbar(dataframe, title, col=None):
    if dataframe.index.nlevels != 1:
        raise RuntimeError(f"The vbar cannot be rendered.")

    column = col or dataframe.columns[0]
    index = dataframe.index.names[0] or "index"

    source = ColumnDataSource(dataframe)
    source.data["color"] = Category20_20[: dataframe.shape[0]]

    fig = figure(
        x_range=FactorRange(*source.data[index]),
        title=title,
        toolbar_location=None,
        height=DEFAULT_HEIGHT,
        width=DEFAULT_WIDTH,
        tools="hover",
        tooltips=f"@{{{index}}}: @{{{column}}}{{0.000}}",
    )
    fig.vbar(x=index, top=column, width=0.3, color="color", source=source)
    return _customize_vbar_fig(fig)


def pie(dataframe, title, col=None):
    if dataframe.index.nlevels != 1:
        raise RuntimeError(f"The pie chart cannot be rendered.")

    column = col or dataframe.columns[0]
    index = dataframe.index.names[0] or "index"
    source = ColumnDataSource(dataframe)

    source.data["angle"] = dataframe[column] / dataframe[column].sum() * 2 * pi
    source.data["color"] = Category20_20[: dataframe.shape[0]]

    fig = figure(
        x_range=(-0.5, 1.0),
        height=DEFAULT_HEIGHT,
        width=DEFAULT_WIDTH,
        title=title,
        toolbar_location=None,
        tools="hover",
        tooltips=f"@{{{index}}}: @{{{column}}}{{0.000}}",
    )

    fig.wedge(
        x=0,
        y=1,
        radius=0.4,
        start_angle=cumsum("angle", include_zero=True),
        end_angle=cumsum("angle"),
        line_color="white",
        fill_color="color",
        legend_field=index,
        source=source,
    )

    fig.axis.axis_label = None
    fig.axis.visible = False
    fig.grid.grid_line_color = None
    return fig


def vbar_stack(dataframe, title):
    if dataframe.index.nlevels != 2 or len(dataframe.columns) != 1:
        raise RuntimeError("The stack vbar cannot be rendered.")

    pivot_dataframe = dataframe.unstack(-1, fill_value=0)
    pivot_dataframe.columns = pivot_dataframe.columns.get_level_values(-1)
    stackers = list(pivot_dataframe.columns)

    source = ColumnDataSource(pivot_dataframe)
    flatten_index_names = "_".join(pivot_dataframe.index.names)

    fig = figure(
        x_range=FactorRange(*source.data[flatten_index_names]),
        title=title,
        toolbar_location=None,
        height=DEFAULT_HEIGHT,
        width=DEFAULT_WIDTH,
        tools="hover",
        tooltips="$name: @$name{0.000}",
    )

    fig.vbar_stack(
        stackers,
        x=flatten_index_names,
        color=Category20_20[: len(stackers)],
        width=0.4,
        legend_label=stackers,
        line_color="white",
        source=source,
    )

    fig.add_layout(fig.legend[0], "right")
    return _customize_vbar_fig(fig)


def vbar_grouped(dataframe, title, col=None):
    if dataframe.index.nlevels != 2:
        raise RuntimeError("The grouped vbar cannot be rendered.")

    column = col or dataframe.columns[0]

    source = ColumnDataSource(dataframe)
    source.data["colors"] = Category20_20[: dataframe.shape[0]]

    flatten_index_names = "_".join(dataframe.index.names)

    fig = figure(
        x_range=FactorRange(*source.data[flatten_index_names]),
        height=DEFAULT_HEIGHT,
        width=DEFAULT_WIDTH,
        title=title,
        toolbar_location=None,
        tools="hover",
        tooltips=f"@{{{column}}}{{0.00}}",
    )

    fig.vbar(
        x=flatten_index_names, top=column, width=0.4, source=source, color="colors"
    )

    fig.y_range.start = 0
    fig.x_range.range_padding = 0.1
    fig.xgrid.grid_line_color = None
    fig.ygrid.grid_line_color = "grey"
    fig.ygrid.grid_line_alpha = 0.2
    fig.ygrid.minor_grid_line_color = "grey"
    fig.ygrid.minor_grid_line_alpha = 0.1
    fig.xaxis.major_label_orientation = 1
    return _customize_vbar_fig(fig)


def vbar_grouped_stack(dataframe, title):
    if dataframe.index.nlevels != 3 or len(dataframe.columns) != 1:
        raise RuntimeError("The grouped stack vbar cannot be rendered.")

    pivot_dataframe = dataframe.unstack(-1, fill_value=0)
    pivot_dataframe.columns = pivot_dataframe.columns.get_level_values(-1)
    stackers = list(pivot_dataframe.columns)

    source = ColumnDataSource(pivot_dataframe)
    flatten_index_names = "_".join(pivot_dataframe.index.names)

    fig = figure(
        x_range=FactorRange(*source.data[flatten_index_names]),
        height=DEFAULT_HEIGHT,
        width=DEFAULT_WIDTH,
        title=title,
        tools="hover",
        tooltips="$name: @$name{0.000}",
    )

    fig.vbar_stack(
        stackers,
        x=flatten_index_names,
        color=Category20_20[: len(stackers)],
        width=0.4,
        source=source,
        line_color="white",
        legend_label=stackers,
    )
    fig.add_layout(fig.legend[0], "right")
    return _customize_vbar_fig(fig)
