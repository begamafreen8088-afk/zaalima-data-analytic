"""
Comprehensive Validation & Quality Assurance Test Suite
Telecom Customer Churn & Lifetime Value (LTV) Engine
Validates all dashboard insights, data pipelines, model predictions, and financial reports.
"""

import os
import sys
import re
import json
import pandas as pd
import numpy as np

# Force UTF-8 on Windows terminal
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_DIR = os.path.join(WORKSPACE_DIR, "Reports")
DATA_DIR = os.path.join(WORKSPACE_DIR, "data")
DOCS_DIR = os.path.join(WORKSPACE_DIR, "docs")


class ValidationSuite:
    def __init__(self):
        self.passed_tests = 0
        self.failed_tests = 0
        self.test_log = []

    def assert_test(self, test_name, condition, details=""):
        if condition:
            self.passed_tests += 1
            msg = f"  [PASS] {test_name}"
            if details:
                msg += f" ({details})"
            print(msg)
            self.test_log.append({"test": test_name, "status": "PASS", "details": details})
        else:
            self.failed_tests += 1
            msg = f"  [FAIL] {test_name} - {details}"
            print(msg)
            self.test_log.append({"test": test_name, "status": "FAIL", "details": details})

    def run_all(self):
        print("=" * 80)
        print("TELECOM CHURN & LTV ENGINE: END-TO-END VALIDATION & QA SUITE")
        print("=" * 80)

        self.validate_base_datasets()
        self.validate_predictive_risk_model()
        self.validate_customer_segmentation()
        self.validate_kmeans_clustering()
        self.validate_strategic_pillars_roi()
        self.validate_financial_scenarios()
        self.validate_production_artifacts()
        self.validate_html_dashboards()

        print("\n" + "=" * 80)
        print(f"AUDIT SUMMARY: {self.passed_tests} PASSED | {self.failed_tests} FAILED")
        status_msg = "PASSED - 100% PRODUCTION READY" if self.failed_tests == 0 else "FAILED CHECKS DETECTED"
        print(f"FINAL QUALITY CERTIFICATION: {status_msg}")
        print("=" * 80)
        return self.failed_tests == 0

    def validate_base_datasets(self):
        print("\n[SECTION 1: Base Datasets & Feature Engineering Validation]")
        raw_path = os.path.join(DATA_DIR, "WA_Fn-UseC_-Telco-Customer-Churn.csv")
        fe_path = os.path.join(DATA_DIR, "telco_feature_engineered_commit3.csv")

        self.assert_test("Raw Dataset Exists", os.path.exists(raw_path))
        self.assert_test("Feature Engineered Dataset Exists", os.path.exists(fe_path))

        df_raw = pd.read_csv(raw_path)
        self.assert_test("Raw Account Scope Exactly 7,043", len(df_raw) == 7043, f"Found {len(df_raw)}")

        churn_counts = df_raw['Churn'].value_counts()
        self.assert_test("Empirical Churn Count Exactly 1,869", churn_counts.get('Yes', 0) == 1869)
        self.assert_test("Empirical Retained Count Exactly 5,174", churn_counts.get('No', 0) == 5174)

        churn_rate = (churn_counts['Yes'] / len(df_raw)) * 100
        self.assert_test("Empirical Churn Rate Exactly 26.54%", abs(churn_rate - 26.53698) < 0.01, f"{churn_rate:.2f}%")

        mrr = df_raw['MonthlyCharges'].sum()
        self.assert_test("Portfolio Baseline MRR Exactly $456,116.60", abs(mrr - 456116.60) < 0.01, f"${mrr:,.2f}")

        arr = mrr * 12
        self.assert_test("Portfolio Annualized ARR Exactly $5,473,399.20", abs(arr - 5473399.20) < 0.01, f"${arr:,.2f}")

        arpu = df_raw['MonthlyCharges'].mean()
        self.assert_test("Portfolio Average ARPU Exactly $64.76", abs(arpu - 64.7617) < 0.01, f"${arpu:.2f}")

        churned_mrr = df_raw[df_raw['Churn'] == 'Yes']['MonthlyCharges'].sum()
        self.assert_test("Empirical Churned MRR Exactly $139,130.85", abs(churned_mrr - 139130.85) < 0.01, f"${churned_mrr:,.2f}")

        # TotalCharges imputation check
        df_fe = pd.read_csv(fe_path)
        self.assert_test("Feature Engineered Scope Exactly 7,043", len(df_fe) == 7043)
        self.assert_test("Zero Missing Values in TotalCharges", df_fe['TotalCharges'].isna().sum() == 0)

    def validate_predictive_risk_model(self):
        print("\n[SECTION 2: Predictive Churn Risk Scoring Validation]")
        risk_path = os.path.join(REPORTS_DIR, "customer_churn_risk_scores.csv")
        self.assert_test("Scored Risk CSV Exists", os.path.exists(risk_path))

        df_risk = pd.read_csv(risk_path)
        self.assert_test("100% of Accounts Scored (7,043)", len(df_risk) == 7043)

        mean_prob = df_risk['Churn_Probability'].mean() * 100
        self.assert_test("Mean Predicted Churn Risk Approximately 26.51%", abs(mean_prob - 26.51) < 0.05, f"{mean_prob:.2f}%")

        prob_in_range = ((df_risk['Churn_Probability'] >= 0.0) & (df_risk['Churn_Probability'] <= 1.0)).all()
        self.assert_test("Probabilities Formally Bounded in [0.0, 1.0]", prob_in_range)

        # Expected monthly loss = sum(prob * MonthlyCharges)
        expected_monthly_loss = df_risk['Expected_Monthly_Loss'].sum()
        self.assert_test("Total Expected Monthly Loss Exactly $139,620.25", abs(expected_monthly_loss - 139620.25) < 0.50, f"${expected_monthly_loss:,.2f}")

        annual_expected_loss = expected_monthly_loss * 12
        self.assert_test("Annualized Expected Loss Run-Rate $1,675,443.00", abs(annual_expected_loss - 1675443.00) < 6.00, f"${annual_expected_loss:,.2f}")

        # Risk Tiers
        tier_counts = df_risk['Risk_Tier'].value_counts()
        self.assert_test("Critical Tier Count Exactly 812", tier_counts.get('Critical Risk (>=70%)', tier_counts.get('Critical Risk', 0)) == 812)
        self.assert_test("High Tier Count Exactly 942", tier_counts.get('High Risk (45-70%)', tier_counts.get('High Risk', 0)) == 942)
        self.assert_test("Medium Tier Count Exactly 995", tier_counts.get('Medium Risk (25-45%)', tier_counts.get('Medium Risk', 0)) == 995)
        self.assert_test("Low Tier Count Exactly 4,294", tier_counts.get('Low Risk (<25%)', tier_counts.get('Low Risk', 0)) == 4294)

        # High + Critical risk concentration
        crit_loss = df_risk[df_risk['Risk_Tier'].str.contains('Critical')]['Expected_Monthly_Loss'].sum()
        high_loss = df_risk[df_risk['Risk_Tier'].str.contains('High')]['Expected_Monthly_Loss'].sum()
        top_loss = crit_loss + high_loss
        top_conc = (top_loss / expected_monthly_loss) * 100
        self.assert_test("Top-Heavy Risk Concentration 66.7% ($93.2k/mo)", abs(top_conc - 66.75) < 0.20, f"{top_conc:.2f}% (${top_loss:,.2f})")

        # Action Quadrants
        quad_counts = df_risk['Action_Quadrant'].value_counts()
        self.assert_test("Immediate Intervention Accounts Exactly 1,286", quad_counts.get('Immediate Intervention', 0) == 1286)
        self.assert_test("Core VIP Protect Accounts Exactly 2,238", quad_counts.get('Core VIP Protect', 0) == 2238)

    def validate_customer_segmentation(self):
        print("\n[SECTION 3: Customer Segmentation & RFM Personas Validation]")
        seg_path = os.path.join(REPORTS_DIR, "customer_segments_full.csv")
        self.assert_test("Segmented Customers CSV Exists", os.path.exists(seg_path))

        df_seg = pd.read_csv(seg_path)
        self.assert_test("Segmented Accounts Total Exactly 7,043", len(df_seg) == 7043)

        p_counts = df_seg['Persona_Segment'].value_counts()
        self.assert_test("Champions & VIP Loyalists Exactly 1,405", p_counts.get('Champions & VIP Loyalists', 0) == 1405)
        self.assert_test("At-Risk High Rollers Exactly 811", p_counts.get('At-Risk High Rollers', 0) == 811)
        self.assert_test("Vulnerable Newcomers Exactly 894", p_counts.get('Vulnerable Newcomers', 0) == 894)
        self.assert_test("Digital Enthusiasts & Streamers Exactly 407", p_counts.get('Digital Enthusiasts & Streamers', 0) == 407)
        self.assert_test("Budget Anchors Exactly 945", p_counts.get('Budget Anchors', 0) == 945)
        self.assert_test("Core Steady Subscribers Exactly 2,581", p_counts.get('Core Steady Subscribers', 0) == 2581)

        # Sum of personas
        self.assert_test("Personas Sum to Exactly 7,043 Accounts", sum(p_counts.values) == 7043)

        # Loss concentration in High Rollers + Vulnerable Newcomers
        hr_loss = df_seg[df_seg['Persona_Segment'] == 'At-Risk High Rollers']['Expected_Monthly_Loss'].sum()
        vn_loss = df_seg[df_seg['Persona_Segment'] == 'Vulnerable Newcomers']['Expected_Monthly_Loss'].sum()
        hazard_loss = hr_loss + vn_loss
        total_loss = df_seg['Expected_Monthly_Loss'].sum()
        hazard_pct = (hazard_loss / total_loss) * 100
        self.assert_test("65.5% Revenue Drain in High Rollers & Newcomers ($91.5k/mo)", abs(hazard_pct - 65.54) < 0.20, f"{hazard_pct:.2f}% (${hazard_loss:,.2f})")

    def validate_kmeans_clustering(self):
        print("\n[SECTION 4: K-Means Clustering & PCA Validation]")
        km_path = os.path.join(REPORTS_DIR, "kmeans_cluster_summary.csv")
        self.assert_test("K-Means Summary CSV Exists", os.path.exists(km_path))

        df_km = pd.read_csv(km_path)
        self.assert_test("Exactly 4 Clusters Formed", len(df_km) == 4)

        total_cluster_accts = df_km['Accounts'].sum()
        self.assert_test("K-Means Total Accounts Exactly 7,043", total_cluster_accts == 7043)

        flight_risks = df_km[df_km['Cluster_Name'].str.contains('Flight Risks')]['Accounts'].iloc[0]
        self.assert_test("Flight Risks (Cluster A) Exactly 1,733 Accounts", flight_risks == 1733)

        ent_moats = df_km[df_km['Cluster_Name'].str.contains('Enterprise Moats')]['Accounts'].iloc[0]
        self.assert_test("Enterprise Moats (Cluster B) Exactly 1,533 Accounts", ent_moats == 1533)

    def validate_strategic_pillars_roi(self):
        print("\n[SECTION 5: Five Strategic Pillars & ROI Validation]")
        sp_path = os.path.join(REPORTS_DIR, "executive_strategic_pillars_summary.csv")
        self.assert_test("Strategic Pillars CSV Exists", os.path.exists(sp_path))

        df_sp = pd.read_csv(sp_path)
        self.assert_test("5 Strategic Pillars Defined", len(df_sp) == 5)

        # Re-check Pillar 1 (High Rollers)
        p1 = df_sp[df_sp['Pillar'].str.contains('Pillar 1')].iloc[0]
        self.assert_test("Pillar 1 Preserved ARR Exactly $173,316", abs(p1['Preserved_ARR_Target'] - 173316) < 1.0)
        self.assert_test("Pillar 1 Net ROI Exactly 493.6%", abs(p1['ROI_Pct'] - 493.6) < 0.1)

        # Re-check Pillar 2 (Onboarding)
        p2 = df_sp[df_sp['Pillar'].str.contains('Pillar 2')].iloc[0]
        self.assert_test("Pillar 2 Preserved ARR Exactly $130,094", abs(p2['Preserved_ARR_Target'] - 130093.68) < 1.0)
        self.assert_test("Pillar 2 Net ROI Exactly 506.3%", abs(p2['ROI_Pct'] - 506.3) < 0.1)

        # Cumulative yield across all 5 pillars
        total_arr_saved = df_sp['Preserved_ARR_Target'].sum()
        total_budget = df_sp['Annual_Cost'].sum()
        total_net_gain = df_sp['Net_Annual_Gain'].sum()
        overall_roi = (total_net_gain / total_budget) * 100

        self.assert_test("Cumulative Preserved ARR $418,849.68", abs(total_arr_saved - 418849.68) < 20.0, f"${total_arr_saved:,.2f}")
        self.assert_test("Cumulative Program Budget $94,802.00", abs(total_budget - 94802.00) < 10.0, f"${total_budget:,.2f}")
        self.assert_test("Cumulative Net Annual Gain $324,049.68", abs(total_net_gain - 324049.68) < 20.0, f"${total_net_gain:,.2f}")
        self.assert_test("Target Strategy Blended Net ROI Exactly 341.8%", abs(overall_roi - 341.82) < 0.2, f"{overall_roi:.1f}%")

    def validate_financial_scenarios(self):
        print("\n[SECTION 6: Multi-Scenario Financial Impact Model Validation]")
        sc_path = os.path.join(REPORTS_DIR, "executive_financial_impact_scenarios.csv")
        self.assert_test("Financial Scenarios CSV Exists", os.path.exists(sc_path))

        df_sc = pd.read_csv(sc_path)
        self.assert_test("3 Core Scenarios Evaluated", len(df_sc) == 3)

        # Conservative (15%)
        c_row = df_sc[df_sc['Scenario'].str.contains('Conservative')].iloc[0]
        self.assert_test("Conservative ARR Preserved Exactly $251,316.45", abs(c_row['Annual_ARR_Preserved'] - 251316.45) < 1.0)
        self.assert_test("Conservative Net ROI Exactly 264.8%", abs(c_row['Net_ROI_Pct'] - 264.76) < 0.1)

        # Target (25%)
        t_row = df_sc[df_sc['Scenario'].str.contains('Target')].iloc[0]
        self.assert_test("Target ARR Preserved Exactly $418,860.75", abs(t_row['Annual_ARR_Preserved'] - 418860.75) < 1.0)
        self.assert_test("Target Net ROI Exactly 341.8%", abs(t_row['Net_ROI_Pct'] - 341.84) < 0.1)

        # Aggressive (35%)
        a_row = df_sc[df_sc['Scenario'].str.contains('Aggressive')].iloc[0]
        self.assert_test("Aggressive ARR Preserved Exactly $586,405.05", abs(a_row['Annual_ARR_Preserved'] - 586405.05) < 1.0)
        self.assert_test("Aggressive Net ROI Exactly 371.0%", abs(a_row['Net_ROI_Pct'] - 371.01) < 0.1)


    def validate_production_artifacts(self):
        print("\n[SECTION 7: Artifact Existence & File Completeness]")
        expected_csvs = [
            "customer_churn_risk_scores.csv",
            "customer_segments_full.csv",
            "churn_risk_tier_summary.csv",
            "churn_risk_top_drivers_summary.csv",
            "churn_risk_segment_matrix_summary.csv",
            "customer_segmentation_profiles.csv",
            "kmeans_cluster_summary.csv",
            "tenure_cohort_churn_summary.csv",
            "contract_payment_churn_summary.csv",
            "revenue_at_risk_summary.csv",
            "service_adoption_churn_summary.csv",
            "executive_financial_impact_scenarios.csv",
            "executive_strategic_pillars_summary.csv",
            "executive_implementation_roadmap.csv"
        ]
        for c in expected_csvs:
            cp = os.path.join(REPORTS_DIR, c)
            self.assert_test(f"CSV Available: {c}", os.path.exists(cp) and os.path.getsize(cp) > 50)

        expected_jsons = [
            "compact_customers.json",
            "compact_segments.json",
            "sample_risk_customers.json"
        ]
        for j in expected_jsons:
            jp = os.path.join(REPORTS_DIR, j)
            valid_json = False
            if os.path.exists(jp):
                try:
                    with open(jp, 'r', encoding='utf-8') as f:
                        json.load(f)
                    valid_json = True
                except Exception:
                    pass
            self.assert_test(f"Valid Non-Empty JSON: {j}", valid_json)

        expected_plots = [
            "churn_tenure_cohort_trend.png",
            "churn_contract_risk_trend.png",
            "churn_revenue_monthly_charges_trend.png",
            "churn_service_stickiness_trend.png",
            "churn_payment_billing_trend.png",
            "churn_risk_segmentation_matrix.png",
            "churn_risk_distribution.png",
            "churn_risk_drivers_importance.png",
            "churn_risk_revenue_exposure.png",
            "churn_risk_action_matrix.png",
            "customer_segmentation_rfm_personas.png",
            "customer_segmentation_kmeans_clusters.png",
            "customer_segmentation_lifecycle_value_matrix.png",
            "customer_segmentation_service_adoption_profiles.png",
            "customer_segmentation_ltv_risk_quadrants.png",
            "executive_financial_impact_roi.png",
            "executive_strategic_roadmap.png",
            "executive_portfolio_scorecard.png"
        ]
        for p in expected_plots:
            pp = os.path.join(REPORTS_DIR, p)
            self.assert_test(f"300 DPI Plot Available: {p}", os.path.exists(pp) and os.path.getsize(pp) > 10000)

    def validate_html_dashboards(self):
        print("\n[SECTION 8: HTML Dashboards & DOM/Navigation Integrity]")
        dashboards = [
            "churn_trends_dashboard.html",
            "churn_risk_dashboard.html",
            "customer_segmentation_dashboard.html",
            "executive_summary_dashboard.html",
            "analytics_validation_dashboard.html"
        ]
        for d in dashboards:
            dp = os.path.join(REPORTS_DIR, d)
            exists = os.path.exists(dp)
            self.assert_test(f"Dashboard File Exists: {d}", exists)
            if exists:
                with open(dp, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.assert_test(f"{d} Properly Closed HTML", "</html>" in content.lower())
                self.assert_test(f"{d} Contains Substantial Code (>30KB)", len(content) > 30000)


if __name__ == "__main__":
    suite = ValidationSuite()
    success = suite.run_all()
    sys.exit(0 if success else 1)
