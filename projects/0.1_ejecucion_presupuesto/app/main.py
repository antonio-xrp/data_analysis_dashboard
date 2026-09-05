import streamlit as st

import pandas as pd

from pathlib import Path

from utils.data import load_data
from utils.format import formato_monto


from charts.line import crear_line_chart
from charts.bar import crear_bar_chart

from services.presupuesto import (
    filtrar_presupuesto,
    filtrar_ejecucion,
    preparar_evolucion,
    calcular_kpis,
    agrupar_ejecucion
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
            "DISTRITO_EJECUTORA_NOMBRE"]
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

ejecucion_entidad = agrupar_ejecucion(
    presupuesto_filtrado,
    ejecucion_filtrada,
)


fig = crear_bar_chart(
    df  = ejecucion_entidad,
    x   = "EJECUCION_%",
    y   = "DISTRITO_EJECUTORA_NOMBRE",
    text = "EJECUCION_%",
    title = "RANKING POR EJECUCIÓN",
    labels = {
        "DISTRITO_EJECUTORA_NOMBRE" : "DISTRITO",
        "EJECUCION_%":"EJECUCIÓN"
    },
    text_template="%{text:.1f}",
    text_position = "outside",
    xaxis_title = "",
    yaxis_title = "DISTRITOS",
    hover_template = "%{y}: %{x:.1f}%",
    xaxis_ticksuffix = "%"
)

st.plotly_chart(
    fig,
    use_container_width=True,
)


