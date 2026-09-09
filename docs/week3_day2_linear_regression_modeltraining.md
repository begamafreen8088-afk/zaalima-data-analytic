# Week 3 - Day 2: Linear Regression Model Training

## Objective

The objective of this task was to train a Linear Regression model for Customer Lifetime Value (LTV) prediction using the prepared regression dataset.

## Dataset

LTV Prepared Dataset (ltv_prepared_dataset.csv)

## Model Development

1. Feature Selection

The input features were selected from the prepared dataset, and the LTV column was used as the target variable.

2. Train-Test Split

The dataset was divided into training and testing sets using an 80:20 ratio to evaluate model performance on unseen data.

3. Linear Regression Model

A Linear Regression model was trained using the training dataset to learn the relationship between customer attributes and Customer Lifetime Value.

4. Prediction Generation

The trained model was used to generate LTV predictions on the test dataset.

5. Model Saving

The trained Linear Regression model was saved for future evaluation and comparison with other regression models.

## Implementation Steps

1. Loaded the prepared LTV dataset.
2. Selected feature columns and target variable (LTV).
3. Split the dataset into training and testing sets.
4. Trained a Linear Regression model.
5. Generated predictions using the trained model.
6. Saved the trained model for future use.

## Output Files

* scripts/feature_engineering.ipynb
* data/ltv_prepared_dataset.csv
* data/linear_regression_model.pkl

## Results

The Linear Regression model was successfully trained on the prepared LTV dataset. Predictions were generated on the test data, and the trained model was saved for future evaluation and comparison.

## Conclusion

The Linear Regression model was successfully developed and trained for Customer Lifetime Value prediction. The model established a baseline regression approach for estimating customer value and will be compared with advanced regression models in subsequent project stages.