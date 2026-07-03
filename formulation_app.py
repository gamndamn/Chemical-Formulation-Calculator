import streamlit as st
import pandas as pd

st.set_page_config(page_title="Advanced Formulation Lab", layout="wide")

st.title("Chemical Formulation Calculator")
st.write("Multi-solvent compatibility audit and precise concentration inputs.")

# --- 1. THE DATABASE (Multi-solvent Structure) ---
# Each chemical now has specific solubility limits for different solvents
CHEMICAL_DATABASE = {
    "Salicylic Acid": {
        "max_safe_pct": 2.0,
        "solubility": {"Water": 0.2, "Ethanol": 14.0, "Mineral Oil": 0.5}
    },
    "Vitamin C (Ascorbic Acid)": {
        "max_safe_pct": 15.0,
        "solubility": {"Water": 33.0, "Ethanol": 2.0, "Mineral Oil": 0.0}
    },
    "Niacinamide": {
        "max_safe_pct": 10.0,
        "solubility": {"Water": 10.0, "Ethanol": 8.0, "Mineral Oil": 0.1}
    }
}

# --- 2. SIDEBAR INPUTS ---
st.sidebar.header("Batch Parameters")
total_weight = st.sidebar.number_input("Total Batch Weight (grams)", min_value=10, max_value=5000, value=200, step=10)

# Extract available solvents dynamically from our database logic
available_solvents = ["Water", "Ethanol", "Mineral Oil"]
base_solvent = st.sidebar.selectbox("Select Base Solvent", available_solvents)

# --- 3. MAIN INTERFACE & KEYBOARD INPUT ---
st.subheader("Configure Active Ingredient")
active_name = st.selectbox("Select Active Chemical", list(CHEMICAL_DATABASE.keys()))

# Using st.number_input allows the user to type from the keyboard instead of sliding
concentration = st.number_input(
    label=f"Enter Concentration of {active_name} (%)",
    min_value=0.0,
    max_value=100.0,
    value=2.0,
    step=0.1,
    format="%.1f" # This forces 1 decimal place precision (e.g., 2.5)
)

# --- 4. CALCULATIONS ---
active_grams = (concentration / 100) * total_weight
solvent_grams = total_weight - active_grams

# --- 5. RESULTS & AUTOMATED AUDIT ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Recipe Breakdown")
    recipe_data = {
        "Component": [active_name, f"{base_solvent} (Base)"],
        "Percentage (%)": [concentration, 100.0 - concentration],
        "Required Weight (g)": [round(active_grams, 2), round(solvent_grams, 2)]
    }
    st.table(pd.DataFrame(recipe_data))

with col2:
    st.subheader("Dynamic Safety & Solubility Audit")
    
    max_safe = CHEMICAL_DATABASE[active_name]["max_safe_pct"]
    
    # DYNAMIC LOOKUP: Get solubility specifically for the chosen solvent!
    solubility_limit = CHEMICAL_DATABASE[active_name]["solubility"].get(base_solvent, 0.0)
    
    flagged = False

    # Audit 1: Safety Limit Check
    if concentration > max_safe:
        st.error(f"**Safety Hazard:** {concentration}% exceeds the maximum safe limit of **{max_safe}%**.")
        flagged = True

    # Audit 2: Dynamic Solvent Solubility Check
    if concentration > solubility_limit:
        st.warning(
            f"⚠️ **Solubility Warning:** Potential precipitation! "
            f"Max solubility of {active_name} in **{base_solvent}** is **{solubility_limit}%**. "
            f"The active ingredient may not completely dissolve."
        )
        flagged = True

    if not flagged:
        st.success(f"✅ Formulation passed all checks for use in **{base_solvent}**.")