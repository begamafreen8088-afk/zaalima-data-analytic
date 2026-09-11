"""
Generate Executive Summary Analytics, High-Resolution Plots, and C-Suite Master Report
Customer Churn Prediction & Lifetime Value (LTV) Engine - Week 4 Day 4
"""

import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

# Directory Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
REPORTS_DIR = os.path.join(BASE_DIR, "Reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

# Styling Configuration for Publication-Grade Charts
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['figure.titlesize'] = 16
plt.rcParams['figure.titleweight'] = 'bold'

# Curated Executive Palette
EMERALD = '#10b981'
CRIMSON = '#ef4444'
AMBER = '#f59e0b'
ORANGE = '#f97316'
INDIGO = '#6366f1'
CYAN = '#0ea5e9'
PURPLE = '#a855f7'
DARK_SLATE = '#0f172a'
LIGHT_SLATE = '#f8fafc'
CARD_BG = '#1e293b'

print("=" * 80)
print("WEEK 4 DAY 4: EXECUTIVE SUMMARY & STRATEGIC RECOMMENDATIONS ANALYTICS")
print("=" * 80)

# 1. Load Data
scores_path = os.path.join(REPORTS_DIR, "customer_churn_risk_scores.csv")
segments_path = os.path.join(REPORTS_DIR, "customer_segments_full.csv")

if os.path.exists(segments_path):
    df = pd.read_csv(segments_path)
    print(f"Loaded segmented customer dataset: {len(df):,} records from {segments_path}")
elif os.path.exists(scores_path):
    df = pd.read_csv(scores_path)
    print(f"Loaded risk-scored customer dataset: {len(df):,} records from {scores_path}")
else:
    raise FileNotFoundError("Could not find customer_segments_full.csv or customer_churn_risk_scores.csv")

# Compute Core Vital Signs
total_customers = len(df)
total_mrr = df['MonthlyCharges'].sum()
annualized_revenue = total_mrr * 12
avg_arpu = df['MonthlyCharges'].mean()

# Calculate Empirical Churn & Expected Loss
df['Actual_Churn_Numeric'] = df['Churn'].apply(lambda x: 1 if str(x).lower() in ['yes', '1', 'true'] else 0)
empirical_churn_rate = df['Actual_Churn_Numeric'].mean() * 100

if 'Expected_Monthly_Loss' in df.columns:
    total_expected_loss_mo = df['Expected_Monthly_Loss'].sum()
elif 'Churn_Probability' in df.columns:
    df['Expected_Monthly_Loss'] = df['MonthlyCharges'] * df['Churn_Probability']
    total_expected_loss_mo = df['Expected_Monthly_Loss'].sum()
else:
    df['Expected_Monthly_Loss'] = df['MonthlyCharges'] * df['Actual_Churn_Numeric']
    total_expected_loss_mo = df['Expected_Monthly_Loss'].sum()
annualized_risk_exposure = total_expected_loss_mo * 12
risk_exposure_pct = (total_expected_loss_mo / total_mrr) * 100

print(f"Total Customer Accounts: {total_customers:,}")
print(f"Total Monthly Recurring Revenue (MRR): ${total_mrr:,.2f}")
print(f"Annualized Revenue Run-Rate: ${annualized_revenue:,.2f}")
print(f"Average ARPU: ${avg_arpu:.2f}/mo")
print(f"Empirical Churn Rate: {empirical_churn_rate:.2f}%")
print(f"Total Monthly Revenue at Risk: ${total_expected_loss_mo:,.2f} ({risk_exposure_pct:.1f}% of MRR)")
print(f"Annualized Risk Exposure: ${annualized_risk_exposure:,.2f}")

# -------------------------------------------------------------------------
# 2. Multi-Scenario Financial Impact & ROI Model
# -------------------------------------------------------------------------
scenarios = [
    {
        'Scenario': 'Conservative (15% Reduction)',
        'Churn_Reduction_Pct': 15.0,
        'Monthly_MRR_Saved': total_expected_loss_mo * 0.15,
        'Annual_ARR_Preserved': total_expected_loss_mo * 0.15 * 12,
        'Est_Monthly_Cost': 5741.67,
        'Est_Annual_Program_Cost': 68900.00,
    },
    {
        'Scenario': 'Target / Realistic (25% Reduction)',
        'Churn_Reduction_Pct': 25.0,
        'Monthly_MRR_Saved': total_expected_loss_mo * 0.25,
        'Annual_ARR_Preserved': total_expected_loss_mo * 0.25 * 12,
        'Est_Monthly_Cost': 7900.00,
        'Est_Annual_Program_Cost': 94800.00,
    },
    {
        'Scenario': 'Aggressive (35% Reduction)',
        'Churn_Reduction_Pct': 35.0,
        'Monthly_MRR_Saved': total_expected_loss_mo * 0.35,
        'Annual_ARR_Preserved': total_expected_loss_mo * 0.35 * 12,
        'Est_Monthly_Cost': 10375.00,
        'Est_Annual_Program_Cost': 124500.00,
    }
]

for s in scenarios:
    s['Net_Annual_Financial_Gain'] = s['Annual_ARR_Preserved'] - s['Est_Annual_Program_Cost']
    s['Net_ROI_Pct'] = (s['Net_Annual_Financial_Gain'] / s['Est_Annual_Program_Cost']) * 100

scenarios_df = pd.DataFrame(scenarios)
scenarios_csv_path = os.path.join(REPORTS_DIR, "executive_financial_impact_scenarios.csv")
scenarios_df.to_csv(scenarios_csv_path, index=False)
print(f"Saved financial scenarios to: {scenarios_csv_path}")

# -------------------------------------------------------------------------
# 3. Five High-Impact Strategic Pillars Summary
# -------------------------------------------------------------------------
pillars = [
    {
        'Pillar': 'Pillar 1: Concierge Retention Protocol',
        'Target_Cohort': 'At-Risk High Rollers',
        'Target_Accounts': 811,
        'Base_ARPU': 90.86,
        'Current_Risk_Loss_Mo': 48143.34,
        'Preserved_MRR_Target': 14443.00,
        'Preserved_ARR_Target': 173316.00,
        'Annual_Cost': 29196.00,
        'Net_Annual_Gain': 144120.00,
        'ROI_Pct': 493.6,
        'Owner': 'Customer Success & VIP Retention',
        'Primary_Action': 'Dedicated CSM 24-hr SLA, $15/mo renewal credit, complimentary 1-yr Tech & Security bundle'
    },
    {
        'Pillar': 'Pillar 2: 90-Day Digital Onboarding & Moat Engineering',
        'Target_Cohort': 'Vulnerable Newcomers',
        'Target_Accounts': 894,
        'Base_ARPU': 67.93,
        'Current_Risk_Loss_Mo': 43364.54,
        'Preserved_MRR_Target': 10841.14,
        'Preserved_ARR_Target': 130093.68,
        'Annual_Cost': 21456.00,
        'Net_Annual_Gain': 108637.68,
        'ROI_Pct': 506.3,
        'Owner': 'Growth Marketing & Digital Onboarding',
        'Primary_Action': '3-stage automated nurture, complimentary 60-day security trial, $10 autopay bonus'
    },
    {
        'Pillar': 'Pillar 3: Contract Commitment & Migration Architecture',
        'Target_Cohort': 'Month-to-Month High-Spend Subscribers',
        'Target_Accounts': 1850,
        'Base_ARPU': 74.99,
        'Current_Risk_Loss_Mo': 24500.00,
        'Preserved_MRR_Target': 4900.00,
        'Preserved_ARR_Target': 58800.00,
        'Annual_Cost': 18500.00,
        'Net_Annual_Gain': 40300.00,
        'ROI_Pct': 217.8,
        'Owner': 'Commercial & Pricing Strategy',
        'Primary_Action': 'Tiered annual contract discount ($10/mo discount or 2 free streaming months for 2-yr lock-in)'
    },
    {
        'Pillar': 'Pillar 4: Payment Modernization & Autopay Transition',
        'Target_Cohort': 'Electronic Check Subscribers',
        'Target_Accounts': 2365,
        'Base_ARPU': 74.05,
        'Current_Risk_Loss_Mo': 15600.00,
        'Preserved_MRR_Target': 3120.00,
        'Preserved_ARR_Target': 37440.00,
        'Annual_Cost': 14190.00,
        'Net_Annual_Gain': 23250.00,
        'ROI_Pct': 163.8,
        'Owner': 'Billing Operations & Product Experience',
        'Primary_Action': 'One-time $15 statement credit upon switching to automated Credit Card / Bank ACH billing'
    },
    {
        'Pillar': 'Pillar 5: Defensive Service Moat & Add-On Penetration',
        'Target_Cohort': 'Fiber Optic Users Lacking Security/Support',
        'Target_Accounts': 1580,
        'Base_ARPU': 88.50,
        'Current_Risk_Loss_Mo': 8000.00,
        'Preserved_MRR_Target': 1600.00,
        'Preserved_ARR_Target': 19200.00,
        'Annual_Cost': 11458.00,
        'Net_Annual_Gain': 7742.00,
        'ROI_Pct': 67.6,
        'Owner': 'Product Cross-Sell & Customer Care',
        'Primary_Action': 'Consolidated $5/mo Cyber-Defense bundle (Online Security + Tech Support), closing 27% risk gap'
    }
]

pillars_df = pd.DataFrame(pillars)
pillars_csv_path = os.path.join(REPORTS_DIR, "executive_strategic_pillars_summary.csv")
pillars_df.to_csv(pillars_csv_path, index=False)
print(f"Saved strategic pillars to: {pillars_csv_path}")

# -------------------------------------------------------------------------
# 4. Phased Implementation Roadmap Summary
# -------------------------------------------------------------------------
roadmap = [
    {
        'Phase': 'Phase 1: Immediate Crisis Intervention',
        'Timeline': 'Days 1 - 30',
        'Target_Audience': 'At-Risk High Rollers (811 accounts) & Critical Risk Tier',
        'Key_Milestones': 'Launch Concierge 24-hr outreach; Establish retention incentive approval guidelines; Implement daily risk alert feeds for CSMs.',
        'Primary_Deliverable': 'Dedicated retention hotline & Concierge contract lock-in protocol.',
        'Target_Monthly_Savings': '$14,443/mo',
        'Owner': 'Customer Success & VIP Retention'
    },
    {
        'Phase': 'Phase 2: Digital Moats & Friction Removal',
        'Timeline': 'Days 31 - 60',
        'Target_Audience': 'Vulnerable Newcomers (894 accounts) & Electronic Check users (2,365 accounts)',
        'Key_Milestones': 'Deploy 90-day automated onboarding nurture sequence; Roll out $15 Autopay migration portal; Launch $5/mo Cyber-Defense cross-sell bundle.',
        'Primary_Deliverable': 'Automated drip marketing engine & Autopay enrollment incentive workflows.',
        'Target_Monthly_Savings': '$13,961/mo',
        'Owner': 'Growth Marketing & Billing Operations'
    },
    {
        'Phase': 'Phase 3: Continuous Machine Learning & Scale',
        'Timeline': 'Days 61 - 90',
        'Target_Audience': 'Entire Portfolio (7,043 accounts) & Future Inbound Signups',
        'Key_Milestones': 'Integrate FastAPI prediction engine into production CRM/Billing; Automate weekly model drift & retraining; Deploy executive BI dashboards to executive leadership.',
        'Primary_Deliverable': 'Real-time automated scoring API & self-updating executive analytics portal.',
        'Target_Monthly_Savings': '$6,500/mo',
        'Owner': 'Data Science & Platform Engineering'
    }
]

roadmap_df = pd.DataFrame(roadmap)
roadmap_csv_path = os.path.join(REPORTS_DIR, "executive_implementation_roadmap.csv")
roadmap_df.to_csv(roadmap_csv_path, index=False)
print(f"Saved implementation roadmap to: {roadmap_csv_path}")

# -------------------------------------------------------------------------
# 5. Generate Publication-Grade Executive Plots (300 DPI)
# -------------------------------------------------------------------------

# Plot 1: Financial Impact & Multi-Scenario ROI
fig, axes = plt.subplots(1, 3, figsize=(20, 6.5))
fig.patch.set_facecolor('#ffffff')

# Subplot 1A: Preserved ARR vs Program Cost
bar_width = 0.35
scen_labels = ['Conservative\n(15% Churn Cut)', 'Target / Realistic\n(25% Churn Cut)', 'Aggressive\n(35% Churn Cut)']
x = np.arange(len(scen_labels))

ax1 = axes[0]
rects1 = ax1.bar(x - bar_width/2, scenarios_df['Annual_ARR_Preserved'] / 1000, bar_width, label='Preserved ARR ($k/yr)', color=EMERALD, edgecolor='none', alpha=0.9)
rects2 = ax1.bar(x + bar_width/2, scenarios_df['Est_Annual_Program_Cost'] / 1000, bar_width, label='Program Cost ($k/yr)', color=CRIMSON, edgecolor='none', alpha=0.85)

ax1.set_title('Annual Revenue Preserved vs. Program Cost', fontsize=13, fontweight='bold', pad=15)
ax1.set_ylabel('Annual Value ($k / year)', fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(scen_labels, fontweight='bold')
ax1.legend(loc='upper left', frameon=True)
ax1.set_ylim(0, 680)

for rect in rects1:
    h = rect.get_height()
    ax1.annotate(f'${h:.1f}k', xy=(rect.get_x() + rect.get_width() / 2, h),
                 xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', fontweight='bold', color='#065f46')

for rect in rects2:
    h = rect.get_height()
    ax1.annotate(f'${h:.1f}k', xy=(rect.get_x() + rect.get_width() / 2, h),
                 xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', fontweight='bold', color='#991b1b')

# Subplot 1B: Net Annual Financial Gain
ax2 = axes[1]
bars2 = ax2.bar(scen_labels, scenarios_df['Net_Annual_Financial_Gain'] / 1000, color=[CYAN, INDIGO, PURPLE], width=0.5, edgecolor='none')
ax2.set_title('Net Annual Financial Gain ($k / year)', fontsize=13, fontweight='bold', pad=15)
ax2.set_ylabel('Net Annual Bottom-Line Profit ($k)', fontweight='bold')
ax2.set_ylim(0, 550)

for bar in bars2:
    h = bar.get_height()
    ax2.annotate(f'+${h:.1f}k', xy=(bar.get_x() + bar.get_width() / 2, h),
                 xytext=(0, 5), textcoords="offset points", ha='center', va='bottom', fontweight='bold', fontsize=12, color=DARK_SLATE)

# Subplot 1C: Net Program ROI Multiplier
ax3 = axes[2]
bars3 = ax3.bar(scen_labels, scenarios_df['Net_ROI_Pct'], color=[AMBER, ORANGE, EMERALD], width=0.5, edgecolor='none')
ax3.set_title('Projected Net Program ROI (%)', fontsize=13, fontweight='bold', pad=15)
ax3.set_ylabel('Return on Investment (%)', fontweight='bold')
ax3.set_ylim(0, 450)

for bar in bars3:
    h = bar.get_height()
    ax3.annotate(f'{h:.1f}%\n({h/100 + 1:.1f}x Return)', xy=(bar.get_x() + bar.get_width() / 2, h),
                 xytext=(0, 5), textcoords="offset points", ha='center', va='bottom', fontweight='bold', fontsize=11, color=DARK_SLATE)

plt.suptitle('Customer Churn & LTV Engine: Executive Financial Impact & ROI Scenarios', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
roi_plot_path = os.path.join(REPORTS_DIR, "executive_financial_impact_roi.png")
plt.savefig(roi_plot_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"Generated high-res plot: {roi_plot_path}")

# Plot 2: Strategic Pillars Contribution & Roadmap
fig, (ax_p, ax_r) = plt.subplots(1, 2, figsize=(18, 6.5))
fig.patch.set_facecolor('#ffffff')

# Subplot 2A: Revenue Saved by Strategic Pillar
p_names = ['P1: Concierge\nHigh Rollers', 'P2: 90-Day\nOnboarding', 'P3: Contract\nCommitment', 'P4: Autopay\nModernization', 'P5: Security\nMoat Bundle']
p_savings = [p['Preserved_ARR_Target'] / 1000 for p in pillars]
p_colors = [CRIMSON, ORANGE, INDIGO, CYAN, EMERALD]

bars_p = ax_p.bar(p_names, p_savings, color=p_colors, width=0.55)
ax_p.set_title('Target Annual Revenue Preserved by Strategic Pillar ($k/yr)', fontsize=13, fontweight='bold', pad=15)
ax_p.set_ylabel('Preserved ARR ($k / year)', fontweight='bold')
ax_p.set_ylim(0, 200)

total_target_arr = sum(p_savings)
for bar, val in zip(bars_p, p_savings):
    pct = (val / total_target_arr) * 100
    ax_p.annotate(f'${val:.1f}k\n({pct:.1f}%)', xy=(bar.get_x() + bar.get_width() / 2, val),
                  xytext=(0, 5), textcoords="offset points", ha='center', va='bottom', fontweight='bold', fontsize=10)

# Subplot 2B: 90-Day Implementation Timeline & Cumulative Value Ramp
phases = ['Phase 1\n(Days 1-30)', 'Phase 2\n(Days 31-60)', 'Phase 3\n(Days 61-90)']
monthly_cumulative = [14.44, 14.44 + 13.96, 14.44 + 13.96 + 6.50]
annual_cumulative = [m * 12 for m in monthly_cumulative]

ax_r.plot(phases, annual_cumulative, marker='o', color=INDIGO, linewidth=3.5, markersize=10, label='Cumulative Preserved ARR ($k/yr)')
ax_r.fill_between(phases, annual_cumulative, color=INDIGO, alpha=0.15)
ax_r.set_title('90-Day Execution Timeline & Preserved Revenue Ramp-Up', fontsize=13, fontweight='bold', pad=15)
ax_r.set_ylabel('Cumulative Annualized Savings ($k/yr)', fontweight='bold')
ax_r.set_ylim(0, 480)

for i, (p, a) in enumerate(zip(phases, annual_cumulative)):
    ax_r.annotate(f'${a:.1f}k/yr\n(${monthly_cumulative[i]:.1f}k/mo)', xy=(p, a),
                  xytext=(0, 10), textcoords="offset points", ha='center', va='bottom', fontweight='bold', color=DARK_SLATE)

ax_r.grid(True, linestyle='--', alpha=0.5)

plt.suptitle('Strategic Retention Pillars: Revenue Allocation & Execution Cadence', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
roadmap_plot_path = os.path.join(REPORTS_DIR, "executive_strategic_roadmap.png")
plt.savefig(roadmap_plot_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"Generated high-res plot: {roadmap_plot_path}")

# Plot 3: Executive Scorecard & Portfolio Vital Signs
fig, axes = plt.subplots(2, 2, figsize=(16, 11))
fig.patch.set_facecolor('#ffffff')

# Subplot 3A: Churn Risk Tier Distribution
risk_tier_df = pd.read_csv(os.path.join(REPORTS_DIR, "churn_risk_tier_summary.csv"))
tier_colors = [EMERALD, AMBER, ORANGE, CRIMSON]
ax_a = axes[0, 0]
wedges, texts, autotexts = ax_a.pie(
    risk_tier_df['Accounts'],
    labels=risk_tier_df['Risk_Tier'],
    autopct='%1.1f%%',
    startangle=140,
    colors=tier_colors,
    wedgeprops={'edgecolor': 'white', 'linewidth': 2}
)
for at in autotexts:
    at.set_color('white')
    at.set_fontweight('bold')
for t in texts:
    t.set_fontweight('bold')
ax_a.set_title('Customer Base Risk Tier Breakdown (7,043 Accounts)', fontsize=13, fontweight='bold', pad=10)

# Subplot 3B: Monthly Recurring Revenue Loss Exposure by Risk Tier
ax_b = axes[0, 1]
bars_b = ax_b.bar(risk_tier_df['Risk_Tier'], risk_tier_df['Expected_Loss'] / 1000, color=tier_colors, width=0.55)
ax_b.set_title('Expected Monthly Churn Loss by Risk Tier ($k/mo)', fontsize=13, fontweight='bold', pad=10)
ax_b.set_ylabel('Expected Monthly Loss ($k/mo)', fontweight='bold')
ax_b.set_ylim(0, 60)

for bar in bars_b:
    h = bar.get_height()
    ax_b.annotate(f'${h:.1f}k', xy=(bar.get_x() + bar.get_width() / 2, h),
                  xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', fontweight='bold')

# Subplot 3C: Top Hazard Catalysts vs Defensive Moats (Net Risk %)
ax_c = axes[1, 0]
drivers_df = pd.read_csv(os.path.join(REPORTS_DIR, "churn_risk_top_drivers_summary.csv"))
top_drivers = drivers_df.sort_values(by='Risk_Increase', ascending=True).tail(6)

bars_c = ax_c.barh(top_drivers['Factor'], top_drivers['Risk_Increase'], color=CRIMSON, alpha=0.85, height=0.55)
ax_c.set_title('Top Structural Hazard Multipliers (+% Churn Probability)', fontsize=13, fontweight='bold', pad=10)
ax_c.set_xlabel('Net Risk Differential (+% Points)', fontweight='bold')
ax_c.set_xlim(0, 42)

for bar in bars_c:
    w = bar.get_width()
    ax_c.annotate(f'+{w:.1f}%', xy=(w, bar.get_y() + bar.get_height() / 2),
                  xytext=(6, 0), textcoords="offset points", ha='left', va='center', fontweight='bold', color='#991b1b')

# Subplot 3D: High-Impact Personas Expected Monthly Loss ($k/mo)
ax_d = axes[1, 1]
persona_df = pd.read_csv(os.path.join(REPORTS_DIR, "customer_segmentation_profiles.csv"))
p_sorted = persona_df.sort_values(by='Expected_Loss', ascending=True)
p_colors_d = [EMERALD, CYAN, PURPLE, INDIGO, ORANGE, CRIMSON]

bars_d = ax_d.barh(p_sorted['Persona_Segment'], p_sorted['Expected_Loss'] / 1000, color=p_colors_d, height=0.55)
ax_d.set_title('Expected Monthly Revenue Loss by Persona ($k/mo)', fontsize=13, fontweight='bold', pad=10)
ax_d.set_xlabel('Monthly Loss ($k/mo)', fontweight='bold')
ax_d.set_xlim(0, 56)

for bar in bars_d:
    w = bar.get_width()
    ax_d.annotate(f'${w:.1f}k', xy=(w, bar.get_y() + bar.get_height() / 2),
                  xytext=(6, 0), textcoords="offset points", ha='left', va='center', fontweight='bold')

plt.suptitle('Customer Portfolio Health Scorecard & Attrition Vulnerability Diagnostics', fontsize=16, fontweight='bold', y=1.01)
plt.tight_layout()
scorecard_plot_path = os.path.join(REPORTS_DIR, "executive_portfolio_scorecard.png")
plt.savefig(scorecard_plot_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"Generated high-res plot: {scorecard_plot_path}")

# -------------------------------------------------------------------------
# 6. Generate Comprehensive C-Suite Master Report (Markdown)
# -------------------------------------------------------------------------
report_md = f"""# C-Level Executive Report & Strategic Business Recommendations
## Customer Churn Prediction & Lifetime Value (LTV) Engine — Week 4 Capstone
**Reporting Date:** September 2026 | **Target Audience:** Chief Executive Officer (CEO), Chief Revenue Officer (CRO), Chief Operating Officer (COO), Chief Marketing Officer (CMO)

---

## 1. Executive Summary & C-Suite Briefing

Customer attrition is the single greatest inhibitor to enterprise growth in subscription telecom businesses. Over the past 4 weeks, the Data Science & Analytics Engineering team has designed, validated, and operationalized an enterprise-grade **Customer Churn Prediction & Lifetime Value (LTV) Engine** covering the entire **7,043-customer portfolio**.

### Portfolio Vital Signs (Baseline Diagnostic):
- **Total Customer Accounts:** 7,043 subscribers
- **Total Monthly Recurring Revenue (MRR):** ${total_mrr:,.2f}
- **Annualized Revenue Run-Rate (ARR):** ${annualized_revenue:,.2f}
- **Portfolio Baseline Churn Rate:** {empirical_churn_rate:.2f}% (1,869 accounts lost historically)
- **Total Monthly Revenue at Immediate Risk:** **${total_expected_loss_mo:,.2f} / month** ({risk_exposure_pct:.1f}% of total MRR)
- **Annualized Revenue Exposure:** **${annualized_risk_exposure:,.2f} / year**

![Portfolio Health Scorecard](executive_portfolio_scorecard.png)

### The Primary Strategic Discovery: 65.5% Loss Concentration
Rather than being uniformly distributed across the customer base, **$91,508/month (65.5%) of the company's total churn risk exposure is concentrated in just two customer segments**:
1. **At-Risk High Rollers (811 accounts | 11.5% of base):** Paying **$90.86/month**, suffering an acute **84.09% empirical churn rate**, causing **$48,143/month ($577.7k/year)** in revenue destruction.
2. **Vulnerable Newcomers (894 accounts | 12.7% of base):** Paying **$67.93/month**, suffering a **79.75% empirical churn rate**, causing **$43,365/month ($520.4k/year)** in lost cash flow.

By transitioning from indiscriminate, broad-brush discounting to **machine-learning-guided precision retention**, the company can preserve up to **$418,861/year in recurring profit** with a net program ROI exceeding **340%**.

---

## 2. Machine Learning Architecture & Analytical Synthesis

Across Weeks 1 through 4, the engineering pipeline evaluated the full lifecycle of predictive modeling, feature engineering, explainable AI, and operational scoring:

| Lifecycle Stage | Implementation & Architecture | Key Results & Benchmarks | Business Utility |
| :--- | :--- | :--- | :--- |
| **Week 1: Data Engineering** | PostgreSQL database ingestion, relational integrity constraints, clean schema normalization, and exploratory data analysis. | 7,043 validated accounts, zero schema violations, baseline retention benchmarks established. | Clean, audited single source of truth for portfolio analytics. |
| **Week 2: Churn Prediction** | Trained Logistic Regression, Random Forest, and XGBoost classifiers; SHAP explainability analysis. | **ROC-AUC: 0.846**, Accuracy: 80.4%, Recall: 79.2% on flight risks. Top drivers: Month-to-Month contracts, Online Security, and Tenure. | Real-time churn probability scoring for every customer account. |
| **Week 3: LTV Regression** | Linear Regression, Random Forest Regressor, and XGBoost Regressor with hyperparameter tuning; FastAPI prediction service. | **R² Score: 0.887**, MAE: $412.30, RMSE: $684.10. Production-ready `/predict` and `/batch_predict` REST endpoints. | Instant calculation of customer forward lifetime value and value-at-risk. |
| **Week 4 Day 1: Churn Trends** | Cohort survival analysis, contract risk trends, payment channel friction, and 2x2 value-risk quadrant analysis. | Longitudinal tenure analysis proving churn falls from **52.9% in months 0–6** down to **9.5% in months 49–72**. | Pinpointed the exact structural points of customer failure. |
| **Week 4 Day 2: Risk Cockpit** | Calibrated risk scoring into Critical (≥70%), High (45–70%), Medium (25–45%), and Low (<25%) tiers. | Critical and High tiers isolate 1,754 accounts driving **66.7% ($93.2k/mo)** of company revenue loss. | Operational tiering for frontline customer success teams. |
| **Week 4 Day 3: Segmentation** | Unsupervised K-Means clustering ($k=4$), 2D PCA projection (91.1% explained variance), and RFM behavioral personas. | Discovered 6 operational personas and isolated the **68.4% premium onboarding churn cliff**. | Customized playbooks aligned to customer behavioral typologies. |

---

## 3. Root Cause Diagnostics: The 5 Drivers of Attrition

Quantitative evaluation of feature hazard odds and risk differentials identified 5 core structural points of failure:

1. **The Contract Structure Vulnerability (+36.1% Net Risk):**
   - Subscribers on **Month-to-Month contracts suffer a 42.7% churn rate**, compared to **11.2% for 1-year contracts** and **2.8% for 2-year contracts**.
   - 3,875 customers (55.0% of the entire company) remain uncommitted on month-to-month terms, driving 88.5% of all historical churn.
2. **The Absence of Protective Service Moats (+30.7% and +30.0% Net Risk):**
   - Customers without **Online Security** suffer a **42.0% churn rate**, versus **14.6% for customers with security** (27.4% net differential).
   - Customers without **Tech Support** suffer a **41.7% churn rate**, versus **15.2% for those with tech support** (26.5% net differential).
   - Only 12.3% of At-Risk High Rollers have Tech Support. High bandwidth without support produces rapid churn.
3. **The Early-Tenure Onboarding Cliff (+30.0% Net Risk):**
   - Churn is **52.9% during the first 6 months** of customer life, tapering to 35.9% in months 7–12, and plunging below 10% after year 4.
   - For high-spend subscribers ($>90/mo), first-year churn reaches **68.4%**. If a high-value customer is not actively guided through onboarding in days 1–90, they abandon the service.
4. **Payment Channel Friction & Manual Billing (+28.8% Net Risk):**
   - Customers utilizing **Electronic Checks endure a 45.6% churn rate** (surging to **53.7%** on month-to-month plans).
   - In contrast, automated Credit Card and Bank ACH subscribers average an 11.8% churn rate. Electronic check processing friction and manual monthly billing trigger monthly cancellation decisions.
5. **Fiber Optic Infrastructure Dissatisfaction (+28.0% Net Risk):**
   - Fiber optic subscribers exhibit a **42.2% churn rate**, compared to **18.9% for standard DSL subscribers**.
   - Fiber is priced at a premium (~$80–$100/mo) but is frequently sold without defensive security or dedicated support, amplifying customer expectations and competitor vulnerability.

---

## 4. Five Actionable Strategic Recommendations

To address these failure modes, we propose **Five Actionable Strategic Pillars**, each backed by dedicated budgets, departmental ownership, SLA metrics, and quantified return on investment.

![Strategic Pillars & Roadmap](executive_strategic_roadmap.png)

### Pillar 1: Concierge Retention Protocol for At-Risk High Rollers
- **Target Audience:** 811 accounts generating ~$91/mo ARPU on month-to-month contracts ($73.7k/mo MRR | $48.1k/mo loss).
- **Executive Rationale:** This segment is responsible for **34.5% of total company churn losses**. Losing these high-ARPU subscribers severely damages cash flow and EBITDA.
- **Operational Execution:**
  - Automated webhook alerts route accounts immediately into the Senior Customer Success retention queue within 2 hours of entering the Critical/High risk threshold.
  - Mandatory **24-Hour Contact SLA** via direct phone call from a dedicated Account Specialist.
  - **Incentive Offer:** A structured $15/month contract renewal credit for 12 months, paired with a complimentary 1-year Cyber-Defense Suite (Tech Support + Online Security).
- **Financial Return (Target):**
  - Expected Churn Reduction: 30.0% retention rate.
  - **Monthly MRR Preserved:** **$14,443.00 / month**
  - **Annual ARR Preserved:** **$173,316.00 / year**
  - Annual Retention Budget: $29,196.00 (incentives + staff capacity).
  - **Net Annual Bottom-Line Profit:** **+$144,120.00 / year (493.6% Net ROI)**
- **Departmental Owner:** VP of Customer Success & Retention Operations.

### Pillar 2: 90-Day Digital Onboarding & Moat Engineering
- **Target Audience:** 894 early-tenure subscribers (<12 months) paying ~$68/mo with elevated risk ($43.4k/mo loss).
- **Executive Rationale:** Early churn is an onboarding failure. Customers paying moderate-to-high rates churn within 90 days due to configuration frustration or bill shock.
- **Operational Execution:**
  - Automated 3-stage customer onboarding drip sequence triggered upon service activation:
    - *Day 1–7:* Interactive setup confirmation, speed testing verification, and digital welcome kit.
    - *Day 14–30:* Complimentary 60-day activation of Online Security and Device Protection.
    - *Day 45–60:* Proactive check-in survey with automated routing to tier-2 support for any reported latency.
  - **First-Renewal Bridge Incentive:** A $10 statement credit for completing initial 90-day milestone and enabling autopay.
- **Financial Return (Target):**
  - Expected Churn Reduction: 25.0% retention rate.
  - **Monthly MRR Preserved:** **$10,841.14 / month**
  - **Annual ARR Preserved:** **$130,093.68 / year**
  - Annual Retention Budget: $21,456.00.
  - **Net Annual Bottom-Line Profit:** **+$108,637.68 / year (506.3% Net ROI)**
- **Departmental Owner:** Head of Growth Marketing & Digital Customer Experience.

### Pillar 3: Contract Commitment & Migration Architecture
- **Target Audience:** 3,875 Month-to-Month subscribers (42.7% baseline churn vs 11.2% for 1-year contracts).
- **Executive Rationale:** Month-to-month contracts are the #1 structural churn catalyst (+36.1% risk). Transitioning accounts into 12- or 24-month commitments provides massive structural churn insulation.
- **Operational Execution:**
  - Launch a targeted "Loyalty Rate Lock Guarantee" campaign across digital self-service portals and billing invoices.
  - **Tiered Commitment Offer:**
    - *1-Year Term:* Guaranteed $10/month discount for 12 months with complimentary router upgrade.
    - *2-Year Term:* Guaranteed $15/month discount plus 6 months free streaming add-on (Premium Tech Support).
- **Financial Return (Target):**
  - Expected Churn Reduction: 20.0% conversion of vulnerable high-spend accounts.
  - **Monthly MRR Preserved:** **$4,900.00 / month**
  - **Annual ARR Preserved:** **$58,800.00 / year**
  - Annual Program Cost: $18,500.00.
  - **Net Annual Bottom-Line Profit:** **+$40,300.00 / year (217.8% Net ROI)**
- **Departmental Owner:** Chief Revenue Officer & Director of Commercial Pricing.

### Pillar 4: Payment Modernization & Autopay Transition
- **Target Audience:** 2,365 Electronic Check users (53.7% churn on month-to-month contracts).
- **Executive Rationale:** Manual electronic check payments create monthly friction, payment failure points, and active cancellation prompts. Automated payments lower churn by 28.8 percentage points.
- **Operational Execution:**
  - Launch a company-wide "Friction-Free Autopay Migration" campaign.
  - **Incentive:** One-time **$15 instant bill credit** upon enrolling in recurring Credit Card or Bank ACH automatic billing.
  - Introduce in-app one-click payment tokenization and SMS autopay enrollment prompts.
- **Financial Return (Target):**
  - Expected Churn Reduction: 20.0% risk mitigation.
  - **Monthly MRR Preserved:** **$3,120.00 / month**
  - **Annual ARR Preserved:** **$37,440.00 / year**
  - Annual Program Cost: $14,190.00.
  - **Net Annual Bottom-Line Profit:** **+$23,250.00 / year (163.8% Net ROI)**
- **Departmental Owner:** VP of Billing Operations & Product Experience.

### Pillar 5: Defensive Service Moat & Add-On Penetration
- **Target Audience:** 1,580 Fiber Optic subscribers lacking defensive add-ons.
- **Executive Rationale:** Online Security and Tech Support lower churn by 27.2% and 26.5% respectively. Bundling these services builds competitive moats.
- **Operational Execution:**
  - Discontinue selling unbundled, unprotected high-speed Fiber Optic plans.
  - Introduce the **"Cyber-Shield Pack"**: Online Security + Tech Support + Online Backup bundled at **$5.00/month** (discounted from $10.00 à la carte).
  - Enable customer service agents with instant 1-click bundle provisioning during support interactions.
- **Financial Return (Target):**
  - Expected Churn Reduction: 20.0% risk reduction across adoption cohorts.
  - **Monthly MRR Preserved:** **$1,600.00 / month**
  - **Annual ARR Preserved:** **$19,200.00 / year**
  - Annual Program Cost: $11,458.00.
  - **Net Annual Bottom-Line Profit:** **+$7,742.00 / year (67.6% Net ROI)**
- **Departmental Owner:** VP of Product Management & Customer Care.

---

## 5. Multi-Scenario Financial Impact & ROI Model

To provide executive leadership with realistic financial planning boundaries, we modeled three performance scenarios based on total monthly revenue at risk (${total_expected_loss_mo:,.2f}/mo):

![Financial Impact and ROI](executive_financial_impact_roi.png)

### Comprehensive Scenario Matrix:

| Metric | Conservative (15% Churn Cut) | Target / Realistic (25% Churn Cut) | Aggressive (35% Churn Cut) |
| :--- | :---: | :---: | :---: |
| **Monthly MRR Saved** | **${scenarios[0]['Monthly_MRR_Saved']:,.2f} / mo** | **${scenarios[1]['Monthly_MRR_Saved']:,.2f} / mo** | **${scenarios[2]['Monthly_MRR_Saved']:,.2f} / mo** |
| **Annualized ARR Preserved** | **${scenarios[0]['Annual_ARR_Preserved']:,.2f} / yr** | **${scenarios[1]['Annual_ARR_Preserved']:,.2f} / yr** | **${scenarios[2]['Annual_ARR_Preserved']:,.2f} / yr** |
| **Annual Program Budget (Est.)** | ${scenarios[0]['Est_Annual_Program_Cost']:,.2f} / yr | ${scenarios[1]['Est_Annual_Program_Cost']:,.2f} / yr | ${scenarios[2]['Est_Annual_Program_Cost']:,.2f} / yr |
| **Net Annual Bottom-Line Profit** | **+${scenarios[0]['Net_Annual_Financial_Gain']:,.2f} / yr** | **+${scenarios[1]['Net_Annual_Financial_Gain']:,.2f} / yr** | **+${scenarios[2]['Net_Annual_Financial_Gain']:,.2f} / yr** |
| **Net Program ROI (%)** | **{scenarios[0]['Net_ROI_Pct']:.1f}%** | **{scenarios[1]['Net_ROI_Pct']:.1f}%** | **{scenarios[2]['Net_ROI_Pct']:.1f}%** |
| **Capital Return Multiplier** | **{scenarios[0]['Net_ROI_Pct']/100 + 1:.2f}x** | **{scenarios[1]['Net_ROI_Pct']/100 + 1:.2f}x** | **{scenarios[2]['Net_ROI_Pct']/100 + 1:.2f}x** |

### Executive Takeaway:
Under the **Target (Realistic) Plan**, the retention program requires an investment of **$94,800/year** across customer incentive credits, digital automation, and team capacity. In return, it recovers **$418,861/year in recurring top-line revenue**, generating a **net financial gain of $324,061/year** to the enterprise bottom line (a **341.8% net ROI**). Even in the most conservative scenario, the initiative yields **+$182,416/year** in net value.

---

## 6. Phased Operational Implementation Roadmap (90 Days)

The execution of these recommendations is organized into three 30-day sequential phases designed for rapid value realization and low operational disruption:

```mermaid
gantt
    title 90-Day Retention Implementation Roadmap
    dateFormat  YYYY-MM-DD
    section Phase 1: Crisis (D1-30)
    Concierge High Roller SLA :2026-10-01, 30d
    Critical Risk Tier Feeds    :2026-10-01, 15d
    Incentive Governance Setup  :2026-10-05, 20d
    section Phase 2: Moats (D31-60)
    90-Day Onboarding Drip      :2026-11-01, 30d
    Autopay $15 Migration       :2026-11-01, 30d
    Cyber-Shield Bundle Launch  :2026-11-15, 25d
    section Phase 3: Scale (D61-90)
    FastAPI CRM Integration     :2026-12-01, 30d
    Automated Retraining MLOps  :2026-12-10, 20d
    Executive KPI Cockpit Live  :2026-12-15, 15d
```

### Milestone Breakdown:
1. **Phase 1: Immediate Crisis Intervention (Days 1–30):**
   - *Focus:* At-Risk High Rollers (811 accounts) & Critical Risk Tier.
   - *Actions:* Establish 24-hour phone outreach SLA; provide CSMs with daily scored customer feeds; empower specialists with $15/mo retention credit authority.
   - *Target Run-Rate Savings:* **$14,443/month**.
2. **Phase 2: Digital Moats & Friction Removal (Days 31–60):**
   - *Focus:* Vulnerable Newcomers (894 accounts) & Electronic Check users (2,365 accounts).
   - *Actions:* Deploy automated 3-stage email/SMS onboarding sequence; launch $15 instant credit autopay migration campaign; activate $5/mo Cyber-Defense bundle.
   - *Cumulative Run-Rate Savings:* **$28,404/month**.
3. **Phase 3: Continuous Machine Learning & Enterprise Scale (Days 61–90):**
   - *Focus:* Entire Portfolio (7,043 accounts) & Continuous Production Scoring.
   - *Actions:* Connect FastAPI `/predict` and `/batch_predict` microservice to core billing/CRM; implement automated drift detection and monthly retraining; launch live C-Suite BI dashboard.
   - *Cumulative Target Run-Rate Savings:* **$34,905/month ($418.8k/year)**.

---

## 7. Departmental RACI & Governance Matrix

To ensure accountability, operational responsibilities are assigned across key executive stakeholders:

| Department | Executive Leader | Accountable Tasks | Key Performance Indicator (KPI) |
| :--- | :--- | :--- | :--- |
| **Customer Success** | VP Customer Success | Concierge High Roller outreach; 24-hr SLA compliance; VIP customer loyalty check-ins. | High Roller Churn Rate (target <55%); VIP accounts retained. |
| **Growth Marketing** | Chief Marketing Officer | 90-day onboarding automated drip; promotional retention messaging; autopay campaign. | Early-tenure month 1–6 churn rate (target <35%); Autopay adoption %. |
| **Billing Operations** | VP Finance / Operations | Electronic check migration portal; bill credit execution; autopay payment processing. | Electronic check user share (target reduction from 33.6% to <20%). |
| **Product Experience** | VP Product Management | Cyber-Shield service bundle creation; self-service contract renewal UX; speed diagnostics. | Defensive service adoption (Tech Support/Security penetration >45%). |
| **Data Science & ML** | Head of Data Science | FastAPI model serving; monthly model retraining; feature drift monitoring; risk calibration. | Model ROC-AUC (>0.82); Prediction latency (<150ms); Calibration error (<5%). |

---

## 8. Summary of Generated Production Artifacts

The complete analytical and operational intelligence suite is published in the repository under `Reports/`:

| Artifact | Type | Description |
| :--- | :---: | :--- |
| [`Reports/executive_summary_dashboard.html`](file:///c:/Users/shiva/OneDrive/Desktop/Customer-Churn-LTV/Reports/executive_summary_dashboard.html) | Interactive Web App | C-Suite command center with live dynamic ROI simulator, strategic pillars, and interactive roadmap |
| [`Reports/executive_financial_impact_roi.png`](file:///c:/Users/shiva/OneDrive/Desktop/Customer-Churn-LTV/Reports/executive_financial_impact_roi.png) | 300 DPI Plot | Multi-scenario financial return comparison, net gain, and ROI multipliers |
| [`Reports/executive_strategic_roadmap.png`](file:///c:/Users/shiva/OneDrive/Desktop/Customer-Churn-LTV/Reports/executive_strategic_roadmap.png) | 300 DPI Plot | Strategic pillar ARR contribution breakdown and 90-day execution value ramp |
| [`Reports/executive_portfolio_scorecard.png`](file:///c:/Users/shiva/OneDrive/Desktop/Customer-Churn-LTV/Reports/executive_portfolio_scorecard.png) | 300 DPI Plot | Executive dashboard visual summarizing vital signs, risk tiers, hazard catalysts, and personas |
| [`Reports/executive_financial_impact_scenarios.csv`](file:///c:/Users/shiva/OneDrive/Desktop/Customer-Churn-LTV/Reports/executive_financial_impact_scenarios.csv) | Summary Data | Multi-scenario model metrics (ARR preserved, program costs, net gain, ROI %) |
| [`Reports/executive_strategic_pillars_summary.csv`](file:///c:/Users/shiva/OneDrive/Desktop/Customer-Churn-LTV/Reports/executive_strategic_pillars_summary.csv) | Summary Data | Operational figures, account counts, budgets, and yields for the 5 strategic pillars |
| [`Reports/executive_implementation_roadmap.csv`](file:///c:/Users/shiva/OneDrive/Desktop/Customer-Churn-LTV/Reports/executive_implementation_roadmap.csv) | Summary Data | 90-day phased execution timeline, deliverables, targets, and departmental ownership |
| [`Reports/customer_churn_risk_scores.csv`](file:///c:/Users/shiva/OneDrive/Desktop/Customer-Churn-LTV/Reports/customer_churn_risk_scores.csv) | Scored Portfolio | Individual customer-level risk probabilities, risk tiers, and suggested actions (7,043 rows) |
| [`Reports/customer_segments_full.csv`](file:///c:/Users/shiva/OneDrive/Desktop/Customer-Churn-LTV/Reports/customer_segments_full.csv) | Master Roster | Full customer records with behavioral RFM personas and K-Means cluster assignments |
| [`scripts/generate_executive_summary.py`](file:///c:/Users/shiva/OneDrive/Desktop/Customer-Churn-LTV/scripts/generate_executive_summary.py) | Python Script | Analytical engine computing executive metrics, publication charts, and summary datasets |
| [`scripts/build_executive_dashboard.py`](file:///c:/Users/shiva/OneDrive/Desktop/Customer-Churn-LTV/scripts/build_executive_dashboard.py) | Python Script | HTML dashboard compiler with embedded ROI calculator and dynamic UI logic |

---

## 9. Conclusion & Action Required

The Customer Churn Prediction & Lifetime Value (LTV) Engine has demonstrated that customer churn is neither random nor inevitable. It is driven by identifiable structural catalysts—specifically month-to-month contracts, manual billing friction, and unbundled premium bandwidth—and is overwhelmingly concentrated in two high-spend customer cohorts.

By executing the **Target Retention Plan (25% churn reduction)**, executive leadership can immediately protect **$418,861/year in recurring revenue**, delivering a **$324,061/year net profit addition** and securing long-term customer equity.

### Recommended Next Steps for Leadership:
1. **Approve Phase 1 Budget:** Authorize the initial $25,000 allocation for the Concierge VIP retention credit pool and CSM capacity.
2. **Mandate Customer Success SLA:** Direct Customer Success leadership to enforce the 24-hour outreach SLA for the 811 At-Risk High Rollers.
3. **Greenlight Digital Journeys:** Authorize Growth Marketing and Billing Operations to begin Day 31 development of the automated 90-day onboarding sequence and Autopay migration workflows.
"""

report_path = os.path.join(REPORTS_DIR, "executive_summary_and_business_recommendations.md")
with open(report_path, 'w', encoding='utf-8') as f:
    f.write(report_md)
print(f"Generated C-Suite master report: {report_path}")
print("=" * 80)
print("EXECUTIVE SUMMARY & BUSINESS RECOMMENDATIONS SCRIPT COMPLETE!")
print("=" * 80)
