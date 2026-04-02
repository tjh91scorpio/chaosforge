import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO

def generate_chaos_finance_report(income, fixed_expenses, variable_spends):
    total_fixed = fixed_expenses
    total_var_avg = sum(avg for avg, std in variable_spends.values())
    disposable_income = income - total_fixed - total_var_avg
    if disposable_income < 0:
        report = {'status': 'CRITICAL: Negative disposable income. Immediate budget overhaul needed.'}
        return report, None, None
    
    total_var = sum(std ** 2 for _, std in variable_spends.values())
    volatility = total_var / (disposable_income + 1e-6)
    r = 3.0 + min(0.999, volatility * 0.15)
    
    x = 0.5
    path = [x]
    for _ in range(200):
        x = r * x * (1 - x)
        path.append(min(max(x, 0), 1))
    
    sim_spending = [total_fixed + total_var_avg + (p * disposable_income) for p in path]
    
    is_chaotic = r > 3.57
    risk_level = 'HIGH CHAOS RISK: Your spending is in the chaotic regime — small habit changes can trigger massive unpredictable spirals or windfalls!' if is_chaotic else 'STABLE: Your finances are in a predictable attractor zone.'
    
    if variable_spends:
        highest_var_cat = max(variable_spends, key=lambda k: variable_spends[k][1])
        anchor_suggestion = f"ANCHOR YOUR {highest_var_cat.upper()} spending to a strict fixed limit each month. This directly lowers your chaos parameter r and prevents spirals."
    else:
        anchor_suggestion = "Add more variable categories to refine analysis."
    
    report = {
        'your_chaos_factor_r': round(r, 4),
        'risk_level': risk_level,
        'explanation': f"Your chaos factor (r = {round(r,4)}) comes from your spending volatility. In chaos theory, when r > 3.57 the system becomes unpredictable — just like how one impulse buy can snowball into debt.",
        'simulation_summary': f"200-month simulation: Average projected spend ${round(np.mean(sim_spending), 2)}. Max swing: ${round(max(sim_spending) - min(sim_spending), 2)} (chaotic swings possible if r high).",
        'anchor_recommendation': anchor_suggestion,
        'next_step': 'To stabilize: Track and cap the highest-variance category. Re-run with updated data in 30 days.',
        'status': 'SUCCESS'
    }
    
    # Generate charts (no saving to disk)
    rs = np.linspace(2.5, 4.0, 400)
    bifur_y = []
    for rr in rs:
        xx = 0.5
        for _ in range(100):
            xx = rr * xx * (1 - xx)
        bifur_y.append(xx)
    fig1 = plt.figure(figsize=(8, 5))
    plt.plot(rs, bifur_y, ',k', alpha=0.6)
    plt.axvline(r, color='red', linestyle='--', linewidth=2, label=f'YOUR r = {round(r,4)}')
    plt.title('ChaosForge Bifurcation Diagram: Your Spending Chaos Map')
    plt.xlabel('Chaos Parameter (r) - higher = more unpredictable')
    plt.ylabel('Spending Fraction (0=under control, 1=overspend)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    fig2 = plt.figure(figsize=(8, 5))
    months = np.arange(len(path))
    plt.plot(months, sim_spending, 'b-', linewidth=1.5)
    plt.axhline(income, color='green', linestyle='--', label='Your Monthly Income')
    plt.title('ChaosForge Spending Spiral Simulation (200 Months)')
    plt.xlabel('Months into the Future')
    plt.ylabel('Projected Total Monthly Spending ($)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    return report, fig1, fig2

# ====================== STREAMLIT APP ======================
st.set_page_config(page_title="ChaosForge", page_icon="🌀", layout="wide")
st.title("🌀 ChaosForge")
st.markdown("**The world's first chaos-theory spending spiral predictor** — invented live by Grok. Enter your numbers and see if your budget will explode.")

col1, col2 = st.columns(2)
with col1:
    income = st.number_input("Your monthly income ($)", value=4500.0, min_value=0.0, step=50.0)
    fixed_expenses = st.number_input("Fixed monthly expenses ($)", value=2200.0, min_value=0.0, step=50.0)

st.subheader("Variable spending categories (your biggest chaos triggers)")
variable_spends = {}
default_cats = ["Groceries", "Dining Out", "Entertainment", "Gas/Transport", "Shopping", "Misc"]
default_avg = [450, 300, 180, 250, 0, 0]
default_std = [90, 150, 120, 40, 0, 0]

for i in range(6):
    c1, c2, c3 = st.columns([3, 2, 2])
    with c1:
        cat = st.text_input(f"Category {i+1}", value=default_cats[i], key=f"cat_{i}")
    with c2:
        avg = st.number_input("Avg monthly spend $", value=default_avg[i], min_value=0.0, key=f"avg_{i}")
    with c3:
        std = st.number_input("Typical swing/std $", value=default_std[i], min_value=0.0, key=f"std_{i}")
    if cat.strip() and (avg > 0 or std > 0):
        variable_spends[cat.strip()] = (avg, std)

if st.button("🚀 Generate Chaos Report", type="primary", use_container_width=True):
    if not variable_spends:
        st.error("Add at least one variable category!")
    else:
        report, fig1, fig2 = generate_chaos_finance_report(income, fixed_expenses, variable_spends)
        
        if report.get('status') == 'CRITICAL: Negative disposable income. Immediate budget overhaul needed.':
            st.error(report['status'])
        else:
            st.success("✅ Report ready!")
            st.subheader("=== YOUR CHAOSFORGE REPORT ===")
            for k, v in report.items():
                st.write(f"**{k.replace('_', ' ').title()}**: {v}")
            
            st.subheader("Your Chaos Maps")
            c1, c2 = st.columns(2)
            with c1:
                st.pyplot(fig1)
                buf1 = BytesIO()
                fig1.savefig(buf1, format="png", dpi=300, bbox_inches="tight")
                buf1.seek(0)
                st.download_button("⬇️ Download Bifurcation Diagram", buf1, "chaosforge_bifurcation.png", "image/png")
            with c2:
                st.pyplot(fig2)
                buf2 = BytesIO()
                fig2.savefig(buf2, format="png", dpi=300, bbox_inches="tight")
                buf2.seek(0)
                st.download_button("⬇️ Download Spending Spiral", buf2, "chaosforge_spending_path.png", "image/png")
            
            st.balloons()

st.markdown("---")
st.markdown("**Made instantly for you by Grok.** This app is 100% free to use forever. Love it? [Tip the creator on Ko-fi](https://ko-fi.com/yourusername) or share it!")
st.caption("Pro tip: Replace the Ko-fi link above with your own after you set it up (takes 2 minutes, completely free).")
