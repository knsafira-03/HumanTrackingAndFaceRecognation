import streamlit as st
import plotly.express as px
import pandas as pd


def render_charts():

    col1, col2, col3 = st.columns([1, 1, 2])

    # ---------------- Entry ----------------

    with col1:

        df = pd.DataFrame({

            "Hour":[
                "06","07","08","09","10",
                "11","12","13","14","15",
                "16","17","18"
            ],

            "Entry":[
                1,2,5,9,13,
                15,10,12,8,5,
                4,6,2
            ]

        })

        fig = px.line(
            df,
            x="Hour",
            y="Entry",
            markers=True
        )

        fig.update_layout(
            title="Entry per Hour",
            height=320,

            paper_bgcolor="white",
            plot_bgcolor="white",

            font=dict(
                family="Poppins",
                color="#334155",
                size=13,
            ),

            margin=dict(
                l=20,
                r=20,
                t=45,
                b=20,
            ),

            hoverlabel=dict(
                bgcolor="white",
                font_size=13,
                font_family="Poppins",
            ),

            xaxis=dict(
                showgrid=False,
                zeroline=False,
            ),

            yaxis=dict(
                gridcolor="#EEF2F7",
                zeroline=False,
            ),
        )

        fig.update_traces(
            line=dict(width=3),
            marker=dict(size=7),
            line_shape="spline",
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

    # ---------------- Exit ----------------

    with col2:

        df = pd.DataFrame({

            "Hour":[
                "06","07","08","09","10",
                "11","12","13","14","15",
                "16","17","18"
            ],

            "Exit":[
                0,1,3,4,7,
                8,10,6,5,2,
                1,3,2
            ]

        })

        fig = px.line(
            df,
            x="Hour",
            y="Exit",
            markers=True
        )

        fig.update_layout(
            title="Exit per Hour",
            height=320,

            paper_bgcolor="white",
            plot_bgcolor="white",

            font=dict(
                family="Poppins",
                color="#334155",
                size=13,
            ),

            margin=dict(
                l=20,
                r=20,
                t=45,
                b=20,
            ),

            hoverlabel=dict(
                bgcolor="white",
                font_size=13,
                font_family="Poppins",
            ),

            xaxis=dict(
                showgrid=False,
                zeroline=False,
            ),

            yaxis=dict(
                gridcolor="#EEF2F7",
                zeroline=False,
            ),
        )

        fig.update_traces(
            line=dict(width=3),
            marker=dict(size=7),
            line_shape="spline",
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

    # ---------------- Unauthorized ----------------

    with col3:

        df = pd.DataFrame({

            "Date":[
                "24 Jul",
                "25 Jul",
                "26 Jul",
                "27 Jul",
                "28 Jul",
                "29 Jul",
                "30 Jul"
            ],

            "Unauthorized":[
                6,
                15,
                30,
                18,
                15,
                12,
                6
            ]

        })

        fig = px.area(

            df,

            x="Date",

            y="Unauthorized",

            markers=True

        )

        fig.update_layout(
            title="Unauthorized Trends",
            height=320,

            paper_bgcolor="white",
            plot_bgcolor="white",

            font=dict(
                family="Poppins",
                color="#334155",
                size=13,
            ),

            margin=dict(
                l=20,
                r=20,
                t=45,
                b=20,
            ),

            hoverlabel=dict(
                bgcolor="white",
                font_size=13,
                font_family="Poppins",
            ),

            xaxis=dict(
                showgrid=False,
                zeroline=False,
            ),

            yaxis=dict(
                gridcolor="#EEF2F7",
                zeroline=False,
            ),
        )

        fig.update_traces(
            line_shape="spline",
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