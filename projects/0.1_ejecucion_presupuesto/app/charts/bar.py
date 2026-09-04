from typing import Callable

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def crear_bar_chart(
    df: pd.DataFrame,
    *,
    x: str,
    y: str,
    orientation: str = "h",
    text: str | None = None,
    title: str | None = None,
    labels: dict[str, str] | None = None,
    text_template: str | None = None,
    text_position: str = "outside",
    hover_template: str | None = None,
    height: int | None = None,
    height_per_row: int = 35,
    min_height: int = 500,
    xaxis_title: str | None = None,
    yaxis_title: str | None = None,
    xaxis_ticksuffix: str | None = None,
    hovermode: str = "y",
    add_reference_line: bool = False,
    reference_x: float | None = None,
    reference_label: str | None = None,
    categoryorder: str | None = None,
    xaxis_range: tuple[float, float] | None = None,
) -> go.Figure:

    if df.empty:
        raise ValueError("El DataFrame está vacío.")

    required_columns = [x, y]

    if text:
        required_columns.append(text)

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Las siguientes columnas no existen en el DataFrame: "
            f"{missing_columns}"
        )

    fig = px.bar(
        df,
        x=x,
        y=y,
        orientation=orientation,
        text=text,
        labels=labels,
        title=title,
    )

    if text_template:
        fig.update_traces(
            texttemplate=text_template,
            textposition=text_position,
        )

    if hover_template:
        fig.update_traces(
            hovertemplate=hover_template
        )

    if height is None:
        height = max(
            min_height,
            len(df) * height_per_row
        )

    fig.update_layout(
        height=height,
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        hovermode=hovermode,
    )

    if xaxis_ticksuffix:
        fig.update_xaxes(
            ticksuffix=xaxis_ticksuffix
        )

    if categoryorder:
        fig.update_yaxes(
            categoryorder=categoryorder
        )

    if add_reference_line and reference_x is not None:
        fig.add_vline(
            x=reference_x,
            line_dash="dash",
            annotation_text=reference_label,
            annotation_position="top",
        )

    return fig