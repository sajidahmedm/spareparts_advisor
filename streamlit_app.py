import streamlit as st
import base64
import requests
import os

# ================== UTILS ==================
def get_base64_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

BASE_DIR = os.path.dirname(__file__)
car_base64 = get_base64_image(
    os.path.join(BASE_DIR, "m8-competition-coupe-header.jpg")
)

# ================== CONFIG ==================
st.set_page_config(
    page_title="Spare Part Advisor",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================== SIDEBAR ==================
with st.sidebar:
    st.markdown("## ⚙️ Controls")
    dark_mode = st.toggle("🌙 Dark Mode", value=True)
    st.markdown("---")
    vehicle_type = st.selectbox("🚗 Vehicle Type", ["2-wheeler", "4-wheeler"])

# ================== THEME ==================
card_bg = "rgba(15,17,26,0.65)" if dark_mode else "rgba(255,255,255,0.85)"
text_color = "#FFFFFF" if dark_mode else "#111111"

# ================== STYLES ==================
st.markdown(f"""
<style>

/* ===== FULL SCREEN BACKGROUND ONLY IMAGE ===== */
html, body, [data-testid="stApp"] {{
    background: none !important;
}}

[data-testid="stAppViewContainer"] {{
    background:
        linear-gradient(rgba(0,0,0,0.45), rgba(0,0,0,0.45)),
        url("data:image/jpeg;base64,{car_base64}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}}

/* ===== REMOVE ALL STREAMLIT BACKGROUND BLOCKS ===== */
[data-testid="stAppViewBlockContainer"],
[data-testid="block-container"],
[data-testid="stVerticalBlock"],
[data-testid="stHorizontalBlock"] {{
    background: transparent !important;
    box-shadow: none !important;
}}

/* ===== SIDEBAR SMOOTH IN + OUT ===== */
[data-testid="stSidebar"] {{
    transition:
        transform 0.6s cubic-bezier(.22,1,.36,1),
        opacity 0.6s cubic-bezier(.22,1,.36,1);
}}

[data-testid="stSidebar"][aria-hidden="false"] {{
    opacity: 1;
    transform: translateX(0);
}}

[data-testid="stSidebar"][aria-hidden="true"] {{
    opacity: 0;
    transform: translateX(-40px);
    pointer-events: none;
}}

/* ===== MAIN GLASS CARD (ONLY ONE VISIBLE CARD) ===== */
.main > div {{
    max-width: 720px;
    margin: auto;
    padding: 2.6rem;
    background: {card_bg};
    color: {text_color};
    border-radius: 26px;
    box-shadow: 0 45px 90px rgba(0,0,0,0.6);
    animation: smoothEnter 0.9s cubic-bezier(.22,1,.36,1);
}}

/* ===== TITLE ===== */
h1 {{
    text-align: center;
    font-weight: 900;
    margin-bottom: 2rem;
    letter-spacing: 1px;
}}

/* ===== INPUTS ===== */
input, select {{
    transition: all 0.4s cubic-bezier(.22,1,.36,1);
}}

input:focus, select:focus {{
    transform: scale(1.03);
}}

/* ===== BUTTON ===== */
.stButton > button {{
    width: 100%;
    padding: 0.9rem;
    border-radius: 16px;
    font-size: 16px;
    font-weight: 700;
    background: linear-gradient(135deg, #2563EB, #38BDF8);
    color: white;
    border: none;
    transition: all 0.4s cubic-bezier(.22,1,.36,1);
}}

.stButton > button:hover {{
    transform: translateY(-5px) scale(1.04);
    box-shadow: 0 22px 55px rgba(56,189,248,0.7);
}}

.stButton > button:active {{
    transform: scale(0.97);
}}

/* ===== RESULT ANIMATION ===== */
.fade {{
    animation: fadeUp 0.75s cubic-bezier(.22,1,.36,1);
}}

@keyframes smoothEnter {{
    from {{
        opacity: 0;
        transform: translateY(40px) scale(0.94);
    }}
    to {{
        opacity: 1;
        transform: translateY(0) scale(1);
    }}
}}

@keyframes fadeUp {{
    from {{
        opacity: 0;
        transform: translateY(24px);
    }}
    to {{
        opacity: 1;
        transform: translateY(0);
    }}
}}

</style>
""", unsafe_allow_html=True)

# ================== TITLE ==================
st.markdown("<h1>🛠️ Spare Part Advisor</h1>", unsafe_allow_html=True)

# ================== PART DATA ==================
two_wheeler_parts = [
    "Crankshaft", "Cylinder Head", "Piston & Rings", "Connecting Rod",
    "Valves", "Battery", "Alternator", "Starter Motor",
    "Ignition System", "Chain", "Brake Pads", "Clutch"
]

four_wheeler_parts = [
    "Radiator", "Fuel Injector", "ECU", "Timing Belt",
    "Disc Brake", "Transmission", "Differential",
    "Shock Absorber", "AC Compressor", "Clutch Plate"
]

parts = two_wheeler_parts if vehicle_type == "2-wheeler" else four_wheeler_parts

# ================== SEARCH ==================
search = st.text_input("🔍 Search spare part")
filtered = [p for p in parts if search.lower() in p.lower()] if search else parts

if filtered:
    part = st.selectbox("Select spare part", filtered)
else:
    st.warning("No matching parts found")
    part = None

# ================== API ==================
if part and st.button("Get Info"):
    with st.spinner("Fetching part details..."):
        try:
            res = requests.post(
                "http://127.0.0.1:5000/get_info",
                json={"part": part, "vehicle_type": vehicle_type}
            )

            if res.status_code == 200:
                data = res.json()
                st.markdown("<div class='fade'>", unsafe_allow_html=True)
                st.subheader(f"🔧 {data['name']}")
                st.markdown(f"**Description:** {data['description']}")
                st.markdown(f"**Usage:** {data['usage']}")
                st.markdown("### 📺 YouTube Recommendations")
                for lang, link in data["videos"].items():
                    st.markdown(f"- **{lang}**: [Watch Video]({link})")
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.error("Part information not found")

        except Exception as e:
            st.error(f"Backend error: {e}")
