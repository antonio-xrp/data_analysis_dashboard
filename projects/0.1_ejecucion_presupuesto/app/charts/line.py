from typing import Sequence

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def crear_line_chart(
    df: pd.DataFrame,
    x: str,
    y: str | Sequence[str],
    *,
    title: str | None = None,
    labels: dict[str, str] | None = None,
    markers: bool = True,
    height: int = 450,
    xaxis_title: str | None = None,
    yaxis_title: str | None = None,
    legend_title: str | None = None,
    hovermode: str = "x unified",
    hovertemplate: str | None = None,
) -> go.Figure:
    """
    Crea un gráfico de líneas reutilizable.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame con los datos.

    x : str
        Nombre de la columna para el eje X.

    y : str | Sequence[str]
        Nombre de una o varias columnas para el eje Y.

    title : str | None
        Título del gráfico.

    labels : dict[str, str] | None
        Diccionario para cambiar etiquetas del gráfico.

    markers : bool
        Muestra puntos sobre las líneas.

    height : int
        Altura del gráfico en píxeles.

    xaxis_title : str | None
        Título personalizado del eje X.

    yaxis_title : str | None
        Título personalizado del eje Y.

    legend_title : str | None
        Título de la leyenda.

    hovermode : str
        Comportamiento del hover.

    hovertemplate : str | None
        Formato personalizado del tooltip.

    Returns
    -------
    go.Figure
        Figura de Plotly.
    """

    # 1. Validaciones

    if df.empty:
        raise ValueError("El DataFrame está vacío.")

    y_columns = [y] if isinstance(y, str) else list(y)

    required_columns = [x, *y_columns]

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

    # gráfico

    fig = px.line(
        df,
        x=x,
        y=y_columns,
        markers=markers,
        labels=labels,
        title=title,
    )

    # LAYOUT

    fig.update_layout(
        height=height,
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        legend_title=legend_title,
        hovermode=hovermode,
    )

    # HOVER
    if hovertemplate:
        fig.update_traces(
            hovertemplate=hovertemplate
        )

    return fig