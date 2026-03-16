import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Page Config
st.set_page_config(page_title="MediScan AI Analysis", layout="wide")

st.title("🔬 MediScan AI-Driven Diagnostics Lab: ROI Simulator")
st.markdown("Adjust the sidebar parameters to see how AI impacts profitability and operational efficiency.")

# --- SIDEBAR: INPUT PARAMETERS ---
st.sidebar.header("💼 Business Variables")
investment = st.sidebar.number_input("Initial Investment (₹)", value=30000000, step=1000000)
annual_reports = st.sidebar.slider("Annual Report Volume", 50000, 500000, 100000)
cost_per_report = st.sidebar.number_input("Cost per Manual Report (₹)", value=500)

st.sidebar.header("🤖 AI Performance")
time_reduction = st.sidebar.slider("Time Reduction Efficiency (%)", 10, 90, 50) / 100
error_reduction = st.sidebar.slider("Error Reduction Efficiency (%)", 10, 90, 40) / 100

st.sidebar.header("⚠️ Risk Factors")
error_rate = st.sidebar.slider("Current Error Rate (%)", 1.0, 10.0, 5.0) / 100
cost_per_error = st.sidebar.number_input("Avg. Cost per Error (₹)", value=5000)

# --- CALCULATIONS ---
current_total_processing_cost = annual_reports * cost_per_report
savings_labor = current_total_processing_cost * time_reduction

current_error_cost = annual_reports * error_rate * cost_per_error
savings_errors = current_error_cost * error_reduction

total_annual_savings = savings_labor + savings_errors
net_benefit_y1 = total_annual_savings - investment
roi = (total_annual_savings / investment) * 100

# --- METRIC CARDS ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Annual Savings", f"₹{total_annual_savings:,.0f}")
col2.metric("Year 1 Net Benefit", f"₹{net_benefit_y1:,.0f}")
col3.metric("ROI (%)", f"{roi:.2f}%")
col4.metric("Breakeven (Months)", f"{min(12, (investment/total_annual_savings)*12):.1f}")

st.divider()

# --- DATA SIMULATION ---
@st.cache_data
def get_sim_data(n, t_red):
    np.random.seed(42)
    manual = np.random.normal(120, 30, n)
    ai = manual * (1 - t_red)
    return pd.DataFrame({"Manual": manual, "AI-Driven": ai})

df_sim = get_sim_data(1000, time_reduction)

# --- VISUALIZATIONS ---
tab1, tab2 = st.tabs(["📊 Financial Analysis", "🔬 Operational Impact"])

with tab1:
    fig1, ax1 = plt.subplots(1, 2, figsize=(14, 6))
    
    # Chart A: Cumulative Cash Flow
    years = np.arange(0, 4)
    cash_flow = [-investment]
    for y in range(1, 4): cash_flow.append(cash_flow[-1] + total_annual_savings)
    
    ax1[0].plot(years, cash_flow, marker='o', color='green', linewidth=3)
    ax1[0].axhline(0, color='red', linestyle='--')
    ax1[0].set_title("3-Year Cumulative Benefit")
    ax1[0].set_ylabel("Net Profit/Loss (₹)")
    
    # Chart B: Sensitivity Analysis
    scenarios = [0.3, 0.4, 0.5, 0.6]
    scenario_benefits = [(current_total_processing_cost * s + savings_errors) - investment for s in scenarios]
    sns.barplot(x=[f"{int(s*100)}% Speed" for s in scenarios], y=scenario_benefits, ax=ax1[1], palette="viridis")
    ax1[1].set_title("Sensitivity: Profit vs. AI Speed")
    
    st.pyplot(fig1)

with tab2:
    fig2, ax2 = plt.subplots(1, 2, figsize=(14, 6))
    
    # Chart C: Time Distribution
    sns.kdeplot(df_sim['Manual'], color='red', fill=True, label='Manual', ax=ax2[0])
    sns.kdeplot(df_sim['AI-Driven'], color='green', fill=True, label='AI', ax=ax2[0])
    ax2[0].set_title("Processing Time Distribution (Minutes)")
    ax2[0].legend()
    
    # Chart D: Cost Breakdown
    categories = ['Manual', 'AI-Driven']
    labor = [current_total_processing_cost, current_total_processing_cost * (1-time_reduction)]
    risk = [current_error_cost, current_error_cost * (1-error_reduction)]
    
    ax2[1].bar(categories, labor, label='Labor Cost', color='lightgrey')
    ax2[1].bar(categories, risk, bottom=labor, label='Risk Cost', color='salmon')
    ax2[1].set_title("Operational Cost Structure Comparison")
    ax2[1].legend()
    
    st.pyplot(fig2)

st.success(f"**Final Verdict:** At the current scale, the system is {'PROFITABLE' if net_benefit_y1 > 0 else 'NOT PROFITABLE'} in Year 1.")