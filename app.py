import streamlit as st
import pandas as pd
from optimizer import solve_wedding

st.set_page_config(page_title="Wedding Budget Optimizer", layout="wide")

st.title("💍 Wedding Budget Optimizer")
st.write("Helps you decide how to spend and where to cut so you can plan your wedding within your budget.")


def generate_smart_tips(solution_df, remaining):
    """
    Simple, human-friendly tips based on the cut plan.
    Expects solution_df columns: category, package, cost, quality
    """
    tips = []

    # Budget buffer tip
    if remaining <= 0:
        tips.append("Your plan uses the full budget. If you need to cut more, reduce lower-impact categories first (decor, invitations, DJ).")
    elif remaining < 500:
        tips.append("You’re very close to your budget limit. Keep a small buffer for surprise costs (taxes, tips, delivery fees).")
    else:
        tips.append(f"You still have about ${remaining:,.0f} left — keep this as a buffer for last-minute expenses.")

    def get_choice(cat):
        row = solution_df[solution_df["category"].str.lower() == cat.lower()]
        if row.empty:
            return None
        return row.iloc[0]["package"]

    inv = get_choice("Invitations")
    if inv:
        if inv.lower() in ["budget", "mid"]:
            tips.append("Invitations tip: Use e-invites (Canva) + WhatsApp RSVP link to save printing/shipping costs.")
        else:
            tips.append("Invitations tip: Keep luxury invites for close family and use e-invites for friends to reduce counts.")

    dec = get_choice("Decor")
    if dec:
        if dec.lower() == "budget":
            tips.append("Decor tip: Focus on 1–2 statement areas (stage/entrance) and keep the rest minimal (candles, fairy lights).")
        elif dec.lower() == "mid":
            tips.append("Decor tip: Mix real + artificial flowers to keep it premium without going full luxury.")
        else:
            tips.append("Decor tip: Reuse ceremony decor for reception to get more value.")

    dj = get_choice("Music / DJ")
    if dj:
        if dj.lower() in ["budget", "mid"]:
            tips.append("Music tip: Use curated Spotify playlists + hire DJ only for peak dance hours to save money.")
        else:
            tips.append("Music tip: Luxury DJ chosen — ask for MC + crowd engagement add-ons to maximize guest experience.")

    photo = get_choice("Photography")
    if photo:
        if photo.lower() == "luxury":
            tips.append("Photography tip: Great choice — ask for candid + a short highlight reel. Memories last forever.")
        else:
            tips.append("Photography tip: Prioritize key moments (ceremony + couple shoot) and keep extra hours minimal.")

    return tips


# ---- Inputs ----
st.header("1) Inputs")

col1, col2 = st.columns(2)
with col1:
    budget = st.number_input("Total Budget ($)", min_value=0, value=40000, step=500)
with col2:
    cut_amount = st.slider("Cut Amount ($)", min_value=0, max_value=10000, value=2000, step=100)

categories_df = pd.read_csv("categories.csv")

st.subheader("Category Importance (1–10)")
edited_weights = st.data_editor(categories_df, num_rows="fixed", use_container_width=True)

# Save edited weights for solver to use
edited_weights.to_csv("categories.csv", index=False)

run = st.button("Run Optimizer")


# ---- Results ----
if run:
    st.header("2) Results")

    sol_full, cost_full, value_full = solve_wedding(budget)

    new_budget = budget - cut_amount
    if new_budget < 0:
        st.error("Cut amount cannot make budget negative.")
        st.stop()

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
        remaining = new_budget - cost_cut
        st.write(f"**Remaining:** ${remaining:,.0f}")
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

    st.subheader("💡 Smart Wedding Tips (based on your plan)")
    tips = generate_smart_tips(sol_cut, remaining)
    for t in tips:
        st.info(t)
