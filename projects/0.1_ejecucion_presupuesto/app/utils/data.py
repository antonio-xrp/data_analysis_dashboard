import pandas as pd
import streamlit as st


@st.cache_data
def load_data(data_dir):

    presupuesto = pd.read_parquet(
        data_dir / "presupuesto.parquet"
    )

    ejecucion_mensual = pd.read_parquet(
        data_dir / "ejecucion_mensual.parquet"
    )

    return presupuesto, ejecucion_mensual