import streamlit as st

from components.analytics.header import render_header
from components.analytics.cards import render_cards

def render_analytics():

    render_header()
    render_cards()

    st.info("Analytics page is under development.")