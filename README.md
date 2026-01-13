# Supply-Chain-Inventory-Optimizer
Automated demand forecasting and inventory optimization engine using Facebook Prophet and SQL Window Functions.

# AI-Driven Supply Chain Inventory Optimizer

## 1. Executive Summary
This project automates the inventory planning process for a high-velocity retail environment. By integrating **SQL-based ABC Analysis** with **Machine Learning Forecasting (Facebook Prophet)**, the system identifies high-value products and predicts future demand to optimize stock levels.

**Business Value:**
* **Stockout Prevention:** Uses predictive analytics to flag inventory shortages 30 days in advance.
* **Capital Efficiency:** Calculates precise "Safety Stock" levels to prevent over-ordering of Class C (low-value) items.
* **Automated Segmentation:** Replaces manual Excel work with automated SQL pipelines that classify products by revenue contribution (Pareto Principle).

## 2. Technical Architecture
* **Data Warehouse:** MySQL database housing standardized transaction history.
* **Segmentation Engine:** SQL Window Functions perform dynamic **ABC Classification** to prioritize inventory focus.
* **Forecasting Engine:** Python script using **Facebook Prophet** to generate 30-day demand forecasts, accounting for seasonality and trend.
* **Optimization Logic:** Automated calculation of Reorder Points and Safety Stock buffers based on lead time variance.

## 3. Tech Stack
* **Forecasting:** Facebook Prophet (Time-series AI)
* **Database:** MySQL (Window Functions, CTEs)
* **ETL:** Python (Pandas, SQLAlchemy)
* **Visualization:** Matplotlib (Trend Analysis)

## 4. Key Metrics & Logic
* **ABC Class A:** Top 80% of revenue (High Priority).
* **Safety Stock Formula:** $(Max Daily Sales \times Max Lead Time) - (Avg Daily Sales \times Avg Lead Time)$
* **Forecast Confidence:** 95% prediction interval used to account for volatility.
