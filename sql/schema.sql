-- ============================================================================
-- DataCo Smart Supply Chain: Star-Schema Dimensional DDL
-- Database Engine: SQLite 3+ / DuckDB Compatible
-- ============================================================================

PRAGMA foreign_keys = ON;

-- ----------------------------------------------------------------------------
-- 1. Dimension: Dim_Customer (Type 1 SCD)
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS Dim_Customer;
CREATE TABLE Dim_Customer (
    customer_key INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL UNIQUE,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    customer_segment TEXT NOT NULL,
    customer_city TEXT NOT NULL,
    customer_state TEXT NOT NULL,
    customer_country TEXT NOT NULL,
    customer_zipcode TEXT
);

CREATE INDEX idx_dim_cust_id ON Dim_Customer(customer_id);
CREATE INDEX idx_dim_cust_seg ON Dim_Customer(customer_segment);

-- ----------------------------------------------------------------------------
-- 2. Dimension: Dim_Product
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS Dim_Product;
CREATE TABLE Dim_Product (
    product_key INTEGER PRIMARY KEY,
    product_card_id INTEGER NOT NULL UNIQUE,
    product_name TEXT NOT NULL,
    category_id INTEGER NOT NULL,
    category_name TEXT NOT NULL,
    department_id INTEGER NOT NULL,
    department_name TEXT NOT NULL,
    product_price REAL NOT NULL
);

CREATE INDEX idx_dim_prod_cat ON Dim_Product(category_name);
CREATE INDEX idx_dim_prod_dept ON Dim_Product(department_name);

-- ----------------------------------------------------------------------------
-- 3. Dimension: Dim_Shipping
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS Dim_Shipping;
CREATE TABLE Dim_Shipping (
    shipping_mode_key INTEGER PRIMARY KEY,
    shipping_mode_name TEXT NOT NULL UNIQUE,
    scheduled_days INTEGER NOT NULL,
    target_sla_hours INTEGER NOT NULL
);

-- ----------------------------------------------------------------------------
-- 4. Dimension: Dim_Geography
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS Dim_Geography;
CREATE TABLE Dim_Geography (
    geography_key INTEGER PRIMARY KEY,
    market TEXT NOT NULL,
    order_region TEXT NOT NULL,
    order_country TEXT NOT NULL,
    order_state TEXT NOT NULL,
    order_city TEXT NOT NULL
);

CREATE INDEX idx_dim_geo_market ON Dim_Geography(market);
CREATE INDEX idx_dim_geo_region ON Dim_Geography(order_region);

-- ----------------------------------------------------------------------------
-- 5. Dimension: Dim_Date
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS Dim_Date;
CREATE TABLE Dim_Date (
    date_key INTEGER PRIMARY KEY, -- YYYYMMDD
    full_date TEXT NOT NULL,
    day_of_month INTEGER NOT NULL,
    day_of_week_name TEXT NOT NULL,
    month_num INTEGER NOT NULL,
    month_name TEXT NOT NULL,
    quarter INTEGER NOT NULL,
    year INTEGER NOT NULL,
    is_weekend INTEGER NOT NULL
);

CREATE INDEX idx_dim_date_year_month ON Dim_Date(year, month_num);

-- ----------------------------------------------------------------------------
-- 6. Dimension: Dim_Order_Status
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS Dim_Order_Status;
CREATE TABLE Dim_Order_Status (
    order_status_key INTEGER PRIMARY KEY,
    order_status_name TEXT NOT NULL UNIQUE
);

-- ----------------------------------------------------------------------------
-- 7. Fact Table: Fact_Order_Items (Grain: 1 row per order line item)
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS Fact_Order_Items;
CREATE TABLE Fact_Order_Items (
    order_item_key INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    customer_key INTEGER NOT NULL,
    product_key INTEGER NOT NULL,
    geography_key INTEGER NOT NULL,
    shipping_mode_key INTEGER NOT NULL,
    order_date_key INTEGER NOT NULL,
    ship_date_key INTEGER NOT NULL,
    order_status_key INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    product_price REAL NOT NULL,
    gross_sales REAL NOT NULL,
    discount_rate REAL NOT NULL,
    discount_amount REAL NOT NULL,
    net_sales REAL NOT NULL,
    profit_amount REAL NOT NULL,
    profit_margin_ratio REAL NOT NULL,
    scheduled_days INTEGER NOT NULL,
    actual_days INTEGER NOT NULL,
    shipping_delay_days INTEGER NOT NULL,
    is_late_delivery INTEGER NOT NULL,
    is_negative_profit INTEGER NOT NULL,
    predicted_late_prob REAL DEFAULT 0.0,
    FOREIGN KEY (customer_key) REFERENCES Dim_Customer(customer_key),
    FOREIGN KEY (product_key) REFERENCES Dim_Product(product_key),
    FOREIGN KEY (geography_key) REFERENCES Dim_Geography(geography_key),
    FOREIGN KEY (shipping_mode_key) REFERENCES Dim_Shipping(shipping_mode_key),
    FOREIGN KEY (order_date_key) REFERENCES Dim_Date(date_key),
    FOREIGN KEY (ship_date_key) REFERENCES Dim_Date(date_key),
    FOREIGN KEY (order_status_key) REFERENCES Dim_Order_Status(order_status_key)
);

CREATE INDEX idx_fact_order_id ON Fact_Order_Items(order_id);
CREATE INDEX idx_fact_cust_key ON Fact_Order_Items(customer_key);
CREATE INDEX idx_fact_prod_key ON Fact_Order_Items(product_key);
CREATE INDEX idx_fact_geo_key ON Fact_Order_Items(geography_key);
CREATE INDEX idx_fact_ship_key ON Fact_Order_Items(shipping_mode_key);
CREATE INDEX idx_fact_date_key ON Fact_Order_Items(order_date_key);
CREATE INDEX idx_fact_late ON Fact_Order_Items(is_late_delivery);
CREATE INDEX idx_fact_loss ON Fact_Order_Items(is_negative_profit);

-- ----------------------------------------------------------------------------
-- 8. Operational & Reporting View: vw_supply_chain_master
-- ----------------------------------------------------------------------------
DROP VIEW IF EXISTS vw_supply_chain_master;
CREATE VIEW vw_supply_chain_master AS
SELECT 
    f.order_item_key,
    f.order_id,
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.customer_segment,
    p.product_card_id,
    p.product_name,
    p.category_name,
    p.department_name,
    g.market,
    g.order_region,
    g.order_country,
    g.order_city,
    s.shipping_mode_name AS shipping_mode,
    s.scheduled_days AS mode_scheduled_days,
    d_order.full_date AS order_date,
    d_order.year AS order_year,
    d_order.month_num AS order_month,
    d_order.quarter AS order_quarter,
    d_ship.full_date AS ship_date,
    st.order_status_name AS order_status,
    f.quantity,
    f.product_price,
    f.gross_sales,
    f.discount_rate,
    f.discount_amount,
    f.net_sales,
    f.profit_amount,
    f.profit_margin_ratio,
    f.scheduled_days,
    f.actual_days,
    f.shipping_delay_days,
    f.is_late_delivery,
    f.is_negative_profit,
    f.predicted_late_prob
FROM Fact_Order_Items f
JOIN Dim_Customer c ON f.customer_key = c.customer_key
JOIN Dim_Product p ON f.product_key = p.product_key
JOIN Dim_Geography g ON f.geography_key = g.geography_key
JOIN Dim_Shipping s ON f.shipping_mode_key = s.shipping_mode_key
JOIN Dim_Date d_order ON f.order_date_key = d_order.date_key
JOIN Dim_Date d_ship ON f.ship_date_key = d_ship.date_key
JOIN Dim_Order_Status st ON f.order_status_key = st.order_status_key;
