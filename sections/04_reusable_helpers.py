# 5. REUSABLE DISPLAY AND ANALYSIS HELPERS

def _stretch_kwargs(fn):
    """New Streamlit uses width='stretch'; older versions use use_container_width."""
    try:
        params = inspect.signature(fn).parameters
    except (TypeError, ValueError):
        return {}
    if "width" in params and params["width"].default in ("stretch", "content"):
        return {"width": "stretch"}
    if "use_container_width" in params:
        return {"use_container_width": True}
    return {}


PLOT_KW = _stretch_kwargs(st.plotly_chart)
TABLE_KW = _stretch_kwargs(st.dataframe)
BUTTON_KW = _stretch_kwargs(st.button)


def plot(fig):
    st.plotly_chart(fig, **PLOT_KW)


def table(data, **kwargs):
    st.dataframe(data, **TABLE_KW, **kwargs)


def page_header(number, kicker, title, subtitle):
    st.markdown(
        f'<div class="kicker"><span class="kicker-dot"></span>FRAME {number:02d} · {kicker}</div>'
        f'<h1 class="page-title">{title}</h1>'
        f'<p class="subtitle">{subtitle}</p>',
        unsafe_allow_html=True,
    )


def stat_card(label, value, unit="", caption="", dot=TEAL_CHART, dark=False):
    cls = "stat-card dark" if dark else "stat-card"
    unit_html = f'<span class="stat-unit">{unit}</span>' if unit else ""
    st.markdown(
        f'<div class="{cls}"><div class="stat-top"><span class="stat-label">{label}</span>'
        f'<span class="stat-dot" style="background:{dot}"></span></div>'
        f'<div class="stat-value">{value}{unit_html}</div>'
        f'<div class="stat-caption">{caption}</div></div>',
        unsafe_allow_html=True,
    )


def note(html, color=TEAL_CHART):
    st.markdown(
        f'<div class="custom-card" style="border-left: 4px solid {color};">{html}</div>',
        unsafe_allow_html=True,
    )


def chart_style(fig, height=350, title="", subtitle=""):
    heading = ""
    if title:
        heading = f"<b>{title}</b>"
        if subtitle:
            heading += f"<br><span style='font-size:12px;color:{TEXT_MUTED}'>{subtitle}</span>"
    top_margin = 84 if subtitle else (56 if title else 24)
    fig.update_layout(
        title=dict(text=heading, x=0.025, xanchor="left", y=0.95, yanchor="top",
                   font=dict(family="Inter", size=16, color=TEXT_DARK)),
        template="plotly_white",
        height=height,
        paper_bgcolor=CARD_BG,
        plot_bgcolor=CARD_BG,
        font=dict(family="Inter", size=12, color=TEXT_MUTED),
        margin=dict(l=24, r=24, t=top_margin, b=24),
        xaxis=dict(showgrid=False, zeroline=False, color=TEXT_MUTED),
        yaxis=dict(showgrid=True, gridcolor="#F3F4F6", zeroline=False, color=TEXT_MUTED),
        legend=dict(orientation="h", y=-0.2, x=0),
    )
    return fig


def show(fig, height=350, title="", subtitle=""):
    plot(chart_style(fig, height, title, subtitle))


def disorder_bar(means, column, title, subtitle, text_format):
    data = means.reset_index()
    data["Label"] = data["Sleep Disorder"].map(DISORDER_LABELS)
    fig = px.bar(
        data, x=column, y="Label", orientation="h",
        color="Sleep Disorder", color_discrete_map=DISORDER_COLORS,
    )
    fig.update_traces(
        texttemplate=text_format, textposition="outside", cliponaxis=False,
        textfont=dict(color=TEXT_DARK, size=12), width=0.42,
    )
    try:
        fig.update_traces(marker_cornerradius=8)  # needs a recent Plotly
    except ValueError:
        pass
    chart_style(fig, 330, title, subtitle)
    fig.update_layout(showlegend=False)
    fig.update_xaxes(visible=False, range=[0, float(data[column].max()) * 1.3])
    fig.update_yaxes(title=None, showgrid=False, autorange="reversed")
    plot(fig)


def correlation(x, y, data):
    pair = data[[x, y]].dropna()
    if len(pair) < 3 or pair[x].nunique() < 2 or pair[y].nunique() < 2:
        return np.nan, np.nan
    result = pearsonr(pair[x], pair[y])
    return float(result.statistic), float(result.pvalue)


def p_text(p):
    if pd.isna(p):
        return "N/A"
    if p < 0.001:
        return f"{p:.2e}"
    return f"{p:.4f}"


def strength_label(r):
    if pd.isna(r):
        return "not available"
    magnitude = abs(r)
    if magnitude >= 0.70:
        return "strong"
    if magnitude >= 0.40:
        return "moderate"
    if magnitude >= 0.20:
        return "weak"
    return "very weak"


def direction_label(r):
    if pd.isna(r):
        return "no clear direction"
    if r > 0:
        return "positive"
    if r < 0:
        return "negative"
    return "no linear association"


def add_kde_histogram(data, column, x_label, bins=10, color=TEAL_CHART):
    values = data[column].dropna().to_numpy()
    fig = go.Figure()

    fig.add_trace(go.Histogram(
        x=values, nbinsx=bins, name="Number of people",
        marker_color=color, opacity=0.85,
    ))

    if len(values) > 2 and np.std(values) > 0:
        grid = np.linspace(values.min() - 0.3, values.max() + 0.3, 300)
        density = gaussian_kde(values)(grid)
        bin_width = (values.max() - values.min()) / bins
        fig.add_trace(go.Scatter(
            x=grid, y=density * len(values) * bin_width, name="KDE curve", mode="lines",
            line=dict(color=SIDEBAR_BG, width=3),
        ))

    fig.update_layout(xaxis_title=x_label, yaxis_title="Number of people", barmode="overlay")
    return fig


def disorder_groups(data, column):
    return [
        data.loc[data["Sleep Disorder"] == g, column].dropna()
        for g in DISORDER_ORDER if g in data["Sleep Disorder"].unique()
    ]


