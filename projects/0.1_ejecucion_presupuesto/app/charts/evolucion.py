import plotly.express as px
import streamlit as st

from utils.format import nombre_mes


def mostrar_evolucion_lineal(
    df, 
    col_x="MES", 
    cols_y=["MONTO_DEVENGADO", "MONTO_DEVENGADO_ACUMULADO"], 
    titulo="Evolución mensual y acumulada del devengado"
):
   
    df = df.sort_values("FECHA").copy()

    df["MES"] = (
    df["MES_EJE"]
    .map(nombre_mes)
    )

    fig = px.line(
        df,  
        x=col_x,
        y=cols_y,
        markers=True,
        labels={
            col_x: "Mes",
            "value": "Monto",
            "variable": "Indicador",
            "MONTO_DEVENGADO": "Devengado mensual",
            "MONTO_DEVENGADO_ACUMULADO": "Devengado acumulado"
        },
        title=titulo
    )

    fig.update_traces(
        hovertemplate="S/ %{y:,.0f}<extra></extra>"
    )

    fig.update_layout(
        height=450,
        xaxis_title="",
        yaxis_title="Monto (S/)",
        legend_title="",
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)