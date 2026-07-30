import streamlit as st

from components.analytics.header import render_header
from components.analytics.cards import render_cards
from components.analytics.charts import render_charts
from components.analytics.tables import render_table
from components.analytics.peak_hour import render_peak_hour
from components.analytics.donut import render_donut


def render_analytics():

    render_header()

    render_cards()

    render_charts()

    left, middle, right = st.columns([2.2, 1.2, 1])

    with left:
        render_table()

    with middle:
        render_donut()

    with right:
        render_peak_hour()