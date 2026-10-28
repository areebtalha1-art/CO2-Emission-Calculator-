import streamlit as st

EMISSION_FACTORS = {
    
    "India": {
        "Transportation": 0.14, #kgCO2/km
        "Electricity": 0.82, #kgCO2/KwH
        "Diet": 1.25, #kgCO2/meal, 2.5 kgCO2/kg,
        "Waste": 0.1, #kgCO2/kg
    }
}             

st.set_page_config(layout="wide", page_title="CO2 EMISSION CALCY BY HEISENBERG AKA TALHA")



st.title("CO2 Emission Calculator")


#user inputs
st.subheader("Your Country")

country = st.selectbox("Select", ["India","USA","UK","Germany","France","Indonesia","Spain","Brazil"])
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
    waste = waste * 52 #convert meals to yearly

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

    #Display Result
    st.header("Results")

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Carbon Emissions by Categories")
        st.info(f"🚶 Transportation: {transportation_emissions} tonnes Co2 per year")
        st.info(f"⚡Electricity: {electricity_emissions} tonnes Co2 per year")
        st.info(f"🍛Diet: {diet_emissions} tonnes Co2 per year")
        st.info(f"♻️Waste: {waste_emissions} tonnes Co2 per year")

        with col4:
                    st.subheader("Total Carbon Footprint")
                    st.info(f"🌍Your Total Carbon footprint is: {total_emissions} tonnes CO2 per year")
                    st.warning("CO2 emissions per capita in India are equivalent to 2.19 tons per person, an increase by 0.08 over the figure of 2.12 CO2 tons per person registered in 2023.")
            

    category_emissions = {
        "Transportation": transportation_emissions,
        "Electricity": electricity_emissions,
        "Diet": diet_emissions,
        "Waste": waste_emissions,
    }
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
    for category, emissions in category_emissions.items():
        if emissions > category_average:
            st.warning(
                f"Your {category.lower()} emissions ({emissions} tonnes/year) are "
                f"above your per-category average ({category_average:.2f} tonnes/year). "
                f"Try this: {category_actions[category]}"
            )
        else:
            st.info(
                f"Your {category.lower()} emissions are at or below your "
                f"per-category average. To reduce them further: {category_actions[category]}"
            )

    st.subheader("Official articles and resources")
    st.markdown(
        "- [UN ActNow: actions to help the climate](https://www.un.org/en/actnow/)\n"
        "- [U.S. EPA: Green Vehicles](https://www.epa.gov/greenvehicles)\n"
        "- [UNEP: Food Waste Index Report 2024](https://www.unep.org/resources/report/food-waste-index-report-2024)\n"
        "- [Bureau of Energy Efficiency, India](https://beeindia.gov.in/)"
    )
                                                                        
