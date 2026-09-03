import plotly.express as px
import streamlit as st


def mostrar_ejecucion_por_distrito(
    ejecucion_entidad,
    opcion_ranking
):

    st.subheader("Ejecución presupuestal por distrito")

    if opcion_ranking == "Top 10":

        datos_grafico = (
            ejecucion_entidad
            .sort_values(
                "EJECUCION_%",
                ascending=False
            )
            .head(10)
        )

        # Mayor → menor
        datos_grafico = datos_grafico.sort_values(
            "EJECUCION_%",
            ascending=True
        )

    elif opcion_ranking == "Bottom 10":

        datos_grafico = (
            ejecucion_entidad
            .sort_values(
                "EJECUCION_%",
                ascending=True
            )
            .head(10)
        )

        # Menor → mayor
        datos_grafico = datos_grafico.sort_values(
            "EJECUCION_%",
            ascending=True
        )

    else:

        datos_grafico = (
            ejecucion_entidad
            .sort_values(
                "EJECUCION_%",
                ascending=True
            )
        )

    fig = px.bar(
        datos_grafico,
        x="EJECUCION_%",
        y="EJECUTORA_NOMBRE",
        orientation="h",
        text="EJECUCION_%",
        labels={
            "EJECUCION_%": "Ejecución (%)",
            "EJECUTORA_NOMBRE": "Distrito"
        },
        title="Ejecución presupuestal por distrito"
    )

    fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside",
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Ejecución: %{x:.2f}%"
            "<extra></extra>"
        )
    )

    fig.add_vline(
        x=100,
        line_dash="dash",
        annotation_text="100%",
        annotation_position="top"
    )

    fig.update_layout(
        height=max(
            500,
            len(datos_grafico) * 35
        ),
        xaxis_title="Ejecución (%)",
        yaxis_title="",
        xaxis={
            "ticksuffix": "%"
        },
        hovermode="y"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )