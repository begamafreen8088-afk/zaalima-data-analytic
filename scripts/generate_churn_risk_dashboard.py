"""
Generate Comprehensive Churn Risk Diagnostics, Visualizations & Data Assets
Customer Churn Prediction & Lifetime Value (LTV) Engine - Week 4 Day 2
"""

import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import joblib

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
REPORTS_DIR = os.path.join(BASE_DIR, "Reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

# Styling configuration for professional executive-grade charts
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['figure.titlesize'] = 16
plt.rcParams['figure.titleweight'] = 'bold'

CRITICAL_COLOR = '#ef4444'   # Crimson red
HIGH_COLOR = '#f97316'       # Vivid orange
MEDIUM_COLOR = '#f59e0b'     # Amber
LOW_COLOR = '#10b981'        # Emerald green
ACCENT_BLUE = '#0ea5e9'      # Sky blue
ACCENT_INDIGO = '#6366f1'    # Indigo
BG_DARK = '#0f172a'


def load_data_and_models():
    """Load feature engineered customer dataset and trained ML models."""
    fe_path = os.path.join(DATA_DIR, "telco_feature_engineered_commit3.csv")
    raw_path = os.path.join(DATA_DIR, "WA_Fn-UseC_-Telco-Customer-Churn.csv")

    if os.path.exists(fe_path):
        print(f"Loading feature-engineered dataset: {fe_path}")
        df = pd.read_csv(fe_path)
    elif os.path.exists(raw_path):
        print(f"Loading raw dataset: {raw_path}")
        df = pd.read_csv(raw_path)
    else:
        raise FileNotFoundError("Customer dataset could not be found.")

    # Load preprocessor & logistic regression classifier
    prep_path = os.path.join(DATA_DIR, "logistic_regression_preprocessor.pkl")
    clf_path = os.path.join(DATA_DIR, "logistic_regression_model.pkl")

    if os.path.exists(prep_path) and os.path.exists(clf_path):
        print("Loading trained Logistic Regression preprocessor and model...")
        preprocessor = joblib.load(prep_path)
        classifier = joblib.load(clf_path)
        X_trans = preprocessor.transform(df)
        churn_probs = classifier.predict_proba(X_trans)[:, 1]
    else:
        print("Warning: Model pickles not found, applying heuristic baseline risk scoring.")
        m2m = (df['Contract'] == 'Month-to-month').astype(float) * 1.8
        fiber = (df['InternetService'] == 'Fiber optic').astype(float) * 0.9
        no_tech = (df['TechSupport'] == 'No').astype(float) * 0.8
        e_check = (df['PaymentMethod'] == 'Electronic check').astype(float) * 0.7
        tenure_factor = -0.04 * df['tenure']
        z = -1.2 + m2m + fiber + no_tech + e_check + tenure_factor
        churn_probs = 1 / (1 + np.exp(-z))

    # Clean TotalCharges numeric for downstream calculations
    if 'TotalCharges' in df.columns:
        df['TotalCharges'] = pd.to_numeric(df['TotalCharges'].astype(str).str.strip(), errors='coerce')
        df['TotalCharges'] = df['TotalCharges'].fillna(df['MonthlyCharges'] * df['tenure'])

    # Standardize binary churn
    if 'Churn_Numeric' not in df.columns:
        df['Churn_Numeric'] = df['Churn'].map({'Yes': 1, 'No': 0, 1: 1, 0: 0}).fillna(0).astype(int)

    df['Churn_Probability'] = np.round(churn_probs, 4)
    df['Churn_Risk_Score'] = np.round(churn_probs * 100, 1)

    # Load LTV model
    ltv_model_path = os.path.join(DATA_DIR, "best_ltv_model.pkl")
    ltv_data_path = os.path.join(DATA_DIR, "ltv_prepared_dataset.csv")

    if os.path.exists(ltv_model_path) and os.path.exists(ltv_data_path):
        try:
            print("Loading trained Random Forest LTV regression model...")
            ltv_model = joblib.load(ltv_model_path)
            df_ltv = pd.read_csv(ltv_data_path)
            X_ltv = df_ltv.drop(columns=['LTV'], errors='ignore')
            predicted_ltv = ltv_model.predict(X_ltv)
            df['Predicted_LTV'] = np.round(predicted_ltv, 2)
        except Exception as e:
            print(f"Notice: LTV prediction fallback: {e}")
            df['Predicted_LTV'] = np.round(df['MonthlyCharges'] * np.maximum(df['tenure'], 12), 2)
    else:
        df['Predicted_LTV'] = np.round(df['MonthlyCharges'] * np.maximum(df['tenure'], 12), 2)

    # Assign Churn Risk Tiers
    # Critical: >= 70% | High: 45-70% | Medium: 25-45% | Low: < 25%
    def get_risk_tier(prob):
        if prob >= 0.70:
            return 'Critical Risk'
        elif prob >= 0.45:
            return 'High Risk'
        elif prob >= 0.25:
            return 'Medium Risk'
        else:
            return 'Low Risk'

    df['Risk_Tier'] = df['Churn_Probability'].apply(get_risk_tier)

    # Calculate financial exposures
    df['Expected_Monthly_Loss'] = np.round(df['MonthlyCharges'] * df['Churn_Probability'], 2)
    df['Expected_LTV_Loss'] = np.round(df['Predicted_LTV'] * df['Churn_Probability'], 2)

    # 2x2 Value vs Risk Quadrant
    median_charges = df['MonthlyCharges'].median()
    df['Value_Segment'] = np.where(df['MonthlyCharges'] >= median_charges, 'High Value', 'Standard Value')
    df['Risk_Category'] = np.where(df['Churn_Probability'] >= 0.45, 'Elevated Risk', 'Stable')

    def assign_action_quadrant(row):
        val = row['Value_Segment']
        risk = row['Risk_Category']
        if val == 'High Value' and risk == 'Elevated Risk':
            return 'Immediate Intervention'
        elif val == 'High Value' and risk == 'Stable':
            return 'Core VIP Protect'
        elif val == 'Standard Value' and risk == 'Elevated Risk':
            return 'Automated Nurture'
        else:
            return 'Low Maintenance'

    df['Action_Quadrant'] = df.apply(assign_action_quadrant, axis=1)

    # Prescriptive Action Recommendation
    def assign_recommended_action(row):
        quad = row['Action_Quadrant']
        contract = row.get('Contract', '')
        pm = row.get('PaymentMethod', '')
        tech = row.get('TechSupport', '')
        inet = row.get('InternetService', '')

        if quad == 'Immediate Intervention':
            if contract == 'Month-to-month' and inet == 'Fiber optic':
                return 'VIP Concierge: 12-mo Contract + Free Tech Support Bundle'
            elif pm == 'Electronic check':
                return 'Account Exec Call: Autopay Migration + $15 Credit'
            else:
                return 'Dedicated Retention Outreach + 15% Annual Discount'
        elif quad == 'Automated Nurture':
            if contract == 'Month-to-month':
                return 'Digital Drip: $5/mo Contract Lock-In Offer'
            elif tech == 'No':
                return 'In-App Offer: 60-Day Tech Support Trial'
            else:
                return 'Automated Re-engagement & Onboarding Check-in'
        elif quad == 'Core VIP Protect':
            return 'Loyalty Perks: Speed Boost & Exclusive Support Line'
        else:
            return 'Standard Account Care & Feature Discovery'

    df['Recommended_Action'] = df.apply(assign_recommended_action, axis=1)

    return df


def plot_churn_risk_distribution(df):
    """Plot 1: Churn Risk Probability Distribution & Calibrated Tiers."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Subplot 1: Distribution Histogram + KDE
    sns.histplot(df['Churn_Probability'] * 100, bins=35, kde=True, ax=ax1,
                 color=ACCENT_INDIGO, edgecolor='white', alpha=0.65)
    ax1.axvline(25, color=MEDIUM_COLOR, linestyle='--', linewidth=2, label='Medium Risk Threshold (25%)')
    ax1.axvline(45, color=HIGH_COLOR, linestyle='--', linewidth=2, label='High Risk Threshold (45%)')
    ax1.axvline(70, color=CRITICAL_COLOR, linestyle='--', linewidth=2.5, label='Critical Threshold (70%)')

    mean_prob = df['Churn_Probability'].mean() * 100
    ax1.axvline(mean_prob, color='#38bdf8', linestyle='-', linewidth=2, label=f'Portfolio Mean ({mean_prob:.1f}%)')

    ax1.set_title('Churn Risk Probability Score Distribution', pad=15)
    ax1.set_xlabel('Predicted Churn Risk Probability (%)')
    ax1.set_ylabel('Number of Customer Accounts')
    ax1.set_xlim(0, 100)
    ax1.legend(loc='upper right', frameon=True, facecolor='white', framealpha=0.95)

    # Subplot 2: Breakdown by Risk Tier
    tier_order = ['Low Risk', 'Medium Risk', 'High Risk', 'Critical Risk']
    tier_stats = df.groupby('Risk_Tier').agg(
        Accounts=('customerID', 'count'),
        Avg_Prob=('Churn_Probability', lambda s: round(s.mean() * 100, 1)),
        Actual_Churn=('Churn_Numeric', lambda s: round(s.mean() * 100, 1)),
        Total_MRR=('MonthlyCharges', 'sum'),
        Expected_Loss=('Expected_Monthly_Loss', 'sum')
    ).reindex(tier_order).reset_index()

    tier_stats['Pct_Base'] = (tier_stats['Accounts'] / len(df)) * 100
    colors = [LOW_COLOR, MEDIUM_COLOR, HIGH_COLOR, CRITICAL_COLOR]

    bars = ax2.bar(tier_stats['Risk_Tier'], tier_stats['Accounts'], color=colors, width=0.55, edgecolor='none')
    ax2.set_title('Customer Distribution Across Calibrated Risk Tiers', pad=15)
    ax2.set_xlabel('Calibrated Churn Risk Tier')
    ax2.set_ylabel('Account Volume')
    ax2.set_ylim(0, max(tier_stats['Accounts']) * 1.25)

    for bar, (_, row) in zip(bars, tier_stats.iterrows()):
        h = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width() / 2., h + 35,
                 f"{row['Accounts']:,} accts\n({row['Pct_Base']:.1f}%)\nActual: {row['Actual_Churn']:.1f}%",
                 ha='center', va='bottom', fontsize=9.5, fontweight='bold')

    plt.suptitle('PORTFOLIO CHURN RISK PROBABILITY & TIER CALIBRATION', y=1.02, fontsize=16, fontweight='bold')
    plt.tight_layout()

    out_path = os.path.join(REPORTS_DIR, 'churn_risk_distribution.png')
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_path}")
    return tier_stats


def plot_churn_risk_drivers(df):
    """Plot 2: Top Hazard Factors and Protective Feature Impacts on Churn Risk."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6.5))

    # 1. Feature Odds Multipliers / Risk Impact
    risk_factors = [
        ('Month-to-Month Contract', df[df['Contract'] == 'Month-to-month']['Churn_Probability'].mean() * 100,
         df[df['Contract'] != 'Month-to-month']['Churn_Probability'].mean() * 100),
        ('Electronic Check Payment', df[df['PaymentMethod'] == 'Electronic check']['Churn_Probability'].mean() * 100,
         df[df['PaymentMethod'] != 'Electronic check']['Churn_Probability'].mean() * 100),
        ('Fiber Optic Internet', df[df['InternetService'] == 'Fiber optic']['Churn_Probability'].mean() * 100,
         df[df['InternetService'] != 'Fiber optic']['Churn_Probability'].mean() * 100),
        ('Tenure < 6 Months', df[df['tenure'] <= 6]['Churn_Probability'].mean() * 100,
         df[df['tenure'] > 6]['Churn_Probability'].mean() * 100),
        ('No Tech Support', df[df['TechSupport'] == 'No']['Churn_Probability'].mean() * 100,
         df[df['TechSupport'] != 'No']['Churn_Probability'].mean() * 100),
        ('No Online Security', df[df['OnlineSecurity'] == 'No']['Churn_Probability'].mean() * 100,
         df[df['OnlineSecurity'] != 'No']['Churn_Probability'].mean() * 100),
        ('Paperless Billing', df[df['PaperlessBilling'] == 'Yes']['Churn_Probability'].mean() * 100,
         df[df['PaperlessBilling'] != 'Yes']['Churn_Probability'].mean() * 100),
        ('Senior Citizen', df[df['SeniorCitizen'] == 1]['Churn_Probability'].mean() * 100,
         df[df['SeniorCitizen'] == 0]['Churn_Probability'].mean() * 100),
    ]

    factor_df = pd.DataFrame(risk_factors, columns=['Factor', 'With_Factor', 'Without_Factor'])
    factor_df['Risk_Increase'] = factor_df['With_Factor'] - factor_df['Without_Factor']
    factor_df = factor_df.sort_values('Risk_Increase', ascending=True)

    bars1 = ax1.barh(factor_df['Factor'], factor_df['Risk_Increase'],
                     color=[CRITICAL_COLOR if x > 20 else HIGH_COLOR if x > 10 else ACCENT_BLUE for x in factor_df['Risk_Increase']],
                     height=0.6)
    ax1.set_title('Top Churn Risk Drivers (Hazard Differential)', pad=15)
    ax1.set_xlabel('Net Increase in Churn Risk Probability (+%)')
    ax1.set_xlim(0, max(factor_df['Risk_Increase']) * 1.25)

    for bar in bars1:
        w = bar.get_width()
        ax1.text(w + 0.8, bar.get_y() + bar.get_height() / 2.,
                 f"+{w:.1f}%", va='center', ha='left', fontsize=9.5, fontweight='bold')

    # 2. Protective Service Buffers (Risk Reducers)
    protective_factors = [
        ('Two-Year Contract', df[df['Contract'] == 'Two year']['Churn_Probability'].mean() * 100,
         df['Churn_Probability'].mean() * 100),
        ('One-Year Contract', df[df['Contract'] == 'One year']['Churn_Probability'].mean() * 100,
         df['Churn_Probability'].mean() * 100),
        ('Has Online Security', df[df['OnlineSecurity'] == 'Yes']['Churn_Probability'].mean() * 100,
         df['Churn_Probability'].mean() * 100),
        ('Has Tech Support', df[df['TechSupport'] == 'Yes']['Churn_Probability'].mean() * 100,
         df['Churn_Probability'].mean() * 100),
        ('Tenure > 24 Months', df[df['tenure'] > 24]['Churn_Probability'].mean() * 100,
         df['Churn_Probability'].mean() * 100),
        ('Credit Card Autopay', df[df['PaymentMethod'] == 'Credit card (automatic)']['Churn_Probability'].mean() * 100,
         df['Churn_Probability'].mean() * 100),
    ]

    prot_df = pd.DataFrame(protective_factors, columns=['Service', 'Cohort_Risk', 'Baseline'])
    prot_df['Risk_Reduction'] = prot_df['Baseline'] - prot_df['Cohort_Risk']
    prot_df = prot_df.sort_values('Risk_Reduction', ascending=True)

    bars2 = ax2.barh(prot_df['Service'], prot_df['Risk_Reduction'], color=LOW_COLOR, height=0.6)
    ax2.set_title('Protective Moats & Retention Buffers (Risk Reducers)', pad=15)
    ax2.set_xlabel('Net Reduction vs Portfolio Baseline (-%)')
    ax2.set_xlim(0, max(prot_df['Risk_Reduction']) * 1.25)

    for bar in bars2:
        w = bar.get_width()
        ax2.text(w + 0.5, bar.get_y() + bar.get_height() / 2.,
                 f"-{w:.1f}%", va='center', ha='left', fontsize=9.5, fontweight='bold', color='#065f46')

    plt.suptitle('CHURN RISK DRIVERS & RETENTION MOAT QUANTIFICATION', y=1.02, fontsize=16, fontweight='bold')
    plt.tight_layout()

    out_path = os.path.join(REPORTS_DIR, 'churn_risk_drivers_importance.png')
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_path}")
    return factor_df


def plot_churn_risk_revenue_exposure(df):
    """Plot 3: Monthly Recurring Revenue (MRR) & LTV Exposure by Risk Tier."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    tier_order = ['Low Risk', 'Medium Risk', 'High Risk', 'Critical Risk']
    mrr_stats = df.groupby('Risk_Tier').agg(
        Total_MRR=('MonthlyCharges', 'sum'),
        Expected_Loss_MRR=('Expected_Monthly_Loss', 'sum'),
        Total_LTV=('Predicted_LTV', 'sum'),
        Expected_Loss_LTV=('Expected_LTV_Loss', 'sum')
    ).reindex(tier_order).reset_index()

    colors = [LOW_COLOR, MEDIUM_COLOR, HIGH_COLOR, CRITICAL_COLOR]

    # Subplot 1: MRR At Risk Stacked
    x = np.arange(len(tier_order))
    width = 0.5

    bars1 = ax1.bar(x, mrr_stats['Total_MRR'] / 1000, width, label='Total Segment MRR', color='#cbd5e1', edgecolor='none')
    bars2 = ax1.bar(x, mrr_stats['Expected_Loss_MRR'] / 1000, width, label='Expected MRR At Risk', color=colors, edgecolor='none')

    ax1.set_title('Monthly Recurring Revenue (MRR) Exposure by Risk Tier', pad=15)
    ax1.set_xticks(x)
    ax1.set_xticklabels(tier_order)
    ax1.set_ylabel('MRR ($ in Thousands)')
    ax1.set_ylim(0, max(mrr_stats['Total_MRR'] / 1000) * 1.25)
    ax1.legend(loc='upper right', frameon=True)

    for i, row in mrr_stats.iterrows():
        total_k = row['Total_MRR'] / 1000
        loss_k = row['Expected_Loss_MRR'] / 1000
        pct = (row['Expected_Loss_MRR'] / row['Total_MRR']) * 100
        ax1.text(i, total_k + 4, f"Total: ${total_k:.1f}k\nAt Risk: ${loss_k:.1f}k ({pct:.0f}%)",
                 ha='center', va='bottom', fontsize=9, fontweight='bold')

    # Subplot 2: Expected LTV Loss by Risk Tier
    bars_ltv = ax2.bar(tier_order, mrr_stats['Expected_Loss_LTV'] / 1e6, color=colors, width=0.55, edgecolor='none')
    ax2.set_title('Projected Customer Lifetime Value (LTV) Exposure', pad=15)
    ax2.set_ylabel('Expected LTV Loss ($ Millions)')
    ax2.set_ylim(0, max(mrr_stats['Expected_Loss_LTV'] / 1e6) * 1.3)

    for bar, val in zip(bars_ltv, mrr_stats['Expected_Loss_LTV'] / 1e6):
        ax2.text(bar.get_x() + bar.get_width() / 2., val + 0.05,
                 f"${val:.2f}M", ha='center', va='bottom', fontsize=10, fontweight='bold')

    plt.suptitle('FINANCIAL EXPOSURE & VALUE-AT-RISK BY RISK TIER', y=1.02, fontsize=16, fontweight='bold')
    plt.tight_layout()

    out_path = os.path.join(REPORTS_DIR, 'churn_risk_revenue_exposure.png')
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_path}")
    return mrr_stats


def plot_churn_risk_action_matrix(df):
    """Plot 4: 2x2 Value vs Risk Retention Matrix with Prescriptive Action Zones."""
    fig, ax = plt.subplots(figsize=(11, 8.5))

    median_charges = df['MonthlyCharges'].median()
    risk_cutoff = 45.0  # High Risk threshold in percent

    # Sample for scatter clarity
    sample_df = df.sample(min(1500, len(df)), random_state=42)

    quad_colors = {
        'Immediate Intervention': CRITICAL_COLOR,
        'Core VIP Protect': LOW_COLOR,
        'Automated Nurture': HIGH_COLOR,
        'Low Maintenance': ACCENT_INDIGO
    }

    for quad_name, group in sample_df.groupby('Action_Quadrant'):
        ax.scatter(group['Churn_Risk_Score'], group['MonthlyCharges'],
                   c=quad_colors.get(quad_name, '#94a3b8'),
                   label=quad_name, alpha=0.5, s=36, edgecolors='none')

    # Threshold divider lines
    ax.axvline(risk_cutoff, color='#475569', linestyle='--', linewidth=1.5, alpha=0.8)
    ax.axhline(median_charges, color='#475569', linestyle='--', linewidth=1.5, alpha=0.8)

    # Calculate quadrant aggregations
    quad_summary = df.groupby('Action_Quadrant').agg(
        Accounts=('customerID', 'count'),
        Avg_Risk=('Churn_Risk_Score', 'mean'),
        Total_MRR=('MonthlyCharges', 'sum'),
        Expected_Monthly_Loss=('Expected_Monthly_Loss', 'sum'),
        Avg_Monthly_Charges=('MonthlyCharges', 'mean')
    ).reset_index()

    # Annotation cards for each quadrant
    for _, row in quad_summary.iterrows():
        name = row['Action_Quadrant']
        acc = row['Accounts']
        loss = row['Expected_Monthly_Loss']
        mrr = row['Total_MRR']
        pct_base = (acc / len(df)) * 100

        if name == 'Immediate Intervention':
            x, y = 72, 110
            action_txt = "ACTION: VIP Concierge & Contract Subsidy"
        elif name == 'Core VIP Protect':
            x, y = 22, 110
            action_txt = "ACTION: Loyalty Delights & VIP Speed Upgrades"
        elif name == 'Automated Nurture':
            x, y = 72, 26
            action_txt = "ACTION: Automated Drip & Support Trials"
        else:
            x, y = 22, 26
            action_txt = "ACTION: Standard Digital Care & Self-Service"

        ax.text(x, y,
                f"[{name.upper()}]\n{acc:,} Accounts ({pct_base:.1f}%)\nMRR: ${mrr:,.0f} | At Risk: ${loss:,.0f}/mo\n{action_txt}",
                ha='center', va='center', fontsize=9.2, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.55', facecolor='white', edgecolor='#94a3b8', alpha=0.92))

    ax.set_title('CHURN RISK & VALUE RETENTION ACTION MATRIX (2x2)', pad=15)
    ax.set_xlabel('Predicted Churn Risk Probability Score (%) → Increasing Vulnerability')
    ax.set_ylabel('Monthly Charges ($/month) → Increasing Account Value / ARPU')
    ax.set_xlim(0, 100)
    ax.set_ylim(15, 125)
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.16), ncol=4, frameon=True)

    plt.tight_layout()
    out_path = os.path.join(REPORTS_DIR, 'churn_risk_action_matrix.png')
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_path}")
    return quad_summary


def export_data_and_summaries(df, tier_stats, factor_df, mrr_stats, quad_summary):
    """Export scored datasets, analytical summaries, and compact customer sample."""

    # 1. Full Scored Customer Roster
    out_cols = [
        'customerID', 'tenure', 'Contract', 'InternetService', 'PaymentMethod',
        'TechSupport', 'OnlineSecurity', 'PaperlessBilling',
        'MonthlyCharges', 'TotalCharges', 'Churn', 'Churn_Probability', 'Churn_Risk_Score',
        'Risk_Tier', 'Predicted_LTV', 'Expected_Monthly_Loss', 'Expected_LTV_Loss',
        'Value_Segment', 'Action_Quadrant', 'Recommended_Action'
    ]
    avail_cols = [c for c in out_cols if c in df.columns]
    scores_csv = os.path.join(REPORTS_DIR, 'customer_churn_risk_scores.csv')
    df[avail_cols].to_csv(scores_csv, index=False)
    print(f"Exported: {scores_csv} ({len(df):,} records)")

    # 2. Risk Tier Summary CSV
    tier_csv = os.path.join(REPORTS_DIR, 'churn_risk_tier_summary.csv')
    tier_stats.to_csv(tier_csv, index=False)
    print(f"Exported: {tier_csv}")

    # 3. Action Quadrant Summary CSV
    quad_csv = os.path.join(REPORTS_DIR, 'churn_risk_segment_matrix_summary.csv')
    quad_summary.to_csv(quad_csv, index=False)
    print(f"Exported: {quad_csv}")

    # 4. Top Drivers Summary CSV
    drv_csv = os.path.join(REPORTS_DIR, 'churn_risk_top_drivers_summary.csv')
    factor_df.to_csv(drv_csv, index=False)
    print(f"Exported: {drv_csv}")

    # 5. Compact JSON Sample for the Interactive Dashboard Table (Top Critical/High Risk + Representative Sample)
    critical_sample = df[df['Risk_Tier'] == 'Critical Risk'].sort_values('Expected_Monthly_Loss', ascending=False).head(120)
    high_sample = df[df['Risk_Tier'] == 'High Risk'].sort_values('Expected_Monthly_Loss', ascending=False).head(80)
    med_sample = df[df['Risk_Tier'] == 'Medium Risk'].sample(min(30, len(df[df['Risk_Tier'] == 'Medium Risk'])), random_state=42)
    low_sample = df[df['Risk_Tier'] == 'Low Risk'].sample(min(20, len(df[df['Risk_Tier'] == 'Low Risk'])), random_state=42)

    sample_combined = pd.concat([critical_sample, high_sample, med_sample, low_sample])[avail_cols]
    json_path = os.path.join(REPORTS_DIR, 'sample_risk_customers.json')
    sample_combined.to_json(json_path, orient='records', indent=2)
    print(f"Exported: {json_path} ({len(sample_combined)} curated accounts)")


def main():
    print("=" * 70)
    print("Starting Churn Risk Intelligence & Diagnostics Pipeline...")
    print("=" * 70)

    df = load_data_and_models()
    print(f"Dataset successfully loaded with {len(df):,} accounts.")

    # High-level portfolio metrics
    crit_count = len(df[df['Risk_Tier'] == 'Critical Risk'])
    high_count = len(df[df['Risk_Tier'] == 'High Risk'])
    total_mrr = df['MonthlyCharges'].sum()
    expected_mrr_loss = df['Expected_Monthly_Loss'].sum()
    high_val_crit = len(df[(df['Action_Quadrant'] == 'Immediate Intervention')])

    print(f"Portfolio Mean Churn Risk: {df['Churn_Probability'].mean() * 100:.2f}%")
    print(f"Critical & High Risk Accounts: {crit_count + high_count:,} accounts ({((crit_count + high_count)/len(df))*100:.1f}%)")
    print(f"Total Portfolio MRR: ${total_mrr:,.2f}")
    print(f"Total Expected Monthly Loss: ${expected_mrr_loss:,.2f} ({expected_mrr_loss/total_mrr*100:.1f}% of MRR)")
    print(f"Immediate Intervention (High Value + High Risk): {high_val_crit:,} accounts")

    print("\n[1/4] Generating Churn Risk Probability Distribution Chart...")
    tier_stats = plot_churn_risk_distribution(df)

    print("[2/4] Generating Churn Risk Drivers & Moats Chart...")
    factor_df = plot_churn_risk_drivers(df)

    print("[3/4] Generating Financial Exposure & Value-at-Risk Chart...")
    mrr_stats = plot_churn_risk_revenue_exposure(df)

    print("[4/4] Generating 2x2 Risk & Value Retention Action Matrix...")
    quad_summary = plot_churn_risk_action_matrix(df)

    print("\nExporting structured CSV reports and curated customer JSON...")
    export_data_and_summaries(df, tier_stats, factor_df, mrr_stats, quad_summary)

    print("\nPipeline execution completed successfully!")
    print("=" * 70)


if __name__ == '__main__':
    main()
