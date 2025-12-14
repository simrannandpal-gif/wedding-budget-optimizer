import streamlit as st
import pandas as pd

from optimizer import solve_wedding

st.set_page_config(page_title="Wedding Budget Optimizer", layout="wide")


# -----------------------------
# Smart tips helper functions
# -----------------------------
def generate_smart_tips(solution_df: pd.DataFrame, budget: float, spend: float, remaining: float):
    """
    Create simple, human-friendly wedding planning tips based on the optimizer output.
    Expects solution_df columns: category, package, cost, quality
    """
    tips = []

    # Budget tightness tips
    if remaining <= 0:
        tips.append(
            "Your plan uses the full budget. If you need to cut more, reduce lower-impact categories first (decor, invitations, DJ)."
        )
    elif remaining < 500:
        tips.append(
            "You’re very close to your budget limit. Keep a small buffer for surprise costs (taxes, tips, delivery fees)."
        )
    else:
        tips.append(
            f"You still have about ${remaining:,.0f} left — consider keeping this as a buffer for last-minute expenses."
        )

    def get_choice(cat_name: str):
        row = solution_df[solution_df["category"].str.lower() == cat_name.lower()]
        if row.empty:
            return None
        return str(row.iloc[0]["package"])

    # Invitations
    inv = get_choice("Invitations")
    if inv:
        if inv.lower() in ["budget", "mid"]:
            tips.append("Invitations tip: Use e-invites (Canva) + a WhatsApp RSVP link to save printing/shipping costs.")
        else:
            tips.append("Invitations tip: Keep Luxury invites for close family, and use e-invites for friends to reduce count.")

    # Decor
    dec = get_choice("Decor")
    if dec:
        if dec.lower() == "budget":
            tips.append("Decor tip: Focus on 1–2 statement areas (stage/entrance). Keep the rest minimal (candles, fairy lights, reused florals).")
        elif dec.lower() == "mid":
            tips.append("Decor tip: Mix real + artificial flowers to keep it premium without going full luxury.")
        else:
            tips.append("Decor tip: If decor is Luxury, reuse ceremony decor for reception to get more value.")

    # DJ / Music
    dj = get_choice("Music / DJ")
    if dj:
        if dj.lower() in ["budget", "mid"]:
            tips.append("Music tip: Use curated Spotify playlists for dinner + hire DJ only for peak dance hours to save money.")
        else:
            tips.append("Music tip: Luxury DJ chosen — ask for MC + crowd engagement add-ons to maximize guest experience.")

    # Photography
    photo = get_choice("Photography")
    if photo:
        if photo.lower() == "luxury":
            tips.append("Photography tip: Great choice — ask for candid + short highlight reel. Memories last forever.")
        else:
            tips.append("Photography tip: Prioritize key moments (ceremony + couple shoot). Keep extra hours minimal to reduce cost.")

    # Catering
    cat = get_choice("Catering")
    if cat and cat.lower() in ["budget", "mid"]:
        tips.append("Catering tip: Limit menu items but keep 1–2 signature dishes + a good dessert counter — guests remember taste, not menu length.")

    # Venue
    venue = get_choice("Venue")
    if venue and venue.lower() in ["budget", "mid"]:
        tips.append("Venue tip: Choose off-peak day/time or a venue that includes basics (tables, chairs, lighting) to avoid hidden rentals.")

    return tips


# -----------------------------
# UI
# -----------------------------
st.title("💍 Wedding Budget Optimizer")
st.write("Helps you decide how to spend and where to cut so you can plan your wedding within your budget.")

st.header("1) Inputs")

col1, col2 = st.columns(2)
with col1:
    budget = st.number_input("Total Budget ($)", min_value=0, value=40000, step=500)
with col2:
    cut_amount = st.slider("Cut Amount ($)", min_value=0, max_value=10000, value=2000, step=100)

categories_df = pd.read_csv("categories.csv")

st.subheader("Category Importance (1–10)")
edited_weights = st.data_editor(categories_df, num_rows="fixed", use_container_width=True)
edited_weights.to_csv("categories.csv", index=False)

run = st.button("Run Optimizer")


# -----------------------------
# Results
# -----------------------------
if run:
    st.header("2) Results")

    # Full budget plan
    sol_full, cost_full, value_full = solve_wedding(budget)

    # Cut budget plan
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

    # Impact + tips
    st.subheader("📉 Impact")
    st.write(f"**Cut Amount:** ${cut_amount:,.0f}")
    st.write(f"**Value Lost:** {value_full - value_cut:,.2f}")

    st.subheader("💡 Smart Wedding Tips (based on your cut plan)")
    remaining_cut = new_budget - cost_cut
    tips = generate_smart_tips(sol_cut, new_budget, cost_cut, remaining_cut)

    for t in tips:
        st.info(t)

