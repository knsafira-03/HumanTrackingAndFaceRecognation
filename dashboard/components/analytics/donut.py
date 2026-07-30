import streamlit as st
import plotly.express as px


def render_donut():

    labels = [
        "Entry",
        "Exit",
        "Unauthorized",
    ]

    values = [
        131,
        60,
        18,
    ]

    fig = px.pie(
        names=labels,
        values=values,
        hole=0.72,
        color=labels,
        color_discrete_map={
            "Entry": "#22C55E",
            "Exit": "#3B82F6",
            "Unauthorized": "#EF4444",
        },
    )

    fig.update_traces(
        textinfo="percent",
        textfont_size=13,
        marker=dict(line=dict(color="white", width=2)),
    )

    fig.update_layout(
        title="Event Distribution",

        height=350,

        paper_bgcolor="white",
        plot_bgcolor="white",

        margin=dict(
            l=20,
            r=20,
            t=40,
            b=20
        ),

        font=dict(
            family="Poppins",
            color="#334155",
            size=13,
        ),

        legend=dict(
            orientation="h",
            y=-0.10,
            x=0.5,
            xanchor="center",
        ),

        showlegend=True,
    )

    st.plotly_chart(
        fig,
        width="stretch",
        config={
            "displayModeBar": False,
            "responsive": True,
            "displaylogo": False,
        },
    )