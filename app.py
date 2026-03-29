from fpdf import FPDF
from sklearn.linear_model import LinearRegression
import streamlit as st
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import time
import pydeck as pdk
import joblib
model = joblib.load("maternal_risk_model.pkl")


st.set_page_config(page_title="RuralShield", layout="wide")
button_style = """
<style>
div.home-tile div[data-testid="stButton"] > button {
    min-height: 200px; 
    min-width: 200px;
    width: 80%;

    font-size: 100px;
    font-weight: 800 !important;
    line-height: 1.2 !important;
    background-color: #ffffff;
    color: #1E1E1E !important;

    border: 3px solid #E0E0E0 !important;
    border-radius: 30px !important;

    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    transition: all 0.25s ease-in-out;
    white-space: pre-wrap !important;
}

/* Hover effect */
div[data-testid="stButton"] > button:hover {
    border-color: #ff4b4b !important;
    color: #ff4b4b !important;
    transform: scale(1.03);
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
}
</style>
"""

st.markdown(button_style, unsafe_allow_html=True)
# --- SESSION STATE ---
if "page" not in st.session_state:
    st.session_state.page = "home"
@st.cache_data
def load_supply_data():

    return pd.DataFrame({
        "Region":[
            "Rural District A",
            "Rural District B",
            "Rural District C",
            "Rural District D",
            "Rural District E"
        ],

        "lat":[25.20,25.23,25.28,25.26,25.30],
        "lon":[55.27,55.30,55.32,55.29,55.34],

        "Population":[52000,41000,67000,36000,48000],
        "Hospital_Beds":[110,45,60,20,50],
        "Doctors":[32,14,18,8,16],
        "Malnutrition_Rate_%":[18,32,25,40,21],
        "Anemia_%":[20,66,38,25,43],
        "Child_Anemia_%":[30,46,38,52,35],
        "Maternal_Risk_Cases":[120,210,170,260,140],
        "Vaccination_Coverage_%":[78,61,70,55,74],
        "Clean_Water_Access_%":[82,60,68,52,75]
    })


@st.cache_data
def load_disease_data():

    return pd.DataFrame({
        "Region":[
            "Rural District A",
            "Rural District B",
            "Rural District C",
            "Rural District D",
            "Rural District E"
        ],

        "lat":[25.20,25.23,25.28,25.26,25.30],
        "lon":[55.27,55.30,55.32,55.29,55.34],
        "Population":[52000,41000,67000,36000,48000],

        "Malaria":[85,40,120,65,50],
        "Dengue":[22,8,30,15,12],
        "Cholera":[6,3,10,4,2],
        "Tuberculosis":[18,9,21,12,10],
        "Measles":[12,6,15,8,7],
        "COVID":[9,4,11,5,3]
    })

st.markdown(button_style, unsafe_allow_html=True)
# --- SESSION STATE ---
if "page" not in st.session_state:
    st.session_state.page = "home"


# --- HOME PAGE ---
def home():

    st.title("RuralShield")
    st.subheader("Public Health Action System for Low-Resource Areas")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="home-tile">', unsafe_allow_html=True)
        if st.button("🌍\n\n\nPublic Health", use_container_width=True):
            st.session_state.page = "public_health"
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="home-tile">', unsafe_allow_html=True)
        if st.button("🍼\n\n\nMaternal Care", use_container_width=True):
            st.session_state.page = "maternal"
        st.markdown('</div>', unsafe_allow_html=True)        
        st.markdown("This is a hackathon prototype for educational purposes and not a substitute for professional medical advice.", unsafe_allow_html=True)

# --- PUBLIC HEALTH PAGE ---
def public_health():
    st.title("Public Health ")
    tab1, tab2 = st.tabs(["Supply Gap Detection", "Infectious Disease Tracking"])

    # -------------------------
    # TAB 1 – SUPPLY GAP HEATMAP
    # -------------------------
    with tab1:
        st.subheader("Supply Gap Detection")
        # -------------------------
        # DATA (FOCUSED ON NUTRITION)
        # -------------------------
        df = pd.DataFrame({
            "Region":[
                " District A",
                " District B",
                " District C",
                " District D",
                " District E"
            ],
            "lat":[25.20,25.23,25.28,25.26,25.30],
            "lon":[55.27,55.30,55.32,55.29,55.34],

            "Anemia":[32,14,58,48,22],
            "Child_Anemia":[50,20,54,89,10],
            "Child_Malnutrition":[78,61,70,55,74],

            "Iron_Supply_Level": ["Low", "Adequate", "Low", "Very Low", "Adequate"],
    "Food_Access": ["Medium", "Low", "Medium", "Critical", "Medium"],

    # NEW FACTORS
    "Water_Quality": ["Moderate", "Poor", "Poor", "Moderate", "Good"],
    "Sanitation_Level": ["Medium", "Low", "Low", "Low", "High"],
    "Hygiene_Awareness": ["Low", "Medium", "Low", "Low", "High"]
        })

        # -------------------------
        # MAP (OPTIONAL CONTEXT)
        # -------------------------
        st.map(df[["lat","lon"]])

        # -------------------------
        # ISSUE DETECTION ENGINE
        # -------------------------
        def detect_issues(row):
            issues = []

            if row["Anemia"] > 50:
                issues.append("Severe anemia")
            if row["Child_Anemia"] > 60:
                issues.append("Child anemia crisis")
            if row["Child_Malnutrition"] > 65:
                issues.append("Child malnutrition")
            if row["Food_Access"] == "Low":
                issues.append("Food insecurity")
            if row["Water_Quality"] == "Poor":
                issues.append("Unsafe drinking water")
            if row['Sanitation_Level'] == "Low":
                issues.append("Poor sanitation")
            if row['Hygiene_Awareness'] == "Low":
                issues.append("Low hygiene awareness")
            return issues
        df["Issues"] = df.apply(detect_issues, axis=1)

        # -------------------------
        # ACTION GENERATION ENGINE
        # -------------------------
        def generate_actions(issues):
            actions = []

            if "Severe anemia" in issues:
                actions.append("Distribute iron & folic acid supplements")
            if "Child anemia crisis" in issues:
                actions.append("School-based nutrition programs")
            if "Child malnutrition" in issues:
                actions.append("Emergency feeding programs")
            if "Food insecurity" in issues:
                actions.append("Food aid & subsidy programs")
            if "Unsafe drinking water" in issues:
                actions.append("Provide clean water + sanitation support")
            if "Poor sanitation" in issues:
                actions.append("Sanitation infrastructure (toilets, waste systems)")
            if "Low hygiene awareness" in issues:
                actions.append("Community hygiene education programs")
            if "Food crisis" in issues:
                actions.append("Emergency food aid + nutrition packages")
            return ", ".join(actions) if actions else "Routine monitoring"

        df["Recommended_Action"] = df["Issues"].apply(generate_actions)

        # -------------------------
        # SEVERITY SCORING
        # -------------------------
        def severity_score(row):
            score = 0

            score += 3 if row["Anemia"] > 50 else 1
            score += 3 if row["Child_Anemia"] > 60 else 1
            score += 3 if row["Child_Malnutrition"] > 65 else 1
            score += 2 if row["Food_Access"] == "Low" else 0
            score += 2 if row["Water_Quality"] == "Poor" else 0

            return score

        df["Severity"] = df.apply(severity_score, axis=1)

        # Sort by priority
        df = df.sort_values("Severity", ascending=False)

        # -------------------------
        # FINAL OUTPUT (MAIN FEATURE)
        # -------------------------
        st.subheader(" Priority Nutrition Intervention Regions")

        # MALNUTRITION SEVERITY SCORING (0-100)
        df['Severity_Score'] = (
            (df['Anemia'] / 40 * 25) +           # WHO threshold ~40%
            (df['Child_Anemia'] / 50 * 35) +     # Child threshold ~50%
            (df['Child_Malnutrition'] / 60 * 30) + # Malnutrition threshold ~60%
            (df['Iron_Supply_Level'].map({'Very Low':25, 'Low':15, 'Medium':5, 'Adequate':0}) * 0.1)
        ).round(1)
        display_data = df[['Severity_Score']].copy()
        display_data = display_data.sort_values('Severity_Score', ascending=False)
        st.dataframe(
            display_data.style
            .background_gradient(subset=['Severity_Score'], cmap='Reds')
            .format({'Severity_Score': '{:.1f}', 'Child_Anemia_%': '{:.0f}%', 'Child_Malnutrition_%': '{:.0f}%'})
        )

        # -------------------------
        # OPTIONAL TABLE (FOR DEBUG / DETAILS)
        # -------------------------
        # Remove unwanted columns
        display_df = df.drop(columns=["lat", "lon"], errors="ignore")
        # Reorder columns (put important ones first)
        priority_cols = ["Region", "Issues", "Recommended_Action", "Severity"]
        # Get remaining columns dynamically
        remaining_cols = [col for col in display_df.columns if col not in priority_cols]
        # Final column order
        final_cols = priority_cols + remaining_cols
        # Display
        st.dataframe(display_df[final_cols])
        
        # EMERGENCY BUTTON
        if st.button(" Generate Crisis Report", type="primary"):
            csv = display_data.to_csv(index=False)
            st.download_button(
                " Download Priority Intervention List",
                csv,
                "rural_malnutrition_crisis.csv",
                "text/csv"
            )


    
    # -------------------------
    # TAB 2 – INFECTIOUS DISEASE TRACKING
    # -------------------------
    with tab2:
        st.subheader("Infectious Disease Surveillance")

        disease_data = pd.DataFrame({
            "Region":[
                "Rural District A",
                "Rural District B",
                "Rural District C",
                "Rural District D",
                "Rural District E"
            ],
            "lat":[25.20,25.23,25.28,25.26,25.30],
            "lon":[55.27,55.30,55.32,55.29,55.34],

            "Population":[52000,41000,67000,36000,48000],
            "Malaria":[85,40,120,65,50],
            "Dengue":[22,8,30,15,12],
            "Cholera":[6,3,10,4,2],
            "Tuberculosis":[18,9,21,12,10],
            "Measles":[12,6,15,8,7],
            "COVID":[9,4,11,5,3]
        })
          
        disease = st.selectbox(
        "Select Disease to Monitor",
        [
            "Malaria",
            "Dengue",
            "Cholera",
            "Tuberculosis",
            "Measles",
            "COVID"
        ])     
        chart_data = disease_data.set_index("Region")[disease]
        st.subheader(f"{disease} Cases by Region")
        st.bar_chart(chart_data)
        disease_data["Cases_per_1000"] = (
        disease_data[disease] / disease_data["Population"] * 1000).round(2)
        outbreak = disease_data[disease_data["Cases_per_1000"] > 1]

        top_region = disease_data.loc[disease_data[disease].idxmax()]

        st.warning(f" Highest Risk Region: {top_region['Region']}")
        st.subheader("Disease Transmission Network")

        G = nx.Graph()
        # Add districts as nodes
        for i,row in disease_data.iterrows():
            G.add_node(row["Region"], cases=row[disease])

        # Simulated transmission links (district connectivity)
        connections = [
            ("Rural District A","Rural District B"),
            ("Rural District B","Rural District C"),
            ("Rural District C","Rural District D"),
            ("Rural District D","Rural District E"),
            ("Rural District A","Rural District C")
        ]

        G.add_edges_from(connections)
      # Node colors based on case count
        node_colors = []
        for node in G.nodes:
            cases = G.nodes[node]["cases"]

            if cases > 100:
                node_colors.append("red")
            elif cases > 50:
                node_colors.append("orange")
            elif cases > 20:
                node_colors.append("yellow")
            else:
                node_colors.append("green")

        # Draw graph
        fig, ax = plt.subplots()
        pos = nx.spring_layout(G)
        nx.draw(
            G,
            pos,
            with_labels=True,
            node_color=node_colors,
            node_size=200,
            font_size=9,
            ax=ax
        )
        if st.checkbox("Show Transmission Network"):
            st.pyplot(fig)
            
        disease_data["Water_Quality"] = ["Good","Poor","Moderate","Poor","Moderate"]
        disease_data["Mosquito_Index"] = [70,40,85,60,55]
        disease_data["Sanitation_Level"] = ["Medium","Low","Medium","Low","High"]
        def get_cause(row, disease):
            if disease == "Malaria" or disease == "Dengue":
                return "High mosquito density" if row["Mosquito_Index"] > 60 else "Moderate risk"
            elif disease == "Cholera":
                return "Poor water quality" if row["Water_Quality"] == "Poor" else "Safe"
            elif disease == "Tuberculosis":
                return "Overcrowding / poor ventilation"
            elif disease == "Measles":
                return "Low vaccination coverage"
            elif disease == "COVID":
                return "Community transmission"
        disease_data["Likely_Cause"] = disease_data.apply(lambda row: get_cause(row, disease), axis=1)
        st.subheader("Causes and Recommended Action")

        def intervention(row, disease, get_cause):
            if disease == "Malaria":
                if get_cause == "High mosquito density":
                    return "Send for stagnant water inspection"
                return "Distribute mosquito nets"
            elif disease == "Dengue":
                return "Eliminate stagnant water"
            elif disease == "Cholera":
                return "Provide clean water + ORS"
            elif disease == "Tuberculosis":
                return "Screen close contacts"
            elif disease == "Measles":
                return "Urgent vaccination campaign"
            elif disease == "COVID":
                return "Isolation + mask distribution"
        disease_data["Action"] = disease_data.apply(lambda row: intervention(row, disease, get_cause), axis=1)
        growth_rate = 1.15  # assume 15% increase
        disease_data["Predicted_Cases (Next week)"] = (disease_data[disease] * growth_rate).astype(int)
        st.write(disease_data[["Region","Likely_Cause", "Predicted_Cases (Next week)", "Action"]])

        # st.subheader("Outbreak Map")
        # st.map(disease_data[["lat","lon"]])
#         disease_data["Outbreak_Risk"] = (
#     (disease_data[disease] / disease_data["Population"]) * 1000 * 0.5 +
#     (disease_data["Mosquito_Index"] / 100) * 0.3 +
#     (disease_data["Water_Quality"].map({"Poor":1, "Moderate":0.5, "Good":0}) * 0.2)
# ).round(2)
#         st.subheader("Overall Outbreak Risk Score")
#         st.subheader("Outbreak Risk Ranking")
#         st.write(disease_data.sort_values("Outbreak_Risk", ascending=False)[["Region","Outbreak_Risk"]])
        
    if st.button("⬅ Back to Home"):
        st.session_state.page = "home"


# --- MATERNAL HEALTH PAGE ---
def maternal_health():
    st.title("Maternal Health Module")

    tab1, tab2 = st.tabs(["Action Engine", "Facility Matching"])
    def generate_referral():
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200,10,"Maternal Referral Slip",ln=True)
            pdf.cell(200,10,f"Triage Level: {triage}",ln=True)
            pdf.cell(200,10,f"Risk Score: {risk_percent}%",ln=True)
            pdf.cell(200,10,"Recommended Facility:",ln=True)
            # pdf.cell(200,10,service_matches.iloc[0]["Facility"],ln=True)

            file="referral.pdf"
            pdf.output(file)

            return file
    # ----------------------
    # ACTION ENGINE TAB
    # ----------------------
    with tab1:

        st.subheader("Risk Detection & Action Engine")

        age = st.number_input("Mother Age", 12, 60, 20)
        sys_bp = st.number_input("Systolic BP", 60, 250, 120)
        dia_bp = st.number_input("Diastolic BP", 40, 150, 80)
        bs = st.number_input("Blood Sugar (mmol/L)", 2.0, 20.0, 5.0)
        temp = st.number_input("Body Temperature (°C)", 34.0, 42.0, 37.0)
        hr = st.number_input("Heart Rate (bpm)", 40, 180, 80)
           
        if st.button("Run Risk Assessment"):
            input_data = [[age, sys_bp, dia_bp, bs, temp, hr]]
            prediction = model.predict(input_data)[0]
            probability = model.predict_proba(input_data).max() * 100

            if prediction == "high risk":
                triage = "Critical"
                color = "red"
                action = "Immediate hospital referral"
            elif prediction == "mid risk":
                triage = "Moderate"
                color = "orange"
                action = "Frequent monitoring and medical consultation"
            else:
                triage = "Low"
                color = "green"
                action = "Routine antenatal care"

            risk_score = 0
            risk_factors = []
            recommendations = []

            if sys_bp > 140 and sys_bp<180:
                risk_score += 10
                risk_factors.append("High Systolic BP")
                recommendations.append("Take antihypertensive medication")
            
            if sys_bp > 180:
                risk_score += 20
                risk_factors.append("Very High Systolic BP")
                recommendations.append("Take antihypertensive medication")

            if dia_bp > 90 and dia_bp<100:
                risk_score += 10
                risk_factors.append("High Diastolic BP")
                recommendations.append("Monitor BP daily")
            
            if dia_bp > 100:
                risk_score += 20
                risk_factors.append("Very High Diastolic BP")
                recommendations.append("Monitor BP daily and take medicines")

            if bs > 8 and bs<10:
                risk_score += 10
                risk_factors.append("High Blood Sugar")
                recommendations.append("Gestational diabetes screening & diet control")

            if bs > 10:
                risk_score += 20
                risk_factors.append("High Blood Sugar")
                recommendations.append("Gestational diabetes screening & diet control")

            if temp > 38:
                risk_score +=25
                risk_factors.append("Fever detected")
                recommendations.append("Check for infection")

            if hr > 110:
                risk_score += 20
                risk_factors.append("Elevated heart rate")
                recommendations.append("Cardiac evaluation recommended")
            risk_percent = min(risk_score, 100)

            # TRIAGE
            if risk_percent >= 80:
                triage = "Critical"
                action = "Immediate referral to emergency obstetric facility"
                color = "red"
            elif risk_percent >= 60:
                triage = "High risk"
                action = "Schedule visit to the nearest facility"
                color = "orange"
            elif risk_percent >= 40:
                triage = "Moderate risk"
                action ="Monitor closely and schedule doctor visit"
                color = "yellow"
            else:
                triage = "Low risk"
                action = "You are safe"
                color = "green"
        
            st.markdown(f"<h4 style='color:{color}'>Triage Category: {triage}. Risk Probability {risk_percent}% </h4>", unsafe_allow_html=True)
            st.subheader(" ")

            st.subheader("🩺 Key Risk Factors & Recommendations")
            if risk_factors:
                for factor, rec in zip(risk_factors, recommendations):
                    st.warning(f"{factor} — {rec}")
            else:
                st.success("No major clinical risk factors detected")
            

            if triage == "Critical":
                file = generate_referral()
                with open(file,"rb") as f:
                    st.download_button(
                        "Download Referral Slip",
                        f,
                        file_name="referral.pdf"
                    )

    # ----------------------
    # FACILITY MATCHING TAB
    # ----------------------

    with tab2:
        facilities = pd.DataFrame({

            "Facility":[
            "Dubai Hospital",
            "Latifa Women and Children Hospital",
            "Rashid Hospital",
            "Mediclinic City Hospital",
            "NMC Royal Hospital Dubai",
            "Al Qassimi Hospital",
            "University Hospital Sharjah",
            "Zulekha Hospital Sharjah",
            "Thumbay Hospital Ajman",
            "Saudi German Hospital Ajman",
            "Sheikh Shakhbout Medical City",
            "Corniche Hospital",
            "Burjeel Hospital Abu Dhabi",
            "RAK Hospital",
            "Ibrahim Bin Hamad Obaidullah Hospital"
            ],

            "City":[
            "Dubai","Dubai","Dubai","Dubai","Dubai",
            "Sharjah","Sharjah","Sharjah",
            "Ajman","Ajman",
            "Abu Dhabi","Abu Dhabi","Abu Dhabi",
            "Ras Al Khaimah","Ras Al Khaimah"
            ],

            "District":[
            "Deira","Oud Metha","Oud Metha","Healthcare City","Al Nahda",
            "Al Qassimi","University City","Al Nahda",
            "Al Jurf","Al Tallah",
            "Al Mafraq","Al Danah","Al Najda",
            "Al Seer","Al Uraibi"
            ],

            "lat":[
            25.276987,25.2219,25.2147,25.2285,25.2895,
            25.3463,25.3095,25.3162,
            25.4052,25.3927,
            24.4136,24.4794,24.4667,
            25.7895,25.7751
            ],

            "lon":[
            55.296249,55.3420,55.3075,55.3210,55.3734,
            55.4209,55.4895,55.4230,
            55.5136,55.4761,
            54.6230,54.3705,54.3753,
            55.9762,55.9424
            ],

            "Facility_Type":[
            "Government","Government","Government","Private","Private",
            "Government","Government","Private",
            "Private","Private",
            "Government","Government","Private",
            "Private","Government"
            ],

            "C-section":[
            "Yes","Yes","Yes","Yes","Yes",
            "Yes","Yes","Yes",
            "Yes","Yes",
            "Yes","Yes","Yes",
            "Yes","Yes"
            ],

            "Blood Bank":[
            "Yes","Yes","Yes","Yes","Yes",
            "Yes","Yes","Yes",
            "No","Yes",
            "Yes","Yes","Yes",
            "Yes","Yes"
            ],

            "NICU":[
            "Yes","Yes","Yes","Yes","Yes",
            "Yes","Yes","Yes",
            "No","Yes",
            "Yes","Yes","Yes",
            "Yes","No"
            ],

            "ICU":[
            "Yes","Yes","Yes","Yes","Yes",
            "Yes","Yes","No",
            "No","Yes",
            "Yes","Yes","Yes",
            "Yes","No"
            ],

            "Emergency_OBGYN":[
            "Yes","Yes","Yes","Yes","Yes",
            "Yes","Yes","Yes",
            "No","Yes",
            "Yes","Yes","Yes",
            "No","Yes"
            ],

            "Ventilator":[
            "Yes","Yes","Yes","Yes","Yes",
            "Yes","Yes","Yes",
            "No","Yes",
            "Yes","Yes","Yes",
            "Yes","No"
            ],

            "Beds_Available":[
            45,38,52,30,28,
            40,35,22,
            18,20,
            60,42,35,
            25,30
            ],

            "Ambulance":[
            "Yes","Yes","Yes","Yes","Yes",
            "Yes","Yes","Yes",
            "Yes","Yes",
            "Yes","Yes","Yes",
            "Yes","Yes"
            ],

            "Emergency_Contact":[
            "+97142199999",
            "+97142199998",
            "+97142199997",
            "+97144299999",
            "+97146079999",
            "+97165039999",
            "+97165055888",
            "+97165981111",
            "+97167463000",
            "+97167410000",
            "+97125059999",
            "+97126140000",
            "+97125080000",
            "+97172070000",
            "+97172354444"
            ]

            })

            
        district = st.selectbox(
        "Select District",
        facilities["City"].unique()
        )

        service_needed = st.selectbox(
            "Select Required Service",
            ["Blood Bank", "Ventilator","ICU","Emergency_OBGYN", "C-section","NICU"])

        matches = facilities[
        (facilities["City"] == district) &
        (facilities[service_needed] == "Yes")
        ]
        # Filter by district
        district_matches = facilities[facilities["City"] == district]

        # Filter by service
        service_matches = district_matches[
            district_matches[service_needed] == "Yes"
        ]

        if service_matches.empty:
            st.warning("No facilities found for this service in the selected district.")

        else:
            st.success("Matching Facilities")

            # Simulated travel time calculation
            # Assume 40 km/h average ambulance speed
            service_matches = service_matches.copy()

            # fake distance estimate (demo)
            service_matches["Distance_km"] = np.random.randint(3, 15, size=len(service_matches))

            service_matches["Travel_Time_Min"] = (
                service_matches["Distance_km"] / 40 * 60
            ).round(0)

            st.dataframe(
                service_matches[
                    ["Facility", "City","District", "Distance_km", "Travel_Time_Min", "Facility_Type", "Beds_Available", "Emergency_Contact"]
                ]
            )

            st.subheader("Hospital Locations")
            if "service_matches" in locals() and not service_matches.empty:
                
                layer = pdk.Layer(
                    "ScatterplotLayer",
                    data=service_matches,
                    get_position='[lon, lat]',
                    get_radius=500,
                    get_fill_color=[255, 0, 0],
                    pickable=True
                )

                view_state = pdk.ViewState(
                    latitude=service_matches["lat"].mean(),
                    longitude=service_matches["lon"].mean(),
                    zoom=10
                )

                st.pydeck_chart(pdk.Deck(
                    layers=[layer],
                    initial_view_state=view_state
                ))
            else:
                st.info("Run Facility Matching first to view hospital locations.")

    if st.button("⬅ Back to Home"):
        st.session_state.page = "home"


# --- ROUTER ---
if st.session_state.page == "home":
    home()

elif st.session_state.page == "public_health":
    public_health()

elif st.session_state.page == "maternal":
    maternal_health()