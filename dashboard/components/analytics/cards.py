import streamlit as st


def render_cards():

    c1, c2, c3, c4 = st.columns(4)

    cards = [
        {
            "title": "ENTRY TODAY",
            "value": "11",
            "subtitle": "People",
            "change": "↑ 10%",
            "color": "#22C55E",
            "icon": "↪️"
        },
        {
            "title": "EXIT TODAY",
            "value": "20",
            "subtitle": "People",
            "change": "↑ 15%",
            "color": "#3B82F6",
            "icon": "↩️"
        },
        {
            "title": "UNAUTHORIZED",
            "value": "18",
            "subtitle": "Events",
            "change": "↓ 5%",
            "color": "#EF4444",
            "icon": "🚨"
        },
        {
            "title": "CURRENT OCCUPANCY",
            "value": "3",
            "subtitle": "People Inside",
            "change": "",
            "color": "#8B5CF6",
            "icon": "👥"
        },
    ]

    cols = [c1, c2, c3, c4]

    for col, card in zip(cols, cards):

        with col:

            st.markdown(
                f"""
                <div class="analytics-card"
                     style="border-left:4px solid {card['color']}">

                    <div class="analytics-card-title">
                        {card['title']}
                    </div>

                    <div class="analytics-card-icon">
                        {card['icon']}
                    </div>

                    <div class="analytics-card-value">
                        {card['value']}
                    </div>

                    <div class="analytics-card-sub">
                        {card['subtitle']}
                    </div>

                    <div class="analytics-card-change"
                         style="color:{card['color']}">
                        {card['change']}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )