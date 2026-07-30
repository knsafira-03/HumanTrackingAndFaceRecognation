import streamlit as st
import plotly.express as px
import pandas as pd


def render_peak_hour():

    st.markdown(
        """
        <div class="analytics-section-title">
            Peak Hour
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="peak-hour-badge">
            🕘 09:00 – 10:00
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="peak-hour-subtitle">
            Most Active Hour
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="peak-hour-value">
            25
        </div>

        <div class="peak-hour-people">
            People
        </div>
        """,
        unsafe_allow_html=True,
    )

    df = pd.DataFrame(
        {
            "Hour": list(range(8)),
            "Entry": [2, 8, 16, 10, 7, 6, 5, 2],
        }
    )

    fig = px.bar(
        df,
        x="Hour",
        y="Entry",
        color_discrete_sequence=["#22C55E"],
    )

    fig.update_traces(
        marker_line_width=0,
    )

    fig.update_layout(

        height=150,

        paper_bgcolor="white",
        plot_bgcolor="white",

        margin=dict(
            l=0,
            r=0,
            t=0,
            b=0,
        ),

        xaxis_title=None,
        yaxis_title=None,

        xaxis=dict(
            showgrid=False,
            zeroline=False,
        ),

        yaxis=dict(
            showgrid=False,
            zeroline=False,
        ),
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False,
            "responsive": True,
            "displaylogo": False,
        },
    )