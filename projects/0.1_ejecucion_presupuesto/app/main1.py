import streamlit as st

import pandas as pd 
import plotly.express as px

from pathlib import Path

from utils.data import load_data
from utils.format import formato_monto, nombre_mes

from charts.evolucion import mostrar_evolucion
from charts.ejecucion import mostrar_ejecucion_por_distrito

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
st.title(" PRESUPUESTO Y EJECUCIÓN 📊" )
st.caption("Análisis de presupuesto y ejecución presupuestal")


# # FILTROS

st.sidebar.header("Filtros")

departamentos = sorted(
    presupuesto["DEPARTAMENTO_EJECUTORA_NOMBRE"]
    .dropna()
    .unique()
)

departamento = st.sidebar.selectbox(
    "Departamento",
    departamentos,
    key="filtro_departamento"
)

provincias = sorted(
    presupuesto.loc[
        presupuesto["DEPARTAMENTO_EJECUTORA_NOMBRE"] == departamento,
        "PROVINCIA_EJECUTORA_NOMBRE"
    ]
    .dropna()
    .unique()
)

provincia = st.sidebar.selectbox(
    "Provincia",
    provincias,
    key="filtro_provincia"
)

distritos = sorted(
    presupuesto.loc[
        (presupuesto["DEPARTAMENTO_EJECUTORA_NOMBRE"] == departamento) &
        (presupuesto["PROVINCIA_EJECUTORA_NOMBRE"] == provincia),
        "EJECUTORA_NOMBRE"
    ]
    .dropna()
    .unique()
)

distrito = st.sidebar.selectbox(
    "Distrito",
    ["Todas"] + distritos,
    key="filtro_distrito"
)

meses = sorted(
    ejecucion_mensual.loc[
        ejecucion_mensual["MES_EJE"].between(1, 12),
        "MES_EJE"
    ]
    .dropna()
    .unique()
)

mes = st.sidebar.selectbox(
    "Mes de corte",
    meses,
    format_func=lambda x: pd.to_datetime(
        str(x),
        format="%m"
    ).strftime("%B").capitalize(),
    key="filtro_mes"
)


# FILTRO PRESUPUESTO

presupuesto_filtrado = presupuesto[
    (presupuesto["DEPARTAMENTO_EJECUTORA_NOMBRE"] == departamento) &
    (presupuesto["PROVINCIA_EJECUTORA_NOMBRE"] == provincia)
]

if distrito != "Todas":
    presupuesto_filtrado = presupuesto_filtrado[
        presupuesto_filtrado["EJECUTORA_NOMBRE"] == distrito]

# FILTRO EJECUCIÓN

ejecucion_filtrada = ejecucion_mensual[
    (ejecucion_mensual["DEPARTAMENTO_EJECUTORA_NOMBRE"] == departamento)
    & (ejecucion_mensual["PROVINCIA_EJECUTORA_NOMBRE"] == provincia)
    & (ejecucion_mensual["MES_EJE"] <= mes)
]

if distrito != "Todas":
    ejecucion_filtrada = ejecucion_filtrada[
        ejecucion_filtrada["EJECUTORA_NOMBRE"] == distrito]

# KPI

pia = presupuesto_filtrado["MONTO_PIA"].sum()
pim = presupuesto_filtrado["MONTO_PIM"].sum()

devengado = ejecucion_filtrada["MONTO_DEVENGADO"].sum()

ejecucion = (devengado / pim * 100 if pim > 0 else None)


saldo = pim - devengado

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

with kpi1:
    st.metric(
        "PIA",
        formato_monto(pia)
    )

with kpi2:
    st.metric(
        "PIM",
        formato_monto(pim)
    )

with kpi3:
    st.metric(
        "Devengado",
        formato_monto(devengado)
    )

with kpi4:
    st.metric(
        "Ejecución",
        "N/D" if ejecucion is None else f"{ejecucion:.2f}%"
    )

with kpi5:
    st.metric(
        "Saldo pendiente",
        formato_monto(saldo)
    )
# EVOLUCION MENSUAL


# Nombre corto del mes
# evolucion["MES"] = (
#     evolucion["FECHA"]
#     .dt.strftime("%b")
#     .str.capitalize()
# )

mostrar_evolucion(ejecucion_filtrada)


# EJECUCION POR DISTRITO

opcion_ranking = st.radio(
    "Mostrar",
    ["Todas", "Top 10", "Bottom 10"],
    horizontal=True
)

mostrar_ejecucion_por_distrito(
    ejecucion_entidad,
    opcion_ranking
)

# PIM VS DEVENGADO POR ENTIDAD 


# st.subheader("PIM vs. devengado acumulado por entidad")

# comparacion = ejecucion_entidad[
#     [
#         "EJECUTORA_NOMBRE",
#         "MONTO_PIM",
#         "DEVENGADO_ACUMULADO"
#     ]
# ].copy()

# # Aplicar el mismo ranking seleccionado
# if opcion_ranking == "Top 10":
#     comparacion = (
#         comparacion
#         .sort_values("DEVENGADO_ACUMULADO", ascending=False)
#         .head(10)
#     )

# elif opcion_ranking == "Bottom 10":
#     comparacion = (
#         comparacion
#         .sort_values("DEVENGADO_ACUMULADO", ascending=True)
#         .head(10)
#     )

# # Convertir a formato largo
# comparacion = comparacion.melt(
#     id_vars="EJECUTORA_NOMBRE",
#     value_vars=[
#         "MONTO_PIM",
#         "DEVENGADO_ACUMULADO"
#     ],
#     var_name="INDICADOR",
#     value_name="MONTO"
# )

# # Cambiar nombres para mostrar
# comparacion["INDICADOR"] = comparacion["INDICADOR"].replace({
#     "MONTO_PIM": "PIM",
#     "DEVENGADO_ACUMULADO": "Devengado acumulado"
# })

# fig = px.bar(
#     comparacion,
#     x="MONTO",
#     y="EJECUTORA_NOMBRE",
#     color="INDICADOR",
#     orientation="h",
#     barmode="group",
#     labels={
#         "MONTO": "Monto (S/)",
#         "EJECUTORA_NOMBRE": "Entidad",
#         "INDICADOR": ""
#     },
#     title="PIM vs. devengado acumulado"
# )

# fig.update_layout(
#     height=max(500, len(
#         comparacion["EJECUTORA_NOMBRE"].unique()
#     ) * 35),
#     xaxis_title="Monto (S/)",
#     yaxis_title="",
#     legend_title=""
# )

# st.plotly_chart(
#     fig,
#     use_container_width=True
# )

# #BRECHA PRESUPUESTAL 

# st.subheader("Brecha presupuestal por entidad")

# brecha_entidad = ejecucion_entidad.copy()

# brecha_entidad["BRECHA"] = (
#     brecha_entidad["MONTO_PIM"]
#     - brecha_entidad["DEVENGADO_ACUMULADO"]
# )

# brecha_entidad = (
#     brecha_entidad
#     .sort_values("BRECHA", ascending=False)
# )

# # Aplicar ranking seleccionado
# if opcion_ranking == "Top 10":
#     datos_brecha = brecha_entidad.head(10)

# elif opcion_ranking == "Bottom 10":
#     datos_brecha = (
#         brecha_entidad
#         .sort_values("BRECHA", ascending=True)
#         .head(10)
#     )

# else:
#     datos_brecha = brecha_entidad.copy()

# fig = px.bar(
#     datos_brecha,
#     x="BRECHA",
#     y="EJECUTORA_NOMBRE",
#     orientation="h",
#     text="BRECHA",
#     labels={
#         "BRECHA": "Brecha presupuestal (S/)",
#         "EJECUTORA_NOMBRE": "Entidad"
#     },
#     title="Brecha presupuestal por entidad"
# )

# fig.update_traces(
#     texttemplate="S/ %{text:,.0f}",
#     textposition="outside"
# )

# fig.update_layout(
#     height=max(
#         500,
#         len(datos_brecha) * 35
#     ),
#     xaxis_title="Brecha presupuestal (S/)",
#     yaxis_title=""
# )

# st.plotly_chart(
#     fig,
#     use_container_width=True
# )


# # RANKING ENTIDADES

# st.subheader("Ranking de entidades")

# ranking = (
#     ejecucion_entidad
#     .sort_values(
#         "EJECUCION_%",
#         ascending=False
#     )
#     .reset_index(drop=True)
# )

# ranking.index = ranking.index + 1

# ranking = ranking.rename(
#     columns={
#         "EJECUTORA_NOMBRE": "Entidad",
#         "MONTO_PIM": "PIM",
#         "DEVENGADO_ACUMULADO": "Devengado acumulado",
#         "EJECUCION_%": "Ejecución (%)"
#     }
# )

# st.dataframe(
#     ranking[
#         [
#             "Entidad",
#             "PIM",
#             "Devengado acumulado",
#             "Ejecución (%)"
#         ]
#     ],
#     use_container_width=True,
#     column_config={
#         "PIM": st.column_config.NumberColumn(
#             "PIM",
#             format="S/ %.0f"
#         ),
#         "Devengado acumulado": st.column_config.NumberColumn(
#             "Devengado acumulado",
#             format="S/ %.0f"
#         ),
#         "Ejecución (%)": st.column_config.NumberColumn(
#             "Ejecución (%)",
#             format="%.2f%%"
#         )
#     }
# )