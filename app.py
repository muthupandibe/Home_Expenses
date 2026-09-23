import io
from datetime import date

import pandas as pd
import streamlit as st
import plotly.express as px

from database import (
    get_connection,
    get_categories,
    add_transaction,
    get_transactions,
    get_transaction,
    update_transaction,
    delete_transaction,
    add_or_update_budget,
    get_budgets,
    delete_budget,
    get_dashboard_summary,
    get_category_expense_summary,
    get_monthly_summary,
    get_payment_method_summary
)

from expense_manager import (
    transactions_dataframe,
    calculate_summary,
    category_summary,
    monthly_summary,
    payment_method_summary,
    filter_transactions
)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Home Expenses Management System",
    page_icon="💰",
    layout="wide"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 32px;
        font-weight: bold;
    }

    .sub-title {
        font-size: 18px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# DATABASE TEST
# =========================================================

def test_database_connection():

    try:

        conn = get_connection()

        conn.close()

        return True, ""

    except Exception as e:

        return False, str(e)


# =========================================================
# LOAD TRANSACTIONS
# =========================================================

@st.cache_data(ttl=5)
def load_transactions():

    records = get_transactions()

    return transactions_dataframe(records)


# =========================================================
# LOAD CATEGORIES
# =========================================================

@st.cache_data(ttl=30)
def load_categories(category_type=None):

    return get_categories(category_type)


# =========================================================
# CLEAR CACHE
# =========================================================

def refresh_data():

    load_transactions.clear()

    load_categories.clear()


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">💰 Daily Home Expenses Management and Financial Analysis System</div>',
    unsafe_allow_html=True
)

st.write(
    "Manage household income, expenses, budgets and financial analysis using PostgreSQL and Streamlit."
)


# =========================================================
# DATABASE CONNECTION CHECK
# =========================================================

db_ok, db_error = test_database_connection()

if not db_ok:

    st.error("❌ PostgreSQL database connection failed.")

    st.code(
        db_error,
        language="text"
    )

    st.warning(
        """
        Please check:

        1. PostgreSQL service is running.
        2. Database `home_expenses` exists.
        3. `.env` contains the correct PostgreSQL password.
        4. DB_HOST is `localhost`.
        5. DB_PORT is `5432`.
        """
    )

    st.stop()


st.success("✅ PostgreSQL database connected successfully.")


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("📌 Navigation")

page = st.sidebar.radio(
    "Select Page",
    [
        "Dashboard",
        "Add Transaction",
        "Manage Transactions",
        "Expense Analysis",
        "Budget Management"
    ]
)


# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":

    st.header("📊 Financial Dashboard")

    df = load_transactions()

    summary = calculate_summary(df)

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Total Income",
            f"₹{summary['total_income']:,.2f}"
        )

    with col2:

        st.metric(
            "Total Expenses",
            f"₹{summary['total_expense']:,.2f}"
        )

    with col3:

        st.metric(
            "Balance",
            f"₹{summary['balance']:,.2f}"
        )

    with col4:

        st.metric(
            "Transactions",
            summary["transaction_count"]
        )

    st.divider()

    if df.empty:

        st.info(
            "No transactions available. Add your first transaction."
        )

    else:

        col1, col2 = st.columns(2)

        # -------------------------------------------------
        # CATEGORY PIE
        # -------------------------------------------------

        with col1:

            st.subheader(
                "Expense by Category"
            )

            category_df = category_summary(df)

            if not category_df.empty:

                fig = px.pie(
                    category_df,
                    names="Category",
                    values="Amount",
                    title="Expense Distribution"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

        # -------------------------------------------------
        # MONTHLY CHART
        # -------------------------------------------------

        with col2:

            st.subheader(
                "Monthly Income vs Expense"
            )

            monthly_df = monthly_summary(df)

            if not monthly_df.empty:

                fig = px.bar(
                    monthly_df,
                    x="Month",
                    y="amount",
                    color="transaction_type",
                    barmode="group",
                    title="Monthly Financial Summary"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

        st.subheader(
            "🧾 Recent Transactions"
        )

        display_df = df.head(10).copy()

        if not display_df.empty:

            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True
            )


# =========================================================
# ADD TRANSACTION
# =========================================================

elif page == "Add Transaction":

    st.header("➕ Add Transaction")

    transaction_type = st.selectbox(
        "Transaction Type",
        ["Expense", "Income"]
    )

    categories = load_categories(
        transaction_type
    )

    if not categories:

        st.error(
            "No categories found. Please run database.sql."
        )

        st.stop()

    category_names = [
        row["category_name"]
        for row in categories
    ]

    category_map = {
        row["category_name"]: row["id"]
        for row in categories
    }

    with st.form("add_transaction_form"):

        transaction_date = st.date_input(
            "Transaction Date",
            value=date.today()
        )

        category_name = st.selectbox(
            "Category",
            category_names
        )

        amount = st.number_input(
            "Amount",
            min_value=0.0,
            step=100.0,
            format="%.2f"
        )

        description = st.text_input(
            "Description"
        )

        payment_method = st.selectbox(
            "Payment Method",
            [
                "Cash",
                "UPI",
                "Debit Card",
                "Credit Card",
                "Bank Transfer",
                "Cheque",
                "Other"
            ]
        )

        notes = st.text_area(
            "Notes"
        )

        submitted = st.form_submit_button(
            "Save Transaction"
        )

        if submitted:

            if amount <= 0:

                st.error(
                    "Amount must be greater than zero."
                )

            else:

                try:

                    add_transaction(
                        transaction_date,
                        transaction_type,
                        category_map[category_name],
                        description,
                        amount,
                        payment_method,
                        notes
                    )

                    refresh_data()

                    st.success(
                        "✅ Transaction added successfully."
                    )

                except Exception as e:

                    st.error(
                        f"Error adding transaction: {e}"
                    )


# =========================================================
# MANAGE TRANSACTIONS
# =========================================================

elif page == "Manage Transactions":

    st.header("📝 Manage Transactions")

    df = load_transactions()

    if df.empty:

        st.info(
            "No transactions available."
        )

    else:

        # -------------------------------------------------
        # FILTERS
        # -------------------------------------------------

        col1, col2 = st.columns(2)

        with col1:

            type_filter = st.selectbox(
                "Transaction Type",
                ["All", "Income", "Expense"]
            )

        with col2:

            categories = sorted(
                df["category_name"]
                .dropna()
                .unique()
                .tolist()
            )

            category_filter = st.selectbox(
                "Category",
                ["All"] + categories
            )

        filtered_df = filter_transactions(
            df,
            type_filter,
            category_filter
        )

        st.subheader(
            "Transaction Records"
        )

        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        # -------------------------------------------------
        # DELETE
        # -------------------------------------------------

        st.subheader(
            "🗑️ Delete Transaction"
        )

        transaction_ids = filtered_df["id"].tolist()

        if transaction_ids:

            delete_id = st.selectbox(
                "Select Transaction ID",
                transaction_ids
            )

            if st.button(
                "Delete Selected Transaction"
            ):

                try:

                    delete_transaction(
                        delete_id
                    )

                    refresh_data()

                    st.success(
                        "Transaction deleted successfully."
                    )

                    st.rerun()

                except Exception as e:

                    st.error(
                        f"Error deleting transaction: {e}"
                    )

        st.divider()

        # -------------------------------------------------
        # EDIT TRANSACTION
        # -------------------------------------------------

        st.subheader(
            "✏️ Edit Transaction"
        )

        if transaction_ids:

            edit_id = st.selectbox(
                "Select Transaction to Edit",
                transaction_ids,
                key="edit_transaction_id"
            )

            transaction = get_transaction(
                edit_id
            )

            if transaction:

                edit_type = st.selectbox(
                    "Transaction Type",
                    ["Expense", "Income"],
                    index=(
                        0
                        if transaction["transaction_type"]
                        == "Expense"
                        else 1
                    )
                )

                edit_categories = load_categories(
                    edit_type
                )

                edit_category_names = [
                    row["category_name"]
                    for row in edit_categories
                ]

                edit_category_map = {
                    row["category_name"]: row["id"]
                    for row in edit_categories
                }

                current_category = (
                    transaction["category_name"]
                )

                if current_category not in edit_category_names:

                    current_category = (
                        edit_category_names[0]
                    )

                with st.form(
                    "edit_transaction_form"
                ):

                    edit_date = st.date_input(
                        "Date",
                        value=transaction[
                            "transaction_date"
                        ]
                    )

                    edit_category = st.selectbox(
                        "Category",
                        edit_category_names,
                        index=edit_category_names.index(
                            current_category
                        )
                    )

                    edit_amount = st.number_input(
                        "Amount",
                        min_value=0.0,
                        value=float(
                            transaction["amount"]
                        ),
                        step=100.0
                    )

                    edit_description = st.text_input(
                        "Description",
                        value=(
                            transaction["description"]
                            or ""
                        )
                    )

                    payment_methods = [
                        "Cash",
                        "UPI",
                        "Debit Card",
                        "Credit Card",
                        "Bank Transfer",
                        "Cheque",
                        "Other"
                    ]

                    current_payment = (
                        transaction["payment_method"]
                        or "Cash"
                    )

                    if current_payment not in payment_methods:

                        current_payment = "Other"

                    edit_payment = st.selectbox(
                        "Payment Method",
                        payment_methods,
                        index=payment_methods.index(
                            current_payment
                        )
                    )

                    edit_notes = st.text_area(
                        "Notes",
                        value=(
                            transaction["notes"]
                            or ""
                        )
                    )

                    update_button = st.form_submit_button(
                        "Update Transaction"
                    )

                    if update_button:

                        if edit_amount <= 0:

                            st.error(
                                "Amount must be greater than zero."
                            )

                        else:

                            try:

                                update_transaction(
                                    edit_id,
                                    edit_date,
                                    edit_type,
                                    edit_category_map[
                                        edit_category
                                    ],
                                    edit_description,
                                    edit_amount,
                                    edit_payment,
                                    edit_notes
                                )

                                refresh_data()

                                st.success(
                                    "Transaction updated successfully."
                                )

                                st.rerun()

                            except Exception as e:

                                st.error(
                                    f"Error updating transaction: {e}"
                                )


# =========================================================
# EXPENSE ANALYSIS
# =========================================================

elif page == "Expense Analysis":

    st.header("📈 Expense Analysis")

    df = load_transactions()

    if df.empty:

        st.info(
            "No transaction data available for analysis."
        )

    else:

        # -------------------------------------------------
        # CATEGORY ANALYSIS
        # -------------------------------------------------

        category_df = category_summary(df)

        if not category_df.empty:

            st.subheader(
                "💰 Expense by Category"
            )

            fig = px.bar(
                category_df,
                x="Category",
                y="Amount",
                title="Total Expense by Category"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # -------------------------------------------------
        # PAYMENT METHOD
        # -------------------------------------------------

        payment_df = payment_method_summary(df)

        if not payment_df.empty:

            st.subheader(
                "💳 Expense by Payment Method"
            )

            fig = px.pie(
                payment_df,
                names="payment_method",
                values="amount",
                title="Payment Method Distribution"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # -------------------------------------------------
        # MONTHLY EXPENSE
        # -------------------------------------------------

        monthly_df = monthly_summary(df)

        if not monthly_df.empty:

            expense_monthly = monthly_df[
                monthly_df["transaction_type"]
                == "Expense"
            ]

            if not expense_monthly.empty:

                st.subheader(
                    "📅 Monthly Expense Trend"
                )

                fig = px.line(
                    expense_monthly,
                    x="Month",
                    y="amount",
                    markers=True,
                    title="Monthly Expense Trend"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

        # -------------------------------------------------
        # SUMMARY TABLE
        # -------------------------------------------------

        st.subheader(
            "📋 Category Summary"
        )

        if not category_df.empty:

            category_display = category_df.copy()

            category_display[
                "Amount"
            ] = category_display[
                "Amount"
            ].round(2)

            st.dataframe(
                category_display,
                use_container_width=True,
                hide_index=True
            )


# =========================================================
# BUDGET MANAGEMENT
# =========================================================

elif page == "Budget Management":

    st.header("🎯 Budget Management")

    expense_categories = load_categories(
        "Expense"
    )

    if not expense_categories:

        st.error(
            "No expense categories available."
        )

        st.stop()

    category_names = [
        row["category_name"]
        for row in expense_categories
    ]

    category_map = {
        row["category_name"]: row["id"]
        for row in expense_categories
    }

    # -----------------------------------------------------
    # ADD / UPDATE BUDGET
    # -----------------------------------------------------

    st.subheader(
        "➕ Set Monthly Budget"
    )

    with st.form("budget_form"):

        budget_month = st.date_input(
            "Budget Month",
            value=date.today().replace(day=1)
        )

        budget_category = st.selectbox(
            "Expense Category",
            category_names
        )

        budget_amount = st.number_input(
            "Budget Amount",
            min_value=0.0,
            step=500.0,
            format="%.2f"
        )

        save_budget = st.form_submit_button(
            "Save / Update Budget"
        )

        if save_budget:

            if budget_amount <= 0:

                st.error(
                    "Budget amount must be greater than zero."
                )

            else:

                try:

                    add_or_update_budget(
                        budget_month,
                        category_map[
                            budget_category
                        ],
                        budget_amount
                    )

                    st.success(
                        "✅ Budget saved successfully."
                    )

                except Exception as e:

                    st.error(
                        f"Error saving budget: {e}"
                    )

    st.divider()

    # -----------------------------------------------------
    # DISPLAY BUDGETS
    # -----------------------------------------------------

    st.subheader(
        "📋 Existing Budgets"
    )

    budgets = get_budgets()

    if budgets:

        budget_df = pd.DataFrame(
            budgets
        )

        budget_df[
            "budget_amount"
        ] = pd.to_numeric(
            budget_df["budget_amount"],
            errors="coerce"
        )

        st.dataframe(
            budget_df,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        # -------------------------------------------------
        # DELETE BUDGET
        # -------------------------------------------------

        budget_ids = [
            row["id"]
            for row in budgets
        ]

        delete_budget_id = st.selectbox(
            "Select Budget ID to Delete",
            budget_ids
        )

        if st.button(
            "Delete Selected Budget"
        ):

            try:

                delete_budget(
                    delete_budget_id
                )

                st.success(
                    "Budget deleted successfully."
                )

                st.rerun()

            except Exception as e:

                st.error(
                    f"Error deleting budget: {e}"
                )

    else:

        st.info(
            "No budgets have been created yet."
        )


# =========================================================
# REPORT EXPORT
# =========================================================

st.sidebar.divider()

st.sidebar.subheader(
    "📥 Export Report"
)

try:

    export_df = load_transactions()

    if not export_df.empty:

        csv_data = export_df.to_csv(
            index=False
        )

        st.sidebar.download_button(
            label="Download CSV",
            data=csv_data,
            file_name="home_expenses_report.csv",
            mime="text/csv"
        )

        excel_buffer = io.BytesIO()

        with pd.ExcelWriter(
            excel_buffer,
            engine="openpyxl"
        ) as writer:

            export_df.to_excel(
                writer,
                index=False,
                sheet_name="Transactions"
            )

        st.sidebar.download_button(
            label="Download Excel",
            data=excel_buffer.getvalue(),
            file_name="home_expenses_report.xlsx",
            mime=(
                "application/vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet"
            )
        )

except Exception as e:

    st.sidebar.error(
        f"Export error: {e}"
    )