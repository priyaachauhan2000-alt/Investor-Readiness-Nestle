import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="Nestlé India Investor Readiness Dashboard",
    page_icon="📈",
    layout="wide"
)

# ----------------------------
# TITLE
# ----------------------------
st.title("📈 Nestlé India Investor Readiness Dashboard")
st.markdown("### MBA Finance Project")
st.markdown("---")

# ----------------------------
# EXCEL FILE
# ----------------------------
EXCEL_FILE = "data/Nestle_India_Investor_Readiness.xlsx"

# ----------------------------
# LOAD SHEET FUNCTION
# ----------------------------
@st.cache_data
def load_sheet(sheet_name):
    try:
        df = pd.read_excel(
            EXCEL_FILE,
            sheet_name=sheet_name,
            header=1
        )

        df = df.dropna(how="all")
        df.columns = [str(c).strip() for c in df.columns]
        df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

        return df

    except Exception as e:
        st.error(f"Unable to load sheet: {sheet_name}")
        st.error(e)
        return pd.DataFrame()

# ----------------------------
# SIDEBAR
# ----------------------------
st.sidebar.title("📂 Navigation")

page = st.sidebar.selectbox(
    "Select Dashboard",
    [
        "Home",
        "Executive Summary",
        "Financial Projections",
        "Product Revenue",
        "Market Sizing",
        "Quarterly Summary"
    ]
)

st.sidebar.markdown("---")
st.sidebar.write("**Company:** Nestlé India")
st.sidebar.write("**Project:** Investor Readiness")

# ======================================================
# HOME PAGE
# ======================================================

if page == "Home":

    st.header("Welcome")

    st.write("""
This dashboard provides a simple overview of Nestlé India's
financial performance and investor readiness.

The dashboard is built using:

- Streamlit
- Python
- Pandas
- Plotly
- Excel
""")

    col1, col2, col3 = st.columns(3)

    col1.metric("Company", "Nestlé India")
    col2.metric("Industry", "FMCG")
    col3.metric("Dashboard", "Investor Readiness")

    st.markdown("---")

    st.subheader("Available Reports")

    st.write("""
- Executive Summary
- Financial Projections
- Product Revenue
- Market Sizing
- Quarterly Summary
""")
# ======================================================
# EXECUTIVE SUMMARY
# ======================================================

elif page == "Executive Summary":

    st.header("📊 Executive Summary")

    df = load_sheet("Executive Summary")

    if df.empty:
        st.warning("No data found.")
    else:

        st.dataframe(df, use_container_width=True, hide_index=True)

        st.markdown("### Key Highlights")

        col1, col2, col3 = st.columns(3)

        try:
            latest = df.columns[-1]

            revenue = df.iloc[0][latest]
            ebitda = df.iloc[1][latest]
            profit = df.iloc[2][latest]

            col1.metric("Revenue", revenue)
            col2.metric("EBITDA", ebitda)
            col3.metric("Net Profit", profit)

        except:
            st.info("KPI cards could not be generated.")

        st.markdown("---")

        try:

            chart_df = df.iloc[:3]

            fig = px.bar(
                chart_df,
                x=df.columns[0],
                y=latest,
                color=df.columns[0],
                text=latest,
                title="Financial Performance"
            )

            fig.update_layout(showlegend=False)

            st.plotly_chart(fig, use_container_width=True)

        except:
            st.info("Chart unavailable.")

# ======================================================
# FINANCIAL PROJECTIONS
# ======================================================

elif page == "Financial Projections":

    st.header("📈 Financial Projections")

    df = load_sheet("Financial Projections")

    if df.empty:
        st.warning("No data found.")
    else:

        st.dataframe(df, use_container_width=True, hide_index=True)

        numeric_cols = df.select_dtypes(include="number").columns.tolist()

        if len(numeric_cols) > 0:

            fig = px.line(
                df,
                x=df.columns[0],
                y=numeric_cols,
                markers=True,
                title="Financial Projection Trend"
            )

            st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        st.subheader("Projection Overview")

        try:

            fig2 = px.bar(
                df,
                x=df.columns[0],
                y=numeric_cols,
                barmode="group",
                title="Year-wise Comparison"
            )

            st.plotly_chart(fig2, use_container_width=True)

        except:
            st.info("Comparison chart unavailable.")
          # ======================================================
# PRODUCT REVENUE
# ======================================================

elif page == "Product Revenue":

    st.header("🍫 Product Revenue")

    df = load_sheet("Product Revenue")

    if df.empty:
        st.warning("No data found.")
    else:

        st.dataframe(df, use_container_width=True, hide_index=True)

        numeric_cols = df.select_dtypes(include="number").columns.tolist()

        if len(numeric_cols) > 0:

            latest = numeric_cols[-1]

            fig = px.pie(
                df,
                names=df.columns[0],
                values=latest,
                hole=0.45,
                title="Product Revenue Distribution"
            )

            st.plotly_chart(fig, use_container_width=True)

            fig2 = px.bar(
                df,
                x=df.columns[0],
                y=latest,
                color=df.columns[0],
                title="Revenue by Product"
            )

            fig2.update_layout(showlegend=False)

            st.plotly_chart(fig2, use_container_width=True)


# ======================================================
# MARKET SIZING
# ======================================================

elif page == "Market Sizing":

    st.header("🌍 Market Sizing")

    df = load_sheet("Market Sizing")

    if df.empty:
        st.warning("No data found.")
    else:

        st.dataframe(df, use_container_width=True, hide_index=True)

        numeric_cols = df.select_dtypes(include="number").columns.tolist()

        if len(numeric_cols) > 0:

            fig = px.bar(
                df,
                x=df.columns[0],
                y=numeric_cols[0],
                color=df.columns[0],
                title="Market Size Analysis"
            )

            fig.update_layout(showlegend=False)

            st.plotly_chart(fig, use_container_width=True)


# ======================================================
# QUARTERLY SUMMARY
# ======================================================

elif page == "Quarterly Summary":

    st.header("📑 Quarterly Summary")

    df = load_sheet("Quarterly Summary")

    if df.empty:
        st.warning("No data found.")
    else:

        st.dataframe(df, use_container_width=True, hide_index=True)

        numeric_cols = df.select_dtypes(include="number").columns.tolist()

        if len(numeric_cols) > 0:

            fig = px.line(
                df,
                x=df.columns[0],
                y=numeric_cols,
                markers=True,
                title="Quarterly Performance"
            )

            st.plotly_chart(fig, use_container_width=True)


# ======================================================
# FOOTER
# ======================================================

st.markdown("---")

st.markdown(
"""
<center>

### Nestlé India Investor Readiness Dashboard

Developed using **Python • Streamlit • Pandas • Plotly**

MBA Finance Project

</center>
""",
unsafe_allow_html=True
)
