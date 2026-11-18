
# 4. SIDEBAR NAVIGATION AND FILTERING

import streamlit as st
from typing import TYPE_CHECKING, Any

# These names are provided by the app's shared section namespace at runtime.
# Declare them for static analysis without overriding the injected values.
if TYPE_CHECKING:
    df: Any
    NAV_NAMES: Any
    DISORDER_ORDER: Any
    DISORDER_LABELS: Any
    SOURCE_RECORDS: Any

SPARKLE = (
    "<svg width='20' height='20' viewBox='0 0 24 24' fill='none' stroke='#D1F07A' "
    "stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'>"
    "<path d='M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9z'/>"
    "<path d='M19 16l.7 1.8L21.5 18.5l-1.8.7L19 21l-.7-1.8-1.8-.7 1.8-.7z'/></svg>"
)
MOON = (
    "<svg width='24' height='24' viewBox='0 0 24 24' fill='#132A25' stroke='#132A25' "
    "stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'>"
    "<path d='M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z'/></svg>"
)


def set_page(name):
    st.session_state["page"] = name


if st.session_state.get("page") not in NAV_NAMES:
    st.session_state["page"] = NAV_NAMES[0]


# ---- Filter state ----
occupations = sorted(df["Occupation"].dropna().unique().tolist())
disorders = DISORDER_ORDER


def reset_filters():
    st.session_state["f_occ"] = list(occupations)
    for d in disorders:
        st.session_state[f"f_dis_{d}"] = True


st.session_state.setdefault("f_occ", list(occupations))
for d in disorders:
    st.session_state.setdefault(f"f_dis_{d}", True)


with st.sidebar:
    st.markdown(
        f"<div class='brand'><div class='brand-logo'>{MOON}</div>"
        "<div class='brand-text'><b>Somnia</b> / insights</div></div>"
        "<div class='side-label'>WORKSPACE</div>",
        unsafe_allow_html=True,
    )

    with st.container(key="navlist"):
        for _n, _name in enumerate(NAV_NAMES, start=1):
            st.button(
                _name,
                key=f"nav_{_n}",
                type="primary" if st.session_state["page"] == _name else "secondary",
                on_click=set_page,
                args=(_name,),
            )

    page = st.session_state["page"]

    with st.container(key="filterbox"):
        st.markdown(
            "<div class='filter-title'>FILTERS <span>Refine the data</span></div>",
            unsafe_allow_html=True,
        )

        # Occupation
        st.markdown(
            f"<div class='filter-label'>OCCUPATION "
            f"<span>{len(st.session_state['f_occ'])} of {len(occupations)} selected</span></div>",
            unsafe_allow_html=True,
        )

        with st.expander("Choose occupations"):
            st.multiselect(
                "Occupation",
                occupations,
                key="f_occ",
                label_visibility="collapsed",
            )

        # Sleep disorder
        st.markdown(
            "<div class='filter-label'>SLEEP DISORDER</div>",
            unsafe_allow_html=True,
        )

        for d in disorders:
            st.checkbox(DISORDER_LABELS[d], key=f"f_dis_{d}")

        # Apply selections
        selected_occupations = st.session_state["f_occ"]
        selected_disorders = [
            d for d in disorders
            if st.session_state[f"f_dis_{d}"]
        ]

        shown = int((
            df["Occupation"].isin(selected_occupations)
            & df["Sleep Disorder"].isin(selected_disorders)
        ).sum())

        # Footer
        with st.container(key="f_foot"):
            fc1, fc2 = st.columns([3, 2])

            fc1.markdown(
                f"<div class='filter-count'>Showing {shown:,} of {len(df):,}</div>",
                unsafe_allow_html=True,
            )

            fc2.button(
                ":material/refresh: Reset",
                key="f_reset",
                on_click=reset_filters,
            )

    st.markdown(
        f"<div class='side-card'><div class='side-card-icon'>{SPARKLE}</div>"
        "<b>Research workspace</b>"
        f"<span>Sleep Health &amp; Lifestyle Dataset · {SOURCE_RECORDS:,} records</span></div>",
        unsafe_allow_html=True,
    )


# Apply the sidebar selections to the dataset.
filtered = df[
    df["Occupation"].isin(selected_occupations)
    & df["Sleep Disorder"].isin(selected_disorders)
].copy()


if filtered.empty:
    st.warning(
        "No records match the selected filters. Adjust the filters in the sidebar."
    )
    st.stop()
