"""
Builder script to generate Reports/customer_segmentation_dashboard.html
Customer Churn Prediction & Lifetime Value (LTV) Engine - Week 4 Day 3
"""

import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_DIR = os.path.join(BASE_DIR, "Reports")
compact_json_path = os.path.join(REPORTS_DIR, "compact_segments.json")

if os.path.exists(compact_json_path):
    with open(compact_json_path, 'r') as f:
        compact_data = json.load(f)
else:
    compact_data = []

json_str = json.dumps(compact_data)

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Customer Segmentation & Behavioral Intelligence Suite</title>
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
      --high-orange: #f97316;
      --medium-amber: #f59e0b;
      --low-emerald: #10b981;
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

    .glow-sphere-1 {{
      position: fixed;
      top: -120px;
      right: 10%;
      width: 650px;
      height: 650px;
      background: radial-gradient(circle, rgba(168, 85, 247, 0.12) 0%, rgba(99, 102, 241, 0.05) 45%, transparent 70%);
      pointer-events: none;
      z-index: 0;
    }}

    .glow-sphere-2 {{
      position: fixed;
      bottom: -150px;
      left: 5%;
      width: 700px;
      height: 700px;
      background: radial-gradient(circle, rgba(16, 185, 129, 0.08) 0%, rgba(14, 165, 233, 0.04) 50%, transparent 70%);
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

    header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      flex-wrap: wrap;
      gap: 1.5rem;
      margin-bottom: 2.2rem;
      padding-bottom: 1.8rem;
      border-bottom: 1px solid var(--border-color);
    }}

    .header-left h1 {{
      font-size: 2.1rem;
      font-weight: 800;
      letter-spacing: -0.03em;
      background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 50%, #94a3b8 100%);
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
      background: rgba(168, 85, 247, 0.15);
      color: #c084fc;
      border: 1px solid rgba(168, 85, 247, 0.3);
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
      gap: 0.75rem;
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
      background: var(--accent-purple);
      border-color: var(--accent-purple);
      color: #ffffff;
      box-shadow: 0 4px 14px rgba(168, 85, 247, 0.35);
    }}

    .btn-primary:hover {{
      background: #9333ea;
      border-color: #9333ea;
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

    .btn-danger {{
      background: rgba(239, 68, 68, 0.12);
      border-color: rgba(239, 68, 68, 0.3);
      color: #f87171;
    }}

    .btn-danger:hover {{
      background: rgba(239, 68, 68, 0.2);
      border-color: #f87171;
    }}

    /* KPI Grid */
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
      font-size: 1.85rem;
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

    /* Tabs */
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
      background: var(--accent-purple);
      color: #ffffff;
      border-color: var(--accent-purple);
      box-shadow: 0 4px 14px rgba(168, 85, 247, 0.35);
    }}

    /* Tab Content */
    .tab-panel {{
      display: none;
      animation: fadeIn 0.3s ease;
    }}

    .tab-panel.active {{
      display: block;
    }}

    @keyframes fadeIn {{
      from {{ opacity: 0; transform: translateY(6px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}

    /* Dashboard Layouts */
    .dashboard-section {{
      background: var(--bg-card);
      backdrop-filter: blur(14px);
      border: 1px solid var(--border-color);
      border-radius: 1.25rem;
      padding: 2rem;
      margin-bottom: 2rem;
    }}

    .section-header {{
      margin-bottom: 1.6rem;
    }}

    .section-title {{
      font-size: 1.35rem;
      font-weight: 700;
      color: #ffffff;
      letter-spacing: -0.01em;
    }}

    .section-desc {{
      color: var(--text-muted);
      font-size: 0.9rem;
      margin-top: 0.25rem;
    }}

    .chart-box {{
      background: rgba(0, 0, 0, 0.35);
      border: 1px solid var(--border-color);
      border-radius: 1rem;
      padding: 1.25rem;
      display: flex;
      justify-content: center;
      align-items: center;
      margin-bottom: 1.5rem;
      overflow: hidden;
    }}

    .chart-box img {{
      max-width: 100%;
      height: auto;
      border-radius: 0.5rem;
      transition: transform 0.2s ease;
    }}

    .grid-2col {{
      display: grid;
      grid-template-columns: 1.15fr 1fr;
      gap: 1.8rem;
    }}

    @media (max-width: 1024px) {{
      .grid-2col {{
        grid-template-columns: 1fr;
      }}
    }}

    /* Persona Cards Grid */
    .persona-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 1.25rem;
      margin-top: 1.5rem;
    }}

    .persona-card {{
      background: rgba(15, 23, 42, 0.9);
      border: 1px solid var(--border-color);
      border-radius: 1rem;
      padding: 1.4rem;
      border-top: 4px solid var(--accent-color, #94a3b8);
      position: relative;
    }}

    .persona-title {{
      font-size: 1.05rem;
      font-weight: 700;
      color: #ffffff;
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 0.6rem;
    }}

    .persona-badge {{
      font-size: 0.7rem;
      font-weight: 700;
      padding: 0.2rem 0.6rem;
      border-radius: 9999px;
      text-transform: uppercase;
      background: rgba(255, 255, 255, 0.08);
    }}

    .persona-desc {{
      font-size: 0.85rem;
      color: var(--text-muted);
      margin-bottom: 1rem;
      line-height: 1.5;
    }}

    .persona-stats {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 0.75rem;
      background: rgba(0, 0, 0, 0.25);
      padding: 0.85rem;
      border-radius: 0.6rem;
      font-size: 0.82rem;
    }}

    .persona-stat-item label {{
      display: block;
      color: var(--text-muted);
      font-size: 0.72rem;
      text-transform: uppercase;
    }}

    .persona-stat-item span {{
      font-weight: 700;
      font-family: var(--font-mono);
      font-size: 0.95rem;
      color: #f1f5f9;
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
      font-size: 0.86rem;
      text-align: left;
    }}

    th {{
      background: rgba(15, 23, 42, 0.95);
      color: var(--text-muted);
      font-weight: 700;
      text-transform: uppercase;
      font-size: 0.74rem;
      letter-spacing: 0.05em;
      padding: 0.85rem 1rem;
      border-bottom: 1px solid var(--border-color);
    }}

    td {{
      padding: 0.75rem 1rem;
      border-bottom: 1px solid rgba(255, 255, 255, 0.04);
      color: #e2e8f0;
    }}

    tr:hover td {{
      background: rgba(255, 255, 255, 0.02);
    }}

    /* Explorer Filters */
    .filter-bar {{
      display: flex;
      flex-wrap: wrap;
      gap: 1rem;
      margin-bottom: 1.5rem;
      background: rgba(0, 0, 0, 0.3);
      padding: 1.2rem;
      border-radius: 0.85rem;
      border: 1px solid var(--border-color);
    }}

    .filter-item {{
      flex: 1;
      min-width: 180px;
      display: flex;
      flex-direction: column;
      gap: 0.35rem;
    }}

    .filter-item label {{
      font-size: 0.74rem;
      text-transform: uppercase;
      font-weight: 700;
      color: var(--text-muted);
    }}

    .form-control {{
      background: rgba(15, 23, 42, 0.95);
      border: 1px solid var(--border-color);
      border-radius: 0.55rem;
      padding: 0.55rem 0.85rem;
      color: #ffffff;
      font-size: 0.85rem;
      outline: none;
      font-family: var(--font-sans);
    }}

    .form-control:focus {{
      border-color: var(--accent-purple);
      box-shadow: 0 0 0 2px rgba(168, 85, 247, 0.25);
    }}

    /* Pagination */
    .pagination-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 1.2rem;
      font-size: 0.85rem;
      color: var(--text-muted);
    }}

    .btn-sm {{
      padding: 0.35rem 0.75rem;
      font-size: 0.8rem;
    }}

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
          Customer Segmentation & Behavioral Analytics
          <span class="badge-pill">Week 4 Day 3 Milestone</span>
          <span class="badge-pill badge-version">ML: K-Means (k=4) + PCA 2D</span>
        </h1>
        <p class="header-subtitle">
          RFM Behavioral Personas, Unsupervised ML Clusters, Lifecycle × Value Cross-Tabulations & Tailored Retention Strategies
        </p>
      </div>

      <div class="header-actions">
        <a href="churn_trends_dashboard.html" class="btn btn-switch" title="View Churn Trend Reports">
          <span>📈</span> Churn Trends
        </a>
        <a href="churn_risk_dashboard.html" class="btn btn-danger" title="View Predictive Churn Risk Dashboard">
          <span>⚠️</span> Churn Risk Dashboard
        </a>
        <button onclick="window.print()" class="btn" title="Print Report">
          <span>🖨️</span> Print
        </button>
        <button onclick="exportSegmentsCSV()" class="btn btn-primary" title="Export Full Segments CSV">
          <span>📥</span> Export Segments CSV
        </button>
      </div>
    </header>

    <!-- Top KPI Grid -->
    <div class="kpi-grid">
      <div class="kpi-card" style="--accent-color: var(--accent-purple);">
        <div class="kpi-label">Strategic Personas</div>
        <div class="kpi-value" style="color: #c084fc;">6 Personas</div>
        <div class="kpi-subtext">
          <span class="dot" style="color: #c084fc;">●</span> 7,043 Accounts Classified
        </div>
      </div>

      <div class="kpi-card" style="--accent-color: var(--low-emerald);">
        <div class="kpi-label">Champions & VIP Loyalists</div>
        <div class="kpi-value" style="color: var(--low-emerald);">1,405</div>
        <div class="kpi-subtext">
          <span class="dot" style="color: var(--low-emerald);">●</span> 19.9% base | $131.5k MRR | 3.6% Churn
        </div>
      </div>

      <div class="kpi-card" style="--accent-color: var(--critical-red);">
        <div class="kpi-label">At-Risk High Rollers</div>
        <div class="kpi-value" style="color: var(--critical-red);">811</div>
        <div class="kpi-subtext">
          <span class="dot" style="color: var(--critical-red);">●</span> $48.1k/mo MRR At Risk (84.1% Churn)
        </div>
      </div>

      <div class="kpi-card" style="--accent-color: var(--high-orange);">
        <div class="kpi-label">Vulnerable Newcomers</div>
        <div class="kpi-value" style="color: var(--high-orange);">894</div>
        <div class="kpi-subtext">
          <span class="dot" style="color: var(--high-orange);">●</span> $43.4k/mo MRR At Risk (79.8% Churn)
        </div>
      </div>

      <div class="kpi-card" style="--accent-color: var(--accent-indigo);">
        <div class="kpi-label">ML Clusters (K-Means)</div>
        <div class="kpi-value" style="color: #a5b4fc;">4 Clusters</div>
        <div class="kpi-subtext">
          <span class="dot" style="color: #a5b4fc;">●</span> 91.1% PCA 2D Explained Variance
        </div>
      </div>

      <div class="kpi-card" style="--accent-color: var(--accent-cyan);">
        <div class="kpi-label">Enterprise Moats (C-B)</div>
        <div class="kpi-value" style="color: var(--accent-cyan);">$5,936</div>
        <div class="kpi-subtext">
          <span class="dot" style="color: var(--accent-cyan);">●</span> Mean LTV across 1,533 long-term VIPs
        </div>
      </div>
    </div>

    <!-- Navigation Tabs -->
    <div class="nav-tabs">
      <button class="nav-tab active" onclick="switchTab('personas')">👥 Behavioral RFM Personas</button>
      <button class="nav-tab" onclick="switchTab('kmeans')">🤖 K-Means Clustering & PCA</button>
      <button class="nav-tab" onclick="switchTab('lifecycle')">🗺️ Lifecycle × Spend Matrix</button>
      <button class="nav-tab" onclick="switchTab('services')">🛠️ Service Stickiness</button>
      <button class="nav-tab" onclick="switchTab('portfolio')">🎯 LTV vs. Churn Hazard Matrix</button>
      <button class="nav-tab" onclick="switchTab('explorer')">🔍 Interactive Segment Explorer</button>
      <button class="nav-tab" onclick="switchTab('playbooks')">📋 Retention Playbooks</button>
    </div>

    <!-- TAB 1: Behavioral RFM Personas -->
    <div id="tab-personas" class="tab-panel active">
      <div class="dashboard-section">
        <div class="section-header">
          <h2 class="section-title">Strategic RFM & Behavioral Personas</h2>
          <p class="section-desc">Multi-dimensional segmentation classifying customer accounts by tenure longevity, ARPU, service breadth, and churn propensity.</p>
        </div>

        <div class="chart-box">
          <img src="customer_segmentation_rfm_personas.png" alt="Customer Segmentation RFM Personas">
        </div>

        <!-- Persona Cards -->
        <div class="persona-grid">
          <div class="persona-card" style="--accent-color: #10b981;">
            <div class="persona-title">
              <span>Champions & VIP Loyalists</span>
              <span class="persona-badge" style="color: #10b981;">Ultra High Value</span>
            </div>
            <p class="persona-desc">Tenure &ge;36 months, premium monthly spend (&ge;$70/mo), low churn risk (&lt;25%). Multi-product adoption creates strong structural moats.</p>
            <div class="persona-stats">
              <div class="persona-stat-item"><label>Accounts</label><span>1,405 (19.9%)</span></div>
              <div class="persona-stat-item"><label>Avg ARPU</label><span>$93.62/mo</span></div>
              <div class="persona-stat-item"><label>Churn Rate</label><span style="color: #10b981;">3.56%</span></div>
              <div class="persona-stat-item"><label>Total MRR</label><span>$131,532/mo</span></div>
            </div>
          </div>

          <div class="persona-card" style="--accent-color: #ef4444;">
            <div class="persona-title">
              <span>At-Risk High Rollers</span>
              <span class="persona-badge" style="color: #ef4444;">Highest Hazard</span>
            </div>
            <p class="persona-desc">Paying premium rates (&ge;$70/mo) but operating on month-to-month terms without protective tech support or security add-ons. 84.1% churn rate.</p>
            <div class="persona-stats">
              <div class="persona-stat-item"><label>Accounts</label><span>811 (11.5%)</span></div>
              <div class="persona-stat-item"><label>Avg ARPU</label><span>$90.86/mo</span></div>
              <div class="persona-stat-item"><label>Churn Rate</label><span style="color: #ef4444;">84.09%</span></div>
              <div class="persona-stat-item"><label>MRR At Risk</label><span style="color: #ef4444;">$48,143/mo</span></div>
            </div>
          </div>

          <div class="persona-card" style="--accent-color: #f97316;">
            <div class="persona-title">
              <span>Vulnerable Newcomers</span>
              <span class="persona-badge" style="color: #f97316;">Critical Flight Risk</span>
            </div>
            <p class="persona-desc">Subscribed &le;6 months on month-to-month contracts with acute initial friction. 79.8% churn rate within first 180 days.</p>
            <div class="persona-stats">
              <div class="persona-stat-item"><label>Accounts</label><span>894 (12.7%)</span></div>
              <div class="persona-stat-item"><label>Avg ARPU</label><span>$67.93/mo</span></div>
              <div class="persona-stat-item"><label>Churn Rate</label><span style="color: #f97316;">79.75%</span></div>
              <div class="persona-stat-item"><label>MRR At Risk</label><span style="color: #f97316;">$43,365/mo</span></div>
            </div>
          </div>

          <div class="persona-card" style="--accent-color: #a855f7;">
            <div class="persona-title">
              <span>Digital Enthusiasts & Streamers</span>
              <span class="persona-badge" style="color: #a855f7;">Growth Engine</span>
            </div>
            <p class="persona-desc">Fiber optic subscribers with heavy Streaming TV & Movies adoption (&ge;4 services). High ARPU with moderate churn (20.4%).</p>
            <div class="persona-stats">
              <div class="persona-stat-item"><label>Accounts</label><span>407 (5.8%)</span></div>
              <div class="persona-stat-item"><label>Avg ARPU</label><span>$99.14/mo</span></div>
              <div class="persona-stat-item"><label>Churn Rate</label><span style="color: #a855f7;">20.39%</span></div>
              <div class="persona-stat-item"><label>Total MRR</label><span>$40,350/mo</span></div>
            </div>
          </div>

          <div class="persona-card" style="--accent-color: #0ea5e9;">
            <div class="persona-title">
              <span>Budget Anchors</span>
              <span class="persona-badge" style="color: #0ea5e9;">Stable Foundation</span>
            </div>
            <p class="persona-desc">Price-conscious long-tenure customers (&ge;24m) spending &lt;$45/mo on DSL or basic phone lines. Near-zero churn rate (1.69%).</p>
            <div class="persona-stats">
              <div class="persona-stat-item"><label>Accounts</label><span>945 (13.4%)</span></div>
              <div class="persona-stat-item"><label>Avg ARPU</label><span>$24.13/mo</span></div>
              <div class="persona-stat-item"><label>Churn Rate</label><span style="color: #0ea5e9;">1.69%</span></div>
              <div class="persona-stat-item"><label>Total MRR</label><span>$22,804/mo</span></div>
            </div>
          </div>

          <div class="persona-card" style="--accent-color: #6366f1;">
            <div class="persona-title">
              <span>Core Steady Subscribers</span>
              <span class="persona-badge" style="color: #6366f1;">Mainstream Core</span>
            </div>
            <p class="persona-desc">The backbone of portfolio revenue. Moderate tenure, balanced monthly fees ($49/mo), and reliable cash flow with low-to-moderate churn (12.6%).</p>
            <div class="persona-stats">
              <div class="persona-stat-item"><label>Accounts</label><span>2,581 (36.6%)</span></div>
              <div class="persona-stat-item"><label>Avg ARPU</label><span>$49.21/mo</span></div>
              <div class="persona-stat-item"><label>Churn Rate</label><span style="color: #6366f1;">12.59%</span></div>
              <div class="persona-stat-item"><label>Total MRR</label><span>$127,008/mo</span></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 2: K-Means Clustering & PCA -->
    <div id="tab-kmeans" class="tab-panel">
      <div class="dashboard-section">
        <div class="section-header">
          <h2 class="section-title">Unsupervised K-Means Machine Learning Clustering & PCA Space</h2>
          <p class="section-desc">Mathematical clustering based on standardized multidimensional coordinates, validated by Elbow Inertia, Silhouette Analysis, and 2D Principal Component Projection.</p>
        </div>

        <div class="chart-box">
          <img src="customer_segmentation_kmeans_clusters.png" alt="K-Means Clusters and PCA">
        </div>

        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th>Cluster Name</th>
                <th>Account Volume</th>
                <th>Avg Tenure</th>
                <th>Avg Monthly Spend</th>
                <th>Avg Churn Risk</th>
                <th>Mean LTV</th>
                <th>Primary Strategic Imperative</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong style="color: #ef4444;">Cluster A: High-Churn Flight Risks</strong></td>
                <td>1,733 accounts</td>
                <td>8.6 months</td>
                <td>$75.66/mo</td>
                <td><strong style="color: #ef4444;">65.1%</strong></td>
                <td>$708</td>
                <td>Urgent SLA outreach, contract subsidies & security bundling</td>
              </tr>
              <tr>
                <td><strong style="color: #10b981;">Cluster B: High-Value Enterprise Moats</strong></td>
                <td>1,533 accounts</td>
                <td>62.4 months</td>
                <td>$95.54/mo</td>
                <td><strong style="color: #10b981;">13.7%</strong></td>
                <td><strong style="color: #10b981;">$5,936</strong></td>
                <td>VIP Concierge loyalty perks, hardware upgrade prioritisation</td>
              </tr>
              <tr>
                <td><strong style="color: #0ea5e9;">Cluster C: Low-Cost Basic Loyalists</strong></td>
                <td>2,158 accounts</td>
                <td>26.8 months</td>
                <td>$27.42/mo</td>
                <td>10.9%</td>
                <td>$682</td>
                <td>Low-touch automated support; cross-sell broadband/streaming</td>
              </tr>
              <tr>
                <td><strong style="color: #a855f7;">Cluster D: Mid-Tier Digital Mainstream</strong></td>
                <td>1,619 accounts</td>
                <td>36.8 months</td>
                <td>$73.72/mo</td>
                <td>18.1%</td>
                <td>$2,627</td>
                <td>Speed boosts & autopay enrollment incentives</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- TAB 3: Lifecycle × Spend Matrix -->
    <div id="tab-lifecycle" class="tab-panel">
      <div class="dashboard-section">
        <div class="section-header">
          <h2 class="section-title">Customer Lifecycle Stage &times; Spend Tier Matrix Heatmaps</h2>
          <p class="section-desc">Cross-tabulation heatmaps isolating account volume concentration, empirical churn percentage, and monthly revenue loss exposure.</p>
        </div>

        <div class="chart-box">
          <img src="customer_segmentation_lifecycle_value_matrix.png" alt="Lifecycle Value Matrix">
        </div>

        <div class="grid-2col" style="margin-top: 1.5rem;">
          <div style="background: rgba(0,0,0,0.25); padding: 1.25rem; border-radius: 0.85rem; border: 1px solid var(--border-color);">
            <h4 style="color: #f87171; margin-bottom: 0.5rem;">⚠️ The High-ARPU Early Tenure Trap</h4>
            <p style="font-size: 0.88rem; color: var(--text-muted);">
              Customers in the <strong>New (0-12m) cohort paying Premium (&gt;$90/mo)</strong> suffer an empirical churn rate exceeding <strong>68.4%</strong>. When premium buyers encounter onboarding friction or price-to-value disconnects early, they exit immediately, causing the largest single revenue leak in the portfolio.
            </p>
          </div>
          <div style="background: rgba(0,0,0,0.25); padding: 1.25rem; border-radius: 0.85rem; border: 1px solid var(--border-color);">
            <h4 style="color: #34d399; margin-bottom: 0.5rem;">🛡️ The Veteran Retention Moat</h4>
            <p style="font-size: 0.88rem; color: var(--text-muted);">
              Across all spend tiers, customer churn drops below <strong>7.5% once customers pass month 48</strong>. Even in the highest spend tier (&gt;$90/mo), veteran accounts maintain a 92%+ retention rate, proving that long-tenure habituation and multi-product integration create virtually impenetrable retention moats.
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 4: Service Stickiness -->
    <div id="tab-services" class="tab-panel">
      <div class="dashboard-section">
        <div class="section-header">
          <h2 class="section-title">Service Ecosystem Penetration & Technology Stickiness</h2>
          <p class="section-desc">Evaluating how value-added add-ons (Tech Support, Online Security, Streaming, Device Protection) build retention barriers across personas.</p>
        </div>

        <div class="chart-box">
          <img src="customer_segmentation_service_adoption_profiles.png" alt="Service Adoption Profiles">
        </div>

        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th>Behavioral Persona</th>
                <th>Tech Support</th>
                <th>Online Security</th>
                <th>Device Protection</th>
                <th>Online Backup</th>
                <th>Fiber Optic</th>
                <th>Streaming TV</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong style="color: #10b981;">Champions & VIP Loyalists</strong></td>
                <td>68.2%</td>
                <td>69.8%</td>
                <td>74.1%</td>
                <td>72.5%</td>
                <td>61.4%</td>
                <td>78.9%</td>
              </tr>
              <tr>
                <td><strong style="color: #a855f7;">Digital Enthusiasts & Streamers</strong></td>
                <td>41.5%</td>
                <td>39.8%</td>
                <td>68.3%</td>
                <td>62.7%</td>
                <td>100.0%</td>
                <td>98.5%</td>
              </tr>
              <tr>
                <td><strong style="color: #ef4444;">At-Risk High Rollers</strong></td>
                <td><strong style="color: #ef4444;">12.3%</strong></td>
                <td><strong style="color: #ef4444;">10.7%</strong></td>
                <td>32.1%</td>
                <td>28.4%</td>
                <td>89.6%</td>
                <td>64.2%</td>
              </tr>
              <tr>
                <td><strong style="color: #f97316;">Vulnerable Newcomers</strong></td>
                <td><strong style="color: #f97316;">14.1%</strong></td>
                <td><strong style="color: #f97316;">13.8%</strong></td>
                <td>21.5%</td>
                <td>22.0%</td>
                <td>58.2%</td>
                <td>38.4%</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- TAB 5: Portfolio LTV vs. Churn Hazard Matrix -->
    <div id="tab-portfolio" class="tab-panel">
      <div class="dashboard-section">
        <div class="section-header">
          <h2 class="section-title">Strategic Portfolio Matrix: Customer Lifetime Value (LTV) vs. Churn Hazard</h2>
          <p class="section-desc">Bubble distribution plotting customer accounts by predicted lifetime value and churn probability, sized by monthly charges and mapped to 4 investment zones.</p>
        </div>

        <div class="chart-box">
          <img src="customer_segmentation_ltv_risk_quadrants.png" alt="LTV vs Churn Hazard Quadrants">
        </div>
      </div>
    </div>

    <!-- TAB 6: Interactive Segment Explorer -->
    <div id="tab-explorer" class="tab-panel">
      <div class="dashboard-section">
        <div class="section-header">
          <h2 class="section-title">Live Customer Segment Explorer</h2>
          <p class="section-desc">Interactive query engine to search, filter, and inspect scored customer records across personas, risk tiers, and K-Means clusters.</p>
        </div>

        <!-- Filter Controls -->
        <div class="filter-bar">
          <div class="filter-item">
            <label for="searchId">Search Customer ID</label>
            <input type="text" id="searchId" class="form-control" placeholder="e.g. 7590-VHVEG" onkeyup="filterData()">
          </div>

          <div class="filter-item">
            <label for="filterPersona">Persona Segment</label>
            <select id="filterPersona" class="form-control" onchange="filterData()">
              <option value="ALL">All Personas (All 6)</option>
              <option value="Champions & VIP Loyalists">Champions & VIP Loyalists</option>
              <option value="At-Risk High Rollers">At-Risk High Rollers</option>
              <option value="Vulnerable Newcomers">Vulnerable Newcomers</option>
              <option value="Digital Enthusiasts & Streamers">Digital Enthusiasts & Streamers</option>
              <option value="Budget Anchors">Budget Anchors</option>
              <option value="Core Steady Subscribers">Core Steady Subscribers</option>
            </select>
          </div>

          <div class="filter-item">
            <label for="filterCluster">ML Cluster</label>
            <select id="filterCluster" class="form-control" onchange="filterData()">
              <option value="ALL">All Clusters</option>
              <option value="Cluster A">Cluster A: High-Churn Flight Risks</option>
              <option value="Cluster B">Cluster B: High-Value Enterprise Moats</option>
              <option value="Cluster C">Cluster C: Low-Cost Basic Loyalists</option>
              <option value="Cluster D">Cluster D: Mid-Tier Digital Mainstream</option>
            </select>
          </div>

          <div class="filter-item">
            <label for="filterTier">Risk Tier</label>
            <select id="filterTier" class="form-control" onchange="filterData()">
              <option value="ALL">All Risk Tiers</option>
              <option value="Critical Risk">Critical Risk (&ge;70%)</option>
              <option value="High Risk">High Risk (45-70%)</option>
              <option value="Medium Risk">Medium Risk (25-45%)</option>
              <option value="Low Risk">Low Risk (&lt;25%)</option>
            </select>
          </div>
        </div>

        <!-- Explorer Table -->
        <div class="table-container">
          <table id="customerTable">
            <thead>
              <tr>
                <th>Customer ID</th>
                <th>Persona Segment</th>
                <th>ML Cluster</th>
                <th>Tenure</th>
                <th>Contract</th>
                <th>Monthly Spend</th>
                <th>Churn Risk</th>
                <th>Risk Tier</th>
                <th>Predicted LTV</th>
                <th>RFM Health</th>
              </tr>
            </thead>
            <tbody id="tableBody">
              <!-- Dynamically populated via JS -->
            </tbody>
          </table>
        </div>

        <!-- Pagination Controls -->
        <div class="pagination-bar">
          <div id="resultCount">Showing 0 of 0 accounts</div>
          <div style="display: flex; gap: 0.5rem;">
            <button id="btnPrev" class="btn btn-sm" onclick="changePage(-1)">Previous</button>
            <span id="pageIndicator" style="display: flex; align-items: center; font-weight: 700;">Page 1</span>
            <button id="btnNext" class="btn btn-sm" onclick="changePage(1)">Next</button>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 7: Retention Playbooks -->
    <div id="tab-playbooks" class="tab-panel">
      <div class="dashboard-section">
        <div class="section-header">
          <h2 class="section-title">Persona-Targeted Retention & Action Playbooks</h2>
          <p class="section-desc">Prescriptive intervention playbooks engineered specifically for the hazard factors and willingness-to-pay of each customer segment.</p>
        </div>

        <div style="display: flex; flex-direction: column; gap: 1.25rem;">
          <div style="background: rgba(239, 68, 68, 0.08); border-left: 4px solid #ef4444; padding: 1.25rem; border-radius: 0.6rem;">
            <h3 style="color: #f87171; font-size: 1.1rem; margin-bottom: 0.4rem;">1. At-Risk High Rollers: Concierge Retention SLA (24-Hour Protocol)</h3>
            <p style="font-size: 0.88rem; color: #cbd5e1; margin-bottom: 0.6rem;">
              <strong>Trigger:</strong> Scored in At-Risk High Rollers ($90.86/mo avg spend with &ge;45% churn probability).
            </p>
            <ul style="font-size: 0.86rem; color: var(--text-muted); margin-left: 1.5rem; line-height: 1.6;">
              <li><strong>Incentive:</strong> Complimentary 12-month Tech Support & Online Security bundle (addressing the primary hazard factor).</li>
              <li><strong>Contract Subsidy:</strong> Offer a $15/month bill credit in exchange for a 1-year agreement, saving $780/yr in net account revenue.</li>
              <li><strong>Channel:</strong> Outbound direct phone contact from dedicated Senior Customer Success Manager.</li>
            </ul>
          </div>

          <div style="background: rgba(249, 115, 22, 0.08); border-left: 4px solid #f97316; padding: 1.25rem; border-radius: 0.6rem;">
            <h3 style="color: #fb923c; font-size: 1.1rem; margin-bottom: 0.4rem;">2. Vulnerable Newcomers: 90-Day Digital Onboarding Nurture</h3>
            <p style="font-size: 0.88rem; color: #cbd5e1; margin-bottom: 0.6rem;">
              <strong>Trigger:</strong> Tenure &le;6 months on month-to-month terms without security/support features.
            </p>
            <ul style="font-size: 0.86rem; color: var(--text-muted); margin-left: 1.5rem; line-height: 1.6;">
              <li><strong>Incentive:</strong> 60-day free trial of Online Backup and Antivirus Protection during day 14 check-in.</li>
              <li><strong>Billing Education:</strong> $10 credit to set up Credit Card or Bank ACH Autopay to eliminate monthly manual payment friction.</li>
              <li><strong>Channel:</strong> Automated SMS and in-app interactive walkthroughs.</li>
            </ul>
          </div>

          <div style="background: rgba(16, 185, 129, 0.08); border-left: 4px solid #10b981; padding: 1.25rem; border-radius: 0.6rem;">
            <h3 style="color: #34d399; font-size: 1.1rem; margin-bottom: 0.4rem;">3. Champions & VIP Loyalists: Platinum Loyalty Preservation</h3>
            <p style="font-size: 0.88rem; color: #cbd5e1; margin-bottom: 0.6rem;">
              <strong>Trigger:</strong> Tenure &ge;36 months, ARPU &ge;$70/mo, churn risk &lt;25%.
            </p>
            <ul style="font-size: 0.86rem; color: var(--text-muted); margin-left: 1.5rem; line-height: 1.6;">
              <li><strong>Loyalty Perks:</strong> Priority routing in support queue (skip-the-line), complimentary router hardware refresh every 24 months.</li>
              <li><strong>Advocacy:</strong> Two-way referral incentive ($25 credit for both referrer and referred subscriber).</li>
              <li><strong>Goal:</strong> Maintain zero-churn stability and defend against fiber competitor poaching.</li>
            </ul>
          </div>

          <div style="background: rgba(168, 85, 247, 0.08); border-left: 4px solid #a855f7; padding: 1.25rem; border-radius: 0.6rem;">
            <h3 style="color: #c084fc; font-size: 1.1rem; margin-bottom: 0.4rem;">4. Digital Enthusiasts & Streamers: Bandwidth Expansion & Entertainment Bundles</h3>
            <p style="font-size: 0.88rem; color: #cbd5e1; margin-bottom: 0.6rem;">
              <strong>Trigger:</strong> High streaming activity on Fiber optic internet.
            </p>
            <ul style="font-size: 0.86rem; color: var(--text-muted); margin-left: 1.5rem; line-height: 1.6;">
              <li><strong>Perks:</strong> Complimentary Gigabit speed boost for 6 months upon contract extension.</li>
              <li><strong>Cross-Sell:</strong> Discounted streaming ecosystem bundle (Device Protection + Cloud DVR + Backup).</li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <footer>
      <p>&copy; 2026 Telecom Customer Churn Prediction & Lifetime Value (LTV) Engine | Week 4 Day 3 Milestone</p>
      <p style="margin-top: 0.35rem; font-size: 0.78rem; color: #64748b;">
        Generated automatically with Python, Scikit-Learn, Pandas, Seaborn & Matplotlib. Data: 7,043 Accounts.
      </p>
    </footer>
  </div>

  <!-- Interactive JavaScript Engine -->
  <script>
    const customerData = {json_str};
    let filteredData = [...customerData];
    let currentPage = 1;
    const pageSize = 12;

    function switchTab(tabId) {{
      document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
      document.querySelectorAll('.nav-tab').forEach(b => b.classList.remove('active'));

      const target = document.getElementById('tab-' + tabId);
      if (target) {{
        target.classList.add('active');
      }}

      // Set active nav button
      const buttons = document.querySelectorAll('.nav-tab');
      buttons.forEach(btn => {{
        if (btn.getAttribute('onclick').includes(tabId)) {{
          btn.classList.add('active');
        }}
      }});
    }}

    function filterData() {{
      const search = document.getElementById('searchId').value.trim().toLowerCase();
      const persona = document.getElementById('filterPersona').value;
      const cluster = document.getElementById('filterCluster').value;
      const tier = document.getElementById('filterTier').value;

      filteredData = customerData.filter(item => {{
        const matchId = !search || item.id.toLowerCase().includes(search);
        const matchPersona = persona === 'ALL' || item.persona === persona;
        const matchCluster = cluster === 'ALL' || item.cluster.includes(cluster);
        const matchTier = tier === 'ALL' || item.tier === tier;
        return matchId && matchPersona && matchCluster && matchTier;
      }});

      currentPage = 1;
      renderTable();
    }}

    function renderTable() {{
      const tbody = document.getElementById('tableBody');
      tbody.innerHTML = '';

      const total = filteredData.length;
      const totalPages = Math.ceil(total / pageSize) || 1;
      if (currentPage > totalPages) currentPage = totalPages;
      if (currentPage < 1) currentPage = 1;

      const start = (currentPage - 1) * pageSize;
      const end = Math.min(start + pageSize, total);
      const pageSlice = filteredData.slice(start, end);

      if (pageSlice.length === 0) {{
        tbody.innerHTML = '<tr><td colspan="10" style="text-align: center; padding: 2rem; color: #94a3b8;">No matching customer records found.</td></tr>';
      }} else {{
        pageSlice.forEach(row => {{
          const tr = document.createElement('tr');
          const probPct = (row.prob * 100).toFixed(1);
          
          let tierColor = '#10b981';
          if (row.tier === 'Critical Risk') tierColor = '#ef4444';
          else if (row.tier === 'High Risk') tierColor = '#f97316';
          else if (row.tier === 'Medium Risk') tierColor = '#f59e0b';

          let personaColor = '#6366f1';
          if (row.persona === 'Champions & VIP Loyalists') personaColor = '#10b981';
          else if (row.persona === 'At-Risk High Rollers') personaColor = '#ef4444';
          else if (row.persona === 'Vulnerable Newcomers') personaColor = '#f97316';
          else if (row.persona === 'Digital Enthusiasts & Streamers') personaColor = '#a855f7';
          else if (row.persona === 'Budget Anchors') personaColor = '#0ea5e9';

          tr.innerHTML = `
            <td><strong style="font-family: var(--font-mono); color: #f8fafc;">${{row.id}}</strong></td>
            <td><span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: ${{personaColor}}; margin-right: 6px;"></span>${{row.persona}}</td>
            <td><span style="font-size: 0.8rem; color: #94a3b8;">${{row.cluster}}</span></td>
            <td>${{row.tenure}} mo</td>
            <td>${{row.contract}}</td>
            <td><strong style="font-family: var(--font-mono);">$${{row.charges.toFixed(2)}}</strong></td>
            <td><strong style="color: ${{tierColor}}; font-family: var(--font-mono);">${{probPct}}%</strong></td>
            <td><span style="color: ${{tierColor}}; font-weight: 600; font-size: 0.78rem;">${{row.tier}}</span></td>
            <td><strong style="color: #a5b4fc; font-family: var(--font-mono);">$${{row.ltv.toFixed(0)}}</strong></td>
            <td><span style="font-family: var(--font-mono);">${{row.rfm.toFixed(1)}}</span></td>
          `;
          tbody.appendChild(tr);
        }});
      }}

      document.getElementById('resultCount').textContent = `Showing ${{total > 0 ? start + 1 : 0}}-${{end}} of ${{total}} accounts`;
      document.getElementById('pageIndicator').textContent = `Page ${{currentPage}} of ${{totalPages}}`;
      document.getElementById('btnPrev').disabled = currentPage === 1;
      document.getElementById('btnNext').disabled = currentPage >= totalPages;
    }}

    function changePage(delta) {{
      currentPage += delta;
      renderTable();
    }}

    function exportSegmentsCSV() {{
      let csv = 'CustomerID,PersonaSegment,MLCluster,Tenure,Contract,MonthlyCharges,ChurnProbability,RiskTier,PredictedLTV,RFMHealthScore\\n';
      filteredData.forEach(r => {{
        csv += `"${{r.id}}","${{r.persona}}","${{r.cluster}}",${{r.tenure}},"${{r.contract}}",${{r.charges}},${{r.prob}},"${{r.tier}}",${{r.ltv}},${{r.rfm}}\\n`;
      }});

      const blob = new Blob([csv], {{ type: 'text/csv;charset=utf-8;' }});
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.setAttribute('download', 'filtered_customer_segments.csv');
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }}

    // Initialize on load
    renderTable();
  </script>
</body>
</html>
"""

output_path = os.path.join(REPORTS_DIR, "customer_segmentation_dashboard.html")
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Generated: {output_path} ({len(html_content):,} bytes)")
