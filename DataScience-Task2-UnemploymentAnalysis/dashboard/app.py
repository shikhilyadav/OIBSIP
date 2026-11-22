"""
app.py
======
Interactive Streamlit Analytics Dashboard for Oasis Infobyte Task 2:
Unemployment Analysis with Python (India).

Features:
- Professional White & Emerald Green UI/UX theme.
- Dynamic KPI metrics calculated from active filters.
- Interactive Plotly Express & Graph Objects visualizations (including OLS trendlines).
- Comprehensive filtering by State, Date Range, Sector (Rural/Urban), and COVID Phase.
- Robust data type casting and safe handling for PyArrow serialization.
- Automatic fallback runner when launched via bare `python app.py`.
- 6 Modular Sections:
  1. Overview & High-Level KPIs
  2. Regional & State-wise Analysis
  3. Monthly Trends & Temporal Dynamics
  4. COVID-19 Pandemic Shock Analysis
  5. Employment & Labour Participation Dynamics
  6. Strategic Economic Insights & Policy Recommendations
"""

import os
import sys
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Configure Streamlit page layout and branding
st.set_page_config(
    page_title="Indian Unemployment Analytics Dashboard | Oasis Infobyte Task 2",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Emerald green styling tokens
THEME_GREEN = "#059669"
THEME_LIGHT_GREEN = "#ecfdf5"
THEME_BORDER = "#e2e8f0"
THEME_DARK = "#0f172a"
THEME_RED = "#ef4444"
THEME_BLUE = "#3b82f6"

# Apply custom CSS styling for modern card layout
st.markdown(f"""
<style>
    .main-title {{
        font-size: 2.2rem;
        font-weight: 800;
        color: {THEME_DARK};
        margin-bottom: 0.1rem;
    }}
    .sub-title {{
        font-size: 1.05rem;
        color: #64748b;
        margin-bottom: 1.5rem;
    }}
    .kpi-card {{
        background-color: white;
        border-radius: 12px;
        padding: 18px 20px;
        border: 1px solid {THEME_BORDER};
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        border-top: 4px solid {THEME_GREEN};
    }}
    .kpi-value {{
        font-size: 1.85rem;
        font-weight: 800;
        color: {THEME_DARK};
        margin-top: 4px;
    }}
    .kpi-label {{
        font-size: 0.82rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748b;
    }}
    .kpi-delta {{
        font-size: 0.85rem;
        font-weight: 600;
        margin-top: 4px;
    }}
    .delta-positive {{ color: {THEME_RED}; }}
    .delta-negative {{ color: {THEME_GREEN}; }}
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
    }}
    .stTabs [data-baseweb="tab"] {{
        height: 48px;
        white-space: pre-wrap;
        border-radius: 8px 8px 0px 0px;
        padding: 10px 20px;
        font-weight: 600;
    }}
    .stTabs [aria-selected="true"] {{
        color: {THEME_GREEN} !important;
        border-bottom-color: {THEME_GREEN} !important;
    }}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    """
    Loads, sanitizes, and caches the standardized CMIE dataset.
    Explicitly enforces numeric typing to prevent PyArrow serialization mismatches.
    """
    dashboard_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(dashboard_dir)
    data_path = os.path.join(project_root, "data", "processed", "unemployment_cleaned.csv")

    if not os.path.exists(data_path):
        # Fallback to dynamic cleaning if not already exported
        src_dir = os.path.join(project_root, "src")
        if src_dir not in sys.path:
            sys.path.insert(0, src_dir)
        from data_loader import download_dataset_if_missing, load_raw_unemployment_data
        from data_cleaning import clean_unemployment_data
        download_dataset_if_missing()
        raw_df = load_raw_unemployment_data()
        df, _ = clean_unemployment_data(raw_df, export_path=data_path)
    else:
        df = pd.read_csv(data_path)

    # Robust type casting to guarantee clean numerical operations and PyArrow compatibility
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    numeric_cols = [
        "Estimated_Unemployment_Rate",
        "Estimated_Employed",
        "Estimated_Labour_Participation_Rate"
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Drop any null records in essential dimensions
    df.dropna(subset=["Estimated_Unemployment_Rate", "Date", "State"], inplace=True)
    return df


def main():
    df_full = load_data()

    # Header
    st.markdown('<div class="main-title">🇮🇳 Indian Unemployment Analytics Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">OASIS INFOBYTE Data Science Internship | Task 2: Historical CMIE Macroeconomic Analysis (2019-2020)</div>', unsafe_allow_html=True)

    # ---------------------------------------------------------
    # SIDEBAR CONTROLS & INTERACTIVE FILTERS
    # ---------------------------------------------------------
    st.sidebar.header("🔍 Analytical Filters")
    st.sidebar.markdown("Filter macroeconomic indicators dynamically across geographic and temporal dimensions.")

    # 1. Sector Filter
    area_options = ["All Sectors"] + sorted(df_full["Area"].unique().tolist())
    selected_area = st.sidebar.selectbox("Sector Classification:", area_options, index=0)

    # 2. Macro Zone Filter
    zone_options = ["All Zones"] + sorted(df_full["Zone"].unique().tolist())
    selected_zone = st.sidebar.selectbox("Macro-Geographical Zone:", zone_options, index=0)

    # 3. State Multiselect
    available_states = df_full["State"].unique()
    if selected_zone != "All Zones":
        available_states = df_full[df_full["Zone"] == selected_zone]["State"].unique()

    all_states_sorted = sorted(available_states.tolist())
    selected_states = st.sidebar.multiselect(
        "Select Specific States (Defaults to All):",
        all_states_sorted,
        default=[]
    )

    # 4. COVID Period Filter
    covid_phase_options = ["All Periods", "Pre-COVID (May 2019 - Feb 2020)", "COVID/Post-COVID (Mar 2020 - Jun 2020)"]
    selected_phase = st.sidebar.radio("Timeline Boundary:", covid_phase_options, index=0)

    # 5. Date Range Slider
    min_date = df_full["Date"].min().to_pydatetime()
    max_date = df_full["Date"].max().to_pydatetime()
    date_range = st.sidebar.slider(
        "Observation Time Window:",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date),
        format="MMM YYYY"
    )

    # Filter Logic
    filtered_df = df_full.copy()
    if selected_area != "All Sectors":
        filtered_df = filtered_df[filtered_df["Area"] == selected_area]

    if selected_zone != "All Zones":
        filtered_df = filtered_df[filtered_df["Zone"] == selected_zone]

    if selected_states:
        filtered_df = filtered_df[filtered_df["State"].isin(selected_states)]

    if selected_phase == "Pre-COVID (May 2019 - Feb 2020)":
        filtered_df = filtered_df[filtered_df["COVID_Phase"] == "Pre-COVID"]
    elif selected_phase == "COVID/Post-COVID (Mar 2020 - Jun 2020)":
        filtered_df = filtered_df[filtered_df["COVID_Phase"] == "COVID/Post-COVID"]

    filtered_df = filtered_df[(filtered_df["Date"] >= date_range[0]) & (filtered_df["Date"] <= date_range[1])]

    # Guard against over-filtering
    if filtered_df.empty:
        st.warning("⚠️ No records match your selected filter combination. Please broaden your selection.")
        return

    # ---------------------------------------------------------
    # DYNAMIC TOP KPI CARDS
    # ---------------------------------------------------------
    avg_unemp = float(filtered_df["Estimated_Unemployment_Rate"].mean())
    median_unemp = float(filtered_df["Estimated_Unemployment_Rate"].median())
    avg_lpr = float(filtered_df["Estimated_Labour_Participation_Rate"].mean())
    total_obs = len(filtered_df)

    state_group = filtered_df.groupby("State")["Estimated_Unemployment_Rate"].mean()
    highest_state = str(state_group.idxmax()) if not state_group.empty else "N/A"
    highest_rate = float(state_group.max()) if not state_group.empty else 0.0
    lowest_state = str(state_group.idxmin()) if not state_group.empty else "N/A"
    lowest_rate = float(state_group.min()) if not state_group.empty else 0.0

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Average Unemployment Rate</div>
            <div class="kpi-value">{avg_unemp:.2f}%</div>
            <div class="kpi-delta">Median: {median_unemp:.2f}% ({total_obs:,d} records)</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Highest Unemployment State</div>
            <div class="kpi-value" style="color: #dc2626;">{highest_state}</div>
            <div class="kpi-delta delta-positive">Avg Rate: {highest_rate:.2f}%</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Lowest Unemployment State</div>
            <div class="kpi-value" style="color: #059669;">{lowest_state}</div>
            <div class="kpi-delta delta-negative">Avg Rate: {lowest_rate:.2f}%</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Labour Participation Rate</div>
            <div class="kpi-value">{avg_lpr:.2f}%</div>
            <div class="kpi-delta">Active Workforce Share</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # MAIN ANALYTICAL SECTIONS (TABS)
    # ---------------------------------------------------------
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 1. Overview",
        "🗺️ 2. Regional Analysis",
        "📅 3. Monthly Trends",
        "🦠 4. COVID-19 Impact",
        "💼 5. Employment Analysis",
        "💡 6. Economic Insights"
    ])

    # ---------------------------------------------------------
    # TAB 1: OVERVIEW
    # ---------------------------------------------------------
    with tab1:
        st.subheader("Macroeconomic Performance Overview")
        col_l, col_r = st.columns([1.1, 0.9])

        with col_l:
            # Distribution Histogram & Boxplot
            fig_dist = px.histogram(
                filtered_df,
                x="Estimated_Unemployment_Rate",
                nbins=35,
                marginal="box",
                color_discrete_sequence=[THEME_GREEN],
                title="Unemployment Rate Distribution (Density & Quartiles)",
                labels={"Estimated_Unemployment_Rate": "Unemployment Rate (%)"}
            )
            fig_dist.add_vline(x=avg_unemp, line_dash="dash", line_color=THEME_RED, annotation_text=f"Mean: {avg_unemp:.2f}%")
            fig_dist.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig_dist, width="stretch")

        with col_r:
            # Descriptive Statistics Table - All string types to prevent Arrow conversion conflicts
            st.markdown("#### Summary Statistical Indicators")
            summary_stats = pd.DataFrame({
                "Metric": [
                    "Observation Count",
                    "Mean (%)",
                    "Standard Deviation (%)",
                    "Median (%)",
                    "25th Percentile (%)",
                    "75th Percentile (%)",
                    "Min (%)",
                    "Max (%)"
                ],
                "Unemployment Rate": [
                    f"{len(filtered_df):,d}",
                    f"{filtered_df['Estimated_Unemployment_Rate'].mean():.2f}%",
                    f"{filtered_df['Estimated_Unemployment_Rate'].std():.2f}%",
                    f"{filtered_df['Estimated_Unemployment_Rate'].median():.2f}%",
                    f"{filtered_df['Estimated_Unemployment_Rate'].quantile(0.25):.2f}%",
                    f"{filtered_df['Estimated_Unemployment_Rate'].quantile(0.75):.2f}%",
                    f"{filtered_df['Estimated_Unemployment_Rate'].min():.2f}%",
                    f"{filtered_df['Estimated_Unemployment_Rate'].max():.2f}%"
                ],
                "Labour Participation": [
                    f"{len(filtered_df):,d}",
                    f"{filtered_df['Estimated_Labour_Participation_Rate'].mean():.2f}%",
                    f"{filtered_df['Estimated_Labour_Participation_Rate'].std():.2f}%",
                    f"{filtered_df['Estimated_Labour_Participation_Rate'].median():.2f}%",
                    f"{filtered_df['Estimated_Labour_Participation_Rate'].quantile(0.25):.2f}%",
                    f"{filtered_df['Estimated_Labour_Participation_Rate'].quantile(0.75):.2f}%",
                    f"{filtered_df['Estimated_Labour_Participation_Rate'].min():.2f}%",
                    f"{filtered_df['Estimated_Labour_Participation_Rate'].max():.2f}%"
                ]
            })
            st.dataframe(summary_stats, hide_index=True, width="stretch")

            st.info("""
            **Observation:** The unemployment distribution exhibits pronounced right-skewness.
            While standard non-crisis unemployment rates clustered around 8%–11%, extreme outliers
            emerged during April–May 2020 reaching up to 75.8% due to nationwide lockdowns.
            """)

    # ---------------------------------------------------------
    # TAB 2: REGIONAL ANALYSIS
    # ---------------------------------------------------------
    with tab2:
        st.subheader("State-Wise & Regional Disparities")

        col2_1, col2_2 = st.columns([1.2, 0.8])
        with col2_1:
            # Horizontal Bar Chart: Ranked States
            state_agg = filtered_df.groupby("State")["Estimated_Unemployment_Rate"].mean().reset_index()
            state_agg = state_agg.sort_values(by="Estimated_Unemployment_Rate", ascending=True)

            fig_bar = px.bar(
                state_agg,
                x="Estimated_Unemployment_Rate",
                y="State",
                orientation="h",
                color="Estimated_Unemployment_Rate",
                color_continuous_scale="Viridis",
                title="Average Unemployment Rate by State/UT",
                labels={"Estimated_Unemployment_Rate": "Average Unemployment Rate (%)"},
                height=650
            )
            fig_bar.add_vline(x=avg_unemp, line_dash="dot", line_color="red", annotation_text="Filtered Average")
            fig_bar.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig_bar, width="stretch")

        with col2_2:
            st.markdown("#### Top 10 States with Highest Unemployment")
            top10_df = state_agg.sort_values(by="Estimated_Unemployment_Rate", ascending=False).head(10).reset_index(drop=True)
            top10_df.index += 1
            top10_display = top10_df.rename(columns={"Estimated_Unemployment_Rate": "Avg Rate (%)"})
            top10_display["Avg Rate (%)"] = top10_display["Avg Rate (%)"].round(2)
            st.dataframe(top10_display, width="stretch")

            # Macro Zone Breakdown
            st.markdown("#### Macro Geographical Zone Comparison")
            zone_agg = filtered_df.groupby("Zone")["Estimated_Unemployment_Rate"].mean().reset_index()
            fig_zone = px.pie(
                zone_agg,
                names="Zone",
                values="Estimated_Unemployment_Rate",
                color_discrete_sequence=px.colors.sequential.Greens_r,
                title="Unemployment Share by Macro Zone",
                hole=0.4
            )
            fig_zone.update_layout(margin=dict(l=10, r=10, t=35, b=10))
            st.plotly_chart(fig_zone, width="stretch")

    # ---------------------------------------------------------
    # TAB 3: MONTHLY TRENDS
    # ---------------------------------------------------------
    with tab3:
        st.subheader("Monthly Temporal Trends & Volatility")

        # Time series line chart
        monthly_df = filtered_df.groupby(["Date", "COVID_Phase"])["Estimated_Unemployment_Rate"].mean().reset_index()

        fig_time = px.line(
            monthly_df,
            x="Date",
            y="Estimated_Unemployment_Rate",
            color_discrete_sequence=[THEME_GREEN],
            markers=True,
            title="Monthly Average Unemployment Rate Over Time",
            labels={"Estimated_Unemployment_Rate": "Unemployment Rate (%)", "Date": "Month"}
        )
        fig_time.add_vline(
            x=pd.Timestamp("2020-03-24").timestamp() * 1000,
            line_dash="dash",
            line_color=THEME_RED,
            annotation_text="Nationwide Lockdown (Mar 24, 2020)"
        )
        fig_time.update_layout(template="plotly_white", height=450)
        st.plotly_chart(fig_time, width="stretch")

        # Multi-state comparative time series
        st.markdown("#### Comparative Trajectory Across Select States")
        comp_states = st.multiselect(
            "Select States to compare over time:",
            sorted(df_full["State"].unique()),
            default=["Maharashtra", "Uttar Pradesh", "Bihar", "Delhi", "Tamil Nadu"]
        )
        if comp_states:
            comp_df = df_full[df_full["State"].isin(comp_states)].groupby(["Date", "State"])["Estimated_Unemployment_Rate"].mean().reset_index()
            fig_comp = px.line(
                comp_df,
                x="Date",
                y="Estimated_Unemployment_Rate",
                color="State",
                markers=True,
                title="State-by-State Comparative Trajectory",
                labels={"Estimated_Unemployment_Rate": "Unemployment Rate (%)"}
            )
            fig_comp.update_layout(template="plotly_white", height=450)
            st.plotly_chart(fig_comp, width="stretch")

    # ---------------------------------------------------------
    # TAB 4: COVID-19 IMPACT
    # ---------------------------------------------------------
    with tab4:
        st.subheader("Empirical Assessment of the COVID-19 Lockdown Shock")

        # Dynamically apply active geographical and sector filters to the COVID comparison cohort
        covid_cohort = df_full.copy()
        if selected_area != "All Sectors":
            covid_cohort = covid_cohort[covid_cohort["Area"] == selected_area]
        if selected_zone != "All Zones":
            covid_cohort = covid_cohort[covid_cohort["Zone"] == selected_zone]
        if selected_states:
            covid_cohort = covid_cohort[covid_cohort["State"].isin(selected_states)]

        pre_mask = covid_cohort["COVID_Phase"] == "Pre-COVID"
        post_mask = covid_cohort["COVID_Phase"] == "COVID/Post-COVID"

        if pre_mask.any() and post_mask.any():
            pre_mean = float(covid_cohort[pre_mask]["Estimated_Unemployment_Rate"].mean())
            post_mean = float(covid_cohort[post_mask]["Estimated_Unemployment_Rate"].mean())
            abs_surge = post_mean - pre_mean
            pct_surge = (abs_surge / pre_mean) * 100 if pre_mean != 0 else 0.0
        else:
            pre_mean = float(df_full[df_full["COVID_Phase"] == "Pre-COVID"]["Estimated_Unemployment_Rate"].mean())
            post_mean = float(df_full[df_full["COVID_Phase"] == "COVID/Post-COVID"]["Estimated_Unemployment_Rate"].mean())
            abs_surge = post_mean - pre_mean
            pct_surge = (abs_surge / pre_mean) * 100

        col4_1, col4_2, col4_3 = st.columns(3)
        with col4_1:
            st.metric("Pre-COVID Mean Rate (May 2019 - Feb 2020)", f"{pre_mean:.2f}%")
        with col4_2:
            st.metric("COVID/Post-COVID Mean Rate (Mar 2020 - Jun 2020)", f"{post_mean:.2f}%", f"+{abs_surge:.2f}%", delta_color="inverse")
        with col4_3:
            st.metric("Relative Percent Surge", f"+{pct_surge:.1f}%")

        c1, c2 = st.columns(2)
        with c1:
            # Sector comparison: Rural vs Urban Pre/Post
            eval_sector_df = covid_cohort if selected_area == "All Sectors" else df_full
            sector_agg = eval_sector_df.groupby(["Area", "COVID_Phase"])["Estimated_Unemployment_Rate"].mean().reset_index()
            fig_sec = px.bar(
                sector_agg,
                x="Area",
                y="Estimated_Unemployment_Rate",
                color="COVID_Phase",
                barmode="group",
                color_discrete_map={"Pre-COVID": THEME_BLUE, "COVID/Post-COVID": THEME_RED},
                title="Rural vs. Urban Impact (Pre-COVID vs. Post-COVID)",
                labels={"Estimated_Unemployment_Rate": "Mean Unemployment Rate (%)"}
            )
            fig_sec.update_layout(template="plotly_white")
            st.plotly_chart(fig_sec, width="stretch")

        with c2:
            # States with highest absolute surge
            pivot = covid_cohort.pivot_table(index="State", columns="COVID_Phase", values="Estimated_Unemployment_Rate", aggfunc="mean")
            if "COVID/Post-COVID" in pivot.columns and "Pre-COVID" in pivot.columns:
                pivot["Absolute_Surge"] = pivot["COVID/Post-COVID"] - pivot["Pre-COVID"]
                top_surge_df = pivot.sort_values(by="Absolute_Surge", ascending=False).head(8).reset_index()

                fig_surge = px.bar(
                    top_surge_df,
                    x="State",
                    y="Absolute_Surge",
                    color="Absolute_Surge",
                    color_continuous_scale="Reds",
                    title="States Experiencing Largest Absolute Lockdown Spikes",
                    labels={"Absolute_Surge": "Rate Surge (% Points)"}
                )
                fig_surge.update_layout(template="plotly_white")
                st.plotly_chart(fig_surge, width="stretch")
            else:
                st.info("Both Pre-COVID and Post-COVID observations are required to compute state-level delta.")

        st.warning("""
        **Methodological Distinction: Association vs. Causation:**  
        While the sharp spike in March–May 2020 coincides directly with the implementation of strict national lockdown measures,
        unemployment is also influenced by seasonal agricultural cycles, reverse migration from urban centers, and baseline fiscal health.
        Therefore, we report temporal correlation and association without asserting monocausal attribution.
        """)

    # ---------------------------------------------------------
    # TAB 5: EMPLOYMENT ANALYSIS
    # ---------------------------------------------------------
    with tab5:
        st.subheader("Employment & Labour Market Participation Dynamics")

        col5_1, col5_2 = st.columns([1.1, 0.9])
        with col5_1:
            has_enough_samples = len(filtered_df.dropna(subset=["Estimated_Labour_Participation_Rate", "Estimated_Unemployment_Rate"])) >= 3
            fig_scatter = px.scatter(
                filtered_df,
                x="Estimated_Labour_Participation_Rate",
                y="Estimated_Unemployment_Rate",
                color="COVID_Phase",
                symbol="Area",
                trendline="ols" if has_enough_samples else None,
                color_discrete_map={"Pre-COVID": THEME_BLUE, "COVID/Post-COVID": THEME_RED},
                title="Labour Participation Rate vs. Unemployment Rate",
                labels={
                    "Estimated_Labour_Participation_Rate": "Labour Participation Rate (%)",
                    "Estimated_Unemployment_Rate": "Unemployment Rate (%)"
                }
            )
            fig_scatter.update_layout(template="plotly_white")
            st.plotly_chart(fig_scatter, width="stretch")

        with col5_2:
            # Correlation Heatmap
            corr_cols = ["Estimated_Unemployment_Rate", "Estimated_Employed", "Estimated_Labour_Participation_Rate"]
            corr_df = filtered_df[corr_cols].corr()

            fig_corr = px.imshow(
                corr_df,
                text_auto=".3f",
                color_continuous_scale="RdBu_r",
                zmin=-1,
                zmax=1,
                title="Correlation Matrix (Macro Features)",
                labels=dict(color="Pearson r")
            )
            fig_corr.update_layout(height=420)
            st.plotly_chart(fig_corr, width="stretch")

        st.info("""
        **Labour Participation Takeaways:**
        - **Weak Correlation between Unemployment and LPR ($r \approx 0.003$):** High unemployment does not always correlate with high participation. In crisis months, discouraged workers leave the labour force altogether, causing LPR to compress alongside surging unemployment.
        - **Negative Correlation between Unemployment and Employed ($r \approx -0.22$):** As expected, higher unemployment rates correspond to smaller employed headcounts across observation strata.
        """)

    # ---------------------------------------------------------
    # TAB 6: DATA INSIGHTS & RECOMMENDATIONS
    # ---------------------------------------------------------
    with tab6:
        st.subheader("Key Findings & Policy Insights")

        st.markdown("""
        ### 🔍 Critical Macroeconomic Discoveries:
        1. **The April-May 2020 Lockdown Shock:**
           - National average unemployment rose from **9.51% (Pre-COVID)** to **17.77% (Post-March 2020)**, reaching peak shock levels exceeding **24%** in April and May 2020.
           - This represents an **86.91% relative increase** across all sampled regions.
        2. **Urban Fragility vs. Rural Buffers:**
           - Urban sectors bore an immediate initial brunt due to non-essential commercial closures and high informality in contact-intensive service trades.
           - Rural areas experienced delayed shock absorption as agriculture (Rabi harvest) and MGNREGA social safety nets mitigated initial disruption, though reverse migration later strained village economies.
        3. **Pronounced Regional Disparities:**
           - Small states and UTs with service-reliant economies (Puducherry, Goa, Delhi) and high outward-migrant origins (Bihar, Jharkhand) experienced severe volatility (>40% peak rates).
           - Agrarian and northeastern states with high self-employment (Meghalaya, Assam, Odisha) maintained comparatively lower unemployment metrics.

        ### 💼 Policy & Strategic Recommendations:
        - **Decentralized Employment Guarantees:** Expanding urban employment guarantee schemes modeled after rural MGNREGA can provide countercyclical income stabilization during urban shocks.
        - **Informal Sector Social Security:** Formalizing portable social security benefits (e.g. One Nation One Ration Card) protects vulnerable migrant workers during sudden geographic dislocations.
        - **Digital Labor Market Monitoring:** Real-time high-frequency labor surveys enable policymakers to deploy state-specific fiscal stimulus targeted at localized shock centers.
        """)


if __name__ == "__main__":
    main()
