import pandas as pd
from sqlalchemy import create_engine

# PostgreSQL connection
engine = create_engine(
    "postgresql+psycopg2://postgres:Afreen@localhost:5432/telco_churn_do"
)

# Load CSV
df = pd.read_csv(
    "data/WA_Fn-UseC_-Telco-Customer-Churn.csv"
)

# Make CSV column names match PostgreSQL column names
df.columns = df.columns.str.lower()

# Insert data into PostgreSQL
df.to_sql(
    "telco_customer_churn",
    engine,
    if_exists="append",
    index=False
)

print(f"Data loaded successfully! {len(df)} rows inserted.")


print(f"Data loaded successfully! {len(df)} rows inserted.")