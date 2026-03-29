import streamlit as st
import requests

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="CarVal · AI Price Predictor",
    page_icon="🚗",
    layout="centered",
)

# ─────────────────────────────────────────────
#  CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Root & Body ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0a0a0f 0%, #13131c 60%, #0d0d18 100%);
    color: #f0efe9;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 4rem; max-width: 760px; }

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 2.5rem 1rem 2rem;
}
.badge {
    display: inline-block;
    background: rgba(255,107,53,0.12);
    border: 1px solid rgba(255,107,53,0.35);
    border-radius: 100px;
    padding: 5px 18px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #f7c59f;
    margin-bottom: 18px;
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: clamp(38px, 7vw, 62px);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, #ffffff 30%, #f7c59f 60%, #ff6b35 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 14px;
}
.hero p {
    color: #7c7c9a;
    font-size: 15px;
    font-weight: 300;
    line-height: 1.7;
    max-width: 440px;
    margin: 0 auto;
}

/* ── Section labels ── */
.section-label {
    font-family: 'Syne', sans-serif;
    font-size: 10px;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #4ecdc4;
    margin: 1.6rem 0 0.6rem;
    padding-bottom: 6px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
}

/* ── Card wrapper ── */
.card {
    background: #1a1a28;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 20px;
    padding: 2rem 2rem 1.6rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 32px 80px rgba(0,0,0,0.45);
    position: relative;
    overflow: hidden;
}
.card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,107,53,0.55), #ffe66d, rgba(78,205,196,0.55), transparent);
}

/* ── Inputs ── */
div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    border-radius: 10px !important;
    color: #f0efe9 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 15px !important;
    padding: 10px 14px !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
div[data-testid="stTextInput"] input:focus,
div[data-testid="stNumberInput"] input:focus {
    border-color: #ff6b35 !important;
    box-shadow: 0 0 0 3px rgba(255,107,53,0.2) !important;
}

/* ── Select boxes ── */
div[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    border-radius: 10px !important;
    color: #f0efe9 !important;
}

/* ── Labels ── */
label, .stTextInput label, .stNumberInput label, .stSelectbox label {
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 0.07em !important;
    text-transform: uppercase !important;
    color: #7c7c9a !important;
}

/* ── Predict button ── */
div[data-testid="stButton"] > button {
    width: 100%;
    padding: 16px 24px;
    border-radius: 12px;
    border: none;
    background: linear-gradient(135deg, #ff6b35 0%, #ff9a5c 100%);
    color: #ffffff;
    font-family: 'Syne', sans-serif;
    font-size: 18px;
    font-weight: 700;
    letter-spacing: 0.01em;
    cursor: pointer;
    box-shadow: 0 8px 32px rgba(255,107,53,0.3);
    transition: transform 0.15s, box-shadow 0.15s;
    margin-top: 1.2rem;
}
div[data-testid="stButton"] > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 14px 40px rgba(255,107,53,0.4);
}
div[data-testid="stButton"] > button:active {
    transform: translateY(0);
}

/* ── Success result card ── */
.result-success {
    background: linear-gradient(135deg, rgba(78,205,196,0.1), rgba(78,205,196,0.04));
    border: 1px solid rgba(78,205,196,0.3);
    border-radius: 18px;
    padding: 2rem;
    text-align: center;
    margin-top: 1.2rem;
}
.result-label {
    font-size: 10px;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #7c7c9a;
    margin-bottom: 10px;
}
.result-price {
    font-family: 'Syne', sans-serif;
    font-size: 54px;
    font-weight: 800;
    background: linear-gradient(135deg, #4ecdc4, #ffe66d);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
    margin-bottom: 10px;
}
.result-sub {
    color: #7c7c9a;
    font-size: 13px;
}

/* ── Error card ── */
.result-error {
    background: rgba(255,80,80,0.08);
    border: 1px solid rgba(255,80,80,0.28);
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    margin-top: 1rem;
    color: #ff9a9a;
    font-size: 14px;
}

/* ── JSON expander ── */
details {
    background: rgba(0,0,0,0.3) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 10px !important;
}
details summary {
    color: #7c7c9a !important;
    font-size: 13px !important;
    padding: 10px 14px !important;
    cursor: pointer !important;
}
.stJson {
    background: transparent !important;
}

/* ── Divider ── */
hr {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.06);
    margin: 1.2rem 0;
}

/* ── Footer ── */
.footer {
    text-align: center;
    color: #3a3a55;
    font-size: 12px;
    margin-top: 2.5rem;
    padding-bottom: 1rem;
}
.footer span { color: #ff6b35; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  HERO HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="badge">⚡ AI-Powered · Real-time</div>
    <h1>Car Price<br/>Predictor</h1>
    <p>Enter your car's details and our ML model will estimate the fair resale market value instantly.</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  API ENDPOINT CONFIG
# ─────────────────────────────────────────────
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-label">🔌 API Endpoint</div>', unsafe_allow_html=True)
API_URL = st.text_input(
    label="API URL",
    value="http://localhost:8000/predict",
    label_visibility="collapsed",
    placeholder="http://localhost:8000/predict",
)
st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  VEHICLE INFO CARD
# ─────────────────────────────────────────────
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-label">🚗 Vehicle Info</div>', unsafe_allow_html=True)

car_name = st.text_input("Car Name", value="swift", placeholder="e.g. swift, ritz, sx4")

col1, col2 = st.columns(2)
with col1:
    year = st.number_input("Year", min_value=1990, max_value=2026, value=2014, step=1)
with col2:
    present_price = st.number_input("Present Price (₹ Lakhs)", min_value=0.0, value=5.59, step=0.1, format="%.2f")

kms_driven = st.number_input("Kilometres Driven", min_value=0, value=40000, step=1000)

st.markdown("<hr/>", unsafe_allow_html=True)
st.markdown('<div class="section-label">⚙️ Specifications</div>', unsafe_allow_html=True)

col3, col4 = st.columns(2)
with col3:
    fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG"])
with col4:
    seller_type = st.selectbox("Seller Type", ["Dealer", "Individual"])

col5, col6 = st.columns(2)
with col5:
    transmission = st.selectbox("Transmission", ["Manual", "Automatic"])
with col6:
    owner_label = st.selectbox(
        "Owner History",
        ["0 — First Owner", "1 — Second Owner", "3 — Third Owner"]
    )
    owner = int(owner_label.split("—")[0].strip())

st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  BUILD PAYLOAD
# ─────────────────────────────────────────────
payload = {
    "Car_Name":      str(car_name),
    "Year":          int(year),
    "Present_Price": float(present_price),
    "Kms_Driven":    int(kms_driven),
    "Fuel_Type":     str(fuel_type),
    "Seller_Type":   str(seller_type),
    "Transmission":  str(transmission),
    "Owner":         int(owner),
}

with st.expander("📦 View JSON payload being sent"):
    st.json(payload)

# ─────────────────────────────────────────────
#  PREDICT BUTTON
# ─────────────────────────────────────────────
if st.button("Predict Price 💰"):
    with st.spinner("Running prediction..."):
        try:
            res = requests.post(API_URL, json=payload, timeout=20)

            if res.status_code == 200:
                data = res.json()
                pred = data.get("prediction_price", None)

                if pred is None:
                    st.markdown(f"""
                    <div class="result-error">
                        ⚠️ <strong>Prediction key not found.</strong><br/>
                        API responded but no <code>prediction</code> or <code>predicted_price</code> key found.<br/>
                        <small>Full response: {data}</small>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    car_display = car_name.strip().title()
                    st.markdown(f"""
                    <div class="result-success">
                        <div class="result-label">Estimated Resale Value</div>
                        <div class="result-price">₹ {float(pred):.2f} L</div>
                        <div class="result-sub">
                            {year} {car_display} &nbsp;·&nbsp; {fuel_type} &nbsp;·&nbsp; {transmission} &nbsp;·&nbsp; {kms_driven:,} km driven
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            else:
                st.markdown(f"""
                <div class="result-error">
                    ❌ <strong>API Error {res.status_code}</strong><br/>
                    <small>{res.text}</small>
                </div>
                """, unsafe_allow_html=True)

        except requests.exceptions.ConnectionError:
            st.markdown("""
            <div class="result-error">
                ❌ <strong>Connection failed.</strong><br/>
                Could not reach the API. Make sure your FastAPI server is running.
            </div>
            """, unsafe_allow_html=True)

        except requests.exceptions.Timeout:
            st.markdown("""
            <div class="result-error">
                ⏱️ <strong>Request timed out.</strong><br/>
                The API took too long to respond. Try again.
            </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.markdown(f"""
            <div class="result-error">
                ⚠️ <strong>Unexpected error:</strong><br/>
                <small>{str(e)}</small>
            </div>
            """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class="footer">
    Built with <span>♥</span> · Powered by FastAPI + ML · CarVal © 2025
</div>
""", unsafe_allow_html=True)
