try:
    import streamlit as st
except ImportError:  # pragma: no cover - this file is meant to run inside Streamlit.
    st = None

if "NAV_NAMES" not in globals():
    NAV_NAMES = []

if "BUTTON_KW" not in globals():
    BUTTON_KW = {}

if "TEXT_MUTED" not in globals():
    TEXT_MUTED = "#6B7280"

if "page" not in globals():
    page = st.session_state.get("page", NAV_NAMES[0] if NAV_NAMES else "") if st is not None else ""


# 7. PAGE NAVIGATION AND FOOTER
# ------------------------- PAGER ---------------------------

def go_to(step):
    if st is None:
        return
    current = NAV_NAMES.index(st.session_state["page"])
    target = max(0, min(len(NAV_NAMES) - 1, current + step))
    st.session_state["page"] = NAV_NAMES[target]


current_index = NAV_NAMES.index(page) if NAV_NAMES and page in NAV_NAMES else 0
st.markdown("<br>", unsafe_allow_html=True)
prev_col, mid_col, next_col = st.columns([2, 3, 2])
with prev_col:
    if current_index > 0:
        st.button(f"← {NAV_NAMES[current_index - 1]}", key="pager_prev",
                  on_click=go_to, args=(-1,), **BUTTON_KW)
with mid_col:
    st.markdown(f"<p class='pager-label'>FRAME {current_index + 1} OF {len(NAV_NAMES)}</p>",
                unsafe_allow_html=True)
with next_col:
    if current_index < len(NAV_NAMES) - 1:
        st.button(f"{NAV_NAMES[current_index + 1]} →", key="pager_next",
                  on_click=go_to, args=(1,), **BUTTON_KW)


# --------------------------- FOOTER ------------------------
st.markdown("<br><br><hr style='border-color: #E5E7EB;'>", unsafe_allow_html=True)
st.markdown(
    f'<p style="text-align:right;color:{TEXT_MUTED};font-size:0.8rem;">'
    'Somnia / insights<br>Sleep Health &amp; Lifestyle Dataset · 1,000 records</p>',
    unsafe_allow_html=True,
)