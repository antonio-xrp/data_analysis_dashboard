import pandas as pd


def filtrar_presupuesto(
    presupuesto: pd.DataFrame,
    departamento: str,
    provincia: str,
    distrito: str = "Todas",
) -> pd.DataFrame:

    df = presupuesto[
        presupuesto["DEPARTAMENTO_EJECUTORA_NOMBRE"] == departamento
    ].copy()

    if provincia != "Todas":
        df = df[df["PROVINCIA_EJECUTORA_NOMBRE"] == provincia]

    if distrito != "Todas":
        df = df[df["DISTRITO_EJECUTORA_NOMBRE"] == distrito]

    return df


def filtrar_ejecucion(
    ejecucion: pd.DataFrame,
    departamento: str,
    provincia: str,
    distrito: str,
    mes: int,
) -> pd.DataFrame:

    df = ejecucion[
        (ejecucion["DEPARTAMENTO_EJECUTORA_NOMBRE"] == departamento)
        & (ejecucion["MES_EJE"] <= mes)
    ].copy()

    if provincia != "Todas":
        df = df[df["PROVINCIA_EJECUTORA_NOMBRE"] == provincia]

    if distrito != "Todas":
        df = df[df["DISTRITO_EJECUTORA_NOMBRE"] == distrito]

    return df

def preparar_evolucion(
    ejecucion: pd.DataFrame,
) -> pd.DataFrame:

    if ejecucion.empty:
        return pd.DataFrame()

    df = (
        ejecucion
        .groupby("FECHA", as_index=False)["MONTO_DEVENGADO"]
        .sum()
        .sort_values("FECHA")
    )

    df["MONTO_DEVENGADO_ACUMULADO"] = (
        df["MONTO_DEVENGADO"].cumsum()
    )

    return df


def calcular_kpis(
    presupuesto: pd.DataFrame,
    ejecucion: pd.DataFrame,
) -> dict:

    pia = presupuesto["MONTO_PIA"].sum()
    pim = presupuesto["MONTO_PIM"].sum()

    devengado = ejecucion["MONTO_DEVENGADO"].sum()

    ejecucion_pct = (
        devengado / pim * 100
        if pim > 0
        else None
    )

    saldo = pim - devengado

    return {
        "pia": pia,
        "pim": pim,
        "devengado": devengado,
        "ejecucion": ejecucion_pct,
        "saldo": saldo,
    }


def agrupar_ejecucion(
    presupuesto: pd.DataFrame, 
    ejecucion: pd.DataFrame
    ) -> pd.DataFrame:

    df = presupuesto.merge(
        ejecucion,
        on=[
            "ANO_EJE",
            "DEPARTAMENTO_EJECUTORA_NOMBRE",
            "PROVINCIA_EJECUTORA_NOMBRE",
            "DISTRITO_EJECUTORA_NOMBRE",
            ],
        how="inner"
    )

    df = (
        df
        .groupby([
            "ANO_EJE",
            "DISTRITO_EJECUTORA_NOMBRE",
            "MONTO_PIA",
            "MONTO_PIM"])["MONTO_DEVENGADO"]
        .sum()
        .reset_index())

    df["EJECUCION_%"] = (
        df["MONTO_DEVENGADO"]/ 
        df["MONTO_PIM"]) * 100

    df = df.sort_values(
        "EJECUCION_%",
        ascending=True,
    )
    return df   

