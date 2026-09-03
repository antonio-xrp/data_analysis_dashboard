import streamlit as st

import pandas as pd

from pathlib import Path

from utils.data import load_data
from utils.format import formato_monto
from utils.format import nombre_mes


from charts.evolucion import mostrar_evolucion_lineal
from charts.line import crear_line_chart

from services.presupuesto import (
    filtrar_presupuesto,
    filtrar_ejecucion,
    preparar_evolucion,
    calcular_kpis,
)


# CONFIGURACIÓN INICIAL
st.set_page_config(
    page_title = 'PRESUPUESTO Y EJECUCIÓN',
    page_icon="📊",
    layout="wide",
)

# RUTAS

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"

# CARGA DE DATOS

presupuesto, ejecucion_mensual = load_data(DATA_DIR)


# TITULO

st.title("PRESUPUESTO Y EJECUCIÓN MUNICIPALIDADES DISTRITALES 📊")
st.caption("Análisis de presupuesto y ejecución presupuestal")

# FILTROS

col1, col2, col3, col4 = st.columns(4)

with col1:
    departamentos = sorted(
        presupuesto["DEPARTAMENTO_EJECUTORA_NOMBRE"]
        .dropna()
        .unique())

    departamento = st.selectbox(
        "Departamento",
        departamentos
    )

with col2:
    provincias = sorted(
        presupuesto.loc[
            presupuesto["DEPARTAMENTO_EJECUTORA_NOMBRE"] == departamento, "PROVINCIA_EJECUTORA_NOMBRE"]
        .dropna()
        .unique())

    provincia = st.selectbox(
        "Provincia",
        provincias
    )

with col3:
    distritos = sorted(
        presupuesto.loc[
            (presupuesto["DEPARTAMENTO_EJECUTORA_NOMBRE"] == departamento) &
            (presupuesto["PROVINCIA_EJECUTORA_NOMBRE"] == provincia), 
            "EJECUTORA_NOMBRE"]
        .dropna()
        .unique())

    distrito = st.selectbox(
        "Distrito",
        ["Todas"] + distritos
    )

with col4:
    meses = sorted(
        ejecucion_mensual["MES_EJE"]
        .dropna()
        .unique())

    mes = st.selectbox(
        "Mes",
        meses,
        format_func = lambda x : pd.to_datetime(str(x), format="%m")
        .strftime("%B").capitalize()
    )


presupuesto_filtrado = filtrar_presupuesto(
    presupuesto=presupuesto,
    departamento=departamento,
    provincia=provincia,
    distrito=distrito,
)

ejecucion_filtrada = filtrar_ejecucion(
    ejecucion=ejecucion_mensual,
    departamento=departamento,
    provincia=provincia,
    distrito=distrito,
    mes=mes,
)

evolucion = preparar_evolucion(
    ejecucion_filtrada
)

# FILTRO PRESUPUESTO

kpis = calcular_kpis(
    presupuesto=presupuesto_filtrado,
    ejecucion=ejecucion_filtrada,
)


# SHOW KPIS

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

with kpi1:
    st.metric("PIA", formato_monto(kpis["pia"]))

with kpi2:
    st.metric("PIM", formato_monto(kpis["pim"]))

with kpi3:
    st.metric("DEVENGADO", formato_monto(kpis["devengado"]))

with kpi4:
    st.metric(
        "EJECUCIÓN",
        "N/D"
        if kpis["ejecucion"] is None
        else f'{kpis["ejecucion"]:.2f}%'
    )

with kpi5:
    st.metric(
        "SALDO PENDIENTE",
        formato_monto(kpis["saldo"])
    )

# GRAFICOS LINEAL - EVOLUCION ACUMULADA DEVENGADOS

evolucion = preparar_evolucion(
    ejecucion_filtrada
)

fig = crear_line_chart(
    df=evolucion,
    x="FECHA",
    y=[
        "MONTO_DEVENGADO",
        "MONTO_DEVENGADO_ACUMULADO",
    ],
    title="Evolución mensual y acumulada del devengado",
    labels={
        "FECHA": "Mes",
        "value": "Monto",
        "variable": "Indicador",
        "MONTO_DEVENGADO": "Devengado mensual",
        "MONTO_DEVENGADO_ACUMULADO": "Devengado acumulado",
    },
    xaxis_title="",
    yaxis_title="Monto (S/)",
    legend_title="",
    hovertemplate="S/ %{y:,.0f}<extra></extra>",
)

st.plotly_chart(
    fig,
    use_container_width=True
)




# GRAFICO DE BARRAS HORIZONTALES - EJECUCION POR DISTRITO

# ejecucion = ejecucion_filtrada.sort_values("EJECUCION_%",
#                 ascending=True)

# opcion_ranking = st.radio(
#     "Mostrar",
#     ["Todas", "Top 10", "Bottom 10"],
#     horizontal=True
# )

# st.dataframe(ejecucion_filtrada)
# # st.dataframe(presupuesto_filtrado)

# devengado_entidad = (
#     ejecucion_filtrada
#     .groupby("EJECUTORA_NOMBRE",as_index=False)["MONTO_DEVENGADO"]
#     .sum()
#     .rename(
#         columns={
#             "MONTO_DEVENGADO": "DEVENGADO_ACUMULADO"
#             }))

# st.dataframe(devengado_entidad)

# presupuesto_entidad = (
#         presupuesto_filtrado[[
#             "EJECUTORA_NOMBRE",
#             "MONTO_PIM"]]
#         .groupby("EJECUTORA_NOMBRE",as_index=False)["MONTO_PIM"]
#         .sum()
#     )

# st.dataframe(presupuesto_entidad)

# ejecucion_entidad = presupuesto_entidad.merge(
#         devengado_entidad,
#         on="EJECUTORA_NOMBRE",
#         how="left"
#     )

# ejecucion_entidad["DEVENGADO_ACUMULADO"] = (
#         ejecucion_entidad["DEVENGADO_ACUMULADO"]
#         .fillna(0)
#     )

# ejecucion_entidad["EJECUCION_%"] = (
#         ejecucion_entidad["DEVENGADO_ACUMULADO"]
#         / ejecucion_entidad["MONTO_PIM"]
#     ) * 100

# st.dataframe(ejecucion_entidad)

# st.subheader("Ejecución presupuestal por distrito")

# if opcion_ranking == "Top 10":

#     datos_grafico = (
#         ejecucion_entidad
#         .sort_values(
#             "EJECUCION_%",
#             ascending=False
#         )
#         .head(10)
#     )

#     # Mayor → menor
#     datos_grafico = datos_grafico.sort_values(
#         "EJECUCION_%",
#         ascending=True
#     )

# elif opcion_ranking == "Bottom 10":

#     datos_grafico = (
#         ejecucion_entidad
#         .sort_values(
#             "EJECUCION_%",
#             ascending=True
#         )
#         .head(10)
#     )

#     # Menor → mayor
#     datos_grafico = datos_grafico.sort_values(
#         "EJECUCION_%",
#         ascending=True
#     )

# else:

#     datos_grafico = (
#         ejecucion_entidad
#         .sort_values(
#             "EJECUCION_%",
#             ascending=True
#         )
#     )

# fig = px.bar(
#     datos_grafico,
#     x="EJECUCION_%",
#     y="EJECUTORA_NOMBRE",
#     orientation="h",
#     text="EJECUCION_%",
#     labels={
#         "EJECUCION_%": "Ejecución (%)",
#         "EJECUTORA_NOMBRE": "Distrito"
#     },
#     title="Ejecución presupuestal por distrito"
# )

# fig.update_traces(
#     texttemplate="%{text:.1f}%",
#     textposition="outside",
#     hovertemplate=(
#         "<b>%{y}</b><br>"
#         "Ejecución: %{x:.2f}%"
#         "<extra></extra>"
#     )
# )

# fig.add_vline(
#     x=100,
#     line_dash="dash",
#     annotation_text="100%",
#     annotation_position="top"
# )

# fig.update_layout(
#     height=max(
#         500,
#         len(datos_grafico) * 35
#     ),
#     xaxis_title="Ejecución (%)",
#     yaxis_title="",
#     xaxis={
#         "ticksuffix": "%"
#     },
#     hovermode="y"
# )

# st.plotly_chart(
#     fig,
#     use_container_width=True
# )