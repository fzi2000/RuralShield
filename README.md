# 🌍 RuralShield – AI-Powered Public Health Action System

## 🚨 Problem
Every 2 minutes, a woman dies from preventable pregnancy-related causes, and 90% of infectious disease deaths occur in low-resource settings.

These deaths are driven by the **Three Delays**:
- Delay in seeking care
- Delay in reaching the right facility
- Delay in receiving treatment

Frontline workers lack:
- Standardized triage tools
- Visibility into facility capabilities
- Early warning systems for outbreaks and malnutrition

---

##  Solution: RuralShield

RuralShield is a **dual-tier public health intelligence system** designed for low-resource environments.

### AI Action Engine
- Predicts maternal risk using ML (XGBoost)
- Classifies patients (Low → Critical)
- Explains risk factors (XAI-style reasoning)
- Provides personalized recommendations
- Generates referral slips instantly

###  Facility Matching
- Matches patients to hospitals based on:
  - ICU, Blood Bank, NICU, C-section
- Estimates travel time
- Prevents misdirected referrals

---

### Population Health Dashboard

#### 📊 Nutrition & Supply Gap Detection
- Detects:
  - Anemia
  - Malnutrition
  - Food insecurity
  - Water & sanitation issues
- Identifies high-risk regions
- Suggests targeted interventions

####  Infectious Disease Surveillance
- Tracks diseases (Malaria, Dengue, TB, COVID)
- Detects outbreak regions
- Simulates transmission networks
- Recommends interventions

---

### SMS Support (Low Connectivity)
- Enables basic triage via SMS
- Works in rural areas without internet

---

##  Tech Stack
- Python
- Streamlit
- XGBoost (ML model)
- Pandas / NumPy
- PyDeck (maps)
- NetworkX (disease spread)
- Matplotlib (visualizations)

---

##  Architecture
1. Input (Vitals / Region Data)
2. ML Model (Risk Prediction)
3. Rule-based + XAI Layer
4. Action Engine
5. Dashboard Visualization

---

## Impact
- Faster triage decisions
- Reduced maternal mortality
- Early outbreak detection
- Data-driven policy planning
- Improved healthcare equity

---

##  What was built during hackathon
- ML-based maternal risk prediction
- Explainable risk factors module
- Facility matching system
- Nutrition + disease surveillance dashboard
- Interactive maps & intervention engine

---

## ▶️ How to Run
```bash
pip install -r requirements.txt
streamlit run app.py