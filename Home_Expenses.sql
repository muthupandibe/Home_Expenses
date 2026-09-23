-- ==========================================
-- DAILY HOME EXPENSES DATABASE
-- ==========================================

-- Categories
CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    category_name VARCHAR(100) UNIQUE NOT NULL,
    category_type VARCHAR(20) NOT NULL
);

-- Transactions
CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    transaction_date DATE NOT NULL,
    transaction_type VARCHAR(20) NOT NULL,
    category_id INTEGER REFERENCES categories(id),
    description TEXT,
    amount NUMERIC(12,2) NOT NULL CHECK (amount >= 0),
    payment_method VARCHAR(50),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Monthly budgets
CREATE TABLE IF NOT EXISTS budgets (
    id SERIAL PRIMARY KEY,
    budget_month DATE NOT NULL,
    category_id INTEGER REFERENCES categories(id),
    budget_amount NUMERIC(12,2) NOT NULL CHECK (budget_amount >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(budget_month, category_id)
);


-- ==========================================
-- DEFAULT EXPENSE CATEGORIES
-- ==========================================

INSERT INTO categories
(category_name, category_type)
VALUES
('Groceries', 'Expense'),
('Food', 'Expense'),
('Electricity', 'Expense'),
('Water', 'Expense'),
('Rent', 'Expense'),
('Transport', 'Expense'),
('Medical', 'Expense'),
('Education', 'Expense'),
('Shopping', 'Expense'),
('Entertainment', 'Expense'),
('Household', 'Expense'),
('Mobile & Internet', 'Expense'),
('Insurance', 'Expense'),
('Other Expense', 'Expense')
ON CONFLICT (category_name) DO NOTHING;


-- ==========================================
-- DEFAULT INCOME CATEGORIES
-- ==========================================

INSERT INTO categories
(category_name, category_type)
VALUES
('Salary', 'Income'),
('Business', 'Income'),
('Freelance', 'Income'),
('Interest', 'Income'),
('Investment', 'Income'),
('Gift', 'Income'),
('Other Income', 'Income')
ON CONFLICT (category_name) DO NOTHING;

