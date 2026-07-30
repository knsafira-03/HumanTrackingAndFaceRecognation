from components.header import render_header
from components.metrics import render_metrics
from components.activity import render_activity
from components.footer import render_footer


def render_dashboard():

    render_header()

    render_metrics()

    render_activity()

    render_footer()