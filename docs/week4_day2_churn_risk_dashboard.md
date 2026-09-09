# Week 4 Day 2: Predictive Churn Risk Dashboard & Retention Intelligence Engine

## Objective

The objective of this milestone is to operationalize customer churn machine learning predictions and Lifetime Value (LTV) estimates into an interactive, executive-grade **Churn Risk Dashboard**. This system moves beyond static historical reporting to score every customer account in real time, identify high-value accounts at imminent risk of attrition, isolate feature hazard drivers, and prescribe automated retention workflows.

---

## Dataset & Machine Learning Models Used

- **Dataset:** Telco Customer Churn Dataset (`telco_feature_engineered_commit3.csv` and `WA_Fn-UseC_-Telco-Customer-Churn.csv`)
- **Total Customer Base:** 7,043 Accounts
- **Churn Classifier:** Trained Logistic Regression with OneHotEncoder/StandardScaler Pipeline (`logistic_regression_model.pkl`)
- **LTV Regressor:** Trained Random Forest Regressor (`best_ltv_model.pkl`)
- **Portfolio Mean Churn Risk:** 26.51%
- **Critical & High Risk Accounts:** 1,754 Accounts (24.9% of portfolio)
- **Total Portfolio MRR:** $456,116.60 / month
- **Expected Monthly Revenue at Risk:** $139,620.25 / month (30.6% of portfolio MRR)
- **Annualized Risk Exposure Run-Rate:** $1,675,443.00 / year

---

## Analysis Dimensions & Operational Architecture

1. **Continuous Churn Probability Scoring & Tier Calibration:**
   - Evaluated all 7,043 accounts using calibrated logistic regression scoring.
   - Segmented accounts into four standardized tiers:
     - **Critical Risk (≥70%):** 812 accounts | 96.3% empirical churn | $52,754/mo expected loss.
     - **High Risk (45%–70%):** 942 accounts | 73.0% empirical churn | $40,443/mo expected loss.
     - **Medium Risk (25%–45%):** 995 accounts | 26.2% empirical churn | $24,364/mo expected loss.
     - **Low Risk (<25%):** 4,294 accounts | 3.2% empirical churn | $22,059/mo expected loss.

2. **Feature Hazard Driver Quantification:**
   - Calculated net risk differentials (+%) for structural catalysts versus protective retention moats.
   - Identified top hazard multipliers: Month-to-Month contracts (+36.1%), Absence of Online Security (+30.7%), Tenure < 6 months (+30.0%), Lack of Tech Support (+30.0%), and Electronic Check billing (+28.8%).

3. **Financial Exposure & Value-at-Risk:**
   - Quantified monthly recurring revenue (MRR) at risk and estimated customer lifetime value (LTV) exposure across tiers.
   - Confirmed that the top two tiers (Critical + High Risk) drive **66.7% ($93.2k/mo)** of all lost company revenue.

4. **2x2 Risk & Value Retention Matrix:**
   - Cross-tabulated Account Value (Monthly Charges split by median $70.35/mo) and Attrition Propensity (Risk score split at 45%).
   - Isolated the **Immediate Intervention** quadrant: 1,286 accounts accounting for **$78,094.84/mo (55.9%)** of all enterprise churn losses.

5. **Interactive UI & Simulation Capabilities:**
   - Developed `Reports/churn_risk_dashboard.html`: A standalone dark-mode HTML5 application with glassmorphism, responsive KPI cards, and bidirectional navigation to `churn_trends_dashboard.html`.
   - Built a **Live Customer Risk Explorer** with search, multi-factor filtering, and CSV export.
   - Implemented a **Real-Time Customer Risk Simulator** with dynamic SVG gauge and prescriptive retention actions.
   - Implemented a **Portfolio Retention Campaign ROI Simulator** calculating net return on customer retention incentives.

---

## Visualizations & Artifacts Generated

All artifacts were generated programmatically via `scripts/generate_churn_risk_dashboard.py` and `scripts/build_html_dashboard.py` and saved under `Reports/`:

| Artifact | Type | Description |
| :--- | :---: | :--- |
| `Reports/churn_risk_dashboard.html` | UI Application | Standalone interactive executive dashboard with live customer explorer, risk profiler, and ROI simulator |
| `Reports/churn_trends_dashboard.html` | UI Application | Updated historical trend dashboard with cross-navigation toggle |
| `Reports/churn_risk_distribution.png` | Plot (300 DPI) | Risk probability score distribution and calibrated tier volume bars |
| `Reports/churn_risk_drivers_importance.png` | Plot (300 DPI) | Top hazard factors vs protective retention moats |
| `Reports/churn_risk_revenue_exposure.png` | Plot (300 DPI) | Monthly recurring revenue and lifetime value exposure by risk tier |
| `Reports/churn_risk_action_matrix.png` | Plot (300 DPI) | 2x2 Value vs Risk retention segmentation matrix with financial callouts |
| `Reports/customer_churn_risk_scores.csv` | Data | Full 7,043-customer scored roster with probabilities, risk tiers, and recommended actions |
| `Reports/churn_risk_tier_summary.csv` | Data | Aggregated accounts, empirical churn rates, and revenue loss by tier |
| `Reports/churn_risk_segment_matrix_summary.csv` | Data | Aggregated metrics for the four 2x2 action quadrants |
| `Reports/churn_risk_top_drivers_summary.csv` | Data | Quantified feature hazard increases and odds differentials |
| `Reports/sample_risk_customers.json` | Data | Curated customer records for the live browser explorer |
| `Reports/churn_risk_report.md` | Document | Executive retention and churn risk analysis report |

---

## Operational Retention Playbooks

1. **Customer Success 24-Hour SLA (Immediate Intervention):**
   Deploy dedicated account managers to contact the 1,286 accounts in the High-Value / High-Risk quadrant within 24 hours of risk score generation. Provide a $10/mo contract lock-in credit and complimentary Tech Support bundle to protect $78.1k/mo in cash flow.
2. **Automated Marketing Drip (Automated Nurture):**
   Deliver a 3-stage email and SMS re-engagement series to lower-ARPU customers at high risk, featuring self-service discount vouchers and 60-day security trials.
3. **Autopay Migration Incentive:**
   Offer a one-time $15 bill credit to transition the 2,365 Electronic Check customers to recurring automated Credit Card or Bank ACH payments, mitigating a +28.8% churn risk factor.

---

## Conclusion

The Churn Risk Dashboard & Retention Intelligence Engine was successfully established for the Telco Customer Churn & LTV project. By synthesizing trained predictive models into a live, interactive diagnostic suite, the team has transitioned this initiative into operational execution capable of preserving over **$417,000 annually** in recurring customer revenue.
