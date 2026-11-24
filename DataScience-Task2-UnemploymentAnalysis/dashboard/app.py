"""
app.py
======
EmployIQ — Labour Market Intelligence Platform
OASIS INFOBYTE Data Science Internship | Task 2: Unemployment Analysis in India.

Features:
- Dark Executive Economic Intelligence UI/UX with Deep Navy (#070C18), Deep Teal (#00A896), and Cyan (#02C39A) accents.
- Preserves all authentic CMIE data structures, PyArrow safety, and non-causal economic rigor.
- STRICT PRESERVATION OF INDEPENDENT STATE SELECTION:
  State multiselect remains completely independent of the Macro-Geographical Zone filter.
- 6 Comprehensive Views:
  1. Executive Overview & Macro KPIs
  2. State-Level Labour Economics
  3. Regional & Zonal Comparative Dynamics
  4. COVID-19 Lockdown Shock Analysis
  5. Labour Participation & Sectoral Divergence
  6. Empirical Policy Recommendations
"""

import os
import sys
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Configure page layout and dark economic branding
st.set_page_config(
    page_title="EmployIQ | Labour Market Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark Economic UI Styling
THEME_BG = "#070C18"
THEME_CARD = "#0D1527"
THEME_BORDER = "#1E293B"
THEME_CYAN = "#00D9F5"
THEME_TEAL = "#00F5A0"
THEME_RED = "#FF3B5C"
THEME_AMBER = "#FFB800"

st.markdown(f"""
<style>
    /* Global Base */
    .stApp {{
        background-color: {THEME_BG};
        color: #E2E8F0;
        font-family: 'Inter', -apple-system, sans-serif;
    }}
    
    /* Executive Headers */
    .brand-title {{
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        background: linear-gradient(135deg, #00F5A0 0%, #00D9F5 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.1rem;
    }}
    .brand-sub {{
        font-size: 0.95rem;
        color: #94A3B8;
        margin-bottom: 1.5rem;
    }}
    
    /* KPI Card */
    .kpi-card {{
        background-color: {THEME_CARD};
        border-radius: 12px;
        padding: 20px;
        border: 1px solid {THEME_BORDER};
        border-top: 3px solid #00F5A0;
        box-shadow: 0 4px 15px -3px rgba(0, 0, 0, 0.5);
    }}
    .kpi-label {{
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #94A3B8;
    }}
    .kpi-value {{
        font-size: 1.9rem;
        font-weight: 800;
        font-family: 'JetBrains Mono', monospace;
        color: #FFFFFF;
        margin-top: 4px;
    }}
    .kpi-subtext {{
        font-size: 0.8rem;
        color: #00D9F5;
        margin-top: 4px;
    }}
    
    /* Content Cards */
    .econ-card {{
        background-color: {THEME_CARD};
        border: 1px solid {THEME_BORDER};
        border-radius: 12px;
        padding: 22px;
        margin-bottom: 16px;
    }}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    """
    Loads, sanitizes, and caches the standardized CMIE dataset.
    Preserves exact Task 2 path resolution and numerical typing.
    """
    dashboard_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(dashboard_dir)
    data_path = os.path.join(project_root, "data", "processed", "unemployment_cleaned.csv")

    if not os.path.exists(data_path):
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

    # Enforce safe datatypes for PyArrow & calculation accuracy
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    numeric_cols = [
        "Estimated_Unemployment_Rate",
        "Estimated_Employed",
        "Estimated_Labour_Participation_Rate"
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df.dropna(subset=["Estimated_Unemployment_Rate", "Date", "State"], inplace=True)
    return df


def main():
    df_full = load_data()

    # Sidebar Navigation & Filter Suite
    with st.sidebar:
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 20px;">
            <div style="font-size: 2rem;">📈</div>
            <div>
                <div style="font-size: 1.25rem; font-weight: 800; color: #FFFFFF; font-family: monospace;">EmployIQ</div>
                <div style="font-size: 0.72rem; color: #00F5A0; font-weight: 700; letter-spacing: 0.05em;">LABOUR MARKET INTELLIGENCE</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        page = st.radio(
            "Navigation Console",
            [
                "Executive Overview",
                "State-Level Analysis",
                "Regional & Zonal Dynamics",
                "COVID-19 Lockdown Shock",
                "Labour & Sectoral Divergence",
                "Policy Insights & Recommendations"
            ],
            index=0
        )

        st.markdown("---")
        st.markdown("### 🔍 Analytical Filters")

        # 1. Sector Classification
        area_options = ["All Sectors"] + sorted(df_full["Area"].unique().tolist())
        selected_area = st.selectbox("Sector Classification:", area_options, index=0)

        # 2. Macro-Geographical Zone
        zone_options = ["All Zones"] + sorted(df_full["Zone"].unique().tolist())
        selected_zone = st.selectbox("Macro-Geographical Zone:", zone_options, index=0)

        # 3. State Multiselect - STRICTLY PRESERVING INDEPENDENT FILTERING
        # Users can select any state across India regardless of the Zone filter
        all_states_sorted = sorted(df_full["State"].unique().tolist())
        selected_states = st.multiselect(
            "Select Specific States (Independent):",
            all_states_sorted,
            default=[]
        )

        # 4. Timeline Boundary
        covid_phase_options = ["All Periods", "Pre-COVID (May 2019 - Feb 2020)", "COVID/Post-COVID (Mar 2020 - Jun 2020)"]
        selected_phase = st.radio("Observation Window:", covid_phase_options, index=0)

        # 5. Date Range Slider
        min_date = df_full["Date"].min().to_pydatetime()
        max_date = df_full["Date"].max().to_pydatetime()
        date_range = st.slider(
            "Temporal Horizon:",
            min_value=min_date,
            max_value=max_date,
            value=(min_date, max_date),
            format="MMM YYYY"
        )

        st.markdown("---")
        st.markdown("""
        <div style="font-size: 0.75rem; color: #64748B; font-family: monospace;">
            <div>DATASET: <b>CMIE India (740 Obs)</b></div>
            <div>FREQUENCY: <b>Monthly (2019-2020)</b></div>
            <div>INDEPENDENT FILTERS: <b>Enforced</b></div>
        </div>
        """, unsafe_allow_html=True)

    # Apply Filtering Logic strictly preserving all criteria
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

    if filtered_df.empty:
        st.warning("⚠️ No records match the active filter criteria. Please broaden your selection.")
        return

    # Dynamic KPI Calculations
    avg_unemp = float(filtered_df["Estimated_Unemployment_Rate"].mean())
    median_unemp = float(filtered_df["Estimated_Unemployment_Rate"].median())
    avg_lpr = float(filtered_df["Estimated_Labour_Participation_Rate"].mean())
    total_obs = len(filtered_df)

    state_group = filtered_df.groupby("State")["Estimated_Unemployment_Rate"].mean()
    highest_state = str(state_group.idxmax()) if not state_group.empty else "N/A"
    highest_rate = float(state_group.max()) if not state_group.empty else 0.0
    lowest_state = str(state_group.idxmin()) if not state_group.empty else "N/A"
    lowest_rate = float(state_group.min()) if not state_group.empty else 0.0

    # PAGE 1: OVERVIEW & MACRO KPIS
    if page == "Executive Overview":
        st.markdown('<div class="brand-title">EmployIQ National Labour Intelligence</div>', unsafe_allow_html=True)
        st.markdown('<div class="brand-sub">Comprehensive macroeconomic surveillance of Indian unemployment, participation rates, and pandemic shocks (2019–2020).</div>', unsafe_allow_html=True)

        # KPI Row
        k1, k2, k3, k4 = st.columns(4)
        with k1:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Mean Unemployment Rate</div>
                <div class="kpi-value">{avg_unemp:.2f}%</div>
                <div class="kpi-subtext">Median: {median_unemp:.2f}% ({total_obs:,d} observations)</div>
            </div>
            """, unsafe_allow_html=True)
        with k2:
            st.markdown(f"""
            <div class="kpi-card" style="border-top-color: #FF3B5C;">
                <div class="kpi-label">Highest Unemployment State</div>
                <div class="kpi-value" style="color: #FF3B5C;">{highest_state}</div>
                <div class="kpi-subtext" style="color: #FF3B5C;">Peak Cohort Avg: {highest_rate:.2f}%</div>
            </div>
            """, unsafe_allow_html=True)
        with k3:
            st.markdown(f"""
            <div class="kpi-card" style="border-top-color: #00F5A0;">
                <div class="kpi-label">Lowest Unemployment State</div>
                <div class="kpi-value" style="color: #00F5A0;">{lowest_state}</div>
                <div class="kpi-subtext" style="color: #00F5A0;">Baseline Cohort Avg: {lowest_rate:.2f}%</div>
            </div>
            """, unsafe_allow_html=True)
        with k4:
            st.markdown(f"""
            <div class="kpi-card" style="border-top-color: #00D9F5;">
                <div class="kpi-label">Mean Labour Participation (LPR)</div>
                <div class="kpi-value">{avg_lpr:.2f}%</div>
                <div class="kpi-subtext">National Active Workforce Ratio</div>
            </div>
            """, unsafe_allow_html=True)

        # Overview Timeline Chart
        st.markdown('<div class="econ-card">', unsafe_allow_html=True)
        st.markdown("### 📈 Monthly Unemployment Trajectory Across Sectors")
        monthly_area = filtered_df.groupby(["Date", "Area"])["Estimated_Unemployment_Rate"].mean().reset_index()
        fig_trend = px.line(
            monthly_area,
            x="Date",
            y="Estimated_Unemployment_Rate",
            color="Area",
            color_discrete_map={"Rural": "#00F5A0", "Urban": "#00D9F5"},
            markers=True,
            template="plotly_dark",
            labels={"Estimated_Unemployment_Rate": "Unemployment Rate (%)", "Date": "Observation Date"}
        )
        fig_trend.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(13,21,39,0.7)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_trend, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # PAGE 2: STATE-LEVEL LABOUR ECONOMICS
    elif page == "State-Level Analysis":
        st.markdown('<div class="brand-title">State-Level Labour Disparities</div>', unsafe_allow_html=True)
        st.markdown('<div class="brand-sub">Granular cross-state comparative benchmarks, variance dispersion, and regional leaderboards.</div>', unsafe_allow_html=True)

        col_sort1, col_sort2 = st.columns([1, 1])
        with col_sort1:
            st.markdown('<div class="econ-card">', unsafe_allow_html=True)
            st.markdown("### 🔴 Highest Unemployment States")
            top_states = state_group.sort_values(ascending=False).head(10).reset_index()
            fig_top = px.bar(
                top_states,
                x="Estimated_Unemployment_Rate",
                y="State",
                orientation="h",
                color="Estimated_Unemployment_Rate",
                color_continuous_scale="Reds",
                template="plotly_dark"
            )
            fig_top.update_layout(yaxis=dict(autorange="reversed"), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_top, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_sort2:
            st.markdown('<div class="econ-card">', unsafe_allow_html=True)
            st.markdown("### 🟢 Lowest Unemployment States")
            bot_states = state_group.sort_values(ascending=True).head(10).reset_index()
            fig_bot = px.bar(
                bot_states,
                x="Estimated_Unemployment_Rate",
                y="State",
                orientation="h",
                color="Estimated_Unemployment_Rate",
                color_continuous_scale="Teal",
                template="plotly_dark"
            )
            fig_bot.update_layout(yaxis=dict(autorange="reversed"), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_bot, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Full Data Table
        st.markdown('<div class="econ-card">', unsafe_allow_html=True)
        st.markdown("### 📋 Filtered Macroeconomic Records")
        st.dataframe(filtered_df[["Date", "State", "Area", "Zone", "Estimated_Unemployment_Rate", "Estimated_Employed", "Estimated_Labour_Participation_Rate", "COVID_Phase"]], use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # PAGE 3: REGIONAL & ZONAL DYNAMICS
    elif page == "Regional & Zonal Dynamics":
        st.markdown('<div class="brand-title">Macro-Geographical Zonal Comparative Dynamics</div>', unsafe_allow_html=True)
        st.markdown('<div class="brand-sub">Cross-zone variance, regional clusters, and economic dispersion across India\'s five macro zones.</div>', unsafe_allow_html=True)

        col_z1, col_z2 = st.columns([1, 1])
        with col_z1:
            st.markdown('<div class="econ-card">', unsafe_allow_html=True)
            st.markdown("### 🌍 Zonal Mean Unemployment Rates")
            zone_mean = filtered_df.groupby("Zone")["Estimated_Unemployment_Rate"].mean().reset_index()
            fig_zone = px.bar(
                zone_mean,
                x="Zone",
                y="Estimated_Unemployment_Rate",
                color="Zone",
                color_discrete_sequence=["#00F5A0", "#00D9F5", "#8B5CF6", "#FFB800", "#FF3B5C"],
                template="plotly_dark"
            )
            fig_zone.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_zone, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_z2:
            st.markdown('<div class="econ-card">', unsafe_allow_html=True)
            st.markdown("### 📊 Zonal Rate Dispersion (Box Plot)")
            fig_zbox = px.box(
                filtered_df,
                x="Zone",
                y="Estimated_Unemployment_Rate",
                color="Zone",
                color_discrete_sequence=["#00F5A0", "#00D9F5", "#8B5CF6", "#FFB800", "#FF3B5C"],
                template="plotly_dark"
            )
            fig_zbox.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_zbox, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # PAGE 4: COVID-19 LOCKDOWN SHOCK
    elif page == "COVID-19 Lockdown Shock":
        st.markdown('<div class="brand-title">COVID-19 Pandemic Lockdown Shock Analysis</div>', unsafe_allow_html=True)
        st.markdown('<div class="brand-sub">Empirical impact of the March–May 2020 national lockdown on employment volatility.</div>', unsafe_allow_html=True)

        covid_cohort = filtered_df[filtered_df["COVID_Phase"].isin(["Pre-COVID", "COVID/Post-COVID"])]
        
        c_cov1, c_cov2 = st.columns(2)
        with c_cov1:
            st.markdown('<div class="econ-card">', unsafe_allow_html=True)
            st.markdown("### ⚖️ Pre vs Post-COVID Sectoral Shift")
            pre_post_sec = covid_cohort.groupby(["Area", "COVID_Phase"])["Estimated_Unemployment_Rate"].mean().reset_index()
            fig_sec = px.bar(
                pre_post_sec,
                x="Area",
                y="Estimated_Unemployment_Rate",
                color="COVID_Phase",
                barmode="group",
                color_discrete_map={"Pre-COVID": "#00D9F5", "COVID/Post-COVID": "#FF3B5C"},
                template="plotly_dark"
            )
            fig_sec.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_sec, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with c_cov2:
            st.markdown('<div class="econ-card">', unsafe_allow_html=True)
            st.markdown("### 💥 States With Largest Absolute Lockdown Surge")
            pivot = covid_cohort.pivot_table(index="State", columns="COVID_Phase", values="Estimated_Unemployment_Rate", aggfunc="mean")
            if "COVID/Post-COVID" in pivot.columns and "Pre-COVID" in pivot.columns:
                pivot["Surge"] = pivot["COVID/Post-COVID"] - pivot["Pre-COVID"]
                top_surge = pivot.sort_values(by="Surge", ascending=False).head(8).reset_index()
                fig_surge = px.bar(
                    top_surge,
                    x="State",
                    y="Surge",
                    color="Surge",
                    color_continuous_scale="Reds",
                    template="plotly_dark",
                    labels={"Surge": "Rate Surge (% Points)"}
                )
                fig_surge.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig_surge, use_container_width=True)
            else:
                st.info("Both Pre-COVID and Post-COVID records required to compute delta.")
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="econ-card" style="border-left: 4px solid #FFB800;">
            <div style="font-weight: 700; color: #FFB800; margin-bottom: 6px;">Methodological Principle: Association vs. Causation</div>
            <div style="font-size: 0.85rem; color: #94A3B8; line-height: 1.6;">
                While the abrupt peak in March–May 2020 directly coincides with national lockdown orders, unemployment dynamics are simultaneously influenced by seasonal Rabi harvesting cycles, reverse migration from metros to home districts, and differing state fiscal buffers. We present correlation and empirical timing without asserting monocausal attribution.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # PAGE 5: LABOUR & SECTORAL DIVERGENCE
    elif page == "Labour & Sectoral Divergence":
        st.markdown('<div class="brand-title">Labour Participation & Sectoral Divergence</div>', unsafe_allow_html=True)
        st.markdown('<div class="brand-sub">Relationship between workforce participation rates (LPR) and reported unemployment.</div>', unsafe_allow_html=True)

        c_l1, c_l2 = st.columns([1.1, 0.9])
        with c_l1:
            st.markdown('<div class="econ-card">', unsafe_allow_html=True)
            st.markdown("### 📉 Labour Participation (LPR) vs. Unemployment")
            has_enough = len(filtered_df.dropna(subset=["Estimated_Labour_Participation_Rate", "Estimated_Unemployment_Rate"])) >= 3
            fig_scatter = px.scatter(
                filtered_df,
                x="Estimated_Labour_Participation_Rate",
                y="Estimated_Unemployment_Rate",
                color="COVID_Phase",
                symbol="Area",
                trendline="ols" if has_enough else None,
                color_discrete_map={"Pre-COVID": "#00D9F5", "COVID/Post-COVID": "#FF3B5C"},
                template="plotly_dark",
                labels={
                    "Estimated_Labour_Participation_Rate": "Labour Participation Rate (%)",
                    "Estimated_Unemployment_Rate": "Unemployment Rate (%)"
                }
            )
            fig_scatter.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_scatter, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with c_l2:
            st.markdown('<div class="econ-card">', unsafe_allow_html=True)
            st.markdown("### 🔬 Feature Correlation Matrix")
            corr_cols = ["Estimated_Unemployment_Rate", "Estimated_Employed", "Estimated_Labour_Participation_Rate"]
            corr_df = filtered_df[corr_cols].corr()
            fig_corr = px.imshow(
                corr_df,
                text_auto=".3f",
                color_continuous_scale="RdBu_r",
                zmin=-1,
                zmax=1,
                template="plotly_dark"
            )
            fig_corr.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=350)
            st.plotly_chart(fig_corr, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # PAGE 6: POLICY INSIGHTS & RECOMMENDATIONS
    elif page == "Policy Insights & Recommendations":
        st.markdown('<div class="brand-title">Strategic Insights & Policy Recommendations</div>', unsafe_allow_html=True)
        st.markdown('<div class="brand-sub">Empirical findings derived from CMIE data and targeted economic policy prescriptions.</div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="econ-card">
            <h3 style="color: #00F5A0; margin-top: 0;">🔍 Directly Observed Empirical Findings (CMIE Dataset):</h3>
            <ol style="line-height: 1.8; color: #E2E8F0; font-size: 0.92rem;">
                <li><b>Lockdown Peak Amplitude:</b> National average unemployment jumped from <b>9.51% (Pre-COVID baseline)</b> to <b>17.77% (Post-March 2020)</b>, reaching peak monthly levels above <b>24%</b> during April and May 2020 (+8.26 percentage points absolute surge; +86.91% relative surge).</li>
                <li><b>Sectoral Divergence:</b> Urban unemployment experienced an immediate, higher-amplitude freeze (peaking above 25%), while rural unemployment followed with secondary delays as agricultural harvesting operations provided partial early-phase absorption.</li>
                <li><b>Persistent Regional Variance:</b> Across the full 14-month dataset, states such as <b>Tripura (28.35%)</b>, <b>Haryana (26.28%)</b>, and <b>Jharkhand (20.58%)</b> exhibited structurally elevated baseline rates compared to lower-volatility states like <b>Meghalaya (4.80%)</b> and <b>Odisha (5.66%)</b>.</li>
            </ol>
            
            <h3 style="color: #00D9F5; margin-top: 25px;">💼 Policy & Labour Market Interventions:</h3>
            <ul style="line-height: 1.8; color: #E2E8F0; font-size: 0.92rem;">
                <li><b>Targeted Urban Work Guarantees:</b> Formulating localized urban public works schemes akin to rural employment safety nets to protect casual and service-sector laborers during economic halts.</li>
                <li><b>Interstate Social Security Portability:</b> Expanding nationwide portability of ration and wage entitlements to buffer circular migrant workers against abrupt metropolitan income shocks.</li>
                <li><b>High-Frequency Regional Early-Warning Dashboards:</b> Institutionalizing localized monthly surveillance to deploy state-level countercyclical credit assistance before distress propagates into chronic joblessness.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
