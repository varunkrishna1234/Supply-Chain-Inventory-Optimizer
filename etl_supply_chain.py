import pandas as pd
from sqlalchemy import create_engine
import urllib.parse

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------
db_user = 'root'
db_password = 'Rangachary@2'  # <--- UPDATE THIS
db_host = 'localhost'
db_name = 'supply_chain_db'

# Update this path to where your CSV is located
csv_path = r'C:\DATA ANALYST PROJECTS\Supply_Chain_Project\raw data\DataCoSupplyChainDataset.csv'

# ---------------------------------------------------------
# 1. READ DATA (Exact Column Mapping)
# ---------------------------------------------------------
print("Reading CSV...")

# Mapping CSV columns (Left) to Database columns (Right)
# This ensures we only pick what we need.
cols_to_use = [
    'Order Id', 'order date (DateOrders)', 'Product Card Id', 'Category Name',
    'Product Price', 'Sales', 'Order Item Quantity', 
    'shipping date (DateOrders)', 'Days for shipping (real)', 
    'Days for shipment (scheduled)', 'Delivery Status'
]

try:
    df = pd.read_csv(csv_path, usecols=cols_to_use, encoding='ISO-8859-1')
    print(f"CSV Loaded. Rows: {len(df)}")
except Exception as e:
    print(f"Error reading CSV: {e}")
    exit()

# Rename columns to match MySQL table
df.columns = [
    'order_id', 'order_date', 'product_card_id', 'category_name',
    'product_price', 'sales', 'order_item_quantity', 
    'shipping_date', 'days_for_shipping_real', 
    'days_for_shipping_scheduled', 'delivery_status'
]

# Convert Date Columns (Crucial for Time Series)
df['order_date'] = pd.to_datetime(df['order_date'])
df['shipping_date'] = pd.to_datetime(df['shipping_date'])

# ---------------------------------------------------------
# 2. UPLOAD TO SQL
# ---------------------------------------------------------
encoded_password = urllib.parse.quote_plus(db_password)
connection_str = f"mysql+pymysql://{db_user}:{encoded_password}@{db_host}/{db_name}"
engine = create_engine(connection_str)

print("Uploading to MySQL...")
try:
    df.to_sql('raw_supply_chain', con=engine, if_exists='replace', index=False)
    print("SUCCESS: Data loaded into MySQL table 'raw_supply_chain'.")
except Exception as e:
    print(f"Database Error: {e}")