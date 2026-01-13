CREATE DATABASE supply_chain_db;
USE supply_chain_db;

-- Create the staging table
-- We are selecting specific columns relevant to Inventory & Logistics
CREATE TABLE raw_supply_chain (
    order_id INT,
    order_date DATETIME,
    product_card_id INT,
    category_name VARCHAR(100),
    product_price DECIMAL(10,2),
    sales DECIMAL(10,2),
    order_item_quantity INT,
    shipping_date DATETIME,
    days_for_shipping_real INT,
    days_for_shipping_scheduled INT,
    delivery_status VARCHAR(100)
);




/* ABC Inventory Classification 
   Goal: Identify the 'Class A' products that drive the majority of revenue.
*/

WITH product_metrics AS (
    -- 1. Aggregate Sales per Product
    SELECT 
        product_card_id,
        category_name,
        SUM(sales) as total_revenue
    FROM raw_supply_chain
    GROUP BY product_card_id, category_name
),
cumulative_calc AS (
    -- 2. Calculate Running Total of Revenue (Highest to Lowest)
    SELECT 
        product_card_id,
        category_name,
        total_revenue,
        SUM(total_revenue) OVER (ORDER BY total_revenue DESC) as running_total,
        SUM(total_revenue) OVER () as grand_total
    FROM product_metrics
)
-- 3. Assign Class A, B, C based on cumulative percentage
SELECT 
    product_card_id,
    category_name,
    total_revenue,
    (running_total / grand_total) * 100 as cumulative_percentage,
    CASE 
        WHEN (running_total / grand_total) <= 0.80 THEN 'A'
        WHEN (running_total / grand_total) <= 0.95 THEN 'B'
        ELSE 'C'
    END as abc_classification
FROM cumulative_calc
ORDER BY total_revenue DESC;







WITH daily_sales AS (
    -- Step 1: Compress data to 1 row per day
    SELECT 
        DATE(order_date) as sales_date,
        SUM(sales) as daily_revenue
    FROM raw_supply_chain
    GROUP BY DATE(order_date)
)
SELECT 
    sales_date,
    daily_revenue,
    -- Step 2: Calculate average of current day + previous 6 days
    AVG(daily_revenue) OVER (
        ORDER BY sales_date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) as 7_day_moving_avg
FROM daily_sales
ORDER BY sales_date;






SELECT 
    category_name,
    -- Financial Impact
    ROUND(SUM(sales), 2) as total_revenue,
    
    -- Operational Impact: Average Days Late
    -- We only count records where shipment was actually late
    ROUND(AVG(
        CASE 
            WHEN days_for_shipping_real > days_for_shipping_scheduled 
            THEN (days_for_shipping_real - days_for_shipping_scheduled)
            ELSE 0 
        END
    ), 1) as avg_days_delayed
    
FROM raw_supply_chain
GROUP BY category_name
-- Filter: Show me high revenue AND high delay categories
HAVING total_revenue > 50000 AND avg_days_delayed > 0.5
ORDER BY total_revenue DESC;







SELECT 
    DAYNAME(order_date) as day_of_week,
    COUNT(order_id) as total_orders,
    ROUND(SUM(sales), 2) as total_revenue,
    
    -- Calculate % of total orders for context
    ROUND(
        COUNT(order_id) * 100.0 / (SELECT COUNT(*) FROM raw_supply_chain), 
    1) as order_percentage
    
FROM raw_supply_chain
GROUP BY DAYNAME(order_date)
-- Sort logically: Monday to Sunday (requires a trick or field ordering)
ORDER BY total_orders DESC;







