import streamlit as st
import pandas as pd

# Import your existing solver function from optimizer.py
from optimizer import solve_wedding

st.set_page_config(page_title="Wedding Budget Optimizer", layout="wide")

st.title("💍 Wedding Budget Optimizer")
st.write("Helps you decide how to spend and where to cut so you can plan your wedding within your budget.")

# ---- Inputs ----
st.header("1) Inputs")

col1, col2 = st.columns(2)
with col1:
    budget = st.number_input("Total Budget ($)", min_value=0, value=40000, step=500)
with col2:
    cut_amount = st.slider("Cut Amount ($)", min_value=0, max_value=10000, value=2000, step=100)

# Load categories weights
categories_df = pd.read_csv("categories.csv")

st.subheader("Category Importance (1–10)")
edited_weights = st.data_editor(
    categories_df,
    num_rows="fixed",
    use_container_width=True
)

# Save edited weights back to categories.csv so solve_wedding uses them
# (Simple approach for MVP)
edited_weights.to_csv("categories.csv", index=False)

run = st.button("Run Optimizer")

# ---- Results ----
if run:
    st.header("2) Results")

    # Full budget
    sol_full, cost_full, value_full = solve_wedding(budget)

    # Cut budget
    new_budget = budget - cut_amount
    if new_budget < 0:
        st.error("Cut amount cannot make budget negative.")
    else:
        sol_cut, cost_cut, value_cut = solve_wedding(new_budget)

        c1, c2 = st.columns(2)

        with c1:
            st.subheader(f"✅ Full Budget Plan (${budget:,.0f})")
            st.dataframe(sol_full, use_container_width=True)
            st.write(f"**Spend:** ${cost_full:,.0f}")
            st.write(f"**Remaining:** ${budget - cost_full:,.0f}")
            st.write(f"**Value Score:** {value_full:,.2f}")

        with c2:
            st.subheader(f"✅ After Cut Plan (${new_budget:,.0f})")
            st.dataframe(sol_cut, use_container_width=True)
            st.write(f"**Spend:** ${cost_cut:,.0f}")
            st.write(f"**Remaining:** ${new_budget - cost_cut:,.0f}")
            st.write(f"**Value Score:** {value_cut:,.2f}")

        # Compare changes
        st.subheader("🔁 What changed because of the cut?")
        a = sol_full.set_index("category")[["package", "cost", "quality"]]
        b = sol_cut.set_index("category")[["package", "cost", "quality"]]

        compare = a.join(b, lsuffix="_full", rsuffix="_cut")
        compare["changed"] = compare["package_full"] != compare["package_cut"]
        changes_only = compare[compare["changed"]].reset_index()

        if changes_only.empty:
            st.info("No category changed packages.")
        else:
            st.dataframe(changes_only, use_container_width=True)

        st.subheader("📉 Impact")
        st.write(f"**Cut Amount:** ${cut_amount:,.0f}")
        st.write(f"**Value Lost:** {value_full - value_cut:,.2f}")
