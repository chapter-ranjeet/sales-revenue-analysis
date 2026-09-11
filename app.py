"""
Sales & Revenue Analysis Dashboard
====================================
A production-ready, interactive analytics dashboard built with
Streamlit, Pandas, and Plotly.

Launch:
    pip install -r requirements.txt
    streamlit run app.py
"""

import io
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from data_generator import generate_synthetic_data

# ──────────────────────────────────────────────────────────────────────
# Page configuration & global style
# ──────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Sales & Revenue Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------- custom CSS for premium dark-mode feel ----------------
st.markdown(
    """
<style>
/* ── Import expressive dashboard typography ───────────────────── */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

/* ── Root variables ───────────────────────────────────────────── */
:root {
    --bg-primary:    #ffffff;
    --bg-card:       #f4f8f8;
    --bg-card-hover: #e8f1f1;
    --border-subtle: #d6e2e2;
    --accent-blue:   #56c5d0;
    --accent-green:  #8bd450;
    --accent-purple: #f1a66a;
    --accent-orange: #ff8066;
    --accent-red:    #ff6b6b;
    --text-primary:  #111827;
    --text-secondary:#52636a;
    --radius:        10px;
}

/* ── Global resets ────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
    color: var(--text-primary);
}
body {
    background: var(--bg-primary);
    background-image: radial-gradient(circle at 85% 0%, rgba(86,197,208,0.10), transparent 30rem),
                      linear-gradient(rgba(16,35,43,0.025) 1px, transparent 1px),
                      linear-gradient(90deg, rgba(16,35,43,0.025) 1px, transparent 1px);
    background-size: auto, 34px 34px, 34px 34px;
}
.stApp, [data-testid="stAppViewContainer"], [data-testid="stAppViewContainer"] > .main {
    background: var(--bg-primary) !important;
    color: var(--text-primary) !important;
}
[data-testid="stSidebar"] * {
    color: var(--text-primary);
}
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
    color: var(--text-secondary) !important;
}
[data-testid="stFileUploaderDropzone"] {
    background: var(--bg-card) !important;
    border: 1px dashed #3c6870 !important;
}
[data-testid="stFileUploaderDropzone"] * {
    color: var(--text-primary) !important;
}
[data-testid="stFileUploaderDropzone"] button {
    background: #111827 !important;
    color: #ffffff !important;
}
[data-testid="stFileUploaderDropzone"] button * {
    color: #ffffff !important;
}
[data-testid="stSidebar"] input {
    background: var(--bg-card) !important;
    color: var(--text-primary) !important;
    -webkit-text-fill-color: var(--text-primary) !important;
}
[data-baseweb="input"] {
    background: var(--bg-card) !important;
    border-color: var(--border-subtle) !important;
}
[data-baseweb="input"] input {
    color: var(--text-primary) !important;
    -webkit-text-fill-color: var(--text-primary) !important;
}
[data-testid="stSidebar"] [data-baseweb="input"] * {
    color: var(--text-primary) !important;
    -webkit-text-fill-color: var(--text-primary) !important;
}
[data-baseweb="input"] svg {
    fill: var(--accent-blue) !important;
}
header[data-testid="stHeader"] { background: transparent; }
div.block-container { padding-top: 2.25rem; padding-bottom: 3rem; }
h1, h2, h3, h4, h5, h6, .section-header h2, .sidebar-brand .title {
    font-family: 'Space Grotesk', sans-serif !important;
    color: #000000 !important;
    font-weight: 700 !important;
    letter-spacing: 0;
}
section[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid var(--border-subtle);
}

/* ── KPI card styling ─────────────────────────────────────────── */
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, #ffffff, #f1f8f7);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius);
    padding: 18px 20px;
    box-shadow: 0 12px 28px rgba(0,0,0,0.14);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
div[data-testid="stMetric"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.35);
    border-color: var(--accent-blue);
}
div[data-testid="stMetric"] label {
    color: var(--text-secondary) !important;
    font-weight: 500 !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}
div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: var(--text-primary) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1.8rem !important;
}

/* ── Section headers ──────────────────────────────────────────── */
.section-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 2.2rem 0 1rem;
    padding: 0 0 0.65rem 0.85rem;
    border-bottom: 1px solid var(--border-subtle);
    border-left: 3px solid var(--accent-blue);
}
.section-header h2 {
    margin: 0;
    font-size: 1.25rem;
    font-weight: 700;
    color: #000000;
}

/* ── Insight cards ────────────────────────────────────────────── */
.insight-card {
    background: linear-gradient(135deg, #ffffff, #f1f8f7);
    border: 1px solid var(--border-subtle);
    border-left: 3px solid var(--accent-blue);
    border-radius: var(--radius);
    padding: 18px 22px;
    margin-bottom: 10px;
    transition: border-color 0.2s ease;
}
.insight-card:hover { border-left-color: var(--accent-purple); }
.insight-card .label {
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: var(--text-secondary);
    margin-bottom: 6px;
}
.insight-card .value {
    font-size: 1.05rem;
    font-weight: 600;
    color: var(--text-primary);
    line-height: 1.45;
}
.insight-card.green  { border-left-color: var(--accent-green);  }
.insight-card.purple { border-left-color: var(--accent-purple); }
.insight-card.orange { border-left-color: var(--accent-orange); }
.insight-card.red    { border-left-color: var(--accent-red);    }

/* ── Hero banner ──────────────────────────────────────────────── */
.hero-banner {
    position: relative;
    overflow: hidden;
    background: linear-gradient(115deg, #e4f6f4 0%, #d9f0ee 52%, #f8eadf 100%);
    border-radius: 14px;
    padding: 34px 40px;
    margin-bottom: 28px;
    border: 1px solid rgba(86,197,208,0.38);
    box-shadow: 0 18px 36px rgba(16,35,43,0.10);
}
.hero-banner::after {
    content: "";
    position: absolute;
    width: 210px;
    height: 210px;
    right: -60px;
    top: -82px;
    border: 1px solid rgba(241,166,106,0.32);
    border-radius: 50%;
    box-shadow: 0 0 0 18px rgba(241,166,106,0.05), 0 0 0 36px rgba(241,166,106,0.04);
}
.hero-banner h1 {
    margin: 0 0 6px;
    font-size: 1.85rem;
    font-weight: 800;
    color: #000000;
}
.hero-banner p {
    margin: 0;
    color: #30474d;
    font-size: 0.95rem;
}

/* ── Empty state ──────────────────────────────────────────────── */
.empty-state {
    text-align: center;
    padding: 60px 20px;
    color: var(--text-secondary);
    font-size: 1.1rem;
}
.empty-state .icon { font-size: 3rem; margin-bottom: 12px; }

/* ── Expander styling ─────────────────────────────────────────── */
[data-testid="stExpander"] {
    border: 1px solid var(--border-subtle) !important;
    border-radius: var(--radius) !important;
    background: #ffffff !important;
}

/* ── Sidebar branding ─────────────────────────────────────────── */
.sidebar-brand {
    text-align: center;
    padding: 8px 0 22px;
    border-bottom: 1px solid var(--border-subtle);
    margin-bottom: 20px;
}
.sidebar-brand .logo { font-size: 2.2rem; }
.sidebar-brand .title {
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-top: 4px;
}
.sidebar-brand .subtitle {
    font-size: 0.72rem;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 1.2px;
}

/* ── Download button styling ──────────────────────────────────── */
.stDownloadButton > button {
    background: linear-gradient(135deg, #2d8d83 0%, #3ba66f 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    transition: transform 0.15s ease, box-shadow 0.15s ease !important;
}
.stDownloadButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 15px rgba(59,166,111,0.35) !important;
}
</style>
""",
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────────────────────────────
# Plotly colour palette & layout defaults
# ──────────────────────────────────────────────────────────────────────
PLOTLY_COLORS = [
    "#56c5d0", "#f1a66a", "#8bd450", "#ff8066",
    "#ff6b6b", "#83d9d7", "#f5c08f", "#b4e477",
    "#ffad9c", "#f48b9a",
]
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans, sans-serif", color="#111827", size=13),
    margin=dict(l=40, r=30, t=50, b=40),
    xaxis=dict(gridcolor="#d6e2e2", zerolinecolor="#d6e2e2"),
    yaxis=dict(gridcolor="#d6e2e2", zerolinecolor="#d6e2e2"),
    hoverlabel=dict(
        bgcolor="#ffffff",
        font_size=13,
        font_family="DM Sans, sans-serif",
        bordercolor="#b9cccc",
    ),
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        font=dict(size=12),
    ),
)


def apply_layout(fig: go.Figure, **overrides) -> go.Figure:
    """Apply consistent layout to every Plotly figure."""
    merged = {**PLOTLY_LAYOUT, **overrides}
    fig.update_layout(**merged)
    return fig


# ──────────────────────────────────────────────────────────────────────
# Helper: currency / number formatting
# ──────────────────────────────────────────────────────────────────────
def fmt_currency(val: float) -> str:
    if abs(val) >= 1_000_000:
        return f"${val / 1_000_000:,.2f}M"
    if abs(val) >= 1_000:
        return f"${val / 1_000:,.1f}K"
    return f"${val:,.2f}"


def fmt_number(val: float) -> str:
    if abs(val) >= 1_000_000:
        return f"{val / 1_000_000:,.2f}M"
    if abs(val) >= 1_000:
        return f"{val / 1_000:,.1f}K"
    return f"{val:,.0f}"


# ──────────────────────────────────────────────────────────────────────
# Data loading & validation
# ──────────────────────────────────────────────────────────────────────
REQUIRED_COLS = [
    "Order_Date", "Category", "Product",
    "Region", "Units_Sold", "Revenue", "Profit",
]


@st.cache_data(show_spinner=False)
def load_uploaded_file(file_bytes: bytes, file_name: str) -> pd.DataFrame:
    """Parse an uploaded CSV or XLSX file."""
    if file_name.lower().endswith(".csv"):
        df = pd.read_csv(io.BytesIO(file_bytes))
    else:
        df = pd.read_excel(io.BytesIO(file_bytes), engine="openpyxl")

    # Validate required columns
    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        st.error(
            f"**Missing required columns:** {', '.join(missing)}. "
            "Please ensure your file contains: "
            + ", ".join(f"`{c}`" for c in REQUIRED_COLS)
        )
        st.stop()

    df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
    df.dropna(subset=["Order_Date"], inplace=True)
    for col in ["Units_Sold", "Revenue", "Profit"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    return df


@st.cache_data(show_spinner=False)
def load_synthetic() -> pd.DataFrame:
    """Generate & cache the fallback synthetic dataset."""
    return generate_synthetic_data()


# ──────────────────────────────────────────────────────────────────────
# SIDEBAR — data source + global filters
# ──────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="logo">📊</div>
            <div class="title">Revenue Analytics</div>
            <div class="subtitle">Dashboard v2.0</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── File uploader ────────────────────────────────────────────
    st.markdown("#### 📁 Data Source")
    uploaded = st.file_uploader(
        "Upload CSV or XLSX",
        type=["csv", "xlsx"],
        help="Required columns: " + ", ".join(REQUIRED_COLS),
    )

    if uploaded is not None:
        raw_df = load_uploaded_file(uploaded.getvalue(), uploaded.name)
        data_source_label = f"📄 {uploaded.name}"
    else:
        raw_df = load_synthetic()
        data_source_label = "🧪 Synthetic Demo Data (1,500+ rows)"

    st.caption(data_source_label)
    st.divider()

    # ── Date range ───────────────────────────────────────────────
    st.markdown("#### 📅 Date Range")
    min_date = raw_df["Order_Date"].min().date()
    max_date = raw_df["Order_Date"].max().date()
    date_range = st.date_input(
        "Select range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        label_visibility="collapsed",
    )
    # Handle single-date selection gracefully
    if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
        start_dt, end_dt = date_range
    else:
        start_dt = end_dt = date_range if not isinstance(date_range, (list, tuple)) else date_range[0]

    st.divider()

    # ── Region filter ────────────────────────────────────────────
    st.markdown("#### 🌎 Region")
    all_regions = sorted(raw_df["Region"].unique())
    select_all_regions = st.checkbox("Select All Regions", value=True, key="rgn_all")
    if select_all_regions:
        selected_regions = all_regions
    else:
        selected_regions = st.multiselect(
            "Regions", all_regions, default=all_regions, label_visibility="collapsed",
        )

    st.divider()

    # ── Category filter ──────────────────────────────────────────
    st.markdown("#### 🏷️ Category")
    all_categories = sorted(raw_df["Category"].unique())
    select_all_cats = st.checkbox("Select All Categories", value=True, key="cat_all")
    if select_all_cats:
        selected_categories = all_categories
    else:
        selected_categories = st.multiselect(
            "Categories", all_categories, default=all_categories,
            label_visibility="collapsed",
        )

# ──────────────────────────────────────────────────────────────────────
# Apply filters
# ──────────────────────────────────────────────────────────────────────
df = raw_df[
    (raw_df["Order_Date"].dt.date >= start_dt)
    & (raw_df["Order_Date"].dt.date <= end_dt)
    & (raw_df["Region"].isin(selected_regions))
    & (raw_df["Category"].isin(selected_categories))
].copy()

# ──────────────────────────────────────────────────────────────────────
# Hero banner
# ──────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="hero-banner">
        <h1>Sales &amp; Revenue Dashboard</h1>
        <p>Real-time analytics · Dynamic filtering · Automated insights</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────────────────────────────
# Empty-state guard
# ──────────────────────────────────────────────────────────────────────
if df.empty:
    st.markdown(
        """
        <div class="empty-state">
            <div class="icon">🔍</div>
            <p>No data matches the current filters.<br>
            Adjust the <strong>date range</strong>, <strong>regions</strong>,
            or <strong>categories</strong> in the sidebar.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()

# ──────────────────────────────────────────────────────────────────────
# Compute KPIs
# ──────────────────────────────────────────────────────────────────────
total_revenue = df["Revenue"].sum()
total_profit = df["Profit"].sum()
total_units = df["Units_Sold"].sum()
profit_margin = (total_profit / total_revenue * 100) if total_revenue else 0
aov = total_revenue / len(df) if len(df) else 0

# ──────────────────────────────────────────────────────────────────────
# KPI Cards Row
# ──────────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="section-header"><h2>📈 Executive KPIs</h2></div>',
    unsafe_allow_html=True,
)

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Revenue", fmt_currency(total_revenue))
k2.metric("Net Profit", fmt_currency(total_profit), delta=f"{profit_margin:.1f}% margin")
k3.metric("Units Sold", fmt_number(total_units))
k4.metric("Avg Order Value", fmt_currency(aov))

st.markdown("<br>", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────
# ROW 1 — Revenue trend + Regional donut
# ──────────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="section-header"><h2>📊 Core Analytics</h2></div>',
    unsafe_allow_html=True,
)

col_trend, col_donut = st.columns([3, 2])

# ── Revenue Time-Series ─────────────────────────────────────────
with col_trend:
    st.markdown("##### 📈 Revenue Trend (Monthly)")
    monthly = (
        df.set_index("Order_Date")
        .resample("MS")["Revenue"]
        .sum()
        .reset_index()
    )
    monthly.columns = ["Month", "Revenue"]

    fig_trend = go.Figure()
    fig_trend.add_trace(
        go.Scatter(
            x=monthly["Month"],
            y=monthly["Revenue"],
            mode="lines+markers",
            name="Revenue",
            line=dict(color="#56c5d0", width=3, shape="spline"),
            marker=dict(size=7, color="#56c5d0", line=dict(width=2, color="#08141c")),
            fill="tozeroy",
            fillcolor="rgba(88,166,255,0.08)",
            hovertemplate="<b>%{x|%b %Y}</b><br>Revenue: $%{y:,.0f}<extra></extra>",
        )
    )
    apply_layout(
        fig_trend,
        height=400,
        yaxis_title="Revenue ($)",
        xaxis_title="",
        showlegend=False,
    )
    st.plotly_chart(fig_trend, width="stretch", key="trend")

# ── Regional Donut ───────────────────────────────────────────────
with col_donut:
    st.markdown("##### 🌍 Revenue by Region")
    region_rev = df.groupby("Region")["Revenue"].sum().reset_index()
    region_rev = region_rev.sort_values("Revenue", ascending=False)

    fig_donut = go.Figure(
        go.Pie(
            labels=region_rev["Region"],
            values=region_rev["Revenue"],
            hole=0.55,
            marker=dict(
                colors=PLOTLY_COLORS[: len(region_rev)],
                line=dict(color="#08141c", width=2),
            ),
            textinfo="label+percent",
            textfont=dict(size=12),
            hovertemplate="<b>%{label}</b><br>Revenue: $%{value:,.0f}<br>Share: %{percent}<extra></extra>",
        )
    )
    apply_layout(fig_donut, height=400, showlegend=False)
    # Add centre annotation
    fig_donut.add_annotation(
        text=f"<b>{fmt_currency(total_revenue)}</b><br><span style='font-size:11px;color:#52636a'>Total</span>",
        x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="#111827"),
    )
    st.plotly_chart(fig_donut, width="stretch", key="donut")

# ──────────────────────────────────────────────────────────────────────
# ROW 2 — Category breakdown + Top 5 SKUs
# ──────────────────────────────────────────────────────────────────────
col_cat, col_sku = st.columns(2)

# ── Category Revenue vs Profit ───────────────────────────────────
with col_cat:
    st.markdown("##### 🏷️ Revenue vs Profit by Category")
    cat_agg = (
        df.groupby("Category")[["Revenue", "Profit"]]
        .sum()
        .reset_index()
        .sort_values("Revenue", ascending=False)
    )

    fig_cat = go.Figure()
    fig_cat.add_trace(
        go.Bar(
            x=cat_agg["Category"],
            y=cat_agg["Revenue"],
            name="Revenue",
            marker_color="#56c5d0",
            marker_line=dict(width=0),
            hovertemplate="<b>%{x}</b><br>Revenue: $%{y:,.0f}<extra></extra>",
        )
    )
    fig_cat.add_trace(
        go.Bar(
            x=cat_agg["Category"],
            y=cat_agg["Profit"],
            name="Profit",
            marker_color="#8bd450",
            marker_line=dict(width=0),
            hovertemplate="<b>%{x}</b><br>Profit: $%{y:,.0f}<extra></extra>",
        )
    )
    apply_layout(
        fig_cat,
        height=420,
        barmode="group",
        yaxis_title="Amount ($)",
        xaxis_title="",
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
            bgcolor="rgba(0,0,0,0)", font=dict(size=12),
        ),
    )
    st.plotly_chart(fig_cat, width="stretch", key="cat")

# ── Top 5 Products ──────────────────────────────────────────────
with col_sku:
    st.markdown("##### 🏆 Top 5 Products by Revenue")
    top5 = (
        df.groupby("Product")["Revenue"]
        .sum()
        .nlargest(5)
        .reset_index()
        .sort_values("Revenue", ascending=True)
    )

    fig_sku = go.Figure(
        go.Bar(
            x=top5["Revenue"],
            y=top5["Product"],
            orientation="h",
            marker=dict(
                color=top5["Revenue"],
                colorscale=[
                    [0, "#1f3d5c"],
                    [0.5, "#2d6a9f"],
                    [1, "#56c5d0"],
                ],
                line=dict(width=0),
            ),
            text=top5["Revenue"].apply(lambda v: fmt_currency(v)),
            textposition="auto",
            textfont=dict(color="#f1f5f2", size=12, family="DM Sans"),
            hovertemplate="<b>%{y}</b><br>Revenue: $%{x:,.0f}<extra></extra>",
        )
    )
    apply_layout(
        fig_sku,
        height=420,
        xaxis_title="Revenue ($)",
        yaxis_title="",
        showlegend=False,
    )
    st.plotly_chart(fig_sku, width="stretch", key="sku")

# ──────────────────────────────────────────────────────────────────────
# Automated Business Insights Engine
# ──────────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="section-header"><h2>💡 Automated Insights</h2></div>',
    unsafe_allow_html=True,
)


def insight_card(label: str, body: str, color: str = "") -> str:
    """Return HTML for a single insight card."""
    cls = f"insight-card {color}".strip()
    return f"""
    <div class="{cls}">
        <div class="label">{label}</div>
        <div class="value">{body}</div>
    </div>
    """


# Compute insight data
top_cat = df.groupby("Category")["Revenue"].sum().idxmax()
top_cat_rev = df.groupby("Category")["Revenue"].sum().max()
top_region = df.groupby("Region")["Revenue"].sum().idxmax()
top_region_rev = df.groupby("Region")["Revenue"].sum().max()
top_product = df.groupby("Product")["Revenue"].sum().idxmax()
top_product_rev = df.groupby("Product")["Revenue"].sum().max()

margin_health = "Healthy ✅" if profit_margin >= 25 else (
    "Moderate ⚠️" if profit_margin >= 15 else "Critical 🔴"
)
margin_color = "green" if profit_margin >= 25 else (
    "orange" if profit_margin >= 15 else "red"
)

i1, i2 = st.columns(2)
i3, i4 = st.columns(2)

with i1:
    st.markdown(
        insight_card(
            "🏷️ Top Category",
            f"<strong>{top_cat}</strong> leads with "
            f"<strong>{fmt_currency(top_cat_rev)}</strong> in revenue, "
            f"capturing <strong>{top_cat_rev / total_revenue * 100:.1f}%</strong> of total sales.",
        ),
        unsafe_allow_html=True,
    )
with i2:
    st.markdown(
        insight_card(
            "🌍 Top Region",
            f"<strong>{top_region}</strong> is the highest-grossing territory at "
            f"<strong>{fmt_currency(top_region_rev)}</strong>, representing "
            f"<strong>{top_region_rev / total_revenue * 100:.1f}%</strong> market share.",
            "purple",
        ),
        unsafe_allow_html=True,
    )
with i3:
    st.markdown(
        insight_card(
            "🏆 Best-Selling Product",
            f"<strong>{top_product}</strong> is the revenue champion with "
            f"<strong>{fmt_currency(top_product_rev)}</strong> in total sales.",
            "orange",
        ),
        unsafe_allow_html=True,
    )
with i4:
    st.markdown(
        insight_card(
            "💰 Margin Health",
            f"Overall profit margin is <strong>{profit_margin:.1f}%</strong> — "
            f"<strong>{margin_health}</strong>. "
            f"Net profit stands at <strong>{fmt_currency(total_profit)}</strong>.",
            margin_color,
        ),
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────
# Data Export & Inspection
# ──────────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="section-header"><h2>📋 Data Explorer</h2></div>',
    unsafe_allow_html=True,
)

with st.expander(f"View Filtered Data  ({len(df):,} rows)", expanded=False):
    # Format display copy
    display_df = df.copy()
    display_df["Order_Date"] = display_df["Order_Date"].dt.strftime("%Y-%m-%d")
    display_df = display_df.sort_values("Order_Date", ascending=False).reset_index(drop=True)

    st.dataframe(
        display_df,
        width="stretch",
        height=420,
        column_config={
            "Revenue": st.column_config.NumberColumn("Revenue", format="$%.2f"),
            "Profit": st.column_config.NumberColumn("Profit", format="$%.2f"),
            "Units_Sold": st.column_config.NumberColumn("Units Sold", format="%d"),
        },
    )

    # Download button
    csv_data = display_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️  Download Filtered Data as CSV",
        data=csv_data,
        file_name="filtered_sales_data.csv",
        mime="text/csv",
    )

# ──────────────────────────────────────────────────────────────────────
# Footer
# ──────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    """
    <div style="text-align:center; padding: 10px 0 20px; color:#9db2b4; font-size:0.78rem;">
        Sales & Revenue Dashboard · Built with Streamlit & Plotly ·
        Showing <strong>{rows:,}</strong> records across
        <strong>{cats}</strong> categories and
        <strong>{regs}</strong> regions
    </div>
    """.format(rows=len(df), cats=df["Category"].nunique(), regs=df["Region"].nunique()),
    unsafe_allow_html=True,
)
