import psycopg2
from psycopg2.extras import RealDictCursor


# =========================================================
# POSTGRESQL CONNECTION SETTINGS
# =========================================================

HOST = "localhost"
PORT = "5432"
DATABASE = "Home_Expenses"
USER = "postgres"

# CHANGE THIS TO YOUR POSTGRESQL PASSWORD
PASSWORD = "123456"


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_connection():

    return psycopg2.connect(
        host=HOST,
        port=PORT,
        database=DATABASE,
        user=USER,
        password=PASSWORD
    )


# =========================================================
# GENERIC QUERY FUNCTION
# =========================================================

def execute_query(
    query,
    params=None,
    fetch=False,
    fetch_one=False
):

    connection = get_connection()

    try:

        cursor = connection.cursor(
            cursor_factory=RealDictCursor
        )

        cursor.execute(query, params)

        if fetch:

            result = cursor.fetchall()

        elif fetch_one:

            result = cursor.fetchone()

        else:

            connection.commit()
            result = True

        cursor.close()

        if not fetch and not fetch_one:
            connection.commit()

        return result

    except Exception:

        connection.rollback()

        raise

    finally:

        connection.close()


# =========================================================
# CATEGORY FUNCTIONS
# =========================================================

def get_categories(category_type=None):

    if category_type:

        query = """
            SELECT
                id,
                category_name,
                category_type
            FROM categories
            WHERE category_type = %s
            ORDER BY category_name
        """

        return execute_query(
            query,
            (category_type,),
            fetch=True
        )

    query = """
        SELECT
            id,
            category_name,
            category_type
        FROM categories
        ORDER BY category_type, category_name
    """

    return execute_query(
        query,
        fetch=True
    )


# =========================================================
# ADD TRANSACTION
# =========================================================

def add_transaction(
    transaction_date,
    transaction_type,
    category_id,
    description,
    amount,
    payment_method,
    notes
):

    query = """
        INSERT INTO transactions
        (
            transaction_date,
            transaction_type,
            category_id,
            description,
            amount,
            payment_method,
            notes
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        )
    """

    return execute_query(
        query,
        (
            transaction_date,
            transaction_type,
            category_id,
            description,
            amount,
            payment_method,
            notes
        )
    )


# =========================================================
# GET ALL TRANSACTIONS
# =========================================================

def get_transactions():

    query = """
        SELECT
            t.id,
            t.transaction_date,
            t.transaction_type,
            t.category_id,
            c.category_name,
            t.description,
            t.amount,
            t.payment_method,
            t.notes,
            t.created_at
        FROM transactions t

        LEFT JOIN categories c
            ON t.category_id = c.id

        ORDER BY
            t.transaction_date DESC,
            t.id DESC
    """

    return execute_query(
        query,
        fetch=True
    )


# =========================================================
# GET ONE TRANSACTION
# =========================================================

def get_transaction(transaction_id):

    query = """
        SELECT
            t.id,
            t.transaction_date,
            t.transaction_type,
            t.category_id,
            c.category_name,
            t.description,
            t.amount,
            t.payment_method,
            t.notes
        FROM transactions t

        LEFT JOIN categories c
            ON t.category_id = c.id

        WHERE t.id = %s
    """

    return execute_query(
        query,
        (transaction_id,),
        fetch_one=True
    )


# =========================================================
# UPDATE TRANSACTION
# =========================================================

def update_transaction(
    transaction_id,
    transaction_date,
    transaction_type,
    category_id,
    description,
    amount,
    payment_method,
    notes
):

    query = """
        UPDATE transactions

        SET
            transaction_date = %s,
            transaction_type = %s,
            category_id = %s,
            description = %s,
            amount = %s,
            payment_method = %s,
            notes = %s

        WHERE id = %s
    """

    return execute_query(
        query,
        (
            transaction_date,
            transaction_type,
            category_id,
            description,
            amount,
            payment_method,
            notes,
            transaction_id
        )
    )


# =========================================================
# DELETE TRANSACTION
# =========================================================

def delete_transaction(transaction_id):

    query = """
        DELETE FROM transactions
        WHERE id = %s
    """

    return execute_query(
        query,
        (transaction_id,)
    )


# =========================================================
# ADD / UPDATE BUDGET
# =========================================================

def add_or_update_budget(
    budget_month,
    category_id,
    budget_amount
):

    query = """
        INSERT INTO budgets
        (
            budget_month,
            category_id,
            budget_amount
        )

        VALUES
        (
            %s,
            %s,
            %s
        )

        ON CONFLICT
        (
            budget_month,
            category_id
        )

        DO UPDATE SET
            budget_amount = EXCLUDED.budget_amount
    """

    return execute_query(
        query,
        (
            budget_month,
            category_id,
            budget_amount
        )
    )


# =========================================================
# GET BUDGETS
# =========================================================

def get_budgets():

    query = """
        SELECT
            b.id,
            b.budget_month,
            b.category_id,
            c.category_name,
            b.budget_amount
        FROM budgets b

        LEFT JOIN categories c
            ON b.category_id = c.id

        ORDER BY
            b.budget_month DESC,
            c.category_name
    """

    return execute_query(
        query,
        fetch=True
    )


# =========================================================
# DELETE BUDGET
# =========================================================

def delete_budget(budget_id):

    query = """
        DELETE FROM budgets
        WHERE id = %s
    """

    return execute_query(
        query,
        (budget_id,)
    )


# =========================================================
# DASHBOARD SUMMARY
# =========================================================

def get_dashboard_summary():

    query = """
        SELECT

            COALESCE(
                SUM(
                    CASE
                        WHEN transaction_type = 'Income'
                        THEN amount
                        ELSE 0
                    END
                ),
                0
            ) AS total_income,

            COALESCE(
                SUM(
                    CASE
                        WHEN transaction_type = 'Expense'
                        THEN amount
                        ELSE 0
                    END
                ),
                0
            ) AS total_expense,

            COUNT(*) AS transaction_count

        FROM transactions
    """

    return execute_query(
        query,
        fetch_one=True
    )


# =========================================================
# CATEGORY EXPENSE SUMMARY
# =========================================================

def get_category_expense_summary():

    query = """
        SELECT
            c.category_name,
            COALESCE(
                SUM(t.amount),
                0
            ) AS total_amount

        FROM transactions t

        INNER JOIN categories c
            ON t.category_id = c.id

        WHERE t.transaction_type = 'Expense'

        GROUP BY
            c.category_name

        ORDER BY
            total_amount DESC
    """

    return execute_query(
        query,
        fetch=True
    )


# =========================================================
# MONTHLY SUMMARY
# =========================================================

def get_monthly_summary():

    query = """
        SELECT

            DATE_TRUNC(
                'month',
                transaction_date
            )::date AS month,

            COALESCE(
                SUM(
                    CASE
                        WHEN transaction_type = 'Income'
                        THEN amount
                        ELSE 0
                    END
                ),
                0
            ) AS income,

            COALESCE(
                SUM(
                    CASE
                        WHEN transaction_type = 'Expense'
                        THEN amount
                        ELSE 0
                    END
                ),
                0
            ) AS expense

        FROM transactions

        GROUP BY
            DATE_TRUNC(
                'month',
                transaction_date
            )

        ORDER BY month
    """

    return execute_query(
        query,
        fetch=True
    )


# =========================================================
# PAYMENT METHOD SUMMARY
# =========================================================

def get_payment_method_summary():

    query = """
        SELECT

            COALESCE(
                payment_method,
                'Unknown'
            ) AS payment_method,

            SUM(amount) AS total_amount

        FROM transactions

        WHERE transaction_type = 'Expense'

        GROUP BY
            payment_method

        ORDER BY
            total_amount DESC
    """

    return execute_query(
        query,
        fetch=True
    )


# =========================================================
# TEST DATABASE CONNECTION
# =========================================================

if __name__ == "__main__":

    try:

        connection = get_connection()

        print("====================================")
        print("PostgreSQL Connection Successful")
        print("====================================")

        cursor = connection.cursor()

        cursor.execute(
            "SELECT current_database();"
        )

        database_name = cursor.fetchone()

        print(
            "Database:",
            database_name[0]
        )

        cursor.close()

        connection.close()

        print("Connection closed.")

    except Exception as e:

        print("====================================")
        print("PostgreSQL Connection Failed")
        print("====================================")

        print(e)