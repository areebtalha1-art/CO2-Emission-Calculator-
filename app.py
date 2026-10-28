import streamlit as st
import pandas as pd
from html import escape

EMISSION_FACTORS = {
    
    "India": {
        "Transportation": 0.14, #kgCO2/km
        "Electricity": 0.82, #kgCO2/KwH
        "Diet": 1.25, #kgCO2/meal, 2.5 kgCO2/kg,
        "Waste": 0.1, #kgCO2/kg
    }
}             

st.set_page_config(layout="wide", page_title="CO2 EMISSION CALCY BY HEISENBERG AKA TALHA")

st.markdown(
    """
    <style>
    .neon-card {
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
        border: 1px solid rgba(0, 220, 255, 0.6);
        border-radius: 12px;
        background: rgba(0, 220, 255, 0.08);
        box-shadow: 0 0 14px rgba(0, 220, 255, 0.14);
        font-size: 1.05rem;
        line-height: 1.55;
    }
    .neon-card strong {
        display: block;
        margin-bottom: 0.3rem;
        font-size: 1.1rem;
    }
    .neon-card p {
        margin: 0;
    }
    .neon-card--green {
        border-color: rgba(0, 255, 160, 0.6);
        background: rgba(0, 255, 160, 0.08);
        box-shadow: 0 0 14px rgba(0, 255, 160, 0.14);
    }
    .neon-card--pink {
        border-color: rgba(255, 90, 190, 0.6);
        background: rgba(255, 90, 190, 0.08);
        box-shadow: 0 0 14px rgba(255, 90, 190, 0.14);
    }
    .neon-card--amber {
        border-color: rgba(255, 190, 0, 0.65);
        background: rgba(255, 190, 0, 0.08);
        box-shadow: 0 0 14px rgba(255, 190, 0, 0.14);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def render_neon_card(title: str, message: str, color: str = "blue") -> None:
    st.markdown(
        f'<div class="neon-card neon-card--{color}">'
        f"<strong>{escape(title)}</strong><p>{escape(message)}</p></div>",
        unsafe_allow_html=True,
    )



st.title("CO2 Emission Calculator")


#user inputs
st.subheader("Your Country")

country = st.selectbox("Select", list(EMISSION_FACTORS))
country = country.strip()

if country not in EMISSION_FACTORS:
    st.error(f"Emission factors are not available for {country}.")
    st.stop()


col1, col2 = st.columns(2)

with col1:
    st.subheader("🚶 Daily compute distance (in km)")
    distance = st.slider("Distance", 0.0, 100.0, key ="distance_input")

    st.subheader("⚡Monthly Electricity Consumption (in kwh)")
    electricity = st.slider("Electricity", 0.0, 100.0, key ="electricity_input")

with col2:

    st.subheader("♻️Waste Generated per week (in kg)")
    waste = st.slider("Waste", 0.0, 100.0, key ="waste_input")

    st.subheader("🍛Number of Meals per day ")
    meals = st.number_input("Meals", 0, key ="Meals_input")

#normalize inputs
if distance > 0:
    distance = distance * 365 #convert distance to yearly

if electricity > 0:
    electricity = electricity * 12 #convert electricity to yearly

if waste > 0:
    waste = waste * 52 #convert waste to yearly

if meals > 0:
    meals = meals * 365 


#Calculate carbon emissions
transportation_emissions = EMISSION_FACTORS[country]['Transportation'] * distance
electricity_emissions = EMISSION_FACTORS[country]['Electricity'] * electricity
diet_emissions = EMISSION_FACTORS[country]['Diet'] * meals 
waste_emissions = EMISSION_FACTORS[country]['Waste'] * waste

transportation_emissions = round(transportation_emissions / 1000, 2)
electricity_emissions = round(electricity_emissions / 1000, 2)
diet_emissions = round(diet_emissions / 1000, 2)
waste_emissions = round(waste_emissions / 1000, 2)

#convert emissions to tonnes and round off to 2 decimal places

total_emissions = round(
    transportation_emissions + electricity_emissions + waste_emissions + diet_emissions, 2

)

if st.button("Calculate CO2 Emissions"):
    st.session_state["show_results"] = True

if not st.session_state.get("show_results", False):
    render_neon_card(
        "CO₂ emissions and climate",
        "CO₂ emissions come from activities such as transport, electricity use, "
        "food production, and waste. Greenhouse gases trap heat in the atmosphere "
        "and contribute to climate change. This calculator estimates your annual "
        "footprint from your inputs; actual emissions vary with factors such as "
        "your energy source, travel mode, and local waste practices.",
    )

if st.session_state.get("show_results", False):
    #Display Result
    st.header("Results")

    category_emissions = {
        "Transportation": transportation_emissions,
        "Electricity": electricity_emissions,
        "Diet": diet_emissions,
        "Waste": waste_emissions,
    }
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Carbon Emissions by Categories")
        for category, emissions in category_emissions.items():
            render_neon_card(
                category,
                f"{emissions} tonnes CO₂ per year",
                "green",
            )

    with col4:
        st.subheader("Total Carbon Footprint")
        render_neon_card(
            "Your total carbon footprint",
            f"{total_emissions} tonnes CO₂ per year",
            "pink",
        )
        render_neon_card(
            "India per-capita reference",
            "CO₂ emissions per capita in India were 2.19 tonnes per person, "
            "up by 0.08 tonnes from 2.12 tonnes in 2023.",
            "amber",
        )

    category_actions = {
        "Transportation": "Combine errands, choose public transport or carpool when practical, and walk or cycle for shorter trips.",
        "Electricity": "Use LED bulbs and efficient appliances, switch devices off when not in use, and check whether renewable electricity is available.",
        "Diet": "Plan portions to avoid leftovers and try replacing some meals with plant-rich options.",
        "Waste": "Prevent avoidable waste, reuse and recycle materials, and compost food scraps where local services allow.",
    }
    category_average = total_emissions / len(category_emissions)

    st.subheader("Ways to reduce your emissions")
    st.caption(
        "The comparison below is against your average across these four categories, "
        "not a national average."
    )
    categories = list(category_emissions.items())
    for row_start in range(0, len(categories), 2):
        advice_columns = st.columns(2)
        for column, (category, emissions) in zip(
            advice_columns, categories[row_start : row_start + 2]
        ):
            with column:
                if emissions > category_average:
                    render_neon_card(
                        f"{category} — above your category average",
                        f"Your estimate is {emissions} tonnes/year; your "
                        f"per-category average is {category_average:.2f} tonnes/year. "
                        f"Try this: {category_actions[category]}",
                        "amber",
                    )
                else:
                    render_neon_card(
                        f"{category} — at or below your category average",
                        f"To reduce these emissions further: {category_actions[category]}",
                        "green",
                    )

    st.subheader("Estimated emissions compared with averages")
    st.caption(
        "The overall comparison uses the India per-capita average of 2.19 tonnes "
        "of CO₂ per person per year."
    )
    overall_comparison = pd.DataFrame(
        {
            "Tonnes CO₂ per year": [2.19, total_emissions],
        },
        index=["India per-capita average", "Your estimate"],
    )
    st.bar_chart(overall_comparison)

    st.caption(
        "This category comparison uses your own average emissions across the "
        "four categories, not a national category average."
    )
    category_comparison = pd.DataFrame(
        {
            "Your estimate": list(category_emissions.values()),
            "Average per category": [category_average] * len(category_emissions),
        },
        index=list(category_emissions.keys()),
    )
    st.bar_chart(category_comparison)

    st.subheader("Official articles and resources")
    st.markdown(
        "- [UN ActNow: actions to help the climate](https://www.un.org/en/actnow/)\n"
        "- [U.S. EPA: Green Vehicles](https://www.epa.gov/greenvehicles)\n"
        "- [UNEP: Food Waste Index Report 2024](https://www.unep.org/resources/report/food-waste-index-report-2024)\n"
        "- [Bureau of Energy Efficiency, India](https://beeindia.gov.in/)"
    )

st.subheader("Credits")
st.markdown(
    "- Coding & Website: Talha Hamdule\n"
    "- Research: Rishabh Patil\n"
    "- PPT and paper: Safwan Shaikh\n"
    "- Calculations and idea: Sameer S Chavan"
)
