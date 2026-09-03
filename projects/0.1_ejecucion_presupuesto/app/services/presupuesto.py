import pandas as pd


def filtrar_presupuesto(
    presupuesto: pd.DataFrame,
    departamento: str,
    provincia: str,
    distrito: str | None = None,
) -> pd.DataFrame:

    df = presupuesto[
        (presupuesto["DEPARTAMENTO_EJECUTORA_NOMBRE"] == departamento)
        & (presupuesto["PROVINCIA_EJECUTORA_NOMBRE"] == provincia)
    ].copy()

    if distrito != "Todas":
        df = df[df["EJECUTORA_NOMBRE"] == distrito]

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
        & (ejecucion["PROVINCIA_EJECUTORA_NOMBRE"] == provincia)
        & (ejecucion["MES_EJE"] <= mes)
    ].copy()

    if distrito != "Todas":
        df = df[df["EJECUTORA_NOMBRE"] == distrito]

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