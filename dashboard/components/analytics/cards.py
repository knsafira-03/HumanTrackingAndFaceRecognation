import streamlit as st


def render_cards():

    cards = [
        {
            "title": "ENTRY TODAY",
            "value": 11,
            "subtitle": "People",
            "change": "↑ 10%",
            "color": "#22C55E",
            "icon": "↪️",
        },
        {
            "title": "EXIT TODAY",
            "value": 20,
            "subtitle": "People",
            "change": "↑ 15%",
            "color": "#3B82F6",
            "icon": "↩️",
        },
        {
            "title": "UNAUTHORIZED",
            "value": 18,
            "subtitle": "Events",
            "change": "↓ 5%",
            "color": "#EF4444",
            "icon": "🚨",
        },
        {
            "title": "CURRENT OCCUPANCY",
            "value": 3,
            "subtitle": "People Inside",
            "change": "",
            "color": "#8B5CF6",
            "icon": "👥",
        },
    ]

    cols = st.columns(4)

    for col, card in zip(cols, cards):

        with col:
            st.markdown(
    f"""
    <div style="
        height:6px;
        background:{card['color']};
        border-radius:12px 12px 0 0;
        margin-bottom:-8px;">
    </div>
    """,
    unsafe_allow_html=True,
)

            with st.container(border=True):

                top1, top2 = st.columns([5, 1])

                with top1:
                    st.caption(card["title"])

                with top2:
                    st.markdown(
                        f"<div style='font-size:24px;text-align:right'>{card['icon']}</div>",
                        unsafe_allow_html=True,
                    )

                st.markdown(
                    f"""
                    <div class="metric-number">
                        {card["value"]}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.caption(card["subtitle"])

                if card["change"]:

                    st.markdown(
                        f"""
                        <span style="
                            color:{card['color']};
                            font-weight:600;
                            font-size:14px;">
                            {card['change']}
                        </span>

                        <span style="
                            color:#64748B;
                            font-size:13px;">
                            &nbsp;vs yesterday
                        </span>
                        """,
                        unsafe_allow_html=True,
                    )