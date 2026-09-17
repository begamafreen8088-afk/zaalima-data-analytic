"""
Generate Comprehensive Churn Trend Reports
Telecom Customer Churn & Lifetime Value (LTV) Engine
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Ensure output directory exists
REPORTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

# Styling configuration for professional charts
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['figure.titlesize'] = 16
plt.rcParams['figure.titleweight'] = 'bold'

CHURN_COLOR = '#e11d48'      # Vibrant red/rose
RETAIN_COLOR = '#0ea5e9'     # Vibrant blue/cyan
ACCENT_COLOR = '#6366f1'     # Indigo
WARNING_COLOR = '#f59e0b'    # Amber
SUCCESS_COLOR = '#10b981'    # Emerald


def load_and_prepare_data():
    """Load dataset, preferring feature engineered dataset with raw fallback."""
    fe_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "telco_feature_engineered_commit3.csv")
    raw_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "WA_Fn-UseC_-Telco-Customer-Churn.csv")

    if os.path.exists(fe_path):
        print(f"Loading feature engineered dataset from: {fe_path}")
        df = pd.read_csv(fe_path)
    elif os.path.exists(raw_path):
        print(f"Loading raw dataset from: {raw_path}")
        df = pd.read_csv(raw_path)
    else:
        raise FileNotFoundError("Could not locate Telco Customer Churn dataset in data/")

    # Clean TotalCharges if needed
    if 'TotalCharges' in df.columns:
        df['TotalCharges'] = pd.to_numeric(df['TotalCharges'].astype(str).str.strip(), errors='coerce')
        df['TotalCharges'] = df['TotalCharges'].fillna(df['MonthlyCharges'] * df['tenure'])

    # Standardize Churn flag
    if 'Churn_Numeric' not in df.columns:
        df['Churn_Numeric'] = df['Churn'].map({'Yes': 1, 'No': 0, 1: 1, 0: 0}).fillna(0).astype(int)

    # Standardize Tenure cohorts if not present
    if 'Tenure_Cohort' not in df.columns:
        bins = [-1, 6, 12, 24, 48, 72]
        labels = ['0-6 Months', '7-12 Months', '13-24 Months', '25-48 Months', '49-72 Months']
        df['Tenure_Cohort'] = pd.cut(df['tenure'], bins=bins, labels=labels)

    # Standardize Monthly Charges Quintiles / Brackets
    if 'Monthly_Charges_Bracket' not in df.columns:
        bins_mc = [0, 35, 60, 80, 100, 150]
        labels_mc = ['Low (<$35)', 'Moderate ($35-$60)', 'Mid-High ($60-$80)', 'High ($80-$100)', 'Ultra High (>$100)']
        df['Monthly_Charges_Bracket'] = pd.cut(df['MonthlyCharges'], bins=bins_mc, labels=labels_mc)

    return df


def plot_tenure_cohort_trend(df):
    """Plot 1: Churn Rate and Retention Curve across Tenure Cohorts."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Cohort analysis
    cohort_stats = df.groupby('Tenure_Cohort', observed=False).agg(
        Total=('customerID', 'count'),
        Churned=('Churn_Numeric', 'sum'),
        Churn_Rate=('Churn_Numeric', 'mean'),
        Avg_Monthly_Charges=('MonthlyCharges', 'mean')
    ).reset_index()
    cohort_stats['Churn_Rate_Pct'] = cohort_stats['Churn_Rate'] * 100
    cohort_stats['Retention_Rate_Pct'] = 100 - cohort_stats['Churn_Rate_Pct']

    # Subplot 1: Bar chart of Churn Rate by Cohort
    bars = ax1.bar(cohort_stats['Tenure_Cohort'].astype(str), cohort_stats['Churn_Rate_Pct'],
                   color=[CHURN_COLOR if r > 30 else WARNING_COLOR if r > 20 else SUCCESS_COLOR
                          for r in cohort_stats['Churn_Rate_Pct']],
                   width=0.55, edgecolor='none')
    ax1.set_title('Churn Rate by Customer Tenure Cohort', pad=15)
    ax1.set_xlabel('Customer Tenure Lifecycle Cohort')
    ax1.set_ylabel('Churn Rate (%)')
    ax1.set_ylim(0, 60)
    ax1.axhline(df['Churn_Numeric'].mean() * 100, color='gray', linestyle='--', linewidth=1.5,
                label=f'Overall Baseline ({df["Churn_Numeric"].mean() * 100:.1f}%)')

    for bar in bars:
        h = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2., h + 1.2,
                 f'{h:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=11)

    ax1.legend(loc='upper right', frameon=True)
    ax1.tick_params(axis='x', rotation=15)

    # Subplot 2: Cumulative Customer Survival Curve by Month (0-72)
    tenure_curve = df.groupby('tenure').agg(
        Total=('customerID', 'count'),
        Churned=('Churn_Numeric', 'sum')
    ).reset_index()
    tenure_curve['Cum_Total'] = tenure_curve['Total'].cumsum()
    tenure_curve['Cum_Churn'] = tenure_curve['Churned'].cumsum()
    # Survival percentage estimation across months
    months = np.arange(0, 73)
    surv_pct = []
    for m in months:
        active_at_start = (df['tenure'] >= m).sum()
        churn_after_or_at = ((df['tenure'] >= m) & (df['Churn_Numeric'] == 1)).sum()
        pct = (1 - (churn_after_or_at / active_at_start)) * 100 if active_at_start > 0 else 0
        surv_pct.append(pct)

    ax2.plot(months, surv_pct, color=ACCENT_COLOR, linewidth=3, label='Retention Stability Curve')
    ax2.fill_between(months, surv_pct, 100, color=CHURN_COLOR, alpha=0.15, label='Cumulative Attrition Zone')
    ax2.fill_between(months, 0, surv_pct, color=SUCCESS_COLOR, alpha=0.15, label='Retained Base Zone')
    ax2.set_title('Customer Retention & Survival Dynamics Across Months 0–72', pad=15)
    ax2.set_xlabel('Tenure in Months')
    ax2.set_ylabel('Retention Index (%)')
    ax2.set_ylim(40, 105)
    ax2.set_xlim(0, 72)
    ax2.axvline(12, color='#f97316', linestyle=':', linewidth=2, label='Month 12 Milestone')
    ax2.axvline(24, color='#10b981', linestyle=':', linewidth=2, label='Month 24 Loyalty Threshold')
    ax2.legend(loc='lower left', frameon=True)

    plt.suptitle('TENURE LIFECYCLE & COHORT CHURN TRENDS', y=1.02, fontsize=16, fontweight='bold')
    plt.tight_layout()
    output_path = os.path.join(REPORTS_DIR, 'churn_tenure_cohort_trend.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {output_path}")

    return cohort_stats


def plot_contract_risk_trend(df):
    """Plot 2: Churn Rate across Contract Types and Tenure interaction."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Contract summary
    contract_stats = df.groupby('Contract').agg(
        Total=('customerID', 'count'),
        Churned=('Churn_Numeric', 'sum'),
        Churn_Rate=('Churn_Numeric', 'mean'),
        Monthly_Revenue=('MonthlyCharges', 'sum')
    ).reset_index()
    contract_stats['Churn_Rate_Pct'] = contract_stats['Churn_Rate'] * 100

    # Subplot 1: Contract Churn Rates
    bars = ax1.bar(contract_stats['Contract'], contract_stats['Churn_Rate_Pct'],
                   color=[CHURN_COLOR, WARNING_COLOR, SUCCESS_COLOR], width=0.5, edgecolor='none')
    ax1.set_title('Churn Rate by Contract Commitment Type', pad=15)
    ax1.set_ylabel('Churn Rate (%)')
    ax1.set_ylim(0, 50)
    for bar in bars:
        h = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., h + 1.2,
                 f'{h:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=12)

    # Annotate multiplier
    m2m_rate = contract_stats.loc[contract_stats['Contract'] == 'Month-to-month', 'Churn_Rate_Pct'].values[0]
    twoyr_rate = contract_stats.loc[contract_stats['Contract'] == 'Two year', 'Churn_Rate_Pct'].values[0]
    multiplier = m2m_rate / twoyr_rate
    ax1.text(0.5, 38, f"Month-to-Month customers are\n{multiplier:.1f}x more likely to churn\nthan 2-Year contract holders",
             ha='center', va='center', bbox=dict(boxstyle='round,pad=0.6', facecolor='#fee2e2', edgecolor='#ef4444', alpha=0.9),
             fontsize=11, fontweight='bold', color='#991b1b')

    # Subplot 2: Contract Type Churn Trend across Tenure Cohorts
    ct_tenure = df.groupby(['Tenure_Cohort', 'Contract'], observed=False)['Churn_Numeric'].mean().unstack() * 100

    for col, col_color in zip(ct_tenure.columns, [CHURN_COLOR, WARNING_COLOR, SUCCESS_COLOR]):
        ax2.plot(ct_tenure.index.astype(str), ct_tenure[col], marker='o', linewidth=2.8, markersize=8,
                 color=col_color, label=f"{col}")
        for x, y in zip(ct_tenure.index.astype(str), ct_tenure[col]):
            if not np.isnan(y):
                ax2.annotate(f"{y:.1f}%", (x, y), textcoords="offset points", xytext=(0, 8),
                             ha='center', fontsize=9, fontweight='semibold')

    ax2.set_title('Contract Type Churn Trajectory by Tenure Stage', pad=15)
    ax2.set_xlabel('Tenure Cohort')
    ax2.set_ylabel('Churn Rate (%)')
    ax2.set_ylim(0, 65)
    ax2.legend(title='Contract Duration', frameon=True)
    ax2.tick_params(axis='x', rotation=15)

    plt.suptitle('CONTRACT STRUCTURE & COMMITMENT CHURN DYNAMICS', y=1.02, fontsize=16, fontweight='bold')
    plt.tight_layout()
    output_path = os.path.join(REPORTS_DIR, 'churn_contract_risk_trend.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {output_path}")

    return contract_stats


def plot_revenue_monthly_charges_trend(df):
    """Plot 3: Revenue at Risk & Monthly Charges Distribution Trend."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Revenue by Monthly Charges Bracket
    rev_stats = df.groupby('Monthly_Charges_Bracket', observed=False).agg(
        Total_Customers=('customerID', 'count'),
        Churned_Customers=('Churn_Numeric', 'sum'),
        Churn_Rate=('Churn_Numeric', 'mean'),
        Total_MRR=('MonthlyCharges', 'sum'),
        MRR_At_Risk=('MonthlyCharges', lambda s: s[df.loc[s.index, 'Churn_Numeric'] == 1].sum())
    ).reset_index()
    rev_stats['Churn_Rate_Pct'] = rev_stats['Churn_Rate'] * 100

    # Subplot 1: Distribution of Monthly Charges for Churn vs Retained
    sns.kdeplot(data=df[df['Churn_Numeric'] == 0], x='MonthlyCharges', ax=ax1,
                fill=True, color=RETAIN_COLOR, alpha=0.3, label='Retained Customers', linewidth=2.5)
    sns.kdeplot(data=df[df['Churn_Numeric'] == 1], x='MonthlyCharges', ax=ax1,
                fill=True, color=CHURN_COLOR, alpha=0.3, label='Churned Customers', linewidth=2.5)
    ax1.set_title('Monthly Charges Distribution Density: Churn vs Retained', pad=15)
    ax1.set_xlabel('Monthly Charges ($/month)')
    ax1.set_ylabel('Customer Density')
    ax1.axvline(x=70, color='gray', linestyle=':', label='$70/mo Inflection Threshold')
    ax1.legend(loc='upper right', frameon=True)

    # Subplot 2: Monthly Recurring Revenue (MRR) Lost vs Retained by Spend Tier
    x_indices = np.arange(len(rev_stats))
    width = 0.4
    retained_mrr = (rev_stats['Total_MRR'] - rev_stats['MRR_At_Risk']) / 1000
    lost_mrr = rev_stats['MRR_At_Risk'] / 1000

    ax2.bar(x_indices - width/2, retained_mrr, width=width, label='Retained MRR ($k)', color=RETAIN_COLOR, alpha=0.9)
    bars2 = ax2.bar(x_indices + width/2, lost_mrr, width=width, label='Lost MRR ($k) [Churned]', color=CHURN_COLOR, alpha=0.9)

    ax2.set_title('Monthly Recurring Revenue (MRR) Impact by Spend Tier', pad=15)
    ax2.set_xticks(x_indices)
    ax2.set_xticklabels(rev_stats['Monthly_Charges_Bracket'].astype(str), rotation=20, ha='right')
    ax2.set_ylabel('MRR in Thousands (USD $k)')

    for bar, rate in zip(bars2, rev_stats['Churn_Rate_Pct']):
        h = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., h + 1.5,
                 f'{rate:.1f}% churn', ha='center', va='bottom', fontsize=9, fontweight='bold', color='#991b1b')

    ax2.legend(loc='upper left', frameon=True)

    plt.suptitle('FINANCIAL EXPOSURE & MONTHLY CHARGES CHURN IMPACT', y=1.02, fontsize=16, fontweight='bold')
    plt.tight_layout()
    output_path = os.path.join(REPORTS_DIR, 'churn_revenue_monthly_charges_trend.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {output_path}")

    return rev_stats


def plot_service_stickiness_trend(df):
    """Plot 4: Service ecosystem, Internet Type, and Tech Support / Security buffering."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Subplot 1: Internet Service Type Churn Rate & Customer Volume
    inet_stats = df.groupby('InternetService').agg(
        Total=('customerID', 'count'),
        Churned=('Churn_Numeric', 'sum'),
        Churn_Rate=('Churn_Numeric', 'mean'),
        Avg_Monthly_Charges=('MonthlyCharges', 'mean')
    ).reset_index()
    inet_stats['Churn_Rate_Pct'] = inet_stats['Churn_Rate'] * 100

    bars = ax1.bar(inet_stats['InternetService'], inet_stats['Churn_Rate_Pct'],
                   color=[RETAIN_COLOR, CHURN_COLOR, SUCCESS_COLOR], width=0.45)
    ax1.set_title('Churn Rate by Internet Service Architecture', pad=15)
    ax1.set_ylabel('Churn Rate (%)')
    ax1.set_ylim(0, 50)
    for bar, charge in zip(bars, inet_stats['Avg_Monthly_Charges']):
        h = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., h + 1.2,
                 f'{h:.1f}%\n(avg ${charge:.1f}/mo)', ha='center', va='bottom', fontweight='bold', fontsize=10)

    ax1.text(1, 44, "Fiber Optic Churn Hazard:\nHigh price + service issues drive 41.9% churn",
             ha='center', va='center', bbox=dict(boxstyle='square,pad=0.5', facecolor='#fee2e2', edgecolor='#ef4444'),
             fontsize=9.5, fontweight='bold', color='#991b1b')

    # Subplot 2: Protective buffering of Security & Tech Support services
    support_services = ['OnlineSecurity', 'TechSupport', 'OnlineBackup', 'DeviceProtection']
    service_comparison = []

    for s in support_services:
        if s in df.columns:
            has_service = df[df[s] == 'Yes']['Churn_Numeric'].mean() * 100
            no_service = df[df[s] == 'No']['Churn_Numeric'].mean() * 100
            diff = no_service - has_service
            service_comparison.append({
                'Service': s,
                'Has_Service_Churn': has_service,
                'No_Service_Churn': no_service,
                'Churn_Reduction': diff
            })

    sc_df = pd.DataFrame(service_comparison)
    x = np.arange(len(sc_df))
    w = 0.35

    ax2.bar(x - w/2, sc_df['No_Service_Churn'], width=w, label='Without Service', color=CHURN_COLOR, alpha=0.85)
    ax2.bar(x + w/2, sc_df['Has_Service_Churn'], width=w, label='With Service (Protected)', color=SUCCESS_COLOR, alpha=0.85)

    ax2.set_title('Protective "Stickiness" Effect of Value-Added Services', pad=15)
    ax2.set_xticks(x)
    ax2.set_xticklabels([s.replace('Online', 'Online ').replace('Protection', ' Protection') for s in sc_df['Service']])
    ax2.set_ylabel('Churn Rate (%)')
    ax2.set_ylim(0, 50)
    ax2.legend(loc='upper right', frameon=True)

    for i, row in sc_df.iterrows():
        ax2.annotate(f"-{row['Churn_Reduction']:.1f}%",
                     (x[i], max(row['No_Service_Churn'], row['Has_Service_Churn']) + 2.5),
                     ha='center', fontweight='bold', color='#047857', fontsize=10)

    plt.suptitle('SERVICE ECOSYSTEM & PRODUCT STICKINESS ANALYSIS', y=1.02, fontsize=16, fontweight='bold')
    plt.tight_layout()
    output_path = os.path.join(REPORTS_DIR, 'churn_service_stickiness_trend.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {output_path}")

    return inet_stats, sc_df


def plot_payment_billing_trend(df):
    """Plot 5: Payment method friction, billing method, and churn rates."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Payment Method Stats
    pm_stats = df.groupby('PaymentMethod').agg(
        Total=('customerID', 'count'),
        Churned=('Churn_Numeric', 'sum'),
        Churn_Rate=('Churn_Numeric', 'mean'),
        Monthly_Revenue=('MonthlyCharges', 'sum')
    ).reset_index()
    pm_stats['Churn_Rate_Pct'] = pm_stats['Churn_Rate'] * 100
    pm_stats = pm_stats.sort_values('Churn_Rate_Pct', ascending=False)

    colors = [CHURN_COLOR if 'Electronic' in pm else RETAIN_COLOR for pm in pm_stats['PaymentMethod']]
    bars = ax1.barh(pm_stats['PaymentMethod'], pm_stats['Churn_Rate_Pct'], color=colors, height=0.55)
    ax1.set_title('Churn Rate by Customer Payment Method', pad=15)
    ax1.set_xlabel('Churn Rate (%)')
    ax1.set_xlim(0, 55)

    for bar in bars:
        w = bar.get_width()
        ax1.text(w + 1.0, bar.get_y() + bar.get_height()/2.,
                 f'{w:.1f}%', ha='left', va='center', fontweight='bold', fontsize=11)

    ax1.axvline(df['Churn_Numeric'].mean() * 100, color='gray', linestyle='--', label='Baseline Churn Rate')
    ax1.legend(loc='lower right', frameon=True)

    # Subplot 2: Paperless Billing vs Payment Method matrix
    pb_pm = df.groupby(['PaymentMethod', 'PaperlessBilling'])['Churn_Numeric'].mean().unstack() * 100
    pb_pm = pb_pm.loc[pm_stats['PaymentMethod']]  # keep order

    x = np.arange(len(pb_pm))
    width = 0.35

    ax2.bar(x - width/2, pb_pm['No'], width=width, label='Standard Paper Bill', color='#64748b')
    ax2.bar(x + width/2, pb_pm['Yes'], width=width, label='Paperless Billing', color='#f43f5e')

    ax2.set_title('Interaction: Payment Method x Paperless Billing', pad=15)
    ax2.set_xticks(x)
    short_labels = ['Electronic Check', 'Mailed Check', 'Bank Transfer (Auto)', 'Credit Card (Auto)']
    ax2.set_xticklabels(short_labels, rotation=15, ha='right')
    ax2.set_ylabel('Churn Rate (%)')
    ax2.set_ylim(0, 60)
    ax2.legend(loc='upper right', frameon=True)

    plt.suptitle('BILLING CHANNELS & PAYMENT FRICTION CHURN TRENDS', y=1.02, fontsize=16, fontweight='bold')
    plt.tight_layout()
    output_path = os.path.join(REPORTS_DIR, 'churn_payment_billing_trend.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {output_path}")

    return pm_stats


def plot_risk_segmentation_matrix(df):
    """Plot 6: 2x2 Risk Segmentation Matrix (Value vs Risk)."""
    fig, ax = plt.subplots(figsize=(10, 8))

    # Calculate median tenure and monthly charges to construct 4 quadrants
    median_charges = df['MonthlyCharges'].median()
    median_tenure = df['tenure'].median()

    # Define segments
    def assign_quadrant(row):
        high_val = row['MonthlyCharges'] >= median_charges
        high_risk = row['tenure'] < median_tenure or row['Contract'] == 'Month-to-month'
        if high_val and high_risk:
            return 'Immediate Intervention\n(High Spend, High Risk)'
        elif high_val and not high_risk:
            return 'Core VIPs\n(High Spend, Low Risk)'
        elif not high_val and high_risk:
            return 'High Churn / Low ARPU\n(Low Spend, High Risk)'
        else:
            return 'Stable Low Maintenance\n(Low Spend, Low Risk)'

    df['Risk_Quadrant'] = df.apply(assign_quadrant, axis=1)

    quad_stats = df.groupby('Risk_Quadrant').agg(
        Customers=('customerID', 'count'),
        Churn_Rate=('Churn_Numeric', 'mean'),
        Monthly_Revenue=('MonthlyCharges', 'sum'),
        Avg_Monthly_Charge=('MonthlyCharges', 'mean')
    ).reset_index()
    quad_stats['Churn_Rate_Pct'] = quad_stats['Churn_Rate'] * 100
    quad_stats['Lost_Monthly_Rev'] = quad_stats['Monthly_Revenue'] * quad_stats['Churn_Rate']

    # Scatter plot sample of customers for visual representation
    sample_df = df.sample(min(1200, len(df)), random_state=42)
    colors = {
        'Immediate Intervention\n(High Spend, High Risk)': '#ef4444',
        'Core VIPs\n(High Spend, Low Risk)': '#10b981',
        'High Churn / Low ARPU\n(Low Spend, High Risk)': '#f59e0b',
        'Stable Low Maintenance\n(Low Spend, Low Risk)': '#6366f1'
    }

    for quad, group in sample_df.groupby('Risk_Quadrant'):
        ax.scatter(group['tenure'], group['MonthlyCharges'],
                   c=colors.get(quad, '#94a3b8'), label=quad.replace('\n', ' - '),
                   alpha=0.45, s=35, edgecolors='none')

    ax.axvline(median_tenure, color='#475569', linestyle='--', linewidth=1.5, alpha=0.7)
    ax.axhline(median_charges, color='#475569', linestyle='--', linewidth=1.5, alpha=0.7)

    ax.set_title('CUSTOMER RETENTION SEGMENTATION MATRIX', pad=15)
    ax.set_xlabel('Customer Tenure (Months) → Indicator of Loyalty & Stability')
    ax.set_ylabel('Monthly Charges ($/month) → Indicator of Revenue Contribution')

    # Quadrant annotations with summary statistics
    for _, row in quad_stats.iterrows():
        q_name = row['Risk_Quadrant']
        c_count = row['Customers']
        c_rate = row['Churn_Rate_Pct']
        rev_lost = row['Lost_Monthly_Rev']

        if 'Immediate Intervention' in q_name:
            x_pos, y_pos = 12, 112
        elif 'Core VIPs' in q_name:
            x_pos, y_pos = 52, 112
        elif 'High Churn' in q_name:
            x_pos, y_pos = 12, 25
        else:
            x_pos, y_pos = 52, 25

        ax.text(x_pos, y_pos,
                f"{q_name.splitlines()[0]}\n{c_count:,} users | {c_rate:.1f}% Churn\nLoss: ${rev_lost:,.0f}/mo",
                ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='#cbd5e1', alpha=0.92),
                fontweight='bold', fontsize=9.5)

    ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.22), ncol=2, frameon=True)
    plt.tight_layout()
    output_path = os.path.join(REPORTS_DIR, 'churn_risk_segmentation_matrix.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {output_path}")

    return quad_stats


def export_summary_csvs(df, cohort_stats, contract_stats, rev_stats, inet_stats, sc_df, pm_stats, quad_stats):
    """Export summary tables to CSV files for tabular and spreadsheet analysis."""

    # 1. Tenure Cohort Summary
    cohort_csv = os.path.join(REPORTS_DIR, 'tenure_cohort_churn_summary.csv')
    cohort_stats.to_csv(cohort_csv, index=False)
    print(f"Exported: {cohort_csv}")

    # 2. Contract & Payment Method Summary
    cp_merged = df.groupby(['Contract', 'PaymentMethod']).agg(
        Total_Customers=('customerID', 'count'),
        Churned_Customers=('Churn_Numeric', 'sum'),
        Churn_Rate_Pct=('Churn_Numeric', lambda s: round(s.mean() * 100, 2)),
        Avg_MonthlyCharges=('MonthlyCharges', lambda s: round(s.mean(), 2)),
        Total_MRR=('MonthlyCharges', lambda s: round(s.sum(), 2))
    ).reset_index()
    cp_csv = os.path.join(REPORTS_DIR, 'contract_payment_churn_summary.csv')
    cp_merged.to_csv(cp_csv, index=False)
    print(f"Exported: {cp_csv}")

    # 3. Service Adoption Summary
    sc_csv = os.path.join(REPORTS_DIR, 'service_adoption_churn_summary.csv')
    sc_df.to_csv(sc_csv, index=False)
    print(f"Exported: {sc_csv}")

    # 4. Revenue at Risk Summary
    rev_csv = os.path.join(REPORTS_DIR, 'revenue_at_risk_summary.csv')
    rev_stats.to_csv(rev_csv, index=False)
    print(f"Exported: {rev_csv}")


def main():
    print("=" * 60)
    print("Starting Churn Trend Reporting Pipeline...")
    print("=" * 60)

    df = load_and_prepare_data()
    print(f"Successfully prepared dataset with {len(df):,} customer records.")

    overall_churn = df['Churn_Numeric'].mean() * 100
    total_mrr = df['MonthlyCharges'].sum()
    churn_mrr = df.loc[df['Churn_Numeric'] == 1, 'MonthlyCharges'].sum()
    print(f"Overall Churn Rate: {overall_churn:.2f}%")
    print(f"Total Portfolio MRR: ${total_mrr:,.2f}")
    print(f"Total MRR Lost to Churn: ${churn_mrr:,.2f} ({churn_mrr/total_mrr*100:.2f}% of portfolio)")

    print("\n[1/6] Generating Tenure Cohort Trend Chart...")
    cohort_stats = plot_tenure_cohort_trend(df)

    print("[2/6] Generating Contract Structure Trend Chart...")
    contract_stats = plot_contract_risk_trend(df)

    print("[3/6] Generating Revenue & Monthly Charges Trend Chart...")
    rev_stats = plot_revenue_monthly_charges_trend(df)

    print("[4/6] Generating Service Ecosystem & Stickiness Chart...")
    inet_stats, sc_df = plot_service_stickiness_trend(df)

    print("[5/6] Generating Payment & Billing Method Trend Chart...")
    pm_stats = plot_payment_billing_trend(df)

    print("[6/6] Generating Customer Risk Segmentation Matrix...")
    quad_stats = plot_risk_segmentation_matrix(df)

    print("\nExporting structured CSV reports...")
    export_summary_csvs(df, cohort_stats, contract_stats, rev_stats, inet_stats, sc_df, pm_stats, quad_stats)

    print("\nAll Churn Trend Visualizations and Summaries successfully created in Reports/!")
    print("=" * 60)


if __name__ == '__main__':
    main()
