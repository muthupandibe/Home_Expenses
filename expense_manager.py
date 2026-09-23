import pandas as pd


# =========================================================
# CONVERT TRANSACTIONS TO DATAFRAME
# =========================================================

def transactions_dataframe(records):

    if not records:
        return pd.DataFrame()

    df = pd.DataFrame(records)

    if "transaction_date" in df.columns:

        df["transaction_date"] = pd.to_datetime(
            df["transaction_date"]
        )

    if "amount" in df.columns:

        df["amount"] = pd.to_numeric(
            df["amount"],
            errors="coerce"
        )

    return df


# =========================================================
# CALCULATE SUMMARY
# =========================================================

def calculate_summary(df):

    if df.empty:

        return {
            "total_income": 0,
            "total_expense": 0,
            "balance": 0,
            "transaction_count": 0
        }

    income = df.loc[
        df["transaction_type"] == "Income",
        "amount"
    ].sum()

    expense = df.loc[
        df["transaction_type"] == "Expense",
        "amount"
    ].sum()

    return {
        "total_income": income,
        "total_expense": expense,
        "balance": income - expense,
        "transaction_count": len(df)
    }


# =========================================================
# CATEGORY SUMMARY
# =========================================================

def category_summary(df):

    if df.empty:
        return pd.DataFrame()

    expense_df = df[
        df["transaction_type"] == "Expense"
    ].copy()

    if expense_df.empty:
        return pd.DataFrame()

    result = (
        expense_df
        .groupby("category_name", dropna=False)["amount"]
        .sum()
        .reset_index()
    )

    result.columns = [
        "Category",
        "Amount"
    ]

    result = result.sort_values(
        "Amount",
        ascending=False
    )

    return result


# =========================================================
# MONTHLY SUMMARY
# =========================================================

def monthly_summary(df):

    if df.empty:
        return pd.DataFrame()

    df = df.copy()

    df["Month"] = (
        pd.to_datetime(
            df["transaction_date"]
        )
        .dt.to_period("M")
        .astype(str)
    )

    result = (
        df.groupby(
            ["Month", "transaction_type"]
        )["amount"]
        .sum()
        .reset_index()
    )

    return result


# =========================================================
# PAYMENT METHOD SUMMARY
# =========================================================

def payment_method_summary(df):

    if df.empty:
        return pd.DataFrame()

    expense_df = df[
        df["transaction_type"] == "Expense"
    ].copy()

    if expense_df.empty:
        return pd.DataFrame()

    expense_df["payment_method"] = (
        expense_df["payment_method"]
        .fillna("Unknown")
    )

    result = (
        expense_df
        .groupby("payment_method")["amount"]
        .sum()
        .reset_index()
    )

    return result.sort_values(
        "amount",
        ascending=False
    )


# =========================================================
# FILTER TRANSACTIONS
# =========================================================

def filter_transactions(
    df,
    transaction_type="All",
    category="All"
):

    if df.empty:
        return df

    filtered = df.copy()

    if transaction_type != "All":

        filtered = filtered[
            filtered["transaction_type"]
            == transaction_type
        ]

    if category != "All":

        filtered = filtered[
            filtered["category_name"]
            == category
        ]

    return filtered