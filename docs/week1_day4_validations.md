Week 1 Day 4 – Data Validation and Verification

Objective

To verify the integrity and accuracy of the imported Telco Customer Churn dataset using SQL queries and ensure that the data is ready for further analysis and model development.

Tasks Performed

1. Verified the total number of records imported into PostgreSQL.
2. Checked the table structure and available columns.
3. Retrieved sample records to confirm successful data insertion.
4. Performed NULL value checks on important columns.
5. Checked for duplicate customer records.
6. Validated overall database consistency.

SQL Validation Queries Executed

Row Count Verification

SELECT COUNT(*) FROM telco_customer_churn;

Sample Data Verification

SELECT * FROM telco_customer_churn LIMIT 5;

NULL Value Check

SELECT COUNT(*)
FROM telco_customer_churn
WHERE TotalCharges IS NULL;

Duplicate Record Check

SELECT customerID, COUNT(*)
FROM telco_customer_churn
GROUP BY customerID
HAVING COUNT(*) > 1;

Observations

* All customer records were successfully loaded into the PostgreSQL database.
* The dataset contains approximately 7,043 customer records.
* Table columns matched the original Telco dataset structure.
* Sample records were retrieved successfully without errors.
* No major data integrity issues were identified during validation.
* Customer demographic, service, billing, and churn information are available for analysis.
* Database queries executed successfully with expected results.
* The imported data is suitable for further preprocessing and exploratory analysis.

Results

* Database validation completed successfully.
* Data quality checks confirmed successful ingestion.
* The PostgreSQL table is ready for feature engineering and machine learning workflows.

Conclusion

The imported Telco Customer Churn dataset was thoroughly verified using SQL validation queries. Data integrity, completeness, and consistency checks were completed successfully, ensuring that the database is ready for the next stages of the Customer Churn Prediction and Lifetime Value (LTV) Engine project.