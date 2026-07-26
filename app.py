import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Nestlé India Investor Readiness", page_icon="📈", layout="wide")

EXCEL_FILE = "data/Nestle_India_Investor_Readiness.xlsx"

@st.cache_data
def load_sheet(name):
    return pd.read_excel(EXCEL_FILE, sheet_name=name)

st.title("📈 Nestlé India Investor Readiness Dashboard")
page = st.sidebar.selectbox(
    "Select Section",
    [
        "Executive Summary",
        "Assumptions",
        "Financial Projections",
        "Product Revenue",
        "Pricing Scenarios",
        "Unit Economics",
        "Market Sizing",
        "Growth Metrics",
        "Quarterly Summary",
    ],
)

sheet_map = {
    "Executive Summary":"Executive Summary",
    "Assumptions":"Assumptions",
    "Financial Projections":"Financial Projections",
    "Product Revenue":"Product Revenue",
    "Pricing Scenarios":"Pricing Scenarios",
    "Unit Economics":"Unit Economics",
    "Market Sizing":"Market Sizing",
    "Growth Metrics":"Growth Metrics",
    "Quarterly Summary":"Quarterly Summary",
}

try:
    df = load_sheet(sheet_map[page])
    st.header(page)
    st.dataframe(df, use_container_width=True)

    cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    if len(cols) >= 1:
        x = df.columns[0]
        y = cols[-1]
        try:
            st.subheader("Chart")
            fig = px.bar(df, x=x, y=y, title=f"{page} - {y}")
            st.plotly_chart(fig, use_container_width=True)
        except Exception:
            pass

    st.download_button(
        "Download Current Sheet (CSV)",
        df.to_csv(index=False),
        file_name=f"{page.replace(' ','_')}.csv",
        mime="text/csv"
    )
except FileNotFoundError:
    st.error("Excel file not found. Place Nestle_India_Investor_Readiness.xlsx inside the data folder.")
except Exception as e:
    st.error(f"Error: {e}")

st.sidebar.markdown("---")
st.sidebar.info("MBA Finance | Investor Readiness Project | Nestlé India")
