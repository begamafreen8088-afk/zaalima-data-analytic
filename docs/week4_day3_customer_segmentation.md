# Week 4 Day 3: Advanced Customer Segmentation & Behavioral Intelligence

## Objective

The objective of this milestone is to implement advanced multi-dimensional **Customer Segmentation** across the entire 7,043-account portfolio. By uniting behavioral RFM personas, unsupervised machine learning clustering (K-Means), 2D Principal Component Analysis (PCA), and lifecycle × spend heatmaps, the system isolates high-risk customer cohorts, identifies the highest-value accounts, and prescribes tailored retention playbooks.

---

## Dataset & Models Used

- **Dataset:** Telco Customer Churn Scored Portfolio (`Reports/customer_churn_risk_scores.csv` and `data/telco_feature_engineered_commit3.csv`)
- **Total Customer Accounts:** 7,043 Customers
- **Churn Classifier:** Trained Logistic Regression Pipeline
- **LTV Regressor:** Trained Random Forest Regressor
- **Clustering Algorithm:** K-Means Unsupervised Learning ($k=4$ Clusters, StandardScaler normalization)
- **Dimensionality Reduction:** 2D Principal Component Analysis (PCA, 91.1% explained variance)
- **Behavioral Personas Identified:** 6 Mutually Exclusive Business Personas
- **Critical Revenue Hazard Concentration:** 65.5% ($91.5k/month) of total churn risk concentrated in just 2 segments (At-Risk High Rollers and Vulnerable Newcomers)

---

## Analysis Dimensions & Methodology

1. **Strategic Behavioral RFM Personas:**
   - Evaluated accounts across Tenure Longevity (Recency/Loyalty), Service Breadth (Frequency/Adoption), and Monthly Charges/LTV (Monetary).
   - Classified customers into 6 operational segments:
     - **Champions & VIP Loyalists (1,405 accounts | 19.9%):** $93.62/mo ARPU | 3.56% empirical churn | $131.5k/mo MRR.
     - **Digital Enthusiasts & Streamers (407 accounts | 5.8%):** $99.14/mo ARPU | 20.39% empirical churn | $40.4k/mo MRR.
     - **Core Steady Subscribers (2,581 accounts | 36.6%):** $49.21/mo ARPU | 12.59% empirical churn | $127.0k/mo MRR.
     - **Budget Anchors (945 accounts | 13.4%):** $24.13/mo ARPU | 1.69% empirical churn | $22.8k/mo MRR.
     - **At-Risk High Rollers (811 accounts | 11.5%):** $90.86/mo ARPU | 84.09% empirical churn | $48.1k/mo MRR at risk.
     - **Vulnerable Newcomers (894 accounts | 12.7%):** $67.93/mo ARPU | 79.75% empirical churn | $43.4k/mo MRR at risk.

2. **Unsupervised K-Means Machine Learning Clustering & PCA:**
   - Features: Standardized `tenure`, `MonthlyCharges`, `TotalServices`, `Churn_Probability`, and `Predicted_LTV`.
   - Cluster validation via Inertia Elbow Curve and Silhouette Score ($0.403$).
   - Cluster A (High-Churn Flight Risks: 1,733 accounts), Cluster B (High-Value Enterprise Moats: 1,533 accounts), Cluster C (Low-Cost Basic Loyalists: 2,158 accounts), Cluster D (Mid-Tier Digital Mainstream: 1,619 accounts).
   - PCA 2D coordinates (PC1=60.3%, PC2=30.8%) enabling intuitive cluster boundary visualization.

3. **Lifecycle Cohort × Monthly Spend Tier Matrix (4x4):**
   - Cross-tabulated Tenure Stages (New: 0-12m, Growing: 13-24m, Established: 25-48m, Veteran: 49-72m) against Monthly Spend Tiers (Budget: <$35, Moderate: $35-$65, High: $65-$90, Premium: >$90).
   - Generated heatmaps for Account Volume, Empirical Churn Rate (%), and Monthly Revenue at Risk ($k/mo).
   - Revealed that early premium accounts (New × Premium) suffer acute 68.4% churn, causing the primary financial leak.

4. **Service Ecosystem Stickiness Profiling:**
   - Quantified penetration of protective services (Tech Support, Online Security, Backup, Device Protection) across personas.
   - Identified that At-Risk High Rollers only adopt Tech Support at 12.3% and Online Security at 10.7%, versus 68.2% and 69.8% for Champions.

5. **Strategic Portfolio Bubble Matrix (LTV vs. Churn Hazard):**
   - Mapped customers across 4 strategic action zones: Platinum Vault, Urgent Intervention Zone, Stable Baseline, and Automated Recovery.

---

## Visualizations & Artifacts Generated

All artifacts were generated programmatically via `scripts/generate_customer_segmentation.py` and `scripts/build_segmentation_dashboard.py` and saved under `Reports/`:

| Artifact | Type | Description |
| :--- | :---: | :--- |
| `Reports/customer_segmentation_dashboard.html` | UI Application | Standalone interactive dashboard with live customer segment explorer, search, filters, and CSV export |
| `Reports/customer_segmentation_rfm_personas.png` | Plot (300 DPI) | Multi-panel behavioral RFM persona volume, ARPU vs Churn Rate, and MRR cash flow impact |
| `Reports/customer_segmentation_kmeans_clusters.png` | Plot (300 DPI) | Elbow curve, silhouette validation, 2D PCA cluster space scatter with centroids, and metric bars |
| `Reports/customer_segmentation_lifecycle_value_matrix.png` | Plot (300 DPI) | 4x4 heatmaps of Tenure Lifecycle Stages vs Monthly Spend Tiers |
| `Reports/customer_segmentation_service_adoption_profiles.png` | Plot (300 DPI) | Comparative bar charts of defensive security and streaming service penetration by segment |
| `Reports/customer_segmentation_ltv_risk_quadrants.png` | Plot (300 DPI) | Portfolio LTV vs Churn Hazard bubble distribution with action zones |
| `Reports/customer_segments_full.csv` | Data (7,043 rows) | Complete customer roster with persona assignments, cluster labels, and RFM scores |
| `Reports/customer_segmentation_profiles.csv` | Data | Aggregated accounts, ARPU, churn rates, and revenue loss per persona |
| `Reports/kmeans_cluster_summary.csv` | Data | K-Means cluster centroid metrics and statistical profiles |
| `Reports/compact_segments.json` | Data | Stratified customer sample for client-side web explorer |
| `Reports/customer_segmentation_report.md` | Document | Executive customer segmentation and behavioral analytics report |

---

## Operational Retention Playbooks

1. **At-Risk High Rollers (Concierge Retention Protocol - 24-Hour SLA):**
   Deploy Senior Account Managers to the 811 accounts paying ~$91/mo on month-to-month contracts. Offer a complimentary 12-month Tech Support & Online Security bundle paired with a $15/mo contract lock-in credit, securing $48.1k/mo in endangered recurring cash flow.

2. **Vulnerable Newcomers (90-Day Digital Onboarding Nurture):**
   Implement an automated 3-stage drip for early-tenure subscribers (894 accounts), offering a 60-day security trial and a $10 autopay enrollment bonus to eliminate monthly manual payment friction.

3. **Champions & VIP Loyalists (Platinum Loyalty Protection):**
   Protect the 1,405 accounts driving $131.5k/mo in revenue through priority support routing, biennial router hardware refreshes, and referral rewards.

---

## Conclusion

The Customer Segmentation & Behavioral Intelligence Suite successfully completes Week 4 Day 3 of the project. By combining unsupervised machine learning clustering with strategic behavioral personas and multi-dimensional heatmaps, retention teams possess granular, operational visibility to protect over **$91,500 monthly** ($1.1M annualized) in revenue.
