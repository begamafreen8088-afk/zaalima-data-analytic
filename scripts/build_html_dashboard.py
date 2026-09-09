"""
Compiler script to generate Reports/churn_risk_dashboard.html with embedded data and full interactivity.
"""

import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_DIR = os.path.join(BASE_DIR, "Reports")
compact_json_path = os.path.join(REPORTS_DIR, "compact_customers.json")

with open(compact_json_path, 'r') as f:
    compact_data = json.load(f)

json_str = json.dumps(compact_data)

html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Customer Churn Risk Dashboard & Retention Intelligence Suite</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-primary: #090d16;
      --bg-secondary: #0f172a;
      --bg-card: rgba(15, 23, 42, 0.78);
      --border-color: rgba(255, 255, 255, 0.08);
      --border-highlight: rgba(99, 102, 241, 0.4);
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      
      --critical-red: #ef4444;
      --critical-glow: rgba(239, 68, 68, 0.2);
      --high-orange: #f97316;
      --high-glow: rgba(249, 115, 22, 0.2);
      --medium-amber: #f59e0b;
      --medium-glow: rgba(245, 158, 11, 0.2);
      --low-emerald: #10b981;
      --low-glow: rgba(16, 185, 129, 0.2);
      
      --accent-indigo: #6366f1;
      --accent-cyan: #0ea5e9;
      --accent-purple: #a855f7;
      
      --font-sans: 'Inter', system-ui, -apple-system, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      background-color: var(--bg-primary);
      color: var(--text-main);
      font-family: var(--font-sans);
      line-height: 1.6;
      min-height: 100vh;
      overflow-x: hidden;
    }}

    /* Ambient Glow Spheres */
    .glow-sphere-1 {{
      position: fixed;
      top: -120px;
      right: 10%;
      width: 650px;
      height: 650px;
      background: radial-gradient(circle, rgba(239, 68, 68, 0.12) 0%, rgba(99, 102, 241, 0.05) 45%, transparent 70%);
      pointer-events: none;
      z-index: 0;
    }}

    .glow-sphere-2 {{
      position: fixed;
      bottom: -150px;
      left: 5%;
      width: 700px;
      height: 700px;
      background: radial-gradient(circle, rgba(14, 165, 233, 0.08) 0%, rgba(16, 185, 129, 0.03) 50%, transparent 70%);
      pointer-events: none;
      z-index: 0;
    }}

    .container {{
      max-width: 1440px;
      margin: 0 auto;
      padding: 2rem 2rem 5rem;
      position: relative;
      z-index: 1;
    }}

    /* Navigation Header */
    header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 2rem;
      border-bottom: 1px solid var(--border-color);
      padding-bottom: 1.6rem;
      flex-wrap: wrap;
      gap: 1.5rem;
    }}

    .header-left h1 {{
      font-size: 2.15rem;
      font-weight: 800;
      letter-spacing: -0.025em;
      background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 55%, #94a3b8 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      display: flex;
      align-items: center;
      gap: 0.75rem;
      flex-wrap: wrap;
    }}

    .badge-pill {{
      font-size: 0.72rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      font-weight: 700;
      padding: 0.3rem 0.75rem;
      border-radius: 9999px;
      background: rgba(239, 68, 68, 0.14);
      color: #f87171;
      border: 1px solid rgba(239, 68, 68, 0.3);
      -webkit-text-fill-color: initial;
    }}

    .badge-version {{
      background: rgba(99, 102, 241, 0.15);
      color: #a5b4fc;
      border-color: rgba(99, 102, 241, 0.3);
    }}

    .header-subtitle {{
      color: var(--text-muted);
      font-size: 0.96rem;
      margin-top: 0.4rem;
    }}

    .header-actions {{
      display: flex;
      align-items: center;
      gap: 0.85rem;
      flex-wrap: wrap;
    }}

    .btn {{
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      padding: 0.55rem 1.15rem;
      border-radius: 0.75rem;
      font-size: 0.86rem;
      font-weight: 600;
      text-decoration: none;
      cursor: pointer;
      transition: all 0.2s ease;
      border: 1px solid var(--border-color);
      background: rgba(255, 255, 255, 0.04);
      color: #e2e8f0;
    }}

    .btn:hover {{
      background: rgba(255, 255, 255, 0.08);
      border-color: rgba(255, 255, 255, 0.2);
      transform: translateY(-1px);
    }}

    .btn-primary {{
      background: var(--accent-indigo);
      border-color: var(--accent-indigo);
      color: #ffffff;
      box-shadow: 0 4px 14px rgba(99, 102, 241, 0.35);
    }}

    .btn-primary:hover {{
      background: #4f46e5;
      border-color: #4f46e5;
    }}

    .btn-switch {{
      background: rgba(14, 165, 233, 0.12);
      border-color: rgba(14, 165, 233, 0.3);
      color: #38bdf8;
    }}

    .btn-switch:hover {{
      background: rgba(14, 165, 233, 0.2);
      border-color: #38bdf8;
    }}

    /* KPI Cards Grid */
    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(215px, 1fr));
      gap: 1.15rem;
      margin-bottom: 2.2rem;
    }}

    .kpi-card {{
      background: var(--bg-card);
      backdrop-filter: blur(14px);
      border: 1px solid var(--border-color);
      border-radius: 1rem;
      padding: 1.3rem 1.25rem;
      position: relative;
      overflow: hidden;
      transition: all 0.25s ease;
    }}

    .kpi-card:hover {{
      transform: translateY(-3px);
      border-color: var(--border-highlight);
      box-shadow: 0 12px 28px -5px rgba(0, 0, 0, 0.6);
    }}

    .kpi-card::before {{
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 3px;
      background: var(--accent-color, var(--accent-indigo));
    }}

    .kpi-label {{
      font-size: 0.76rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-muted);
      font-weight: 600;
      margin-bottom: 0.35rem;
    }}

    .kpi-value {{
      font-size: 1.9rem;
      font-weight: 800;
      font-family: var(--font-mono);
      letter-spacing: -0.02em;
      margin-bottom: 0.35rem;
    }}

    .kpi-subtext {{
      font-size: 0.78rem;
      display: flex;
      align-items: center;
      gap: 0.4rem;
      color: var(--text-muted);
    }}

    .kpi-subtext span.dot {{
      font-size: 0.7rem;
    }}

    /* Navigation Tabs */
    .nav-tabs {{
      display: flex;
      gap: 0.55rem;
      overflow-x: auto;
      border-bottom: 1px solid var(--border-color);
      padding-bottom: 0.75rem;
      margin-bottom: 2rem;
    }}

    .nav-tab {{
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid var(--border-color);
      color: var(--text-muted);
      padding: 0.6rem 1.2rem;
      border-radius: 0.75rem;
      cursor: pointer;
      font-weight: 600;
      font-size: 0.88rem;
      white-space: nowrap;
      transition: all 0.2s ease;
    }}

    .nav-tab:hover {{
      color: #ffffff;
      background: rgba(255, 255, 255, 0.06);
    }}

    .nav-tab.active {{
      background: var(--accent-indigo);
      color: #ffffff;
      border-color: var(--accent-indigo);
      box-shadow: 0 4px 14px rgba(99, 102, 241, 0.35);
    }}

    /* Tab Content Panels */
    .tab-panel {{
      display: none;
      animation: fadeIn 0.3s ease-in-out forwards;
    }}

    .tab-panel.active {{
      display: block;
    }}

    @keyframes fadeIn {{
      from {{ opacity: 0; transform: translateY(6px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}

    /* Content Cards & Containers */
    .dashboard-section {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 1.25rem;
      padding: 2rem;
      margin-bottom: 2rem;
      backdrop-filter: blur(16px);
    }}

    .section-header {{
      margin-bottom: 1.6rem;
    }}

    .section-title {{
      font-size: 1.45rem;
      font-weight: 700;
      margin-bottom: 0.4rem;
      display: flex;
      align-items: center;
      gap: 0.6rem;
    }}

    .section-desc {{
      color: var(--text-muted);
      font-size: 0.94rem;
    }}

    /* Dual Column Layout */
    .grid-2col {{
      display: grid;
      grid-template-columns: 1.35fr 1fr;
      gap: 2rem;
      align-items: start;
    }}

    @media (max-width: 1060px) {{
      .grid-2col {{
        grid-template-columns: 1fr;
      }}
    }}

    .chart-frame {{
      background: rgba(0, 0, 0, 0.3);
      border: 1px solid var(--border-color);
      border-radius: 1rem;
      padding: 1rem;
      text-align: center;
      box-shadow: 0 4px 24px rgba(0, 0, 0, 0.45);
    }}

    .chart-frame img {{
      max-width: 100%;
      height: auto;
      border-radius: 0.75rem;
      display: block;
      margin: 0 auto;
    }}

    /* Insight List & Cards */
    .insight-list {{
      display: flex;
      flex-direction: column;
      gap: 1rem;
    }}

    .insight-box {{
      background: rgba(255, 255, 255, 0.025);
      border: 1px solid var(--border-color);
      border-radius: 0.85rem;
      padding: 1.2rem 1.25rem;
      border-left: 4px solid var(--accent-color, var(--accent-indigo));
    }}

    .insight-box h4 {{
      font-size: 0.98rem;
      font-weight: 700;
      margin-bottom: 0.4rem;
      color: #f1f5f9;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }}

    .insight-box p {{
      font-size: 0.87rem;
      color: #cbd5e1;
      line-height: 1.55;
    }}

    /* Tables */
    .table-container {{
      overflow-x: auto;
      border-radius: 0.85rem;
      border: 1px solid var(--border-color);
      margin-top: 1rem;
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.88rem;
      text-align: left;
    }}

    th {{
      background: rgba(30, 41, 59, 0.85);
      color: #94a3b8;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      padding: 0.8rem 1rem;
      font-size: 0.75rem;
    }}

    td {{
      padding: 0.85rem 1rem;
      border-bottom: 1px solid rgba(255, 255, 255, 0.04);
      color: #e2e8f0;
    }}

    tr:last-child td {{
      border-bottom: none;
    }}

    tr:hover td {{
      background: rgba(255, 255, 255, 0.02);
    }}

    /* Badges */
    .tier-badge {{
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      padding: 0.22rem 0.65rem;
      border-radius: 9999px;
      font-size: 0.74rem;
      font-weight: 700;
      font-family: var(--font-mono);
      white-space: nowrap;
    }}

    .tier-critical {{
      background: rgba(239, 68, 68, 0.15);
      color: #f87171;
      border: 1px solid rgba(239, 68, 68, 0.35);
    }}

    .tier-high {{
      background: rgba(249, 115, 22, 0.15);
      color: #fb923c;
      border: 1px solid rgba(249, 115, 22, 0.35);
    }}

    .tier-medium {{
      background: rgba(245, 158, 11, 0.15);
      color: #fbbf24;
      border: 1px solid rgba(245, 158, 11, 0.35);
    }}

    .tier-low {{
      background: rgba(16, 185, 129, 0.15);
      color: #34d399;
      border: 1px solid rgba(16, 185, 129, 0.35);
    }}

    .quad-badge {{
      display: inline-block;
      padding: 0.2rem 0.55rem;
      border-radius: 6px;
      font-size: 0.75rem;
      font-weight: 600;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--border-color);
    }}

    /* Interactive Explorer Controls */
    .filter-bar {{
      display: flex;
      flex-wrap: wrap;
      gap: 1rem;
      align-items: center;
      margin-bottom: 1.25rem;
      padding: 1.2rem;
      background: rgba(0, 0, 0, 0.25);
      border: 1px solid var(--border-color);
      border-radius: 0.85rem;
    }}

    .filter-group {{
      display: flex;
      flex-direction: column;
      gap: 0.35rem;
      flex: 1;
      min-width: 170px;
    }}

    .filter-group label {{
      font-size: 0.76rem;
      text-transform: uppercase;
      font-weight: 700;
      color: var(--text-muted);
      letter-spacing: 0.05em;
    }}

    .form-input, .form-select {{
      background: rgba(15, 23, 42, 0.9);
      border: 1px solid var(--border-color);
      border-radius: 0.6rem;
      padding: 0.55rem 0.85rem;
      color: #f1f5f9;
      font-size: 0.85rem;
      font-family: var(--font-sans);
      outline: none;
      transition: border-color 0.2s;
    }}

    .form-input:focus, .form-select:focus {{
      border-color: var(--accent-indigo);
      box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.25);
    }}

    /* Pagination */
    .pagination-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 1rem;
      padding-top: 1rem;
      border-top: 1px solid var(--border-color);
      font-size: 0.85rem;
      color: var(--text-muted);
    }}

    .pagination-buttons {{
      display: flex;
      gap: 0.5rem;
    }}

    /* Simulator Styles */
    .sim-card {{
      background: linear-gradient(135deg, rgba(99, 102, 241, 0.07) 0%, rgba(14, 165, 233, 0.04) 100%);
      border: 1px solid var(--border-highlight);
      border-radius: 1.25rem;
      padding: 2rem;
    }}

    .sim-layout {{
      display: grid;
      grid-template-columns: 1.2fr 1fr;
      gap: 2.2rem;
    }}

    @media (max-width: 950px) {{
      .sim-layout {{
        grid-template-columns: 1fr;
      }}
    }}

    .sim-form {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1.2rem;
    }}

    .sim-control-full {{
      grid-column: 1 / -1;
    }}

    .sim-result-panel {{
      background: rgba(0, 0, 0, 0.4);
      border: 1px solid var(--border-color);
      border-radius: 1rem;
      padding: 1.8rem;
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      justify-content: center;
    }}

    .gauge-wrapper {{
      position: relative;
      width: 200px;
      height: 120px;
      margin: 1rem auto;
    }}

    .gauge-svg {{
      width: 200px;
      height: 120px;
    }}

    .gauge-score {{
      position: absolute;
      bottom: 5px;
      left: 0;
      width: 100%;
      text-align: center;
      font-size: 2.2rem;
      font-weight: 800;
      font-family: var(--font-mono);
    }}

    .roi-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 1rem;
      margin-top: 1.5rem;
      width: 100%;
    }}

    .roi-stat-box {{
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid var(--border-color);
      border-radius: 0.75rem;
      padding: 1rem;
      text-align: center;
    }}

    .roi-stat-val {{
      font-size: 1.6rem;
      font-weight: 800;
      font-family: var(--font-mono);
      color: var(--low-emerald);
      margin-top: 0.25rem;
    }}

    /* Modal */
    .modal-overlay {{
      display: none;
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.75);
      backdrop-filter: blur(8px);
      z-index: 100;
      align-items: center;
      justify-content: center;
    }}

    .modal-overlay.active {{
      display: flex;
    }}

    .modal-card {{
      background: #0f172a;
      border: 1px solid var(--border-highlight);
      border-radius: 1.25rem;
      width: 90%;
      max-width: 600px;
      padding: 2rem;
      position: relative;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.8);
      animation: modalIn 0.25s ease-out;
    }}

    @keyframes modalIn {{
      from {{ opacity: 0; transform: scale(0.95); }}
      to {{ opacity: 1; transform: scale(1); }}
    }}

    .modal-close {{
      position: absolute;
      top: 1.25rem;
      right: 1.25rem;
      background: transparent;
      border: none;
      color: var(--text-muted);
      font-size: 1.4rem;
      cursor: pointer;
    }}

    .modal-close:hover {{
      color: #fff;
    }}

    /* Progress bar in table */
    .risk-bar-container {{
      width: 100%;
      background: rgba(255, 255, 255, 0.06);
      height: 6px;
      border-radius: 3px;
      overflow: hidden;
      margin-top: 0.35rem;
    }}

    .risk-bar-fill {{
      height: 100%;
      border-radius: 3px;
    }}

    /* Footer */
    footer {{
      text-align: center;
      margin-top: 4rem;
      padding-top: 2rem;
      border-top: 1px solid var(--border-color);
      color: var(--text-muted);
      font-size: 0.85rem;
    }}
  </style>
</head>
<body>
  <div class="glow-sphere-1"></div>
  <div class="glow-sphere-2"></div>

  <div class="container">
    <!-- Header -->
    <header>
      <div class="header-left">
        <h1>
          Customer Churn Risk Intelligence Suite
          <span class="badge-pill">Week 4 Day 2 Active</span>
          <span class="badge-pill badge-version">ML Model: Logistic + RF LTV</span>
        </h1>
        <p class="header-subtitle">
          Real-time Customer Risk Scoring, Hazard Drivers, High-Value Financial Exposure & Prescriptive Intervention Playbooks
        </p>
      </div>
      <div class="header-actions">
        <a href="churn_trends_dashboard.html" class="btn btn-switch" title="Switch to Historical Trend Diagnostic Dashboard">
          <span>📈</span> Churn Trends Dashboard
        </a>
        <button onclick="window.print()" class="btn" title="Print Executive Briefing">
          <span>🖨️</span> Print Report
        </button>
        <button onclick="exportTableToCSV()" class="btn btn-primary" title="Export Current Customer Roster as CSV">
          <span>📥</span> Export Roster CSV
        </button>
      </div>
    </header>

    <!-- Top KPI Grid -->
    <div class="kpi-grid">
      <div class="kpi-card" style="--accent-color: var(--critical-red);">
        <div class="kpi-label">Portfolio Mean Churn Risk</div>
        <div class="kpi-value" style="color: var(--critical-red);">26.51%</div>
        <div class="kpi-subtext">
          <span class="dot" style="color: var(--critical-red);">●</span> Overall portfolio baseline probability
        </div>
      </div>

      <div class="kpi-card" style="--accent-color: var(--high-orange);">
        <div class="kpi-label">Critical & High Risk Accounts</div>
        <div class="kpi-value" style="color: var(--high-orange);">1,754</div>
        <div class="kpi-subtext">
          <span class="dot" style="color: var(--high-orange);">●</span> 24.9% of total customer base (≥45% risk)
        </div>
      </div>

      <div class="kpi-card" style="--accent-color: var(--critical-red);">
        <div class="kpi-label">Expected MRR Exposure</div>
        <div class="kpi-value" style="color: #f87171;">$139.6k</div>
        <div class="kpi-subtext">
          <span class="dot" style="color: #f87171);">●</span> 30.6% of portfolio monthly recurring revenue
        </div>
      </div>

      <div class="kpi-card" style="--accent-color: var(--accent-indigo);">
        <div class="kpi-label">Immediate Intervention VIPs</div>
        <div class="kpi-value" style="color: #a5b4fc;">1,286</div>
        <div class="kpi-subtext">
          <span class="dot" style="color: #a5b4fc);">●</span> High spend + high risk ($78.1k/mo loss)
        </div>
      </div>

      <div class="kpi-card" style="--accent-color: var(--critical-red);">
        <div class="kpi-label">Annualized Risk Run-Rate</div>
        <div class="kpi-value" style="color: #fda4af;">$1.68M</div>
        <div class="kpi-subtext">
          <span class="dot" style="color: #fda4af);">●</span> Cumulative 12-month value at risk
        </div>
      </div>

      <div class="kpi-card" style="--accent-color: var(--low-emerald);">
        <div class="kpi-label">Preservable MRR (Target)</div>
        <div class="kpi-value" style="color: var(--low-emerald);">+$34.8k</div>
        <div class="kpi-subtext">
          <span class="dot" style="color: var(--low-emerald);">●</span> 25% intervention recovery opportunity
        </div>
      </div>
    </div>

    <!-- Navigation Tabs -->
    <div class="nav-tabs">
      <button class="nav-tab active" onclick="switchTab('overview')">📊 Executive Risk Overview</button>
      <button class="nav-tab" onclick="switchTab('drivers')">⚡ Risk Drivers & Moats</button>
      <button class="nav-tab" onclick="switchTab('revenue')">💰 Revenue & LTV Exposure</button>
      <button class="nav-tab" onclick="switchTab('matrix')">🎯 2x2 Retention Matrix</button>
      <button class="nav-tab" onclick="switchTab('explorer')">🔍 Live Customer Explorer</button>
      <button class="nav-tab" onclick="switchTab('simulator')">🎛️ Real-Time Risk Simulator</button>
      <button class="nav-tab" onclick="switchTab('roi')">🚀 Campaign ROI Planner</button>
      <button class="nav-tab" onclick="switchTab('playbook')">📋 Operational SLA Playbook</button>
    </div>

    <!-- TAB 1: Executive Overview -->
    <div id="tab-overview" class="tab-panel active">
      <div class="dashboard-section">
        <div class="section-header">
          <h2 class="section-title">Macro Risk Distribution & Calibration Synthesis</h2>
          <p class="section-desc">Distribution of model-predicted customer churn probabilities and empirical calibration against real-world attrition.</p>
        </div>

        <div class="grid-2col">
          <div class="chart-frame">
            <img src="churn_risk_distribution.png" alt="Churn Risk Score Distribution">
          </div>

          <div class="insight-list">
            <div class="insight-box" style="--accent-color: var(--critical-red);">
              <h4><span>⚠️</span> The 66.7% Risk Concentration</h4>
              <p>Just <strong>24.9% of accounts (1,754 customers)</strong> in the Critical (≥70%) and High (45-70%) tiers account for <strong>$93,197/mo (66.7%)</strong> of all monthly churn risk exposure. Interventions must aggressively concentrate resources here.</p>
            </div>

            <div class="insight-box" style="--accent-color: var(--high-orange);">
              <h4><span>🎯</span> 96.3% Model Precision in Critical Tier</h4>
              <p>Accounts scoring in the Critical Risk tier (812 accounts) exhibit an actual churn rate of <strong>96.3%</strong>. This near-certain attrition validates the machine learning classifier's ability to trigger automated triage before account cancellation.</p>
            </div>

            <div class="insight-box" style="--accent-color: var(--low-emerald);">
              <h4><span>🛡️</span> The 61.0% Low-Risk Protective Core</h4>
              <p>4,294 accounts (61.0% of portfolio) maintain churn probabilities below 25%, experiencing a tiny 3.2% churn rate. This core generates $248.1k in safe monthly cash flows.</p>
            </div>

            <div class="table-container">
              <table>
                <thead>
                  <tr>
                    <th>Risk Tier</th>
                    <th>Accounts</th>
                    <th>% Base</th>
                    <th>Avg Prob</th>
                    <th>Actual Churn</th>
                    <th>Total MRR</th>
                    <th>Expected Loss</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><span class="tier-badge tier-critical">Critical (≥70%)</span></td>
                    <td><strong>812</strong></td>
                    <td>11.5%</td>
                    <td>79.4%</td>
                    <td><strong style="color: var(--critical-red);">96.3%</strong></td>
                    <td>$66,254</td>
                    <td><strong style="color: var(--critical-red);">$52,754/mo</strong></td>
                  </tr>
                  <tr>
                    <td><span class="tier-badge tier-high">High (45–70%)</span></td>
                    <td><strong>942</strong></td>
                    <td>13.4%</td>
                    <td>57.4%</td>
                    <td><strong style="color: var(--high-orange);">73.0%</strong></td>
                    <td>$70,275</td>
                    <td><strong style="color: var(--high-orange);">$40,443/mo</strong></td>
                  </tr>
                  <tr>
                    <td><span class="tier-badge tier-medium">Medium (25–45%)</span></td>
                    <td><strong>995</strong></td>
                    <td>14.1%</td>
                    <td>34.0%</td>
                    <td>26.2%</td>
                    <td>$71,498</td>
                    <td>$24,364/mo</td>
                  </tr>
                  <tr>
                    <td><span class="tier-badge tier-low">Low (<25%)</span></td>
                    <td><strong>4,294</strong></td>
                    <td>61.0%</td>
                    <td>8.0%</td>
                    <td><strong style="color: var(--low-emerald);">3.2%</strong></td>
                    <td>$248,090</td>
                    <td>$22,059/mo</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 2: Risk Drivers & Moats -->
    <div id="tab-drivers" class="tab-panel">
      <div class="dashboard-section">
        <div class="section-header">
          <h2 class="section-title">Top Hazard Catalysts & Protective Moats</h2>
          <p class="section-desc">Quantified feature impact on customer churn probability, isolating structural vulnerabilities and defensible retention moats.</p>
        </div>

        <div class="grid-2col">
          <div class="chart-frame">
            <img src="churn_risk_drivers_importance.png" alt="Risk Drivers and Moats">
          </div>

          <div class="insight-list">
            <div class="insight-box" style="--accent-color: var(--critical-red);">
              <h4><span>🔥</span> Month-to-Month Contract: +36.1% Hazard Surge</h4>
              <p>Customers on month-to-month contracts average a <strong>42.7% churn probability</strong>, compared to only 6.7% for customers on fixed 1- or 2-year commitments. Contract flexibility is the primary gateway to attrition.</p>
            </div>

            <div class="insight-box" style="--accent-color: var(--high-orange);">
              <h4><span>🛡️</span> Security & Tech Support: Over 30% Risk Deficit</h4>
              <p>Customers lacking Online Security and Tech Support suffer a <strong>+30.7% and +30.0% surge in churn risk</strong>. These support add-ons serve as defensive buffers against early cancellation.</p>
            </div>

            <div class="insight-box" style="--accent-color: var(--accent-cyan);">
              <h4><span>💳</span> Electronic Check Payment Friction: +28.8% Risk</h4>
              <p>Electronic Check customers average a <strong>45.6% churn risk</strong>, compared to 16.8% for automated credit card and bank transfer payers. Manual monthly billing forces an active renewal decision each billing cycle.</p>
            </div>

            <div class="insight-box" style="--accent-color: var(--low-emerald);">
              <h4><span>🔒</span> Two-Year Commitment: -23.7% Protective Moat</h4>
              <p>A Two-Year contract reduces customer churn probability down to <strong>2.8%</strong> (a 23.7% net drop against portfolio baseline), securing predictable multi-year cash flows.</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 3: Revenue & LTV Exposure -->
    <div id="tab-revenue" class="tab-panel">
      <div class="dashboard-section">
        <div class="section-header">
          <h2 class="section-title">Financial Exposure & Projected Value-at-Risk</h2>
          <p class="section-desc">Quantification of monthly recurring revenue (MRR) and estimated customer lifetime value (LTV) across calibrated risk tiers.</p>
        </div>

        <div class="grid-2col">
          <div class="chart-frame">
            <img src="churn_risk_revenue_exposure.png" alt="Revenue Exposure">
          </div>

          <div class="insight-list">
            <div class="insight-box" style="--accent-color: var(--critical-red);">
              <h4><span>💸</span> Critical Tier Drains $52,754/mo</h4>
              <p>The 812 critical risk accounts alone account for <strong>$52.8k/mo in expected lost revenue</strong> (79.6% of their total segment MRR). Because churn probability is 79.4%, this revenue is projected to vanish within 60 days without emergency outreach.</p>
            </div>

            <div class="insight-box" style="--accent-color: var(--high-orange);">
              <h4><span>📈</span> Combined Monthly Burn: $139,620.25</h4>
              <p>Across the full 7,043 account portfolio, expected churn losses reach <strong>$139,620/mo</strong>, representing <strong>30.6% of the company's total monthly billing</strong> ($456,116.60 MRR).</p>
            </div>

            <div class="insight-box" style="--accent-color: var(--accent-indigo);">
              <h4><span>💎</span> High-ARPU Exposure in Top Brackets</h4>
              <p>Customers paying >$80/mo produce over 62% of all expected revenue losses. When high-ARPU fiber customers churn, the loss per account is nearly 4x higher than standard voice/DSL accounts.</p>
            </div>

            <div class="insight-box" style="--accent-color: var(--low-emerald);">
              <h4><span>🎯</span> 12-Month LTV Protection Target</h4>
              <p>Targeting the top 500 highest-value at-risk accounts preserves an estimated <strong>$720,000+ in multi-year lifetime value</strong> for less than $40,000 in proactive retention incentives.</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 4: 2x2 Retention Matrix -->
    <div id="tab-matrix" class="tab-panel">
      <div class="dashboard-section">
        <div class="section-header">
          <h2 class="section-title">2x2 Churn Risk & Account Value Action Matrix</h2>
          <p class="section-desc">Segmenting customer accounts into four actionable quadrants based on Revenue Contribution (Monthly Charges) and Attrition Propensity (Risk Score).</p>
        </div>

        <div class="grid-2col">
          <div class="chart-frame">
            <img src="churn_risk_action_matrix.png" alt="Retention Action Matrix">
          </div>

          <div class="insight-list">
            <div class="insight-box" style="--accent-color: var(--critical-red);">
              <h4><span>🚨</span> Immediate Intervention (1,286 accounts | $78.1k/mo lost)</h4>
              <p><strong>High Value + High Risk:</strong> These premium accounts generate $113.2k/mo in MRR but have an average 69.1% churn risk. Represents <strong>55.9% of all lost revenue</strong>. Requires 1-on-1 account executive outreach, contract migration subsidies, and complimentary support bundles.</p>
            </div>

            <div class="insight-box" style="--accent-color: var(--high-orange);">
              <h4><span>🤖</span> Automated Nurture (468 accounts | $15.1k/mo lost)</h4>
              <p><strong>Standard Value + High Risk:</strong> Lower ARPU ($49.82/mo) with high churn risk (63.6%). High-touch calls are cost-inefficient here; automated digital email/SMS re-engagement drip campaigns and self-service discount offers are recommended.</p>
            </div>

            <div class="insight-box" style="--accent-color: var(--low-emerald);">
              <h4><span>👑</span> Core VIP Protect (2,238 accounts | $205.9k/mo safe)</h4>
              <p><strong>High Value + Low Risk:</strong> Our most valuable, loyal foundation ($92.02/mo ARPU, 15.9% risk). Prioritize relationship nurturing, VIP loyalty rewards, free speed boosts, and early beta access to prevent competitor poaching.</p>
            </div>

            <div class="insight-box" style="--accent-color: var(--accent-indigo);">
              <h4><span>🌱</span> Low Maintenance (3,051 accounts | $113.6k/mo safe)</h4>
              <p><strong>Standard Value + Low Risk:</strong> Highly stable base (10.6% risk). Keep cost-to-serve low with digital self-service, standard communications, and cross-selling broadband speed upgrades.</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 5: Live Customer Explorer -->
    <div id="tab-explorer" class="tab-panel">
      <div class="dashboard-section">
        <div class="section-header">
          <h2 class="section-title">Live Filterable Customer Risk Explorer</h2>
          <p class="section-desc">Search, filter, and drill into individual customer risk profiles, financial exposures, and prescriptive retention actions.</p>
        </div>

        <!-- Filter Controls -->
        <div class="filter-bar">
          <div class="filter-group">
            <label for="searchInput">Search Customer ID</label>
            <input type="text" id="searchInput" class="form-input" placeholder="e.g. 7590-VHVEG" onkeyup="filterCustomers()">
          </div>

          <div class="filter-group">
            <label for="tierFilter">Risk Tier</label>
            <select id="tierFilter" class="form-select" onchange="filterCustomers()">
              <option value="ALL">All Tiers (250 Sample)</option>
              <option value="Critical Risk">Critical Risk (≥70%)</option>
              <option value="High Risk">High Risk (45–70%)</option>
              <option value="Medium Risk">Medium Risk (25–45%)</option>
              <option value="Low Risk">Low Risk (<25%)</option>
            </select>
          </div>

          <div class="filter-group">
            <label for="contractFilter">Contract Type</label>
            <select id="contractFilter" class="form-select" onchange="filterCustomers()">
              <option value="ALL">All Contracts</option>
              <option value="Month-to-month">Month-to-month</option>
              <option value="One year">One year</option>
              <option value="Two year">Two year</option>
            </select>
          </div>

          <div class="filter-group">
            <label for="quadFilter">Action Quadrant</label>
            <select id="quadFilter" class="form-select" onchange="filterCustomers()">
              <option value="ALL">All Quadrants</option>
              <option value="Immediate Intervention">Immediate Intervention</option>
              <option value="Core VIP Protect">Core VIP Protect</option>
              <option value="Automated Nurture">Automated Nurture</option>
              <option value="Low Maintenance">Low Maintenance</option>
            </select>
          </div>
        </div>

        <!-- Customer Data Table -->
        <div class="table-container">
          <table id="customerTable">
            <thead>
              <tr>
                <th>Customer ID</th>
                <th>Tenure</th>
                <th>Monthly Charge</th>
                <th>Contract</th>
                <th>Internet</th>
                <th>Payment Method</th>
                <th>Risk Score</th>
                <th>Risk Tier</th>
                <th>Expected Loss</th>
                <th>Action Playbook</th>
              </tr>
            </thead>
            <tbody id="customerTableBody">
              <!-- Rendered via JS -->
            </tbody>
          </table>
        </div>

        <!-- Pagination Controls -->
        <div class="pagination-bar">
          <div id="tableInfo">Showing 1 to 15 of 250 records</div>
          <div class="pagination-buttons">
            <button id="prevBtn" class="btn" onclick="prevPage()">Previous</button>
            <button id="nextBtn" class="btn" onclick="nextPage()">Next</button>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 6: Real-Time Risk Simulator -->
    <div id="tab-simulator" class="tab-panel">
      <div class="dashboard-section sim-card">
        <div class="section-header">
          <h2 class="section-title">Interactive Customer Risk & LTV Profiler</h2>
          <p class="section-desc">Test hypothetical customer scenarios in real time using the calibrated logistic model weights to assess churn probability and prescribe retention actions.</p>
        </div>

        <div class="sim-layout">
          <!-- Form Inputs -->
          <div class="sim-form">
            <div class="filter-group sim-control-full">
              <label for="simTenure">Customer Tenure: <strong id="simTenureVal" style="color:#a5b4fc;">6 Months</strong></label>
              <input type="range" id="simTenure" min="0" max="72" value="6" oninput="runSimulation()">
            </div>

            <div class="filter-group sim-control-full">
              <label for="simCharges">Monthly Charges: <strong id="simChargesVal" style="color:#a5b4fc;">$85 / mo</strong></label>
              <input type="range" id="simCharges" min="18" max="120" value="85" oninput="runSimulation()">
            </div>

            <div class="filter-group">
              <label for="simContract">Contract Type</label>
              <select id="simContract" class="form-select" onchange="runSimulation()">
                <option value="m2m" selected>Month-to-month</option>
                <option value="1yr">One year</option>
                <option value="2yr">Two year</option>
              </select>
            </div>

            <div class="filter-group">
              <label for="simInternet">Internet Service</label>
              <select id="simInternet" class="form-select" onchange="runSimulation()">
                <option value="fiber" selected>Fiber optic</option>
                <option value="dsl">DSL</option>
                <option value="none">No Internet</option>
              </select>
            </div>

            <div class="filter-group">
              <label for="simTech">Tech Support</label>
              <select id="simTech" class="form-select" onchange="runSimulation()">
                <option value="no" selected>No Support</option>
                <option value="yes">Subscribed (Yes)</option>
              </select>
            </div>

            <div class="filter-group">
              <label for="simSecurity">Online Security</label>
              <select id="simSecurity" class="form-select" onchange="runSimulation()">
                <option value="no" selected>No Security</option>
                <option value="yes">Subscribed (Yes)</option>
              </select>
            </div>

            <div class="filter-group">
              <label for="simPayment">Payment Method</label>
              <select id="simPayment" class="form-select" onchange="runSimulation()">
                <option value="echeck" selected>Electronic check</option>
                <option value="mail">Mailed check</option>
                <option value="bank">Bank transfer (auto)</option>
                <option value="card">Credit card (auto)</option>
              </select>
            </div>

            <div class="filter-group">
              <label for="simBilling">Paperless Billing</label>
              <select id="simBilling" class="form-select" onchange="runSimulation()">
                <option value="yes" selected>Paperless (Yes)</option>
                <option value="no">Paper Billing (No)</option>
              </select>
            </div>
          </div>

          <!-- Dynamic Result Gauge -->
          <div class="sim-result-panel">
            <h3 style="font-size: 1.1rem; color: #cbd5e1; margin-bottom: 0.2rem;">Predicted Churn Probability</h3>
            
            <div class="gauge-wrapper">
              <svg class="gauge-svg" viewBox="0 0 200 110">
                <path d="M 20 100 A 80 80 0 0 1 180 100" fill="none" stroke="#1e293b" stroke-width="18" stroke-linecap="round"/>
                <path id="gaugePath" d="M 20 100 A 80 80 0 0 1 180 100" fill="none" stroke="var(--critical-red)" stroke-width="18" stroke-dasharray="251.3" stroke-dashoffset="50" stroke-linecap="round"/>
              </svg>
              <div id="simScoreText" class="gauge-score" style="color: var(--critical-red);">78.4%</div>
            </div>

            <div id="simTierBadge" class="tier-badge tier-critical" style="margin-bottom: 1.2rem; font-size: 0.85rem; padding: 0.35rem 1rem;">
              Critical Risk Tier
            </div>

            <div class="roi-grid" style="margin-top: 0.5rem;">
              <div class="roi-stat-box">
                <div class="kpi-label">Expected MRR Loss</div>
                <div id="simExpectedLoss" class="roi-stat-val" style="color: var(--critical-red);">$66.64</div>
              </div>
              <div class="roi-stat-box">
                <div class="kpi-label">Estimated LTV</div>
                <div id="simLtv" class="roi-stat-val" style="color: #38bdf8;">$1,020</div>
              </div>
            </div>

            <div id="simActionBox" class="insight-box" style="margin-top: 1.4rem; width: 100%; text-align: left; --accent-color: var(--critical-red);">
              <h4 id="simActionTitle">Action Required</h4>
              <p id="simActionDesc">VIP Concierge Call: Offer 1-year contract migration with free Tech Support and $10/mo discount.</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 7: Campaign ROI Planner -->
    <div id="tab-roi" class="tab-panel">
      <div class="dashboard-section sim-card">
        <div class="section-header">
          <h2 class="section-title">Portfolio Retention Campaign ROI Simulator</h2>
          <p class="section-desc">Model targeted organizational interventions across the 7,043 customer portfolio to calculate preserved revenue and campaign ROI.</p>
        </div>

        <div class="sim-layout">
          <div class="sim-form">
            <div class="filter-group sim-control-full">
              <label for="roiM2M">Month-to-Month Contract Conversion Rate: <strong id="roiM2MVal" style="color:#a5b4fc;">15%</strong></label>
              <input type="range" id="roiM2M" min="0" max="50" value="15" oninput="runRoiSim()">
              <span style="font-size: 0.76rem; color: var(--text-muted);">Migrate M2M customers to 1-Year or 2-Year commitments</span>
            </div>

            <div class="filter-group sim-control-full">
              <label for="roiTech">Fiber Support Bundle Adoption Rate: <strong id="roiTechVal" style="color:#a5b4fc;">20%</strong></label>
              <input type="range" id="roiTech" min="0" max="50" value="20" oninput="runRoiSim()">
              <span style="font-size: 0.76rem; color: var(--text-muted);">Incentivize high-ARPU Fiber users to add Tech Support</span>
            </div>

            <div class="filter-group sim-control-full">
              <label for="roiAutopay">Electronic Check Autopay Migration: <strong id="roiAutopayVal" style="color:#a5b4fc;">25%</strong></label>
              <input type="range" id="roiAutopay" min="0" max="50" value="25" oninput="runRoiSim()">
              <span style="font-size: 0.76rem; color: var(--text-muted);">Transition manual check payers to automatic credit card/bank billing</span>
            </div>

            <div class="filter-group sim-control-full">
              <label for="roiBudget">Retention Incentive Budget Per Account: <strong id="roiBudgetVal" style="color:#a5b4fc;">$15</strong></label>
              <input type="range" id="roiBudget" min="5" max="50" value="15" step="5" oninput="runRoiSim()">
              <span style="font-size: 0.76rem; color: var(--text-muted);">Bill credit, promotional discount, or hardware voucher</span>
            </div>
          </div>

          <div class="sim-result-panel">
            <h3 style="font-size: 1.1rem; color: #cbd5e1; margin-bottom: 1rem;">Projected Retention Impact & Return</h3>

            <div class="roi-grid">
              <div class="roi-stat-box">
                <div class="kpi-label">Accounts Saved / Mo</div>
                <div id="roiSavedAccts" class="roi-stat-val" style="color: #38bdf8;">184 accts</div>
              </div>
              <div class="roi-stat-box">
                <div class="kpi-label">Monthly MRR Preserved</div>
                <div id="roiSavedMrr" class="roi-stat-val" style="color: var(--low-emerald);">$14,250</div>
              </div>
              <div class="roi-stat-box">
                <div class="kpi-label">Annualized Revenue Saved</div>
                <div id="roiAnnualSaved" class="roi-stat-val" style="color: var(--low-emerald);">$171,000</div>
              </div>
              <div class="roi-stat-box">
                <div class="kpi-label">Net Campaign ROI</div>
                <div id="roiRatio" class="roi-stat-val" style="color: #f59e0b;">9.3x</div>
              </div>
            </div>

            <div class="insight-box" style="margin-top: 1.5rem; width: 100%; text-align: left; --accent-color: var(--low-emerald);">
              <h4><span>💡</span> Business Case Summary</h4>
              <p id="roiSummaryText">
                Investing $18,400 in targeted customer retention incentives prevents 184 customer cancellations per month, returning <strong>$171,000 in preserved annual top-line revenue</strong> at a <strong>9.3x return on investment</strong>.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 8: Operational SLA Playbook -->
    <div id="tab-playbook" class="tab-panel">
      <div class="dashboard-section">
        <div class="section-header">
          <h2 class="section-title">Departmental SLA & Retention Action Playbook</h2>
          <p class="section-desc">Structured operational workflows for Customer Success, Marketing, and Billing to execute targeted churn mitigation.</p>
        </div>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem;">
          <div class="insight-box" style="--accent-color: var(--critical-red); background: rgba(239, 68, 68, 0.03);">
            <h4 style="color: #f87171;">Tier 1: Customer Success (24-Hour SLA)</h4>
            <p><strong>Target:</strong> Immediate Intervention Quadrant (High ARPU, Risk ≥ 70%)</p>
            <ul style="margin: 0.8rem 0 0 1.2rem; font-size: 0.86rem; color: #cbd5e1; line-height: 1.6;">
              <li>Dedicated Account Manager assigned within 24 business hours.</li>
              <li>Outreach call using Script A: Network quality satisfaction review.</li>
              <li>Offer 12-month commitment discount: $10/mo bill reduction + free Tech Support.</li>
              <li>Escalate recurring technical trouble tickets directly to Tier 2 Engineering.</li>
            </ul>
          </div>

          <div class="insight-box" style="--accent-color: var(--high-orange); background: rgba(249, 115, 22, 0.03);">
            <h4 style="color: #fb923c;">Tier 2: Growth & Lifecycle Marketing</h4>
            <p><strong>Target:</strong> Automated Nurture Quadrant & Month-to-Month Accounts</p>
            <ul style="margin: 0.8rem 0 0 1.2rem; font-size: 0.86rem; color: #cbd5e1; line-height: 1.6;">
              <li>Automated 3-part email/SMS re-engagement drip triggering at Day 45 of tenure.</li>
              <li>Complimentary 60-day trial of Online Security and Cloud Backup.</li>
              <li>In-app popups offering $50 gift card for converting to 1-year contract.</li>
              <li>Interactive broadband speed test with one-click support ticket creation.</li>
            </ul>
          </div>

          <div class="insight-box" style="--accent-color: var(--accent-cyan); background: rgba(14, 165, 233, 0.03);">
            <h4 style="color: #38bdf8;">Tier 3: Billing & Payments Optimization</h4>
            <p><strong>Target:</strong> Electronic Check & Paperless Billing Accounts</p>
            <ul style="margin: 0.8rem 0 0 1.2rem; font-size: 0.86rem; color: #cbd5e1; line-height: 1.6;">
              <li>Prominently display "$10 Autopay Welcome Credit" on customer billing portal.</li>
              <li>SMS reminder 48 hours before monthly bill due date with 1-tap card setup.</li>
              <li>Remove paperless friction: Include clear payment breakdown in PDF receipts.</li>
              <li>Implement grace period reminders prior to sending service suspension notices.</li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- Customer Detail Modal -->
    <div id="customerModal" class="modal-overlay" onclick="closeModal(event)">
      <div class="modal-card" onclick="event.stopPropagation()">
        <button class="modal-close" onclick="closeModal()">&times;</button>
        <h3 id="modalTitle" style="font-size: 1.3rem; margin-bottom: 0.4rem; color: #fff;">Customer Profile: 7590-VHVEG</h3>
        <div id="modalTierBadge" class="tier-badge tier-critical" style="margin-bottom: 1.2rem;">Critical Risk Tier</div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.8rem; font-size: 0.88rem; margin-bottom: 1.4rem;">
          <div><span style="color: var(--text-muted);">Tenure:</span> <strong id="modalTenure">1 Month</strong></div>
          <div><span style="color: var(--text-muted);">Monthly Charges:</span> <strong id="modalCharges">$70.35</strong></div>
          <div><span style="color: var(--text-muted);">Contract:</span> <strong id="modalContract">Month-to-month</strong></div>
          <div><span style="color: var(--text-muted);">Internet:</span> <strong id="modalInternet">Fiber optic</strong></div>
          <div><span style="color: var(--text-muted);">Payment:</span> <strong id="modalPayment">Electronic check</strong></div>
          <div><span style="color: var(--text-muted);">Expected Loss:</span> <strong id="modalLoss" style="color: var(--critical-red);">$55.20/mo</strong></div>
        </div>

        <div class="insight-box" style="--accent-color: var(--accent-indigo); background: rgba(99, 102, 241, 0.08);">
          <h4 style="color: #a5b4fc;">Prescribed Retention Playbook</h4>
          <p id="modalAction" style="font-size: 0.9rem; margin-top: 0.35rem;"></p>
        </div>

        <div style="display: flex; justify-content: flex-end; gap: 0.8rem; margin-top: 1.5rem;">
          <button class="btn" onclick="closeModal()">Close</button>
          <button class="btn btn-primary" onclick="alert('Ticket created for Customer Success team!')">Create CS Retention Ticket</button>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <footer>
      <p>Customer Churn Prediction & Lifetime Value (LTV) Engine • Week 4 Day 2 Churn Risk Intelligence Suite</p>
      <p style="margin-top: 0.35rem; font-size: 0.78rem;">Dataset: Telco Customer Churn (7,043 Accounts) • Models: Scikit-Learn Logistic Regression & Random Forest LTV</p>
    </footer>
  </div>

  <!-- Embedded Customer Dataset -->
  <script>
    const CUSTOMER_DATA = {json_str};

    // Tab Switching
    function switchTab(tabId) {{
      document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
      document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
      
      const targetPanel = document.getElementById('tab-' + tabId);
      if (targetPanel) targetPanel.classList.add('active');
      
      const activeBtn = Array.from(document.querySelectorAll('.nav-tab')).find(b => 
        b.getAttribute('onclick').includes(tabId)
      );
      if (activeBtn) activeBtn.classList.add('active');
    }}

    // Customer Explorer Table Logic
    let filteredData = [...CUSTOMER_DATA];
    let currentPage = 1;
    const pageSize = 15;

    function renderTable() {{
      const tbody = document.getElementById('customerTableBody');
      tbody.innerHTML = '';

      const start = (currentPage - 1) * pageSize;
      const end = start + pageSize;
      const pageRecords = filteredData.slice(start, end);

      pageRecords.forEach(c => {{
        const tr = document.createElement('tr');
        
        let tierClass = 'tier-low';
        let barColor = 'var(--low-emerald)';
        if (c.tier === 'Critical Risk') {{ tierClass = 'tier-critical'; barColor = 'var(--critical-red)'; }}
        else if (c.tier === 'High Risk') {{ tierClass = 'tier-high'; barColor = 'var(--high-orange)'; }}
        else if (c.tier === 'Medium Risk') {{ tierClass = 'tier-medium'; barColor = 'var(--medium-amber)'; }}

        tr.innerHTML = `
          <td><strong style="font-family: var(--font-mono); color: #cbd5e1;">${{c.id}}</strong></td>
          <td>${{c.tenure}} mo</td>
          <td>$${{parseFloat(c.charges).toFixed(2)}}</td>
          <td><span style="font-size:0.8rem;">${{c.contract}}</span></td>
          <td>${{c.internet}}</td>
          <td><span style="font-size:0.78rem; color: var(--text-muted);">${{c.payment}}</span></td>
          <td>
            <strong style="color: ${{barColor}};">${{c.risk}}%</strong>
            <div class="risk-bar-container">
              <div class="risk-bar-fill" style="width: ${{c.risk}}%; background: ${{barColor}};"></div>
            </div>
          </td>
          <td><span class="tier-badge ${{tierClass}}">${{c.tier}}</span></td>
          <td><strong style="color: #f87171;">$${{parseFloat(c.loss).toFixed(2)}}</strong></td>
          <td>
            <button class="btn" style="padding: 0.3rem 0.65rem; font-size: 0.74rem;" onclick="viewCustomerModal('${{c.id}}')">
              View Playbook
            </button>
          </td>
        `;
        tbody.appendChild(tr);
      }});

      // Update Pagination Bar
      const total = filteredData.length;
      const pageCount = Math.ceil(total / pageSize) || 1;
      document.getElementById('tableInfo').textContent = `Showing ${{total === 0 ? 0 : start + 1}} to ${{Math.min(end, total)}} of ${{total}} accounts`;
      document.getElementById('prevBtn').disabled = currentPage === 1;
      document.getElementById('nextBtn').disabled = currentPage >= pageCount;
    }}

    function filterCustomers() {{
      const search = document.getElementById('searchInput').value.trim().toLowerCase();
      const tier = document.getElementById('tierFilter').value;
      const contract = document.getElementById('contractFilter').value;
      const quad = document.getElementById('quadFilter').value;

      filteredData = CUSTOMER_DATA.filter(c => {{
        const matchesSearch = !search || c.id.toLowerCase().includes(search);
        const matchesTier = tier === 'ALL' || c.tier === tier;
        const matchesContract = contract === 'ALL' || c.contract === contract;
        const matchesQuad = quad === 'ALL' || c.quad === quad;
        return matchesSearch && matchesTier && matchesContract && matchesQuad;
      }});

      currentPage = 1;
      renderTable();
    }}

    function prevPage() {{
      if (currentPage > 1) {{
        currentPage--;
        renderTable();
      }}
    }}

    function nextPage() {{
      const pageCount = Math.ceil(filteredData.length / pageSize);
      if (currentPage < pageCount) {{
        currentPage++;
        renderTable();
      }}
    }}

    // Export Current Filtered Table to CSV
    function exportTableToCSV() {{
      if (filteredData.length === 0) {{
        alert('No data to export.');
        return;
      }}
      const headers = ['CustomerID', 'Tenure', 'MonthlyCharges', 'Contract', 'InternetService', 'PaymentMethod', 'ChurnRiskScore', 'RiskTier', 'ExpectedMonthlyLoss', 'ActionQuadrant', 'RecommendedAction'];
      let csvContent = headers.join(',') + '\\n';
      
      filteredData.forEach(c => {{
        const row = [
          c.id, c.tenure, c.charges, `"${{c.contract}}"`, `"${{c.internet}}"`,
          `"${{c.payment}}"`, c.risk, `"${{c.tier}}"`, c.loss,
          `"${{c.quad}}"`, `"${{c.action.replace(/"/g, '""')}}"`
        ];
        csvContent += row.join(',') + '\\n';
      }});

      const blob = new Blob([csvContent], {{ type: 'text/csv;charset=utf-8;' }});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `churn_risk_roster_${{new Date().toISOString().slice(0,10)}}.csv`;
      a.click();
    }}

    // Customer Detail Modal
    function viewCustomerModal(customerId) {{
      const customer = CUSTOMER_DATA.find(c => c.id === customerId);
      if (!customer) return;

      document.getElementById('modalTitle').textContent = `Customer Profile: ${{customer.id}}`;
      document.getElementById('modalTenure').textContent = `${{customer.tenure}} Months`;
      document.getElementById('modalCharges').textContent = `$${{parseFloat(customer.charges).toFixed(2)}} / mo`;
      document.getElementById('modalContract').textContent = customer.contract;
      document.getElementById('modalInternet').textContent = customer.internet;
      document.getElementById('modalPayment').textContent = customer.payment;
      document.getElementById('modalLoss').textContent = `$${{parseFloat(customer.loss).toFixed(2)}} / mo`;
      document.getElementById('modalAction').textContent = customer.action;

      const badge = document.getElementById('modalTierBadge');
      badge.textContent = `${{customer.tier}} (${{customer.risk}}% Churn Risk)`;
      badge.className = 'tier-badge';
      if (customer.tier === 'Critical Risk') badge.classList.add('tier-critical');
      else if (customer.tier === 'High Risk') badge.classList.add('tier-high');
      else if (customer.tier === 'Medium Risk') badge.classList.add('tier-medium');
      else badge.classList.add('tier-low');

      document.getElementById('customerModal').classList.add('active');
    }}

    function closeModal(e) {{
      document.getElementById('customerModal').classList.remove('active');
    }}

    // Real-Time Simulator Logic
    function runSimulation() {{
      const tenure = parseFloat(document.getElementById('simTenure').value);
      const charges = parseFloat(document.getElementById('simCharges').value);
      const contract = document.getElementById('simContract').value;
      const internet = document.getElementById('simInternet').value;
      const tech = document.getElementById('simTech').value;
      const security = document.getElementById('simSecurity').value;
      const payment = document.getElementById('simPayment').value;
      const billing = document.getElementById('simBilling').value;

      document.getElementById('simTenureVal').textContent = `${{tenure}} Months`;
      document.getElementById('simChargesVal').textContent = `$${{charges}} / mo`;

      // Logistic regression formula based on model coefficients
      let z = -1.15;
      
      // Tenure impact
      z += -0.042 * tenure;
      
      // Charges impact
      z += 0.012 * (charges - 64.7);

      // Contract
      if (contract === 'm2m') z += 1.65;
      else if (contract === '1yr') z += -0.45;
      else if (contract === '2yr') z += -1.60;

      // Internet
      if (internet === 'fiber') z += 0.85;
      else if (internet === 'dsl') z += -0.15;
      else z += -0.80;

      // Services
      if (tech === 'no') z += 0.40;
      else z += -0.35;

      if (security === 'no') z += 0.35;
      else z += -0.30;

      // Payment
      if (payment === 'echeck') z += 0.65;
      else if (payment === 'mail') z += 0.10;
      else z += -0.45;

      if (billing === 'yes') z += 0.25;

      // Calculate Probability
      let prob = 1 / (1 + Math.exp(-z));
      prob = Math.max(0.01, Math.min(0.98, prob));
      const score = Math.round(prob * 1000) / 10;

      document.getElementById('simScoreText').textContent = `${{score}}%`;

      // Update Gauge SVG Arc
      // Total arc length = 251.3
      const offset = 251.3 * (1 - (score / 100));
      const gaugePath = document.getElementById('gaugePath');
      gaugePath.style.strokeDashoffset = offset;

      let tierName = 'Low Risk Tier';
      let tierClass = 'tier-low';
      let color = 'var(--low-emerald)';
      let actionTitle = 'Standard Account Care';
      let actionDesc = 'Customer is stable. Maintain standard engagement and feature updates.';

      if (score >= 70) {{
        tierName = 'Critical Risk Tier';
        tierClass = 'tier-critical';
        color = 'var(--critical-red)';
        actionTitle = 'Immediate High-Touch Retention Required';
        actionDesc = 'Customer has imminent cancellation risk. Deploy CS Manager call, offer 1-year contract migration with free Tech Support and $10/mo credit.';
      }} else if (score >= 45) {{
        tierName = 'High Risk Tier';
        tierClass = 'tier-high';
        color = 'var(--high-orange)';
        actionTitle = 'Proactive Retention Campaign';
        actionDesc = 'Elevated attrition risk. Send targeted contract lock-in offer and complimentary 60-day Online Security bundle.';
      }} else if (score >= 25) {{
        tierName = 'Medium Risk Tier';
        tierClass = 'tier-medium';
        color = 'var(--medium-amber)';
        actionTitle = 'Digital Re-engagement Drip';
        actionDesc = 'Customer is vulnerable to competitor poaching. Deploy automated email series highlighting network upgrades and autopay incentive.';
      }}

      gaugePath.style.stroke = color;
      document.getElementById('simScoreText').style.color = color;

      const badge = document.getElementById('simTierBadge');
      badge.textContent = tierName;
      badge.className = `tier-badge ${{tierClass}}`;

      const expectedLoss = Math.round(charges * prob * 100) / 100;
      document.getElementById('simExpectedLoss').textContent = `$${{expectedLoss.toFixed(2)}}`;
      document.getElementById('simExpectedLoss').style.color = color;

      const estLtv = Math.round(charges * Math.max(tenure, 14) * (1 - (prob * 0.5)));
      document.getElementById('simLtv').textContent = `$${{estLtv.toLocaleString()}}`;

      document.getElementById('simActionTitle').textContent = actionTitle;
      document.getElementById('simActionDesc').textContent = actionDesc;
      document.getElementById('simActionBox').style.setProperty('--accent-color', color);
    }}

    // Portfolio Retention ROI Planner
    function runRoiSim() {{
      const m2mRate = parseFloat(document.getElementById('roiM2M').value) / 100;
      const techRate = parseFloat(document.getElementById('roiTech').value) / 100;
      const autopayRate = parseFloat(document.getElementById('roiAutopay').value) / 100;
      const budgetPerAcc = parseFloat(document.getElementById('roiBudget').value);

      document.getElementById('roiM2MVal').textContent = `${{Math.round(m2mRate * 100)}}%`;
      document.getElementById('roiTechVal').textContent = `${{Math.round(techRate * 100)}}%`;
      document.getElementById('roiAutopayVal').textContent = `${{Math.round(autopayRate * 100)}}%`;
      document.getElementById('roiBudgetVal').textContent = `$${{budgetPerAcc}}`;

      // Portfolio assumptions based on actual data
      // M2M accounts = 3,875 with 42.7% churn (1,655 churners/mo)
      const m2mSaved = 3875 * m2mRate * 0.31;
      
      // Fiber accounts lacking tech support = 2,246 with 45.3% churn
      const techSaved = 2246 * techRate * 0.26;
      
      // Electronic check accounts = 2,365 with 45.3% churn
      const autopaySaved = 2365 * autopayRate * 0.28;

      const totalSaved = Math.round(m2mSaved + techSaved + autopaySaved);
      const avgMrr = 74.5;
      const monthlyMrrSaved = Math.round(totalSaved * avgMrr);
      const annualSaved = monthlyMrrSaved * 12;

      const totalCampaignCost = Math.round(totalSaved * budgetPerAcc * 6); // 6 months incentive
      const roiRatio = totalCampaignCost > 0 ? Math.round((annualSaved / totalCampaignCost) * 10) / 10 : 0;

      document.getElementById('roiSavedAccts').textContent = `${{totalSaved.toLocaleString()}} accts`;
      document.getElementById('roiSavedMrr').textContent = `$${{monthlyMrrSaved.toLocaleString()}}`;
      document.getElementById('roiAnnualSaved').textContent = `$${{annualSaved.toLocaleString()}}`;
      document.getElementById('roiRatio').textContent = `${{roiRatio}}x`;

      document.getElementById('roiSummaryText').innerHTML = `
        Investing <strong>$${{totalCampaignCost.toLocaleString()}}</strong> in targeted customer retention incentives prevents 
        <strong>${{totalSaved.toLocaleString()}} customer cancellations</strong> per month, returning 
        <strong style="color: var(--low-emerald);">$${{annualSaved.toLocaleString()}} in preserved annual top-line revenue</strong> at a 
        <strong>${{roiRatio}}x return on investment</strong>.
      `;
    }}

    // Initialize Dashboard
    document.addEventListener('DOMContentLoaded', () => {{
      renderTable();
      runSimulation();
      runRoiSim();
    }});
  </script>
</body>
</html>
"""

out_html_path = os.path.join(REPORTS_DIR, "churn_risk_dashboard.html")
with open(out_html_path, 'w', encoding='utf-8') as f:
    f.write(html_template)

print(f"Successfully compiled churn risk dashboard to: {out_html_path}")
print(f"File size: {os.path.getsize(out_html_path):,} bytes")
