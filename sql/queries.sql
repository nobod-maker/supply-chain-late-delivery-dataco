-- ============================================================================
-- DataCo Smart Supply Chain: Enterprise Analytical Queries & CTEs
-- Compatible with SQLite 3+ / DuckDB / PostgreSQL
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Query 1: Operational OTIF %, Late-Delivery Rate & Shipping Delay Gap
-- Analyzes fulfillment SLA compliance by shipping mode and global market.
-- ----------------------------------------------------------------------------
SELECT 
    s.shipping_mode_name AS shipping_mode,
    g.market,
    COUNT(*) AS total_order_items,
    SUM(f.is_late_delivery) AS late_order_items,
    ROUND(100.0 * (COUNT(*) - SUM(f.is_late_delivery)) / COUNT(*), 2) AS otif_rate_pct,
    ROUND(100.0 * SUM(f.is_late_delivery) / COUNT(*), 2) AS late_delivery_pct,
    ROUND(AVG(f.scheduled_days), 2) AS avg_scheduled_days,
    ROUND(AVG(f.actual_days), 2) AS avg_actual_days,
    ROUND(AVG(f.shipping_delay_days), 2) AS avg_delay_gap_days
FROM Fact_Order_Items f
JOIN Dim_Shipping s ON f.shipping_mode_key = s.shipping_mode_key
JOIN Dim_Geography g ON f.geography_key = g.geography_key
GROUP BY s.shipping_mode_name, g.market
ORDER BY late_delivery_pct DESC;

-- ----------------------------------------------------------------------------
-- Query 2: Product Category Profitability & Negative-Profit Order Concentration
-- Identifies profit leakage and loss-order incidence across categories.
-- ----------------------------------------------------------------------------
SELECT 
    p.category_name,
    COUNT(*) AS total_items_sold,
    ROUND(SUM(f.gross_sales), 2) AS total_gross_sales,
    ROUND(SUM(f.net_sales), 2) AS total_net_sales,
    ROUND(SUM(f.profit_amount), 2) AS total_profit,
    ROUND(100.0 * SUM(f.profit_amount) / NULLIF(SUM(f.net_sales), 0), 2) AS net_profit_margin_pct,
    SUM(f.is_negative_profit) AS loss_order_count,
    ROUND(100.0 * SUM(f.is_negative_profit) / COUNT(*), 2) AS loss_order_incidence_pct,
    ROUND(SUM(CASE WHEN f.profit_amount < 0 THEN f.profit_amount ELSE 0 END), 2) AS total_dollar_loss_leakage
FROM Fact_Order_Items f
JOIN Dim_Product p ON f.product_key = p.product_key
GROUP BY p.category_name
ORDER BY total_dollar_loss_leakage ASC;

-- ----------------------------------------------------------------------------
-- Query 3: Discount Banding vs Operating Profitability Matrix
-- Demonstrates the non-linear profit erosion caused by aggressive promotional discounts.
-- ----------------------------------------------------------------------------
SELECT 
    CASE 
        WHEN f.discount_rate = 0.00 THEN '0% (No Discount)'
        WHEN f.discount_rate <= 0.05 THEN '1% - 5%'
        WHEN f.discount_rate <= 0.10 THEN '6% - 10%'
        WHEN f.discount_rate <= 0.15 THEN '11% - 15%'
        WHEN f.discount_rate <= 0.20 THEN '16% - 20%'
        ELSE '> 20% Extreme Discount'
    END AS discount_tier,
    COUNT(*) AS item_count,
    ROUND(SUM(f.net_sales), 2) AS total_net_revenue,
    ROUND(SUM(f.profit_amount), 2) AS total_profit,
    ROUND(100.0 * SUM(f.profit_amount) / NULLIF(SUM(f.net_sales), 0), 2) AS profit_margin_pct,
    SUM(f.is_negative_profit) AS loss_order_count,
    ROUND(100.0 * SUM(f.is_negative_profit) / COUNT(*), 2) AS loss_order_pct
FROM Fact_Order_Items f
GROUP BY 1
ORDER BY MIN(f.discount_rate) ASC;

-- ----------------------------------------------------------------------------
-- Query 4: Month-over-Month (MoM) Order Volume, Sales & Late Trend via LAG()
-- Calculates monthly velocity and growth rates using window functions.
-- ----------------------------------------------------------------------------
WITH Monthly_Rollup AS (
    SELECT 
        d.year,
        d.month_num,
        SUBSTR(d.full_date, 1, 7) AS order_year_month,
        COUNT(DISTINCT f.order_id) AS monthly_orders,
        COUNT(f.order_item_key) AS monthly_items,
        ROUND(SUM(f.net_sales), 2) AS monthly_net_sales,
        ROUND(SUM(f.profit_amount), 2) AS monthly_profit,
        ROUND(100.0 * SUM(f.is_late_delivery) / COUNT(*), 2) AS monthly_late_rate_pct
    FROM Fact_Order_Items f
    JOIN Dim_Date d ON f.order_date_key = d.date_key
    GROUP BY d.year, d.month_num, SUBSTR(d.full_date, 1, 7)
)
SELECT 
    order_year_month,
    monthly_orders,
    monthly_net_sales,
    monthly_profit,
    monthly_late_rate_pct,
    LAG(monthly_net_sales, 1) OVER (ORDER BY order_year_month) AS prev_month_sales,
    ROUND(100.0 * (monthly_net_sales - LAG(monthly_net_sales, 1) OVER (ORDER BY order_year_month)) 
        / NULLIF(LAG(monthly_net_sales, 1) OVER (ORDER BY order_year_month), 0), 2) AS mom_sales_growth_pct,
    ROUND(100.0 * (monthly_profit - LAG(monthly_profit, 1) OVER (ORDER BY order_year_month)) 
        / NULLIF(ABS(LAG(monthly_profit, 1) OVER (ORDER BY order_year_month)), 0), 2) AS mom_profit_growth_pct
FROM Monthly_Rollup
ORDER BY order_year_month ASC;

-- ----------------------------------------------------------------------------
-- Query 5: Regional Fulfillment Ranking & Transit Friction Analysis
-- Highlights the top 10 regions experiencing severe delay gaps and late delivery rates.
-- ----------------------------------------------------------------------------
SELECT 
    g.market,
    g.order_region,
    COUNT(*) AS total_items,
    SUM(f.is_late_delivery) AS late_items,
    ROUND(100.0 * SUM(f.is_late_delivery) / COUNT(*), 2) AS late_rate_pct,
    ROUND(AVG(f.shipping_delay_days), 2) AS avg_delay_gap_days,
    ROUND(SUM(f.profit_amount), 2) AS regional_profit,
    DENSE_RANK() OVER (ORDER BY ROUND(100.0 * SUM(f.is_late_delivery) / COUNT(*), 2) DESC) AS late_risk_rank
FROM Fact_Order_Items f
JOIN Dim_Geography g ON f.geography_key = g.geography_key
GROUP BY g.market, g.order_region
HAVING COUNT(*) >= 100
ORDER BY late_risk_rank ASC
LIMIT 10;
