import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# 1. LOAD DATA
# ---------------------------------------------------------
# Update this to your actual path
csv_path = r'C:\DATA ANALYST PROJECTS\Supply_Chain_Project\raw data\DataCoSupplyChainDataset.csv'

print("Loading Supply Chain Data...")
# We only need the Date and the Quantity sold
df = pd.read_csv(csv_path, encoding='ISO-8859-1', usecols=['order date (DateOrders)', 'Order Item Quantity'])

# Rename to standard names
df.columns = ['ds', 'y']

# Convert text dates to Python DateObjects
# This fixes the "Timezone" error Prophet sometimes gets
df['ds'] = pd.to_datetime(df['ds']).dt.tz_localize(None)

# ---------------------------------------------------------
# 2. PREPARE THE "SIGNAL"
# ---------------------------------------------------------
print("Aggregating Daily Demand...")
# We sum up all sales for each day to get a single "Daily Demand" line
daily_demand = df.groupby('ds')['y'].sum().reset_index()

# Remove outlier noise (Optional, but makes graphs cleaner)
# We keep only days where sales > 0
daily_demand = daily_demand[daily_demand['y'] > 0]

print(f"Training on {len(daily_demand)} days of history...")

# ---------------------------------------------------------
# 3. TRAIN PROPHET MODEL
# ---------------------------------------------------------
# interval_width=0.95 means we want 95% confidence in our prediction
model = Prophet(yearly_seasonality=True, weekly_seasonality=True, interval_width=0.95)
model.fit(daily_demand)

# ---------------------------------------------------------
# 4. PREDICT THE FUTURE (30 Days)
# ---------------------------------------------------------
print("Forecasting next 30 days...")
future = model.make_future_dataframe(periods=30)
forecast = model.predict(future)

# ---------------------------------------------------------
# 5. INVENTORY OPTIMIZATION (The "MBA" Math)
# ---------------------------------------------------------
# We extract just the future 30 days
next_30_days = forecast.tail(30)

# Calculate "Safety Stock"
# Formula: Max Demand * Max Lead Time - Avg Demand * Avg Lead Time
# We simulate a lead time (time to get stock from supplier) of 7 days
max_demand = daily_demand['y'].max()
avg_demand = daily_demand['y'].mean()
lead_time_days = 7 

safety_stock = (max_demand * lead_time_days) - (avg_demand * lead_time_days)

print(f"--- INVENTORY RECOMMENDATION ---")
print(f"Predicted Demand (Next 30 Days): {int(next_30_days['yhat'].sum())} units")
print(f"Recommended Safety Stock Buffer: {int(safety_stock)} units")
print(f"--------------------------------")

# ---------------------------------------------------------
# 6. SAVE OUTPUT
# ---------------------------------------------------------
# We save the forecast to visualize in Power BI later
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_csv('forecast_results.csv', index=False)
print("SUCCESS: Forecast saved to 'forecast_results.csv'")

# Generate a quick plot to check quality
model.plot(forecast)
plt.title("Demand Forecast (Black Dots = Actual, Blue Line = AI Prediction)")
plt.savefig('forecast_chart.png')
print("Chart saved as 'forecast_chart.png'")