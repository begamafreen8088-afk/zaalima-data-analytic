"""
Generate Advanced Customer Segmentation Analytics & High-Resolution Charts
Customer Churn Prediction & Lifetime Value (LTV) Engine - Week 4 Day 3
"""

import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score

# Directory Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
REPORTS_DIR = os.path.join(BASE_DIR, "Reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

# Styling Configuration for Executive-Grade Publication Charts
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['figure.titlesize'] = 16
plt.rcParams['figure.titleweight'] = 'bold'

# Curated Harmonious Color Palette
COLOR_CHAMPIONS = '#10b981'    # Emerald green
COLOR_AT_RISK = '#ef4444'      # Crimson red
COLOR_BUDGET = '#0ea5e9'       # Cyan / Sky blue
COLOR_NEWCOMERS = '#f97316'    # Vivid orange
COLOR_DIGITAL = '#a855f7'      # Vibrant purple
COLOR_STEADY = '#6366f1'       # Indigo
DARK_SLATE = '#1e293b'
MUTED_SLATE = '#64748b'

PERSONA_COLORS = {
    'Champions & VIP Loyalists': COLOR_CHAMPIONS,
    'At-Risk High Rollers': COLOR_AT_RISK,
    'Budget Anchors': COLOR_BUDGET,
    'Vulnerable Newcomers': COLOR_NEWCOMERS,
    'Digital Enthusiasts & Streamers': COLOR_DIGITAL,
    'Core Steady Subscribers': COLOR_STEADY
}


def load_and_merge_data():
    """Load scored risk data and feature engineered customer attributes."""
    risk_scores_path = os.path.join(REPORTS_DIR, "customer_churn_risk_scores.csv")
    fe_path = os.path.join(DATA_DIR, "telco_feature_engineered_commit3.csv")
    raw_path = os.path.join(DATA_DIR, "WA_Fn-UseC_-Telco-Customer-Churn.csv")

    if os.path.exists(risk_scores_path):
        print(f"Loading scored customer risk data: {risk_scores_path}")
        df_risk = pd.read_csv(risk_scores_path)
    else:
        raise FileNotFoundError("Could not locate Reports/customer_churn_risk_scores.csv. Run generate_churn_risk_dashboard.py first.")

    # Load additional features
    if os.path.exists(fe_path):
        print(f"Merging features from: {fe_path}")
        df_fe = pd.read_csv(fe_path)
    elif os.path.exists(raw_path):
        print(f"Merging features from: {raw_path}")
        df_fe = pd.read_csv(raw_path)
    else:
        df_fe = pd.DataFrame()

    if not df_fe.empty:
        extra_cols = [c for c in df_fe.columns if c not in df_risk.columns or c == 'customerID']
        df = pd.merge(df_risk, df_fe[extra_cols], on='customerID', how='left')
    else:
        df = df_risk.copy()

    # Ensure numeric TotalServices
    if 'TotalServices' not in df.columns:
        services = ['PhoneService', 'MultipleLines', 'OnlineSecurity', 'OnlineBackup',
                    'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies']
        df['TotalServices'] = 0
        for s in services:
            if s in df.columns:
                df['TotalServices'] += (df[s].astype(str).str.lower() == 'yes').astype(int)

    # Standardize numeric Churn
    if 'Churn_Numeric' not in df.columns:
        df['Churn_Numeric'] = df['Churn'].map({'Yes': 1, 'No': 0, 1: 1, 0: 0}).fillna(0).astype(int)

    # Standardize numeric charges
    df['MonthlyCharges'] = pd.to_numeric(df['MonthlyCharges'], errors='coerce').fillna(df['MonthlyCharges'].median())
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce').fillna(df['MonthlyCharges'] * df['tenure'])
    df['tenure'] = pd.to_numeric(df['tenure'], errors='coerce').fillna(0).astype(int)

    print(f"Loaded {len(df):,} customer records with {len(df.columns)} dimensions.")
    return df


def assign_behavioral_personas(df):
    """
    Classify customers into 6 mutually exclusive, strategic business personas
    based on tenure longevity, spending intensity, churn propensity, and service adoption.
    """
    def categorize(row):
        tenure = row['tenure']
        charges = row['MonthlyCharges']
        prob = row['Churn_Probability']
        inet = str(row.get('InternetService', ''))
        tv = str(row.get('StreamingTV', ''))
        movies = str(row.get('StreamingMovies', ''))
        services = row.get('TotalServices', 0)

        # 1. Vulnerable Newcomers: Early tenure with acute churn probability
        if tenure <= 6 and prob >= 0.40:
            return 'Vulnerable Newcomers'

        # 2. At-Risk High Rollers: Substantial monthly bill with high attrition propensity
        if charges >= 70 and prob >= 0.45:
            return 'At-Risk High Rollers'

        # 3. Champions & VIP Loyalists: Long tenure, high spend, strong retention moat
        if tenure >= 36 and charges >= 70 and prob < 0.25:
            return 'Champions & VIP Loyalists'

        # 4. Budget Anchors: Price-sensitive, lower spend, long loyal tenure
        if charges < 45 and tenure >= 24 and prob < 0.25:
            return 'Budget Anchors'

        # 5. Digital Enthusiasts & Streamers: Heavy multimedia fiber adoption
        if inet == 'Fiber optic' and (tv == 'Yes' or movies == 'Yes') and services >= 4:
            return 'Digital Enthusiasts & Streamers'

        # 6. Core Steady Subscribers: Balanced mainstream subscribers
        return 'Core Steady Subscribers'

    df['Persona_Segment'] = df.apply(categorize, axis=1)

    # Compute RFM-style combined scoring (Tenure Longevity + Monetary Value - Churn Risk Penalty)
    t_rank = df['tenure'].rank(pct=True) * 100
    m_rank = df['MonthlyCharges'].rank(pct=True) * 100
    r_rank = (1 - df['Churn_Probability']).rank(pct=True) * 100
    df['RFM_Health_Score'] = np.round((t_rank * 0.35 + m_rank * 0.35 + r_rank * 0.30), 1)

    print("Assigned strategic behavioral personas:")
    for name, cnt in df['Persona_Segment'].value_counts().items():
        print(f"  - {name}: {cnt:,} accounts ({cnt/len(df)*100:.1f}%)")

    return df


def perform_kmeans_clustering(df):
    """
    Perform Unsupervised Machine Learning Segmentation using KMeans and 2D PCA projection.
    Features: tenure, MonthlyCharges, TotalServices, Churn_Probability, Predicted_LTV.
    """
    features = ['tenure', 'MonthlyCharges', 'TotalServices', 'Churn_Probability', 'Predicted_LTV']
    X = df[features].copy()

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Evaluate Inertia & Silhouette across k=3 to 6
    k_range = [3, 4, 5, 6]
    inertias = []
    silhouettes = []
    for k in k_range:
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = km.fit_predict(X_scaled)
        inertias.append(km.inertia_)
        sil = silhouette_score(X_scaled, labels, sample_size=2000, random_state=42)
        silhouettes.append(sil)

    # Optimal k=4 clusters provides the best balance of separation and business clarity
    best_k = 4
    final_km = KMeans(n_clusters=best_k, random_state=42, n_init=15)
    df['Cluster_ID'] = final_km.fit_predict(X_scaled)

    # Map Cluster IDs to descriptive names based on centroid attributes
    cluster_profiles = df.groupby('Cluster_ID')[features].mean()
    cluster_name_map = {}
    for cid, row in cluster_profiles.iterrows():
        if row['Churn_Probability'] >= 0.45:
            cluster_name_map[cid] = 'Cluster A: High-Churn Flight Risks'
        elif row['Predicted_LTV'] >= 4500 or (row['tenure'] >= 50 and row['MonthlyCharges'] >= 75):
            cluster_name_map[cid] = 'Cluster B: High-Value Enterprise Moats'
        elif row['MonthlyCharges'] < 40:
            cluster_name_map[cid] = 'Cluster C: Low-Cost Basic Loyalists'
        else:
            cluster_name_map[cid] = 'Cluster D: Mid-Tier Digital Mainstream'

    df['Cluster_Name'] = df['Cluster_ID'].map(cluster_name_map)

    # 2D PCA Projection for visualization
    pca = PCA(n_components=2, random_state=42)
    pca_coords = pca.fit_transform(X_scaled)
    df['PCA_1'] = np.round(pca_coords[:, 0], 3)
    df['PCA_2'] = np.round(pca_coords[:, 1], 3)
    pca_var = pca.explained_variance_ratio_

    eval_data = {
        'k_range': k_range,
        'inertias': inertias,
        'silhouettes': silhouettes,
        'pca_var': pca_var,
        'scaler': scaler,
        'kmeans': final_km
    }

    print(f"K-Means Clustering complete. PCA Explained Variance: PC1={pca_var[0]*100:.1f}%, PC2={pca_var[1]*100:.1f}%")
    return df, eval_data


def plot_rfm_personas(df):
    """
    Plot 1: Strategic Customer RFM & Behavioral Personas.
    Subplot 1: Account volume & share by persona.
    Subplot 2: Average Monthly Charges (ARPU) vs Empirical Churn Rate.
    Subplot 3: Total Portfolio MRR vs Expected Monthly Revenue at Risk ($/mo).
    """
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(21, 6.5))

    persona_order = [
        'Champions & VIP Loyalists',
        'Digital Enthusiasts & Streamers',
        'Core Steady Subscribers',
        'Budget Anchors',
        'At-Risk High Rollers',
        'Vulnerable Newcomers'
    ]

    stats = df.groupby('Persona_Segment').agg(
        Accounts=('customerID', 'count'),
        Avg_Charges=('MonthlyCharges', 'mean'),
        Churn_Rate=('Churn_Numeric', lambda s: s.mean() * 100),
        Total_MRR=('MonthlyCharges', 'sum'),
        Expected_Loss=('Expected_Monthly_Loss', 'sum')
    ).reindex(persona_order).reset_index()

    stats['Pct_Base'] = (stats['Accounts'] / len(df)) * 100
    colors = [PERSONA_COLORS[p] for p in persona_order]

    # Panel 1: Account Volume
    bars1 = ax1.barh(stats['Persona_Segment'], stats['Accounts'], color=colors, height=0.6)
    ax1.set_title('Customer Volume by Behavioral Persona', pad=15)
    ax1.set_xlabel('Number of Customer Accounts')
    ax1.set_xlim(0, max(stats['Accounts']) * 1.25)
    for bar, (_, r) in zip(bars1, stats.iterrows()):
        w = bar.get_width()
        ax1.text(w + 25, bar.get_y() + bar.get_height()/2.,
                 f"{int(w):,} ({r['Pct_Base']:.1f}%)", va='center', ha='left', fontsize=9.5, fontweight='bold')

    # Panel 2: ARPU vs Churn Rate
    y_pos = np.arange(len(persona_order))
    ax2.scatter(stats['Avg_Charges'], y_pos, s=stats['Accounts'] / 3.5, color=colors, alpha=0.85, edgecolors='white', linewidth=1.5)
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(persona_order)
    ax2.set_title('Average Spend (ARPU) vs. Empirical Churn Rate', pad=15)
    ax2.set_xlabel('Average Monthly Charges ($/month)')
    ax2.set_xlim(20, 115)
    for i, r in stats.iterrows():
        ax2.text(r['Avg_Charges'] + 2.5, i,
                 f"ARPU: ${r['Avg_Charges']:.1f}\nChurn: {r['Churn_Rate']:.1f}%",
                 va='center', ha='left', fontsize=9, fontweight='bold')

    # Panel 3: Total MRR vs Revenue at Risk
    w_bar = 0.38
    b1 = ax3.bar(y_pos - w_bar/2, stats['Total_MRR'] / 1000, width=w_bar, label='Total Segment MRR', color='#94a3b8', alpha=0.8)
    b2 = ax3.bar(y_pos + w_bar/2, stats['Expected_Loss'] / 1000, width=w_bar, label='Monthly Revenue at Risk', color=colors, alpha=0.9)
    ax3.set_xticks(y_pos)
    ax3.set_xticklabels([p.split('&')[0].replace('Subscribers','').replace('High Rollers','Whales').strip() for p in persona_order], rotation=25, ha='right')
    ax3.set_title('Total MRR vs. Monthly Cash Exposure ($k/mo)', pad=15)
    ax3.set_ylabel('MRR ($ in Thousands)')
    ax3.set_ylim(0, max(stats['Total_MRR'] / 1000) * 1.3)
    ax3.legend(loc='upper right', frameon=True)
    for bar in b2:
        h = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., h + 1.5, f"${h:.1f}k", ha='center', va='bottom', fontsize=8.5, fontweight='bold')

    plt.suptitle('STRATEGIC CUSTOMER BEHAVIORAL PERSONAS & FINANCIAL EXPOSURE', y=1.02, fontsize=16, fontweight='bold')
    plt.tight_layout()

    out_path = os.path.join(REPORTS_DIR, 'customer_segmentation_rfm_personas.png')
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_path}")
    return stats


def plot_kmeans_clusters(df, eval_data):
    """
    Plot 2: Unsupervised K-Means Machine Learning Clustering & PCA 2D Space.
    Subplot 1: Mathematical Cluster Optimization (Elbow Inertia & Silhouette Scores).
    Subplot 2: 2D Principal Component Projection (PCA) with Cluster Boundaries and Centroids.
    Subplot 3: Cluster Dimensional Profile Bar Chart.
    """
    fig = plt.figure(figsize=(20, 6.5))
    gs = fig.add_gridspec(1, 3, width_ratios=[1, 1.3, 1.2])

    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[0, 2])

    k_range = eval_data['k_range']
    inertias = eval_data['inertias']
    silhouettes = eval_data['silhouettes']

    # Subplot 1: Elbow & Silhouette Curves
    color_inertia = '#6366f1'
    color_sil = '#10b981'

    ax1.plot(k_range, inertias, marker='o', color=color_inertia, linewidth=2.5, markersize=7, label='Inertia (WCSS)')
    ax1.set_xlabel('Number of Clusters (k)', fontweight='bold')
    ax1.set_ylabel('Inertia (WCSS)', color=color_inertia, fontweight='bold')
    ax1.tick_params(axis='y', labelcolor=color_inertia)
    ax1.set_title('K-Means Optimization: Elbow & Silhouette', pad=15)
    ax1.set_xticks(k_range)

    ax1_twin = ax1.twinx()
    ax1_twin.plot(k_range, silhouettes, marker='s', color=color_sil, linewidth=2.5, linestyle='--', markersize=7, label='Silhouette Score')
    ax1_twin.set_ylabel('Silhouette Coefficient', color=color_sil, fontweight='bold')
    ax1_twin.tick_params(axis='y', labelcolor=color_sil)
    ax1_twin.grid(False)

    # Subplot 2: PCA 2D Cluster Space
    cluster_colors = {
        0: '#ef4444',  # Red
        1: '#10b981',  # Emerald
        2: '#0ea5e9',  # Cyan
        3: '#8b5cf6'   # Purple
    }

    # Sample for visual rendering performance
    sample_df = df.sample(min(2000, len(df)), random_state=42)
    for cid in sorted(df['Cluster_ID'].unique()):
        sub = sample_df[sample_df['Cluster_ID'] == cid]
        cname = df[df['Cluster_ID'] == cid]['Cluster_Name'].iloc[0]
        ax2.scatter(sub['PCA_1'], sub['PCA_2'],
                    c=cluster_colors.get(cid, '#94a3b8'),
                    label=f"C{cid}: {cname.split(':')[1].strip()}",
                    alpha=0.55, s=32, edgecolors='none')

    # Plot Cluster Centroids in PCA space
    pca_centroids = sample_df.groupby('Cluster_ID')[['PCA_1', 'PCA_2']].mean()
    for cid, (cx, cy) in pca_centroids.iterrows():
        ax2.scatter(cx, cy, s=180, c='white', marker='X', edgecolors='black', linewidth=2, zorder=10)
        ax2.text(cx, cy + 0.25, f"C{cid}", fontsize=11, fontweight='black', ha='center',
                 bbox=dict(boxstyle='circle,pad=0.2', facecolor='white', alpha=0.9))

    ax2.set_title(f"PCA 2D Cluster Space (Explained Var: {sum(eval_data['pca_var'])*100:.1f}%)", pad=15)
    ax2.set_xlabel('Principal Component 1 (Tenure & Total Spend Driver)')
    ax2.set_ylabel('Principal Component 2 (Monthly Rate & Churn Driver)')
    ax2.legend(loc='upper right', frameon=True, facecolor='white', framealpha=0.9, fontsize=8.5)

    # Subplot 3: Cluster Comparison by Normalized Key Metrics
    cluster_summary = df.groupby('Cluster_Name').agg(
        Accounts=('customerID', 'count'),
        Avg_Tenure=('tenure', 'mean'),
        Avg_Monthly=('MonthlyCharges', 'mean'),
        Avg_Churn_Risk=('Churn_Probability', lambda s: s.mean() * 100),
        Avg_LTV=('Predicted_LTV', 'mean')
    ).reset_index()

    y_pos = np.arange(len(cluster_summary))
    height = 0.2
    c_names_short = [n.split(':')[1].strip() for n in cluster_summary['Cluster_Name']]

    ax3.barh(y_pos - 1.5*height, cluster_summary['Avg_Tenure'], height=height, label='Avg Tenure (mo)', color='#0ea5e9')
    ax3.barh(y_pos - 0.5*height, cluster_summary['Avg_Monthly'], height=height, label='Avg Monthly ($)', color='#6366f1')
    ax3.barh(y_pos + 0.5*height, cluster_summary['Avg_Churn_Risk'], height=height, label='Churn Risk (%)', color='#ef4444')
    ax3.barh(y_pos + 1.5*height, cluster_summary['Avg_LTV'] / 60, height=height, label='LTV Index ($/60)', color='#10b981')

    ax3.set_yticks(y_pos)
    ax3.set_yticklabels(c_names_short, fontsize=9, fontweight='bold')
    ax3.set_title('Cluster Profiles Across Core Dimensions', pad=15)
    ax3.set_xlabel('Metric Scale')
    ax3.legend(loc='lower right', frameon=True, facecolor='white', framealpha=0.9, fontsize=8.5)

    plt.suptitle('UNSUPERVISED K-MEANS MACHINE LEARNING SEGMENTATION & PCA DIAGNOSTICS', y=1.02, fontsize=16, fontweight='bold')
    plt.tight_layout()

    out_path = os.path.join(REPORTS_DIR, 'customer_segmentation_kmeans_clusters.png')
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_path}")
    return cluster_summary


def plot_lifecycle_value_matrix(df):
    """
    Plot 3: Multi-Dimensional 4x4 Lifecycle Cohort vs. Monthly Spend Tier Matrix Heatmaps.
    Heatmap 1: Customer Account Volume.
    Heatmap 2: Empirical Churn Rate (%).
    Heatmap 3: Monthly Revenue at Risk ($ in Thousands).
    """
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(21, 6.2))

    # Define bins
    tenure_bins = [-1, 12, 24, 48, 72]
    tenure_labels = ['New (0-12m)', 'Growing (13-24m)', 'Established (25-48m)', 'Veteran (49-72m)']
    df['Tenure_Lifecycle'] = pd.cut(df['tenure'], bins=tenure_bins, labels=tenure_labels)

    charge_bins = [0, 35, 65, 90, 150]
    charge_labels = ['Budget (<$35)', 'Moderate ($35-$65)', 'High ($65-$90)', 'Premium (>$90)']
    df['Spend_Tier'] = pd.cut(df['MonthlyCharges'], bins=charge_bins, labels=charge_labels)

    # Pivot Tables
    pivot_volume = pd.pivot_table(df, values='customerID', index='Spend_Tier', columns='Tenure_Lifecycle',
                                  aggfunc='count', observed=False).iloc[::-1]

    pivot_churn = pd.pivot_table(df, values='Churn_Numeric', index='Spend_Tier', columns='Tenure_Lifecycle',
                                 aggfunc=lambda s: round(s.mean() * 100, 1), observed=False).iloc[::-1]

    pivot_loss = pd.pivot_table(df, values='Expected_Monthly_Loss', index='Spend_Tier', columns='Tenure_Lifecycle',
                                aggfunc=lambda s: round(s.sum() / 1000, 1), observed=False).iloc[::-1]

    # Heatmap 1: Volume
    sns.heatmap(pivot_volume, annot=True, fmt=',d', cmap='Blues', cbar=False, ax=ax1,
                linewidths=1.5, linecolor='#0f172a', annot_kws={'size': 11, 'weight': 'bold'})
    ax1.set_title('Customer Account Volume', pad=15)
    ax1.set_xlabel('Tenure Lifecycle Cohort')
    ax1.set_ylabel('Monthly Spend Tier')

    # Heatmap 2: Empirical Churn Rate (%)
    sns.heatmap(pivot_churn, annot=True, fmt='.1f', cmap='YlOrRd', cbar=False, ax=ax2,
                linewidths=1.5, linecolor='#0f172a', annot_kws={'size': 11, 'weight': 'bold'})
    ax2.set_title('Empirical Churn Rate (%)', pad=15)
    ax2.set_xlabel('Tenure Lifecycle Cohort')
    ax2.set_ylabel('')

    # Heatmap 3: Revenue at Risk ($k/mo)
    sns.heatmap(pivot_loss, annot=True, fmt='.1f', cmap='Reds', cbar=False, ax=ax3,
                linewidths=1.5, linecolor='#0f172a', annot_kws={'size': 11, 'weight': 'bold'})
    ax3.set_title('Expected Monthly Loss ($k/mo)', pad=15)
    ax3.set_xlabel('Tenure Lifecycle Cohort')
    ax3.set_ylabel('')

    plt.suptitle('CUSTOMER LIFECYCLE STAGE × SPEND TIER CROSS-TABULATION MATRIX', y=1.02, fontsize=16, fontweight='bold')
    plt.tight_layout()

    out_path = os.path.join(REPORTS_DIR, 'customer_segmentation_lifecycle_value_matrix.png')
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_path}")


def plot_service_adoption_profiles(df):
    """
    Plot 4: Service Ecosystem Adoption & Technology Penetration Across Segments.
    Compares adoption of Online Security, Tech Support, Streaming, Device Protection,
    and Fiber Optic internet across the 6 behavioral personas.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 6.5))

    services = {
        'OnlineSecurity': 'Online Security',
        'TechSupport': 'Tech Support',
        'OnlineBackup': 'Online Backup',
        'DeviceProtection': 'Device Protection',
        'StreamingTV': 'Streaming TV',
        'StreamingMovies': 'Streaming Movies'
    }

    persona_order = [
        'Champions & VIP Loyalists',
        'Digital Enthusiasts & Streamers',
        'Core Steady Subscribers',
        'Budget Anchors',
        'At-Risk High Rollers',
        'Vulnerable Newcomers'
    ]

    # Calculate adoption percentages
    adoption_records = []
    for p in persona_order:
        sub = df[df['Persona_Segment'] == p]
        rec = {'Persona': p}
        for col, label in services.items():
            if col in sub.columns:
                rec[label] = (sub[col].astype(str).str.lower() == 'yes').mean() * 100
            else:
                rec[label] = 0
        if 'InternetService' in sub.columns:
            rec['Fiber Optic'] = (sub['InternetService'] == 'Fiber optic').mean() * 100
        adoption_records.append(rec)

    adopt_df = pd.DataFrame(adoption_records).set_index('Persona')

    # Subplot 1: Defensive Security/Support Services vs Vulnerability
    defensive_cols = ['Online Security', 'Tech Support', 'Device Protection', 'Online Backup']
    adopt_df[defensive_cols].plot(kind='bar', ax=ax1, colormap='viridis', width=0.75, edgecolor='none')
    ax1.set_title('Defensive Support & Security Service Penetration (%)', pad=15)
    ax1.set_ylabel('Adoption Rate (%)')
    ax1.set_ylim(0, 100)
    ax1.set_xticklabels([p.split('&')[0].replace('Subscribers','').strip() for p in persona_order], rotation=25, ha='right')
    ax1.legend(loc='upper right', frameon=True)
    ax1.axhline(50, color='#94a3b8', linestyle=':', alpha=0.7)

    # Subplot 2: Fiber Optic & Multimedia Streaming Adoption
    entertainment_cols = ['Fiber Optic', 'Streaming TV', 'Streaming Movies']
    colors_ent = ['#f43f5e', '#8b5cf6', '#0ea5e9']
    adopt_df[entertainment_cols].plot(kind='bar', ax=ax2, color=colors_ent, width=0.65, edgecolor='none')
    ax2.set_title('Broadband Technology & Entertainment Adoption (%)', pad=15)
    ax2.set_ylabel('Adoption Rate (%)')
    ax2.set_ylim(0, 100)
    ax2.set_xticklabels([p.split('&')[0].replace('Subscribers','').strip() for p in persona_order], rotation=25, ha='right')
    ax2.legend(loc='upper left', frameon=True)

    plt.suptitle('SERVICE ECOSYSTEM PENETRATION & RETENTION BUFFER BY PERSONA', y=1.02, fontsize=16, fontweight='bold')
    plt.tight_layout()

    out_path = os.path.join(REPORTS_DIR, 'customer_segmentation_service_adoption_profiles.png')
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_path}")
    return adopt_df


def plot_ltv_risk_quadrants(df):
    """
    Plot 5: Strategic Customer Portfolio Bubble Matrix.
    X-axis: Churn Probability (%).
    Y-axis: Predicted Customer Lifetime Value ($ LTV).
    Bubble Size: Monthly Charges ($ ARPU).
    Bubble Color: Persona Segment.
    Annotations: Investment & Retention Action Zones.
    """
    fig, ax = plt.subplots(figsize=(12, 8))

    sample_df = df.sample(min(1500, len(df)), random_state=42)

    for persona_name, grp in sample_df.groupby('Persona_Segment'):
        ax.scatter(
            grp['Churn_Probability'] * 100,
            grp['Predicted_LTV'],
            s=grp['MonthlyCharges'] * 1.8,
            c=PERSONA_COLORS.get(persona_name, '#94a3b8'),
            label=persona_name,
            alpha=0.6,
            edgecolors='white',
            linewidth=0.6
        )

    # Decision Boundaries
    ax.axvline(45, color='#475569', linestyle='--', linewidth=1.5, alpha=0.8)
    median_ltv = df['Predicted_LTV'].median()
    ax.axhline(median_ltv, color='#475569', linestyle='--', linewidth=1.5, alpha=0.8)

    # Strategic Action Zones
    ax.text(18, max(df['Predicted_LTV']) * 0.88,
            "[PLATINUM VAULT]\nHigh LTV | Low Churn\n• VIP Concierge & Loyalty Perks\n• Multi-year contract lock-ins",
            bbox=dict(boxstyle='round,pad=0.6', facecolor='#ecfdf5', edgecolor='#10b981', alpha=0.9),
            fontsize=9.5, fontweight='bold', color='#065f46')

    ax.text(72, max(df['Predicted_LTV']) * 0.88,
            "[URGENT INTERVENTION ZONE]\nHigh LTV | Elevated Churn\n• Dedicated retention strike team\n• Free tech support + billing credit",
            bbox=dict(boxstyle='round,pad=0.6', facecolor='#fef2f2', edgecolor='#ef4444', alpha=0.9),
            fontsize=9.5, fontweight='bold', color='#991b1b')

    ax.text(18, 500,
            "[STABLE BASELINE]\nLower LTV | Low Churn\n• Automated self-service care\n• Cross-sell fiber & speed boosters",
            bbox=dict(boxstyle='round,pad=0.6', facecolor='#f0f9ff', edgecolor='#0ea5e9', alpha=0.9),
            fontsize=9.5, fontweight='bold', color='#075985')

    ax.text(72, 500,
            "[AUTOMATED RECOVERY]\nLower LTV | Elevated Churn\n• Automated email / SMS re-engagement\n• Low-cost contract incentive offers",
            bbox=dict(boxstyle='round,pad=0.6', facecolor='#fffbeb', edgecolor='#f59e0b', alpha=0.9),
            fontsize=9.5, fontweight='bold', color='#92400e')

    ax.set_title('STRATEGIC CUSTOMER PORTFOLIO MATRIX: LTV VS. CHURN HAZARD', pad=15)
    ax.set_xlabel('Predicted Churn Risk Probability (%) → Increasing Vulnerability')
    ax.set_ylabel('Predicted Customer Lifetime Value ($ LTV) → Increasing Asset Value')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, max(df['Predicted_LTV']) * 1.05)
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.16), ncol=3, frameon=True, fontsize=9)

    plt.tight_layout()
    out_path = os.path.join(REPORTS_DIR, 'customer_segmentation_ltv_risk_quadrants.png')
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_path}")


def export_segmentation_artifacts(df, persona_stats, cluster_summary, adopt_df):
    """Export comprehensive datasets, CSV summaries, and lightweight JSON for web UI."""

    # 1. Full Segmented Dataset
    cols_to_export = [
        'customerID', 'tenure', 'Contract', 'InternetService', 'PaymentMethod',
        'TechSupport', 'OnlineSecurity', 'StreamingTV', 'MonthlyCharges', 'TotalCharges',
        'Churn', 'Churn_Probability', 'Churn_Risk_Score', 'Risk_Tier',
        'Predicted_LTV', 'Expected_Monthly_Loss', 'Persona_Segment', 'Cluster_ID',
        'Cluster_Name', 'RFM_Health_Score'
    ]
    avail_cols = [c for c in cols_to_export if c in df.columns]
    full_csv = os.path.join(REPORTS_DIR, "customer_segments_full.csv")
    df[avail_cols].to_csv(full_csv, index=False)
    print(f"Saved full customer segments CSV: {full_csv} ({len(df)} rows)")

    # 2. Persona Profiles Summary CSV
    profiles_csv = os.path.join(REPORTS_DIR, "customer_segmentation_profiles.csv")
    persona_stats.to_csv(profiles_csv, index=False)
    print(f"Saved persona profiles CSV: {profiles_csv}")

    # 3. K-Means Clusters Summary CSV
    clusters_csv = os.path.join(REPORTS_DIR, "kmeans_cluster_summary.csv")
    cluster_summary.to_csv(clusters_csv, index=False)
    print(f"Saved cluster summary CSV: {clusters_csv}")

    # 4. Compact Sample JSON for Dashboard Interactive Explorer
    sample_recs = []
    for p in df['Persona_Segment'].unique():
        sub = df[df['Persona_Segment'] == p]
        n_take = min(60, len(sub))
        sample_recs.append(sub.sample(n_take, random_state=42))

    compact_df = pd.concat(sample_recs).reset_index(drop=True)
    json_records = []
    for _, r in compact_df.iterrows():
        json_records.append({
            'id': str(r['customerID']),
            'tenure': int(r['tenure']),
            'contract': str(r['Contract']),
            'charges': float(r['MonthlyCharges']),
            'prob': float(r['Churn_Probability']),
            'tier': str(r['Risk_Tier']),
            'ltv': float(r['Predicted_LTV']),
            'persona': str(r['Persona_Segment']),
            'cluster': str(r['Cluster_Name']).split(':')[0].strip(),
            'rfm': float(r['RFM_Health_Score'])
        })

    compact_json = os.path.join(REPORTS_DIR, "compact_segments.json")
    with open(compact_json, 'w') as f:
        json.dump(json_records, f)
    print(f"Saved compact segments JSON for dashboard explorer: {compact_json} ({len(json_records)} records)")


def main():
    print("=" * 70)
    print("TELECOM CUSTOMER SEGMENTATION & BEHAVIORAL ANALYTICS ENGINE")
    print("=" * 70)

    # 1. Load Data
    df = load_and_merge_data()

    # 2. Behavioral & RFM Persona Classification
    df = assign_behavioral_personas(df)

    # 3. Unsupervised K-Means Machine Learning Clustering
    df, eval_data = perform_kmeans_clustering(df)

    # 4. Generate Publication-Quality Visualizations (300 DPI)
    print("\nGenerating Customer Segmentation Charts...")
    persona_stats = plot_rfm_personas(df)
    cluster_summary = plot_kmeans_clusters(df, eval_data)
    plot_lifecycle_value_matrix(df)
    adopt_df = plot_service_adoption_profiles(df)
    plot_ltv_risk_quadrants(df)

    # 5. Export Analytical Artifacts
    print("\nExporting Datasets and Analytics Summaries...")
    export_segmentation_artifacts(df, persona_stats, cluster_summary, adopt_df)

    print("\nAll Customer Segmentation charts and artifacts generated successfully!")
    print("=" * 70)


if __name__ == "__main__":
    main()
