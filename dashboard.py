
import sqlite3
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# Dashboard configuration
st.set_page_config(
    page_title="Banking Data Engineering Platform",
    page_icon="🏦",
    layout="wide"
)

# Find our existing SQLite database
database_file = Path(__file__).parent / "banking.db"

@st.cache_data(ttl=60)
def load_data():
    with sqlite3.connect(database_file) as connection:
        df = pd.read_sql_query(
            "SELECT * FROM transactions", connection
        )
    df["transaction_date"] = pd.to_datetime(
        df["transaction_date"]
    )
    return df

st.title("🏦 Banking Data Engineering Platform")
st.caption("ETL Pipeline | SQL Analytics | Data Quality Monitoring")
st.info("Portfolio demonstration using synthetic banking data.")


# ETL Pipeline Architecture
with st.expander("🔄 View ETL Pipeline Architecture"):
    st.markdown("### Banking Transaction Data Flow")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("📁 EXTRACT")
        st.write("Source: Banking CSV")
        st.write("10,000 simulated records")

    with col2:
        st.warning("⚙️ TRANSFORM")
        st.write("Validate transaction IDs")
        st.write("Check duplicates and amounts")

    with col3:
        st.success("🗄️ LOAD")
        st.write("Destination: SQLite")
        st.write("Validated transaction records")

    st.markdown(
        "**Pipeline:** CSV → Python Validation → SQLite → Dashboard"
    )


if not database_file.exists():
    st.error("Database missing. Run etl_pipeline.py first.")
    st.stop()

df = load_data()

# Sidebar filters
st.sidebar.header("Transaction Filters")

selected_status = st.sidebar.multiselect(
    "Transaction Status",
    options=sorted(df["status"].unique()),
    default=sorted(df["status"].unique())
)

selected_type = st.sidebar.multiselect(
    "Transaction Type",
    options=sorted(df["transaction_type"].unique()),
    default=sorted(df["transaction_type"].unique())
)

filtered_df = df[
    df["status"].isin(selected_status)
    & df["transaction_type"].isin(selected_type)
]

# KPI cards
total_transactions = len(filtered_df)
total_amount = filtered_df["amount"].sum()
successful = (filtered_df["status"] == "Success").sum()
success_rate = (
    successful / total_transactions * 100
    if total_transactions else 0
)

st.subheader("Transaction Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Transactions", f"{total_transactions:,}")
col2.metric("Transaction Value", f"${total_amount:,.2f}")
col3.metric("Successful", f"{successful:,}")
col4.metric("Success Rate", f"{success_rate:.1f}%")

st.divider()

# Charts
left, right = st.columns(2)

with left:
    st.subheader("Transactions by Status")
    status_counts = (
        filtered_df["status"]
        .value_counts()
        .reset_index()
    )
    status_counts.columns = ["Status", "Count"]

    fig = px.pie(
        status_counts,
        names="Status",
        values="Count",
        hole=0.5
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Transactions by Type")
    type_counts = (
        filtered_df["transaction_type"]
        .value_counts()
        .reset_index()
    )
    type_counts.columns = ["Type", "Count"]

    fig = px.bar(
        type_counts,
        x="Type",
        y="Count",
        color="Type"
    )
    st.plotly_chart(fig, use_container_width=True)

# Daily transaction trend
st.subheader("Daily Transaction Trend")

daily = (
    filtered_df.groupby("transaction_date")
    .size()
    .reset_index(name="Transactions")
)

fig = px.line(
    daily,
    x="transaction_date",
    y="Transactions",
    markers=True
)
st.plotly_chart(fig, use_container_width=True)

# Data quality indicators
st.subheader("Data Quality Monitoring")

q1, q2, q3 = st.columns(3)

q1.metric("Missing Customer IDs", int(df["customer_id"].isna().sum()))
q2.metric("Duplicate Transaction IDs", int(df["transaction_id"].duplicated().sum()))
q3.metric("Invalid Amounts", int((df["amount"] <= 0).sum()))

# Transaction records
st.subheader("Banking Transaction Records")
st.dataframe(filtered_df, use_container_width=True, hide_index=True)

st.download_button(
    "Download Filtered Transactions",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_transactions.csv",
    mime="text/csv"
)

st.caption("Built with Python, SQLite, Pandas, Plotly and Streamlit")


# GOLD LAYER ANALYTICS

st.divider()
st.header("🥇 Gold Layer Analytics")
st.caption("Curated transaction summaries from the Medallion pipeline")

gold_file = Path(__file__).parent / "gold" / "transaction_summary.csv"

if gold_file.exists():
    gold_df = pd.read_csv(gold_file)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Transactions by Status")

        fig_gold = px.bar(
            gold_df,
            x="status",
            y="transaction_count",
            color="status",
            text="transaction_count"
        )

        st.plotly_chart(fig_gold, use_container_width=True)

    with col2:
        st.subheader("Transaction Value by Status")

        fig_amount = px.pie(
            gold_df,
            names="status",
            values="total_amount",
            hole=0.5
        )

        st.plotly_chart(fig_amount, use_container_width=True)

    st.subheader("Gold Layer Dataset")
    st.dataframe(gold_df, hide_index=True, use_container_width=True)

    st.success("Gold Layer data loaded successfully!")

else:
    st.warning(
        "Gold dataset not found. Run gold_layer.py first.")



# PIPELINE MONITORING DASHBOARD

st.divider()
st.header("📊 Pipeline Execution Monitoring")
st.caption("Execution history, processing metrics and pipeline health")

with sqlite3.connect(database_file) as monitor_connection:
    runs_df = pd.read_sql_query(
        """
        SELECT *
        FROM pipeline_runs
        ORDER BY run_id DESC
        """,
        monitor_connection
    )

if runs_df.empty:
    st.warning("No pipeline executions recorded yet.")
else:
    # Pipeline performance metrics
    total_runs = len(runs_df)
    successful_runs = (runs_df["status"] == "Success").sum()
    failed_runs = (runs_df["status"] == "Failed").sum()
    total_processed = runs_df["records_processed"].sum()
    avg_duration = runs_df["duration_seconds"].mean()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Runs", f"{total_runs:,}")
    col2.metric("Successful Runs", f"{successful_runs:,}")
    col3.metric("Records Processed", f"{total_processed:,}")
    col4.metric("Avg Duration", f"{avg_duration:.3f}s")

    # Execution status
    st.subheader("Pipeline Health")

    if failed_runs == 0:
        st.success("All recorded pipeline runs completed successfully.")
    else:
        st.error(f"{failed_runs} pipeline run(s) failed.")

    # Processing chart
    st.subheader("Records Processed by Pipeline Run")

    chart_df = runs_df.sort_values("run_id")

    fig_runs = px.bar(
        chart_df,
        x="run_id",
        y=[
            "records_inserted",
            "records_skipped",
            "records_rejected"
        ],
        barmode="stack",
        title="Incremental Load Processing History",
        labels={
            "run_id": "Pipeline Run ID",
            "value": "Number of Records",
            "variable": "Processing Result"
        }
    )

    st.plotly_chart(fig_runs, use_container_width=True)

    # Execution history table
    st.subheader("Pipeline Execution History")

    st.dataframe(
        runs_df[
            [
                "run_id",
                "pipeline_name",
                "start_time",
                "status",
                "records_processed",
                "records_inserted",
                "records_skipped",
                "records_rejected",
                "duration_seconds"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Monitoring data is stored in the SQLite pipeline_runs table."
    )
