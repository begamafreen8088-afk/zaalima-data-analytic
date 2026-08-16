# Week 1 Day 3 - Load Raw Telco CSV Dataset into PostgreSQL

## Objective

Load the Telco Customer Churn CSV dataset into the PostgreSQL database and verify successful data ingestion.

---

## Dataset Information

Dataset Name:
- Telco Customer Churn Dataset

Source File:
- WA_Fn-UseC_-Telco-Customer-Churn.csv

Target Database:
- telco_churn_do

Target Table:
- telco_customer_churn

---

## Data Loading Process

### Step 1: Import Dataset

The raw CSV dataset was imported into PostgreSQL using the Import/Export functionality available in pgAdmin.

### Step 2: Column Mapping

All dataset columns were mapped correctly to the PostgreSQL table schema.

### Step 3: Data Ingestion

Records from the CSV file were successfully inserted into the database table without structural errors.

---

## Verification Queries

### Verify Total Records

```sql
SELECT COUNT(*)
FROM telco_customer_churn;
```

### View First Five Rows

```sql
SELECT *
FROM telco_customer_churn
LIMIT 5;
```

### Verify Table Structure

```sql
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'telco_customer_churn'
ORDER BY ordinal_position;
```

---

## Observations

- Raw Telco dataset loaded successfully into PostgreSQL.
- Table structure matched the CSV dataset columns.
- Customer records were inserted correctly.
- Data is accessible through SQL queries.
- Database is ready for validation and exploratory analysis.

---

## Results

- Database connection established successfully.
- Dataset imported into PostgreSQL.
- Table populated with customer records.
- Initial verification queries executed successfully.

---

## Conclusion

The Telco Customer Churn dataset was successfully loaded into the PostgreSQL database. Data ingestion was completed without major issues, and the dataset is now available for validation, analysis, and churn prediction modeling.