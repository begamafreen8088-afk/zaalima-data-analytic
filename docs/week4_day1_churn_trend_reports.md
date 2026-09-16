# Week 4 Day 1: Comprehensive Churn Trend Reports & Retention Intelligence

## Objective

The objective of this milestone is to synthesize historical customer data, feature-engineered behavioral attributes, and predictive signals into comprehensive, executive-ready Churn Trend Reports. These reports establish clear diagnostic visibility into customer attrition patterns, quantify monthly recurring revenue (MRR) at risk, and provide actionable business recommendations to optimize retention strategies.

---

## Dataset Used

- **Dataset:** Telco Customer Churn Dataset (`telco_feature_engineered_commit3.csv` and `WA_Fn-UseC_-Telco-Customer-Churn.csv`)
- **Total Records:** 7,043 Accounts
- **Baseline Churn Rate:** 26.54% (1,869 churned customers)
- **Total Portfolio MRR:** $456,116.60 / month
- **Monthly Revenue Lost to Churn:** $139,130.85 / month (30.50% of portfolio revenue)
- **Annualized Churn Run-Rate:** $1,669,570.20 / year

---

## Analysis Dimensions & Methodology

1. **Tenure Lifecycle & Cohort Survival Dynamics:**
   - Evaluated churn rates across distinct lifecycle cohorts (0–6m, 7–12m, 13–24m, 25–48m, 49–72m).
   - Constructed a customer retention survival curve across months 0–72 to identify attrition inflection points.

2. **Contract Type & Commitment Disparity:**
   - Assessed churn differentials between Month-to-Month, One-Year, and Two-Year contracts.
   - Evaluated contract type trajectory across customer tenure stages.

3. **Financial Exposure & Spend Tier Concentration:**
   - Performed Kernel Density Estimation (KDE) on Monthly Charges for churned versus retained accounts.
   - Segmented MRR into spend quintiles to isolate where top-line cash flow is lost.

4. **Service Ecosystem & Stickiness Buffer:**
   - Compared broadband technologies (Fiber Optic vs. DSL vs. No Internet).
   - Quantified the protective churn-reduction impact of value-added services (Online Security, Tech Support, Online Backup, Device Protection).

5. **Billing & Payment Channel Friction:**
   - Analyzed customer attrition across manual (Electronic Check, Mailed Check) and automated (Bank ACH, Credit Card) payment methods.
   - Measured the interaction between Paperless Billing and payment methods.

6. **Customer Risk Segmentation Matrix (2x2):**
   - Plotted customer accounts across Loyalty (Tenure) and Account Value (Monthly Charges) to define four actionable intervention quadrants.

---

## Key Findings

1. **The 6-Month Onboarding Cliff:**
   - 52.94% of new customers churn within their first 6 months.
   - By month 24+, retention stabilizes above 80%, and for 48+ months, retention exceeds 90.49%.

2. **The 15.1x Contract Risk Multiplier:**
   - Month-to-Month customers churn at **42.71%**, compared to **11.27%** for One-Year and **2.83%** for Two-Year contracts.
   - Month-to-Month accounts produce 79.5% ($110.6k/mo) of all lost monthly revenue.

3. **High-ARPU Accounts Drive 86.3% of Lost Cash:**
   - The $80–$100 monthly charges bracket has the highest churn rate (**37.02%**) and loses **$58,785.25/month**.
   - Accounts paying >$60/month account for 86.28% ($120,046/month) of all lost revenue.

4. **The Fiber Optic Hazard:**
   - Fiber Optic subscribers exhibit a **41.89%** churn rate despite generating high ARPU ($91.50/mo), compared to 18.96% for DSL.

5. **Support Services Cut Churn by Over 60%:**
   - Customers subscribing to **Online Security** experience a **27.16%** reduction in churn (14.61% vs 41.77%).
   - Customers subscribing to **Tech Support** experience a **26.47%** reduction in churn (15.17% vs 41.64%).

6. **Electronic Check Friction:**
   - Electronic check users churn at **45.29%** overall and **53.73%** on Month-to-Month contracts, while automated credit card payers churn at only 15.24%.

---

## Visualizations & Artifacts Generated

All artifacts were generated programmatically via `scripts/generate_churn_reports.py` and saved under `Reports/`:

| Artifact | Type | Description |
| :--- | :---: | :--- |
| `Reports/churn_tenure_cohort_trend.png` | Plot | Cohort churn bars and customer survival curve (0–72 mo) |
| `Reports/churn_contract_risk_trend.png` | Plot | Contract risk comparison and tenure trajectory |
| `Reports/churn_revenue_monthly_charges_trend.png` | Plot | Monthly charges KDE density and lost MRR by spend tier |
| `Reports/churn_service_stickiness_trend.png` | Plot | Internet service types and support service protection buffers |
| `Reports/churn_payment_billing_trend.png` | Plot | Payment channel friction and paperless billing interaction |
| `Reports/churn_risk_segmentation_matrix.png` | Plot | 2x2 Value vs Risk retention segmentation matrix |
| `Reports/tenure_cohort_churn_summary.csv` | Data | Cohort customer counts, churn rates, and retention percentages |
| `Reports/contract_payment_churn_summary.csv` | Data | Crossed contract and payment channel statistics |
| `Reports/service_adoption_churn_summary.csv` | Data | Net churn reduction metrics for each add-on feature |
| `Reports/revenue_at_risk_summary.csv` | Data | Spend bracket volumes, churn rates, and lost MRR |
| `Reports/churn_trend_report.md` | Doc | Executive retention report with detailed narrative and insights |
| `Reports/churn_trends_dashboard.html` | UI | Interactive dark-mode dashboard with KPI cards and ROI simulator |

---

## Strategic Recommendations

1. **90-Day New Customer Protocol:** Bundle complimentary Tech Support and Online Security for 90 days on all new broadband accounts to alleviate the 52.9% early churn cliff.
2. **Month-to-Month Contract Inoculation:** Provide a $5/month bill discount or free equipment upgrade for customers migrating to 12-month commitments.
3. **Autopay Migration Campaign:** Offer a one-time $10 credit to incentivize electronic check customers to enroll in automated bank or card payments.
4. **Fiber Optic Service Quality Assurance:** Institute proactive line quality monitoring and priority ticket resolution for high-ARPU fiber accounts.

---

## Conclusion

The Churn Trend Reporting suite was successfully established for the Telco Customer Churn & LTV project. The pipeline combines visual diagnostic charts, structured CSV exports, an executive markdown report, and an interactive HTML dashboard. These deliverables transition the project from model training into operational business decision-making and targeted customer retention strategies.
