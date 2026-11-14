# pyright: reportUndefinedVariable=false
# 6. DASHBOARD PAGES
# ============================================================
# FRAME 01 — OVERVIEW
# ============================================================

if page == "Overview":
    page_header(1, "OVERVIEW", "The bigger picture of sleep",
                "A high-level view of the dataset, its key measures, and the first patterns emerging from the analysis.")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        stat_card("Total participants", f"{SOURCE_RECORDS:,}", "", "Source dataset", ACCENT_LIME, dark=True)
    with c2:
        stat_card("Avg. sleep duration", f"{filtered['Sleep Duration'].mean():.2f}", "hrs", "Daily average", TEAL_CHART)
    with c3:
        stat_card("Avg. sleep quality", f"{filtered['Quality of Sleep'].mean():.2f}", "/ 10", "Self-reported score", CORAL_CHART)
    with c4:
        stat_card("Avg. stress level", f"{filtered['Stress Level'].mean():.2f}", "/ 10", "Self-reported score", SLATE_CHART)

    st.markdown("<br>", unsafe_allow_html=True)
    left, right = st.columns(2)

    with left:
        fig = add_kde_histogram(filtered, "Sleep Duration", "Sleep duration (hours)")
        show(fig, 380, "Distribution of sleep duration", "How many people sleep each number of hours")
    with right:
        occ = (filtered.groupby("Occupation", as_index=False)["Quality of Sleep"]
               .mean().sort_values("Quality of Sleep"))
        fig = px.bar(occ, x="Quality of Sleep", y="Occupation", orientation="h",
                     color_discrete_sequence=[TEAL_CHART])
        fig.update_yaxes(showgrid=False, title=None)
        show(fig, 380, "Average sleep quality by occupation", "Score out of 10")

    r_duration, _ = correlation("Sleep Duration", "Quality of Sleep", filtered)
    r_stress, _ = correlation("Stress Level", "Quality of Sleep", filtered)
    r_activity, _ = correlation("Physical Activity Level", "Quality of Sleep", filtered)

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Preliminary findings")

    note(f"<b>Sleep duration → quality:</b> {strength_label(r_duration).title()} {direction_label(r_duration)} association (r = {r_duration:.4f}). Longer sleep duration tends to accompany higher reported sleep quality.", TEAL_CHART)
    note(f"<b>Stress → quality:</b> {strength_label(r_stress).title()} {direction_label(r_stress)} association (r = {r_stress:.4f}). Higher stress tends to accompany lower reported sleep quality.", CORAL_CHART)
    note(f"<b>Physical activity → quality:</b> {strength_label(r_activity).title()} {direction_label(r_activity)} association (r = {r_activity:.4f}). The relationship is positive but comparatively weak.", SLATE_CHART)

    with st.expander("Research questions"):
        for i, question in enumerate(RESEARCH_QUESTIONS, start=1):
            st.markdown(f"**RQ{i}.** {question}")

    with st.expander("Research hypotheses"):
        for title, h0, h1 in HYPOTHESES:
            st.markdown(f"**{title}**")
            st.write(h0)
            st.write(h1)


# ============================================================
# FRAME 02 — DATASET
# ============================================================

elif page == "Dataset":
    page_header(2, "THE DATA", "Dataset overview",
                "A structured view of the source data, its shape, and the variables powering this analysis.")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        stat_card("Total records", f"{SOURCE_RECORDS:,}", "", "Participant rows", ACCENT_LIME, dark=True)
    with c2:
        stat_card("Total variables", f"{SOURCE_VARIABLES}", "", "Across 3 data types", TEAL_CHART)
    with c3:
        stat_card("Missing values", f"{CLEAN_MISSING}", "", "After cleaning", CORAL_CHART)
    with c4:
        stat_card("Duplicate records", f"{DUPLICATES}", "", "Unique rows", SLATE_CHART)

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns(2)
    with col_left:
        st.subheader("Data health")
        st.progress(1.0, text="Completeness: 100%")
        st.progress(1.0, text="Unique records: 100%")
        st.progress(0.5, text="Numerical variables: 7")
        st.progress(0.4, text="Categorical variables: 6")

    with col_right:
        st.markdown(
            f'<div class="stat-card dark"><div class="stat-top">'
            f'<span class="stat-label">Source file</span>'
            f'<span class="stat-dot" style="background:{ACCENT_LIME}"></span></div>'
            f'<div class="stat-value" style="font-size:1.5rem;">Sleep health and lifestyle</div>'
            f'<div class="stat-caption">A complete snapshot of lifestyle and sleep indicators.<br>'
            f'<code style="color:{ACCENT_LIME};background:transparent;padding:0;">'
            f'Sleep_health_and_lifestyle_dataset_1000.csv</code></div></div>',
            unsafe_allow_html=True,
        )

    st.subheader("Variable dictionary")
    dictionary = [
        {"Variable": col, "Type": VARIABLE_DESCRIPTIONS[col][0],
         "Description": VARIABLE_DESCRIPTIONS[col][1], "Status": "✅"}
        for col in REQUIRED_COLUMNS
    ]
    table(pd.DataFrame(dictionary), hide_index=True)

    st.subheader("Dataset preview")
    table(filtered[REQUIRED_COLUMNS].head(10), hide_index=True)

    st.info(f"Data-cleaning note: the source CSV has {raw_disorder_missing} blank cells in 'Sleep Disorder'. These are classified as 'None'.")

    st.subheader("Download data")
    d1, d2 = st.columns(2)
    with d1:
        st.download_button("Download cleaned dataset", data=df.to_csv(index=False).encode("utf-8"),
                           file_name="somnia_cleaned_dataset.csv", mime="text/csv")
    with d2:
        st.download_button("Download original source CSV", data=raw_df.to_csv(index=False).encode("utf-8"),
                           file_name="Sleep_health_and_lifestyle_dataset_1000.csv", mime="text/csv")


# ============================================================
# FRAME 03 — EXPLORATORY ANALYSIS
# ============================================================

elif page == "Exploratory analysis":
    page_header(3, "EXPLORATORY ANALYSIS", "The shape of sleep",
                "Start with the fundamentals. These distributions show how participants are spread across duration, quality, stress, and activity.")

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        stat_card("Average duration", f"{filtered['Sleep Duration'].mean():.2f}", "hrs",
                  f"Median: {filtered['Sleep Duration'].median():.1f} hrs", ACCENT_LIME, dark=True)
    with m2:
        stat_card("Average quality", f"{filtered['Quality of Sleep'].mean():.2f}", "/ 10",
                  f"Mode: {filtered['Quality of Sleep'].mode().iloc[0]:.0f} / 10", CORAL_CHART)
    with m3:
        stat_card("Average stress", f"{filtered['Stress Level'].mean():.2f}", "/ 10",
                  f"Mode: {filtered['Stress Level'].mode().iloc[0]:.0f} / 10", SLATE_CHART)
    with m4:
        stat_card("Average activity", f"{filtered['Physical Activity Level'].mean():.2f}", "min",
                  "Daily average", TEAL_CHART)

    st.markdown("<br>", unsafe_allow_html=True)
    left, right = st.columns(2)

    with left:
        show(add_kde_histogram(filtered, "Sleep Duration", "Sleep duration (hours)"), 360,
             "Sleep duration distribution", "Hours per night")
    with right:
        fig = px.histogram(filtered, x="Quality of Sleep", nbins=10, color_discrete_sequence=[CORAL_CHART])
        show(fig, 360, "Sleep quality distribution", "Self-reported score")

    st.markdown("<br>", unsafe_allow_html=True)
    left, right = st.columns(2)
    with left:
        fig = px.histogram(filtered, x="Stress Level", nbins=8, color_discrete_sequence=[LIME_CHART])
        show(fig, 360, "Stress level distribution", "Self-reported score")
    with right:
        fig = px.histogram(filtered, x="Physical Activity Level", nbins=10, color_discrete_sequence=[SLATE_CHART])
        show(fig, 360, "Physical activity distribution", "Minutes per day")

    st.markdown("<br>", unsafe_allow_html=True)
    note("<b>Distribution observation:</b> In the full dataset, sleep durations are concentrated mainly between 6 and 8 hours. Longer sleep is associated with lower stress in this sample.", TEAL_CHART)

    with st.expander("Numerical summary statistics"):
        summary = filtered[NUMERIC_MEASURES].describe().T
        summary.columns = ["Count", "Mean", "Std. deviation", "Minimum", "25th percentile",
                           "Median", "75th percentile", "Maximum"]
        table(summary.round(2))


# ============================================================
# FRAME 04 — RELATIONSHIPS
# ============================================================

elif page == "Relationships":
    page_header(4, "RELATIONSHIP ANALYSIS", "What moves with sleep quality?",
                "Focused comparisons connect sleep duration, physical activity, and stress directly to the quality of sleep reported by participants.")

    relationships = [
        ("Sleep Duration", "Quality of Sleep", "Sleep duration vs. quality", "Positive relationship", TEAL_CHART),
        ("Physical Activity Level", "Quality of Sleep", "Physical activity vs. quality", "Weak positive relationship", SLATE_CHART),
        ("Stress Level", "Quality of Sleep", "Stress level vs. quality", "Negative relationship", CORAL_CHART),
    ]

    for x, y, title, relationship, color in relationships:
        r, p = correlation(x, y, filtered)

        st.markdown(f"### {title}")
        st.caption(f"{relationship} · Pearson r = {r:.4f} · p-value = {p_text(p)}")

        col1, col2 = st.columns(2)
        with col1:
            fig = px.scatter(filtered, x=x, y=y, color_discrete_sequence=[color])
            fig.update_traces(marker=dict(size=8, opacity=0.7))
            show(fig, 320, "Each point is one participant", f"{x} vs. {y}")
        with col2:
            avg = filtered.groupby(x, as_index=False)[y].mean().sort_values(x)
            line = px.line(avg, x=x, y=y, markers=True, color_discrete_sequence=[SIDEBAR_BG])
            line.update_traces(line=dict(width=3), marker=dict(size=8, color=color))
            show(line, 320, "Average trend", f"Mean {y.lower()} at each {x.lower()}")

        significance = ("The association is statistically significant at the 0.05 level."
                        if p < .05 else
                        "The association is not statistically significant at the 0.05 level.")
        note(f"<b>Interpretation:</b> The observed relationship is {strength_label(r)} and {direction_label(r)} (r = {r:.4f}). {significance} Correlation indicates association, not causation.", color)
        st.markdown("---")

    st.subheader("Which factors show the strongest relationship with sleep quality?")
    corr_vars = ["Sleep Duration", "Age", "Physical Activity Level", "Daily Steps", "Heart Rate", "Stress Level"]
    corr_rows = []
    for col in corr_vars:
        r_val, p_val = correlation(col, "Quality of Sleep", filtered)
        corr_rows.append({"Variable": col, "Pearson r": r_val, "p-value": p_text(p_val)})
    corr_df = pd.DataFrame(corr_rows).sort_values("Pearson r", ascending=False)

    fig = px.bar(corr_df, x="Pearson r", y="Variable", orientation="h", color="Pearson r",
                 color_continuous_scale=[CORAL_CHART, "#F3F4F6", TEAL_CHART], range_color=[-1, 1])
    fig.update_yaxes(showgrid=False, title=None, autorange="reversed")
    show(fig, 380, "Correlation with sleep quality", "Pearson r, from -1 to 1")

    st.subheader("Correlation heatmap")
    heat_columns = ["Age", "Sleep Duration", "Quality of Sleep", "Physical Activity Level",
                    "Stress Level", "Heart Rate", "Daily Steps"]
    corr_matrix = filtered[heat_columns].corr()

    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values, x=corr_matrix.columns, y=corr_matrix.index, zmin=-1, zmax=1,
        colorscale=[[0, CORAL_CHART], [.5, "#F8F9FA"], [1, TEAL_CHART]],
        text=np.round(corr_matrix.values, 2), texttemplate="%{text}",
    ))
    show(fig, 480, "How every measure relates to every other", "Darker teal means a stronger positive link")


# ============================================================
# FRAME 05 — SLEEP DISORDER COMPARISON
# ============================================================

elif page == "Disorder comparison":
    page_header(5, "SLEEP DISORDER COMPARISON", "Three different sleep profiles",
                "Comparing group averages makes the impact of insomnia and sleep apnea tangible.")

    group_means = (
        filtered.groupby("Sleep Disorder")[["Sleep Duration", "Quality of Sleep",
                                            "Physical Activity Level", "Stress Level"]]
        .mean().reindex(DISORDER_ORDER).dropna(how="all")
    )

    cols = st.columns(3)
    for col, group in zip(cols, DISORDER_ORDER):
        with col:
            if group in group_means.index:
                stat_card(DISORDER_LABELS[group], f"{group_means.loc[group, 'Quality of Sleep']:.1f}",
                          "/ 10", "Average sleep quality", DISORDER_DOTS[group], dark=(group == "None"))

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns(2)
    with col_left:
        disorder_bar(group_means, "Quality of Sleep", "Average sleep quality",
                     "A lower score indicates poorer reported sleep", "%{x:.1f} / 10")
    with col_right:
        disorder_bar(group_means, "Sleep Duration", "Average sleep duration",
                     "Hours per night by disorder group", "%{x:.1f} hrs")

    group_quality = disorder_groups(filtered, "Quality of Sleep")
    group_duration = disorder_groups(filtered, "Sleep Duration")

    if len(group_quality) >= 2 and all(len(g) > 0 for g in group_quality):
        f_q, p_q = f_oneway(*group_quality)
        f_d, p_d = f_oneway(*group_duration)

        verdict_q = ("The group means differ significantly at α = 0.05."
                     if p_q < .05 else "There is not sufficient evidence of a difference.")
        verdict_d = ("The group means differ significantly at α = 0.05."
                     if p_d < .05 else "There is not sufficient evidence of a difference.")

        st.markdown(
            '<div class="insight"><h4>The clearest difference</h4>'
            f'<p><b>Quality of sleep:</b> F = {f_q:.2f}, p = {p_text(p_q)}. {verdict_q}<br><br>'
            f'<b>Sleep duration:</b> F = {f_d:.2f}, p = {p_text(p_d)}. {verdict_d}</p></div>',
            unsafe_allow_html=True,
        )
    else:
        st.info("Select at least two sleep disorder groups in the filters to run the ANOVA tests.")


# ============================================================
# FRAME 06 — FINDINGS & CONCLUSION
# ============================================================

elif page == "Findings & conclusion":
    page_header(6, "FINDINGS & CONCLUSION", "The story so far",
                "A concise readout of the analysis, organized around the research questions and hypotheses.")

    r_duration, p_duration = correlation("Sleep Duration", "Quality of Sleep", filtered)
    r_stress, p_stress = correlation("Stress Level", "Quality of Sleep", filtered)
    r_activity, p_activity = correlation("Physical Activity Level", "Quality of Sleep", filtered)

    def finding(title, pill, pill_bg, pill_fg, body):
        st.markdown(
            f'<div class="custom-card"><h4>{title}</h4>'
            f'<span class="pill" style="background:{pill_bg};color:{pill_fg};">{pill}</span>'
            f'<p style="margin-top:10px;">{body}</p></div>',
            unsafe_allow_html=True,
        )

    col1, col2 = st.columns(2)
    with col1:
        finding("Sleep duration → quality", "Positive signal", LIME_CHART, SIDEBAR_BG,
                f"Participants sleeping longer generally report better quality scores. (r = {r_duration:.4f}, p = {p_text(p_duration)})")
        finding("Physical activity → quality", "Moderate signal", LIME_CHART, SIDEBAR_BG,
                f"Daily movement is associated with a modest lift in reported quality. (r = {r_activity:.4f}, p = {p_text(p_activity)})")
    with col2:
        finding("Stress → quality", "Inverse signal", CORAL_CHART, "white",
                f"Stress is the strongest visible lifestyle factor working against quality. (r = {r_stress:.4f}, p = {p_text(p_stress)})")
        finding("Disorders → sleep characteristics", "Clear difference", SLATE_CHART, "white",
                "Disorder groups show distinct quality, stress, and duration profiles.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Hypothesis testing summary")

    group_quality = disorder_groups(filtered, "Quality of Sleep")
    p_anova_q = np.nan
    if len(group_quality) >= 2 and all(len(g) > 0 for g in group_quality):
        p_anova_q = f_oneway(*group_quality).pvalue

    def decision(p):
        return "Reject H₀; H₁ supported" if (not pd.isna(p) and p < .05) else "Fail to reject H₀"

    hypothesis_table = pd.DataFrame([
        {"Hypothesis": "H1 · Sleep duration and quality", "Test": "Pearson correlation",
         "Evidence": f"r = {r_duration:.4f}; p = {p_text(p_duration)}", "Decision": decision(p_duration)},
        {"Hypothesis": "H2 · Stress and quality", "Test": "Pearson correlation",
         "Evidence": f"r = {r_stress:.4f}; p = {p_text(p_stress)}", "Decision": decision(p_stress)},
        {"Hypothesis": "H3 · Disorder group differences", "Test": "One-way ANOVA",
         "Evidence": f"Quality p = {p_text(p_anova_q)}", "Decision": decision(p_anova_q)},
    ])
    table(hypothesis_table, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        f'<div style="background-color:{CARD_DARK};padding:30px 34px;border-radius:18px;">'
        f'<p style="color:{ACCENT_LIME};font-size:0.75rem;font-weight:700;letter-spacing:1px;margin:0;">CONCLUSION</p>'
        f'<h3 style="color:#FFFFFF !important;margin:6px 0 14px 0;">Sleep quality is connected to lifestyle and sleep patterns.</h3>'
        '<p style="color:#A9BDB9;line-height:1.65;font-size:0.95rem;margin:0;">'
        'Across this 1,000-record dataset, sleep duration has a strong positive association '
        'with reported sleep quality, while stress has a strong negative association. '
        'Physical activity has a weaker positive association. The sleep-disorder groups '
        'also show differences in sleep duration and quality. These findings describe '
        'patterns and associations in this dataset; they do not prove that one factor causes another.'
        '</p></div>',
        unsafe_allow_html=True,
    )


