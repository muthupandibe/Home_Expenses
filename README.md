# 💰 Daily Home Expenses Management and Financial Analysis System

## 📌 Project Overview

The **Daily Home Expenses Management and Financial Analysis System** is a Python-based household financial management application developed using **PostgreSQL, Streamlit, Pandas, and Plotly**.

The application helps users record daily income and expenses, organize transactions into categories, manage monthly budgets, and analyze household financial activities through interactive dashboards and visualizations.

The system provides a centralized platform for managing financial records and understanding spending patterns.

---

## 🎯 Project Objective

The main objective of this project is to develop an easy-to-use household financial management system that can:

* Record daily income and expenses
* Categorize financial transactions
* View and manage transaction records
* Update existing transactions
* Delete unwanted transactions
* Manage monthly budgets
* Analyze spending patterns
* Compare income and expenses
* Monitor financial balance
* Analyze expenses by category
* Analyze expenses by payment method
* Track monthly expense trends
* Export transaction reports to CSV and Excel

---

## 🏠 Problem Statement

Managing household expenses manually using notebooks or spreadsheets can make it difficult to track spending patterns and understand overall financial performance.

The proposed system provides a centralized database-driven solution where users can store household financial transactions and analyze them through an interactive web application.

The system uses PostgreSQL for structured data storage and Streamlit for creating an interactive user interface.

---

## 💡 Proposed Solution

The application provides different modules for household financial management.

### Main Modules

1. Dashboard
2. Add Transaction
3. Manage Transactions
4. Expense Analysis
5. Budget Management
6. Report Export

---

# 🛠️ Technologies Used

| Technology | Purpose                        |
| ---------- | ------------------------------ |
| Python     | Application development        |
| PostgreSQL | Database management            |
| Psycopg2   | Python-PostgreSQL connection   |
| Streamlit  | Web application interface      |
| Pandas     | Data processing and analysis   |
| Plotly     | Interactive visualization      |
| OpenPyXL   | Excel report generation        |
| SQL        | Database creation and querying |

---

# 🏗️ System Architecture

```text
                USER
                  |
                  ↓
        ┌───────────────────┐
        │     Streamlit     │
        │    Web Interface  │
        └─────────┬─────────┘
                  |
                  ↓
        ┌───────────────────┐
        │   Python Logic    │
        │ expense_manager.py│
        └─────────┬─────────┘
                  |
                  ↓
        ┌───────────────────┐
        │    database.py    │
        │   Database Layer  │
        └─────────┬─────────┘
                  |
                  ↓
        ┌───────────────────┐
        │    PostgreSQL     │
        │   home_expenses   │
        └───────────────────┘
```

---

# 📂 Project Structure

```text
Home_Expenses/
│
├── app.py
├── database.py
├── expense_manager.py
├── requirements.txt
├── .env
├── .gitignore
│
└── sql/
    └── database.sql
```

---

# 📄 File Description

## `app.py`

Main Streamlit application.

It provides:

* Dashboard
* Add transaction form
* Transaction management
* Expense analysis
* Budget management
* CSV export
* Excel export
* Interactive charts

---

## `database.py`

Handles communication between Python and PostgreSQL.

It contains functions for:

* PostgreSQL connection
* Executing SQL queries
* Category retrieval
* Adding transactions
* Reading transactions
* Updating transactions
* Deleting transactions
* Adding/updating budgets
* Reading budgets
* Deleting budgets
* Dashboard summaries
* Category summaries
* Monthly summaries
* Payment-method summaries

---

## `expense_manager.py`

Contains the data-processing and analysis logic.

It performs:

* DataFrame conversion
* Financial summary calculation
* Category-wise expense analysis
* Monthly analysis
* Payment-method analysis
* Transaction filtering

---

## `sql/database.sql`

Contains the PostgreSQL database structure.

It creates:

* `categories`
* `transactions`
* `budgets`

It also inserts predefined income and expense categories.

---

## `requirements.txt`

Contains the Python libraries required for the project.

```text
streamlit
pandas
plotly
psycopg2-binary
python-dotenv
openpyxl
```

---

# 🗄️ Database Design

The project uses PostgreSQL as the relational database.

## 1. Categories Table

Stores income and expense categories.

```text
categories
-------------------------
id
category_name
category_type
```

Examples:

```text
Groceries       → Expense
Electricity     → Expense
Rent            → Expense
Salary          → Income
Business        → Income
Freelance       → Income
```

---

## 2. Transactions Table

Stores daily financial transactions.

```text
transactions
-------------------------
id
transaction_date
transaction_type
category_id
description
amount
payment_method
notes
created_at
```

Transaction types:

```text
Income
Expense
```

---

## 3. Budgets Table

Stores monthly category-wise budgets.

```text
budgets
-------------------------
id
budget_month
category_id
budget_amount
created_at
```

---

# 🔗 Database Relationships

```text
categories
     |
     | 1
     |
     | N
transactions
```

and

```text
categories
     |
     | 1
     |
     | N
budgets
```

The `category_id` field connects transactions and budgets with the categories table.

---

# 📊 Dashboard

The dashboard provides an overall financial summary.

It displays:

### Total Income

Total amount received through income transactions.

### Total Expenses

Total amount spent through expense transactions.

### Balance

```text
Balance = Total Income - Total Expenses
```

### Transaction Count

Total number of recorded transactions.

---

# 📈 Data Visualization

The application uses Plotly for interactive charts.

## Expense by Category

Shows how household expenses are distributed among categories.

Example:

```text
Groceries
Rent
Food
Transport
Electricity
Medical
Shopping
```

---

## Monthly Income vs Expense

Displays monthly income and expense values for comparison.

This helps users understand financial patterns over time.

---

## Payment Method Analysis

Shows expenses based on payment methods such as:

```text
Cash
UPI
Debit Card
Credit Card
Bank Transfer
Cheque
Other
```

---

## Monthly Expense Trend

Displays how expenses change across different months.

---

# ✏️ CRUD Operations

The system supports CRUD operations.

## Create

Users can add:

* Income
* Expense
* Budget

## Read

Users can view:

* Transactions
* Categories
* Budgets
* Financial summaries

## Update

Users can update existing transactions and budgets.

## Delete

Users can delete:

* Transactions
* Budgets

---

# 🎯 Budget Management

The Budget Management module allows users to define monthly budgets for expense categories.

For example:

```text
Groceries       ₹10,000
Food             ₹5,000
Transport        ₹4,000
Entertainment    ₹3,000
```

The system stores these budgets in PostgreSQL.

If the same month and category are entered again, the existing budget is updated instead of creating a duplicate record.

---

# 📥 Report Export

Users can download transaction data in two formats.

## CSV

```text
home_expenses_report.csv
```

## Excel

```text
home_expenses_report.xlsx
```

Excel files are generated using the `openpyxl` library.

---

# ⚙️ Installation

## Step 1: Install Python

Install Python 3.9 or later.

Verify:

```bash
python --version
```

---

## Step 2: Create Project Folder

Create:

```text
Home_Expenses
```

---

## Step 3: Create Virtual Environment

Open terminal inside the project folder:

```bash
python -m venv .venv
```

---

## Step 4: Activate Virtual Environment

### Windows

```bash
.venv\Scripts\activate
```

After activation:

```text
(.venv)
```

will appear in the terminal.

---

# 📦 Step 5: Install Required Libraries

Run:

```bash
python -m pip install streamlit pandas plotly psycopg2-binary python-dotenv openpyxl
```

Or use:

```bash
python -m pip install -r requirements.txt
```

---

# 🐘 Step 6: Install PostgreSQL

Install PostgreSQL and make sure the PostgreSQL server is running.

The default PostgreSQL port is:

```text
5432
```

---

# 🗄️ Step 7: Create Database

Open PostgreSQL / pgAdmin and execute:

```sql
CREATE DATABASE home_expenses;
```

---

# 🧱 Step 8: Create Tables

Connect to the `home_expenses` database.

Execute:

```text
sql/database.sql
```

This creates:

```text
categories
transactions
budgets
```

and inserts the default categories.

---

# 🔐 Step 9: Configure PostgreSQL Password

Open:

```text
database.py
```

Set your PostgreSQL password:

```python
PASSWORD = "123456"
```

Replace `123456` with the password you created for the PostgreSQL `postgres` user.

The connection configuration is:

```python
HOST = "localhost"
PORT = "5432"
DATABASE = "home_expenses"
USER = "postgres"
PASSWORD = "your_password"
```

---

# 🔌 Step 10: Test Database Connection

Run:

```bash
python database.py
```

Successful output:

```text
====================================
PostgreSQL Connection Successful
====================================
Database: home_expenses
Connection closed.
```

---

# ▶️ Step 11: Run Streamlit Application

Run:

```bash
python -m streamlit run app.py
```

Streamlit will open the application in the browser.

---

# 🖥️ Application Pages

## 1. Dashboard

Provides:

* Total Income
* Total Expenses
* Balance
* Transaction Count
* Expense Category Chart
* Monthly Income/Expense Chart
* Recent Transactions

---

## 2. Add Transaction

Users can enter:

* Transaction type
* Date
* Category
* Amount
* Description
* Payment method
* Notes

---

## 3. Manage Transactions

Users can:

* View transactions
* Filter transactions
* Edit transactions
* Delete transactions

---

## 4. Expense Analysis

Provides:

* Category-wise expenses
* Payment-method analysis
* Monthly expense trends
* Category summary

---

## 5. Budget Management

Users can:

* Set monthly budgets
* Update budgets
* View budgets
* Delete budgets

---

# 🔄 Application Workflow

```text
Start Application
       |
       ↓
Connect to PostgreSQL
       |
       ↓
Display Streamlit Dashboard
       |
       ├───────────────┐
       ↓               ↓
Add Transaction    Manage Transaction
       |               |
       ↓               ↓
PostgreSQL Database ←──┘
       |
       ↓
Financial Analysis
       |
       ├── Category Analysis
       ├── Payment Analysis
       └── Monthly Analysis
       |
       ↓
Budget Management
       |
       ↓
CSV / Excel Report
```

---

# 🔒 Data Validation

The database uses constraints to maintain data quality.

Examples:

* Transaction amount cannot be negative.
* Budget amount cannot be negative.
* Transaction type is restricted to Income or Expense.
* Category names are unique.
* A category can be associated with multiple transactions.
* A monthly category budget is unique.

---

# 📊 Key Features

* ✅ PostgreSQL database
* ✅ Streamlit web application
* ✅ Household income management
* ✅ Household expense management
* ✅ Expense categorization
* ✅ CRUD operations
* ✅ Monthly budget management
* ✅ Financial dashboard
* ✅ Interactive Plotly charts
* ✅ Monthly trend analysis
* ✅ Payment-method analysis
* ✅ CSV export
* ✅ Excel export
* ✅ Relational database design

---

# 📌 Advantages

1. Centralized financial data management
2. Easy transaction entry
3. Structured PostgreSQL storage
4. Interactive financial dashboard
5. Easy expense analysis
6. Monthly budget management
7. Report generation
8. Reduced manual calculation
9. Better understanding of spending patterns
10. Simple and user-friendly interface

---

# 🚀 Future Enhancements

The project can be extended with:

* User login and authentication
* Multiple household users
* Budget vs actual expense comparison
* Budget alert notifications
* Recurring transactions
* Savings goal tracking
* Advanced financial reports
* PDF report generation
* Cloud database deployment
* Mobile-friendly interface
* Machine learning-based expense prediction
* Automatic expense categorization
* Financial forecasting

---

# 🎓 Project Learning Outcomes

Through this project, the following concepts are demonstrated:

* Python programming
* PostgreSQL database management
* SQL queries
* Database relationships
* CRUD operations
* Python database connectivity
* Pandas data processing
* Streamlit application development
* Interactive data visualization
* Financial data analysis
* Report generation
* Modular Python programming

---

# 🧪 Testing

The application should be tested for:

### Database Connection

```text
PostgreSQL → Python → Successful
```

### Transaction Creation

```text
Add transaction → PostgreSQL → Record created
```

### Transaction Update

```text
Edit transaction → PostgreSQL → Record updated
```

### Transaction Delete

```text
Delete transaction → PostgreSQL → Record deleted
```

### Budget Management

```text
Set budget → PostgreSQL → Budget stored
```

### Report Generation

```text
Transactions → Pandas → CSV / Excel
```

---

# ⚠️ Common Errors

## Error: `ModuleNotFoundError`

Install the required library:

```bash
python -m pip install -r requirements.txt
```

---

## Error: PostgreSQL connection failed

Check:

```text
HOST = "localhost"
PORT = "5432"
DATABASE = "home_expenses"
USER = "postgres"
PASSWORD = "your_actual_password"
```

Also make sure PostgreSQL is running.

---

## Error: Database does not exist

Create it:

```sql
CREATE DATABASE home_expenses;
```

---

## Error: Relation does not exist

Run:

```text
sql/database.sql
```

against the `home_expenses` database.

---

# 👩‍💻 Conclusion

The **Daily Home Expenses Management and Financial Analysis System** provides a complete database-driven solution for managing household financial transactions.

By combining **Python, PostgreSQL, Streamlit, Pandas, and Plotly**, the system provides transaction management, budgeting, financial analysis, interactive visualization, and report export in a single application.

The project demonstrates an end-to-end workflow from **database design and SQL operations to Python application development and interactive financial analytics**.

---

## 👨‍💻 Technologies

```text
Python
PostgreSQL
SQL
Streamlit
Pandas
Plotly
Psycopg2
OpenPyXL
```

---

## 📁 Final Project Structure

```text
Home_Expenses/
│
├── app.py
│
├── database.py
│
├── expense_manager.py
│
├── requirements.txt
│
├── .env
│
├── .gitignore
│
└── sql/
    └── database.sql
```

---

## ▶️ Quick Start

```bash
python -m venv .venv

.venv\Scripts\activate

python -m pip install -r requirements.txt

python database.py

python -m streamlit run app.py
```

**Application:** Daily Home Expenses Management and Financial Analysis System
**Database:** PostgreSQL
**Interface:** Streamlit
**Language:** Python
