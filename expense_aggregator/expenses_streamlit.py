import streamlit as st
import pandas as pd
import altair as alt
from expenses import Expenses
import matplotlib.pyplot as plt

plt.style.use("dark_background")

if __name__=="__main__":
    st.set_page_config(page_title="Expestreanse Dashboard", layout="wide")

    st.title("💸 Expense Management Dashboard")

    # --- File Upload ---
    uploaded_file = st.file_uploader(
        "Upload a CSV or Excel file",
        type=["csv", "xlsx", "xls"],
        help="Your file must contain at least: date, amount, category"
    )

    if uploaded_file:
        # --- Load File ---
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.subheader("📄 Raw Data Preview")
        st.dataframe(df.head())

        # --- Basic Normalization ---
        # Try to infer column names
        df.columns = df.columns.str.lower().str.strip()

        # Expected columns: date, amount, category
        required_cols = ["date", "amount", "category"]

        dfE = Expenses(df)

        if not all(col in dfE.df.columns for col in required_cols):
            st.error(f"Your file must contain the following columns: {required_cols}")
            st.stop()


        # --- Summary Metrics ---
        total_expense = dfE.df["amount"].sum()
        avg_expense = dfE.df["amount"].mean()
        num_transactions = len(dfE.df)

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Expense", f"{total_expense:,.2f}")
        col2.metric("Average Expense", f"{avg_expense:,.2f}")
        col3.metric("Transactions", num_transactions)

        # --- Expense by Category ---
        st.subheader("📊 Expense by Category")
        cat_summary = dfE.df.groupby("category")["amount"].sum().reset_index()

        bar_chart = (dfE.summary_by_category(byc='category'))
        st.pyplot(bar_chart)
        #st.altair_chart(bar_chart, use_container_width=True)

        # --- Monthly Trend ---
        st.subheader("📈 Monthly Expense Trend")
        
        line_chart = (
            alt.Chart(dfE.monthly_expense_trend('month', as_index=False))
            .mark_line(point=True)
            .encode(
                x="month:T",
                y="amount:Q",
                tooltip=["month", "amount"]
            )
            .properties(height=400)
        )
        st.altair_chart(line_chart, use_container_width=True)

        # --- Category Breakdown Table ---
        st.subheader("📋 Category Breakdown")
        last_month = dfE.df.sort_values("date", ascending=True).iloc[-1].month
        df_sum = cat_summary.sort_values("amount", ascending=False).assign(pct_of_total=lambda x: x["amount"] / x["amount"].sum() * 100)
        df_sum_last = (dfE.df[dfE.df.month==last_month]
        .groupby(["category"], as_index=False)["amount"].sum()
        .assign(pct_of_total=lambda x: x["amount"] / x["amount"].sum() * 100))

        st.dataframe(df_sum.merge(df_sum_last, on="category", how="left", suffixes=("", f"_{last_month}")).style.format({"amount": "{:,.2f}", "pct_of_total": "{:.2f}%", "amount_last": "{:,.2f}", "pct_of_total_last": "{:.2f}%"}))



        st.subheader("🔧 Select Columns for Analysis")

        col1, col2, col3 = st.columns(3)
        options = [i for i in dfE.df.columns if i not in ('amount', 'timestamp')]
        with col1:
            col_x = st.selectbox("Select first column", options, index=options.index("month") if "month" in options else 0)

        with col2:
            col_y = st.selectbox("Select second column", options, index=options.index("category") if "category" in options else 0)
        with col3:
            col_z = st.selectbox("View as percent of total", [True, False])

        st.write(f"You selected: **{col_x}** and **{col_y}**")
        summary_two_chart = dfE.summary_two(col_x, col_y, as_pct=col_z)
        st.pyplot(summary_two_chart)


    else:
        st.info("Upload a file to begin.")