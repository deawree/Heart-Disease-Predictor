from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

# ─────────────────────────────────────────────────────────────
# Page setup
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Heart Risk Check",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="expanded",
)

BLUE = "#1B6B93"
CORAL = "#C8433B"
GREEN = "#1F7A5C"
AMBER = "#C98A1B"

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&display=swap');

:root {color-scheme: light only;}

/* ── Light surface, whatever the browser or Streamlit theme says ── */
html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: #F4F7F9 !important; color: #16222E !important;
    font-family: 'IBM Plex Sans', system-ui, sans-serif !important;
}
[data-testid="stHeader"] {background: transparent !important;}
#MainMenu, footer {visibility: hidden;}
.block-container {padding-top: 1.6rem; padding-bottom: 3rem; max-width: 1180px;}

/* ── Dark text everywhere ── */
.stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
.stApp p, .stApp li, .stApp label, .stApp legend,
.stApp [data-testid="stMarkdownContainer"] p,
.stApp [data-testid="stWidgetLabel"], .stApp [data-testid="stWidgetLabel"] p,
.stApp [data-testid="stRadio"] label p,
.stApp [data-testid="stSliderThumbValue"], .stApp [data-testid="stTickBarMin"],
.stApp [data-testid="stTickBarMax"] {
    color: #16222E !important;
}
.stApp [data-testid="stCaptionContainer"], .stApp [data-testid="stCaptionContainer"] p {color: #4A5B69 !important;}

/* ── Dropdowns (selectbox): white box, dark text ── */
.stApp [data-baseweb="select"] div,
.stApp [data-baseweb="select"] span {
    background-color: #FFFFFF !important; color: #16222E !important;
    -webkit-text-fill-color: #16222E !important;
}
.stApp [data-baseweb="select"] > div {border: 1px solid #B8C5D0 !important; border-radius: 8px !important;}
.stApp [data-baseweb="select"] svg {fill: #16222E !important;}

/* ── Number inputs ── */
.stApp [data-baseweb="input"], .stApp [data-baseweb="input"] > div, .stApp [data-baseweb="base-input"] {
    background-color: #FFFFFF !important; border-color: #B8C5D0 !important;
}
.stApp input {color: #16222E !important; -webkit-text-fill-color: #16222E !important; background-color: #FFFFFF !important;}
.stApp [data-testid="stNumberInput"] button {background-color: #EAF1F5 !important;}
.stApp [data-testid="stNumberInput"] button svg {fill: #16222E !important;}

/* ── Radio buttons ── */
.stApp label[data-baseweb="radio"] > div:first-child {
    background-color: #FFFFFF !important; border: 2px solid #7C8D9B !important;
}
.stApp label[data-baseweb="radio"]:has(input:checked) > div:first-child {
    background-color: #1B6B93 !important; border-color: #1B6B93 !important;
}

/* Dropdown menus open in a layer outside .stApp */
[data-baseweb="popover"], [data-baseweb="popover"] > div, [data-baseweb="menu"], ul[role="listbox"] {
    background: #FFFFFF !important;
}
[data-baseweb="popover"] li, [data-baseweb="popover"] li *, ul[role="listbox"] li, [data-baseweb="menu"] * {
    color: #16222E !important; background: transparent !important;
}
[data-baseweb="popover"] li:hover, ul[role="listbox"] li[aria-selected="true"] {background: #EAF1F5 !important;}

/* ── Buttons ── */
.stApp .stButton > button, .stApp .stDownloadButton > button {
    background: #FFFFFF !important; border: 1px solid #B8C5D0 !important; border-radius: 8px; font-weight: 500;
}
.stApp .stButton > button p, .stApp .stDownloadButton > button p {color: #16222E !important;}
.stApp .stButton > button:hover, .stApp .stDownloadButton > button:hover {
    border-color: #1B6B93 !important; background: #EAF1F5 !important;
}

.stApp .stButton > button[kind="primary"], .stApp .stButton > button[data-testid="stBaseButton-primary"] {
    background: #1B6B93 !important; border: 1px solid #1B6B93 !important; padding: 0.65rem 1rem;
}
.stApp .stButton > button[kind="primary"] p, .stApp .stButton > button[data-testid="stBaseButton-primary"] p {
    color: #FFFFFF !important; font-weight: 600; font-size: 1.05rem;
}
.stApp .stButton > button[kind="primary"]:hover, .stApp .stButton > button[data-testid="stBaseButton-primary"]:hover {
    background: #155873 !important; border-color: #155873 !important;
}
.stApp .placeholder {
    background: #FFFFFF !important; border: 1px dashed #B8C5D0; border-radius: 12px; padding: 34px 26px; text-align: center;
}
.stApp .placeholder .t {font-size: 1.1rem; font-weight: 600; color: #16222E !important; margin: 0 0 6px 0;}
.stApp .placeholder .d {font-size: 0.95rem; line-height: 1.5; color: #4A5B69 !important; margin: 0;}

/* ── Sidebar ── */
section[data-testid="stSidebar"], section[data-testid="stSidebar"] > div {
    background: #FFFFFF !important; border-right: 1px solid #DCE4EA;
}

/* ── Input cards ── */
.stApp [data-testid="stVerticalBlockBorderWrapper"] {
    background: #FFFFFF !important; border-radius: 12px !important; border-color: #DCE4EA !important;
}
.stApp .group-title {font-weight: 600; font-size: 1.02rem; margin: 0 0 2px 0; color: #16222E !important;}
.stApp .group-note {font-size: 0.86rem; margin: 0 0 10px 0; color: #4A5B69 !important;}

/* ── Header band ── */
.stApp .hero {background: #16222E !important; border-radius: 14px; padding: 28px 32px 0 32px; overflow: hidden; margin-bottom: 22px;}
.stApp .hero h1 {font-size: 2rem; font-weight: 600; margin: 0 0 6px 0; letter-spacing: -0.01em; color: #FFFFFF !important; padding: 0;}
.stApp .hero p {margin: 0 0 14px 0; color: #D3DEE7 !important; font-size: 0.98rem; max-width: 620px; line-height: 1.5;}
.hero svg {display: block; width: 100%; height: 64px;}
.ecg {
    fill: none; stroke: #6FC3E8; stroke-width: 2.2; stroke-linejoin: round; stroke-linecap: round;
    stroke-dasharray: 1400; stroke-dashoffset: 1400; animation: draw 2.4s ease-out forwards;
}
@keyframes draw {to {stroke-dashoffset: 0;}}
@media (prefers-reduced-motion: reduce) {.ecg {animation: none; stroke-dashoffset: 0;}}

/* ── Result card ── */
.stApp .result {
    background: #FFFFFF !important; border: 1px solid #DCE4EA; border-left: 8px solid var(--tone);
    border-radius: 12px; padding: 22px 24px 20px 24px;
}
.stApp .result .pct {font-size: 3.4rem; font-weight: 700; line-height: 1; color: var(--tone) !important; letter-spacing: -0.02em;}
.stApp .result .pct small {font-size: 1.2rem; font-weight: 500; color: #4A5B69 !important; margin-left: 6px; letter-spacing: 0;}
.stApp .result .head {font-size: 1.2rem; font-weight: 600; margin: 10px 0 4px 0; color: #16222E !important;}
.stApp .result .sub {font-size: 0.9rem; color: #4A5B69 !important; line-height: 1.5; margin: 0 0 18px 0;}
.scale {position: relative; display: flex; height: 12px; border-radius: 6px;}
.scale div {height: 100%;}
.scale div:first-child {border-radius: 6px 0 0 6px;}
.scale div:nth-child(3) {border-radius: 0 6px 6px 0;}
.marker {
    position: absolute; top: -5px; width: 4px; height: 22px; background: #16222E;
    border-radius: 2px; transform: translateX(-2px); box-shadow: 0 0 0 2px #FFFFFF;
}
.stApp .ticks {position: relative; height: 18px; margin-top: 10px; font-size: 0.78rem;}
.ticks span {position: absolute; transform: translateX(-50%); color: #4A5B69 !important;}
.ticks span:first-child {transform: none;}
.ticks span:last-child {transform: translateX(-100%);}

/* ── Advice cards ── */
.stApp .advice {
    background: #FFFFFF !important; border: 1px solid #DCE4EA; border-radius: 12px;
    padding: 20px 26px 18px 26px; margin-top: 18px;
}
.stApp .advice h3 {font-size: 1.2rem; font-weight: 600; margin: 0 0 8px 0; padding: 0; color: #16222E !important;}
.stApp .advice h4 {font-size: 1rem; font-weight: 600; margin: 16px 0 4px 0; padding: 0; color: #16222E !important;}
.stApp .advice p, .stApp .advice li {font-size: 1rem; line-height: 1.65; color: #16222E !important;}
.stApp .advice p {margin: 0 0 6px 0;}
.stApp .advice ul {margin: 4px 0 0 0; padding-left: 22px;}
.stApp .advice li {margin-bottom: 6px;}
.stApp .advice li b {font-weight: 600; color: #16222E !important;}
.stApp .advice.alert {background: #FDF1F0 !important; border-color: #EBC3BF; border-left: 8px solid #C8433B;}

.stApp .disclaimer {
    font-size: 0.84rem; line-height: 1.5; background: #F4F7F9 !important;
    border: 1px solid #DCE4EA; border-radius: 10px; padding: 12px 14px; color: #16222E !important;
}
.stApp .disclaimer b {color: #16222E !important;}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# Load files (works with either file name)
# ─────────────────────────────────────────────────────────────
BASE = Path(__file__).parent


def _find(*names):
    for n in names:
        p = BASE / n
        if p.exists():
            return p
    raise FileNotFoundError(f"None of these files were found next to app.py: {', '.join(names)}")


@st.cache_resource(show_spinner=False)
def load_artifacts():
    model = joblib.load(_find("Logistic_Regression_heart.pkl", "Logistic Regression_heart.pkl"))
    scaler = joblib.load(_find("scaler.pkl"))
    columns = joblib.load(_find("columns.pkl"))
    return model, scaler, list(columns)


try:
    model, scaler, expected_columns = load_artifacts()
except FileNotFoundError as e:
    st.error(f"Model files missing. {e}")
    st.stop()

# ─────────────────────────────────────────────────────────────
# Fields
# ─────────────────────────────────────────────────────────────
SEX = {"M": "Male", "F": "Female"}
CHEST = {"ATA": "Atypical angina", "NAP": "Non-anginal pain", "TA": "Typical angina",
         "ASY": "No chest pain symptoms"}
ECG = {"Normal": "Normal", "ST": "ST-T wave abnormality", "LVH": "Left ventricular hypertrophy"}
ANGINA = {"N": "No", "Y": "Yes"}
SLOPE = {"Up": "Upsloping", "Flat": "Flat", "Down": "Downsloping"}
FBS = {0: "No (120 mg/dL or below)", 1: "Yes (above 120 mg/dL)"}

DEFAULTS = dict(age=40, sex="M", cp="ATA", bp=120, chol=200, fbs=0,
                ecg="Normal", hr=150, ang="N", old=1.0, slope="Up")
EXAMPLES = {
    "Lower-risk example": dict(age=34, sex="F", cp="ATA", bp=115, chol=190, fbs=0,
                               ecg="Normal", hr=172, ang="N", old=0.0, slope="Up"),
    "Higher-risk example": dict(age=62, sex="M", cp="ASY", bp=145, chol=260, fbs=1,
                                ecg="ST", hr=108, ang="Y", old=2.8, slope="Flat"),
}
for k, v in DEFAULTS.items():
    st.session_state.setdefault(k, v)
st.session_state.setdefault("result", None)


def apply_values(values):
    """Load example / reset: change the fields and clear any previous result."""
    for k, v in values.items():
        st.session_state[k] = v
    st.session_state["result"] = None


# ─────────────────────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Heart risk check")
    st.markdown("**Try an example**")
    for label, vals in EXAMPLES.items():
        st.button(label, on_click=apply_values, args=(vals,), width="stretch")
    st.button("Reset all fields", on_click=apply_values, args=(DEFAULTS,), width="stretch")
    st.markdown("&nbsp;", unsafe_allow_html=True)
    st.markdown(
        '<div class="disclaimer"><b>This is not a diagnosis.</b> It gives an estimate from the values '
        "you enter and cannot replace a doctor's examination and tests. If you feel unwell, "
        "please get medical care.</div>",
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────────────────────
ECG_PATH = (
    "M0 40 L120 40 L150 40 L165 38 L180 40 L260 40 L285 40 L295 12 L308 58 L322 40 L345 40 "
    "L370 34 L395 40 L520 40 L545 40 L555 10 L568 60 L582 40 L605 40 L630 33 L655 40 "
    "L780 40 L805 40 L815 14 L828 58 L842 40 L865 40 L890 35 L915 40 L1040 40 "
    "L1065 40 L1075 12 L1088 58 L1102 40 L1125 40 L1150 34 L1175 40 L1400 40"
)
st.markdown(
    '<div class="hero"><h1>Heart disease risk check</h1>'
    "<p>Fill in the details below to see your estimated risk and simple steps you can take.</p>"
    f'<svg viewBox="0 0 1400 64" preserveAspectRatio="none" aria-hidden="true">'
    f'<path class="ecg" d="{ECG_PATH}"/></svg></div>',
    unsafe_allow_html=True,
)


# ─────────────────────────────────────────────────────────────
# Prediction
# ─────────────────────────────────────────────────────────────
def build_row(s):
    row = pd.DataFrame(0.0, index=[0], columns=expected_columns)
    row.loc[0, "Age"] = s["age"]
    row.loc[0, "RestingBP"] = s["bp"]
    row.loc[0, "Cholesterol"] = s["chol"]
    row.loc[0, "FastingBS"] = s["fbs"]
    row.loc[0, "MaxHR"] = s["hr"]
    row.loc[0, "Oldpeak"] = s["old"]
    for col in (f"Sex_{s['sex']}", f"ChestPainType_{s['cp']}", f"RestingECG_{s['ecg']}",
                f"ExerciseAngina_{s['ang']}", f"ST_Slope_{s['slope']}"):
        if col in row.columns:
            row.loc[0, col] = 1.0
    return row


def predict(s):
    scaled = scaler.transform(build_row(s))
    return float(model.predict_proba(scaled)[0, 1]), int(model.predict(scaled)[0])


def run_prediction():
    """Runs only when the Predict button is pressed; keeps a snapshot of the inputs used."""
    s = {k: st.session_state[k] for k in DEFAULTS}
    prob, label = predict(s)
    st.session_state["result"] = dict(state=s, prob=prob, label=label)


def risk_tier(p):
    if p >= 0.5:
        return "high", CORAL, "High risk of heart disease"
    if p >= 0.3:
        return "moderate", AMBER, "Moderate risk"
    return "low", GREEN, "Low risk of heart disease"


# ─────────────────────────────────────────────────────────────
# Plain-language advice
# ─────────────────────────────────────────────────────────────
ADVICE = {
    "high": dict(
        title="Please see a doctor soon",
        intro=("Your answers show several signs that are often linked with heart disease. This is not a "
               "diagnosis, and many people with a result like this are fine after a check-up. But it is "
               "better to get checked than to wait."),
        steps=[
            "Book a visit with a doctor within the next few days. A heart specialist (cardiologist) is best, "
            "but a general doctor can start.",
            "Take these results with you and ask about an ECG, blood tests for cholesterol and sugar, and a "
            "treadmill (exercise) test.",
            "Avoid very hard exercise and heavy lifting until you have been checked. Gentle walking is usually fine.",
            "If you smoke, stopping is the best single thing you can do for your heart.",
            "Eat less salt, fried food and sweets. Eat more vegetables, fruit, beans, whole grains and fish.",
            "If a doctor has already given you medicines, take them every day. Do not stop them on your own.",
        ],
    ),
    "moderate": dict(
        title="Your risk is in the middle. Now is a good time to act",
        intro=("Some of your answers raise your risk a little. You are below the point where this tool "
               "calls the risk high, and small changes now can help keep it that way."),
        steps=[
            "Book a routine heart check-up in the next month or two and share these results with the doctor.",
            "Walk briskly for about 30 minutes on most days of the week.",
            "Cut down on salt, fried food and sugary drinks. Eat more vegetables, fruit and whole grains.",
            "Keep a healthy weight, sleep 7 to 8 hours and make time to relax.",
            "Do not smoke, and stay away from other people's smoke.",
        ],
    ),
    "low": dict(
        title="Your risk looks low. Keep it that way",
        intro=("Your answers do not show many warning signs. A low result is reassuring, but it cannot rule out "
               "heart disease, so keep up healthy habits and regular check-ups."),
        steps=[
            "Check your blood pressure, cholesterol and blood sugar about once a year.",
            "Stay active: around 30 minutes of walking or similar activity on most days.",
            "Eat plenty of vegetables, fruit and whole grains, and go easy on salt, fried food and sweets.",
            "Avoid tobacco and keep a healthy weight.",
        ],
    ),
}


def personal_points(s):
    pts = []
    if s["bp"] >= 140:
        pts.append(("Blood pressure is high.",
                    f"Your resting blood pressure is {s['bp']} mm Hg (the top number). Under 120 is ideal. "
                    "Less salt, daily walking and a healthy weight help, and a doctor can tell you if you "
                    "need medicine."))
    elif s["bp"] >= 130:
        pts.append(("Blood pressure is a little high.",
                    f"Your resting blood pressure is {s['bp']} mm Hg. Under 120 is ideal. Cutting back on "
                    "salt and walking daily can bring it down."))
    if s["chol"] >= 240:
        pts.append(("Cholesterol is high.",
                    f"Your cholesterol is {s['chol']} mg/dL (under 200 is desirable). Eat less fried and fatty "
                    "food, and more vegetables, oats, beans and fruit. Ask a doctor whether you need treatment."))
    elif s["chol"] >= 200:
        pts.append(("Cholesterol is slightly high.",
                    f"Your cholesterol is {s['chol']} mg/dL (under 200 is desirable). Less fried food and more "
                    "fibre can help."))
    if s["fbs"] == 1:
        pts.append(("Fasting blood sugar is above normal.",
                    "This can be an early sign of diabetes, which strains the heart. Ask for a blood sugar "
                    "test (such as HbA1c)."))
    if s["ang"] == "Y":
        pts.append(("You get chest pain when you exert yourself.",
                    "Do not push through it. Stop and rest when it happens, and tell a doctor soon."))
    heart_tests = []
    if s["ecg"] != "Normal":
        heart_tests.append("an abnormal resting ECG")
    if s["slope"] in ("Flat", "Down"):
        heart_tests.append("a flat or downward ST slope")
    if s["old"] >= 2:
        heart_tests.append("ST depression of 2 or more")
    if heart_tests:
        pts.append(("Your heart tests show some changes.",
                    "You entered " + ", ".join(heart_tests) + ". These can be signs the heart is under strain, "
                    "so a doctor should look at the actual ECG."))
    if s["cp"] == "ASY":
        pts.append(("No chest pain does not mean a healthy heart.",
                    "Heart disease can be silent, so do not rely on symptoms alone."))
    if s["age"] >= 55:
        pts.append(("Age matters.",
                    "Heart risk rises with age, so regular check-ups become more important."))
    return pts


def advice_html(tier, s):
    a = ADVICE[tier]
    steps = "".join(f"<li>{t}</li>" for t in a["steps"])
    html = (f'<div class="advice"><h3>{a["title"]}</h3><p>{a["intro"]}</p>'
            f'<h4>What you can do</h4><ul>{steps}</ul>')
    pts = personal_points(s)
    html += "<h4>From the numbers you entered</h4>"
    if pts:
        html += "<ul>" + "".join(f"<li><b>{t}</b> {d}</li>" for t, d in pts) + "</ul>"
    else:
        html += "<p>None of your entered values stood out as a concern.</p>"
    html += "</div>"
    return html


EMERGENCY_HTML = (
    '<div class="advice alert"><h3>Get emergency help straight away if you have</h3>'
    "<ul>"
    "<li>Chest pain, pressure or tightness that lasts more than a few minutes</li>"
    "<li>Pain spreading to the arm, shoulder, neck, jaw or back</li>"
    "<li>Sudden shortness of breath, cold sweat, nausea or dizziness</li>"
    "<li>Fainting or feeling like you may faint</li>"
    "</ul>"
    "<p style='margin-top:10px'>Call your local emergency number or go to the nearest hospital. "
    "Do not drive yourself.</p></div>"
)

# ─────────────────────────────────────────────────────────────
# Inputs + result
# ─────────────────────────────────────────────────────────────
left, right = st.columns([1.15, 1], gap="large")

with left:
    with st.container(border=True):
        st.markdown('<p class="group-title">About you</p>'
                    '<p class="group-note">Basic details</p>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.slider("Age (years)", 18, 100, key="age")
        with c2:
            st.radio("Sex", list(SEX), format_func=SEX.get, horizontal=True, key="sex")

    with st.container(border=True):
        st.markdown('<p class="group-title">Blood pressure and blood tests</p>'
                    '<p class="group-note">Values while at rest</p>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.number_input("Resting blood pressure (mm Hg)", 80, 200, key="bp")
        with c2:
            st.number_input("Cholesterol (mg/dL)", 100, 600, key="chol")
        st.radio("Fasting blood sugar above 120 mg/dL", list(FBS), format_func=FBS.get,
                 horizontal=True, key="fbs")

    with st.container(border=True):
        st.markdown('<p class="group-title">Heart tests and symptoms</p>'
                    '<p class="group-note">From ECG and exercise testing</p>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.selectbox("Chest pain type", list(CHEST), format_func=CHEST.get, key="cp")
            st.selectbox("Resting ECG", list(ECG), format_func=ECG.get, key="ecg")
            st.radio("Chest pain during exercise", list(ANGINA), format_func=ANGINA.get,
                     horizontal=True, key="ang")
        with c2:
            st.selectbox("ST slope", list(SLOPE), format_func=SLOPE.get, key="slope")
            st.slider("Max heart rate (bpm)", 60, 220, key="hr")
            st.slider("ST depression (oldpeak)", 0.0, 6.0, step=0.1, key="old")

with left:
    st.button("Predict", type="primary", on_click=run_prediction, width="stretch")

result = st.session_state["result"]

with right:
    if result is None:
        st.markdown(
            '<div class="placeholder"><p class="t">Your result will appear here</p>'
            '<p class="d">Fill in the details on the left, then press Predict.</p></div>',
            unsafe_allow_html=True,
        )
    else:
        state, prob, label = result["state"], result["prob"], result["label"]
        tier, tone, headline = risk_tier(prob)
        pct = round(prob * 100, 1)
        marker = min(max(pct, 0.5), 99.5)

        st.markdown(
            f'<div class="result" style="--tone:{tone}">'
            f'<div class="pct">{pct:.0f}<small>% estimated risk</small></div>'
            f'<div class="head">{headline}</div>'
            f'<div class="sub">A result of 50% or higher is treated as high risk.</div>'
            f'<div class="scale">'
            f'<div style="width:30%;background:{GREEN}"></div>'
            f'<div style="width:20%;background:{AMBER}"></div>'
            f'<div style="width:50%;background:{CORAL}"></div>'
            f'<span class="marker" style="left:{marker}%"></span></div>'
            f'<div class="ticks"><span style="left:0%">0%</span><span style="left:30%">30%</span>'
            f'<span style="left:50%">50%</span><span style="left:100%">100%</span></div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        current = {k: st.session_state[k] for k in DEFAULTS}
        if current != state:
            st.caption("You changed some values after predicting. Press Predict again to update the result.")

        report = pd.DataFrame({
            "Field": ["Age", "Sex", "Chest pain type", "Resting BP (mm Hg)", "Cholesterol (mg/dL)",
                      "Fasting blood sugar > 120", "Resting ECG", "Max heart rate", "Chest pain during exercise",
                      "Oldpeak", "ST slope", "Estimated risk (%)", "Result"],
            "Value": [state["age"], SEX[state["sex"]], CHEST[state["cp"]], state["bp"], state["chol"],
                      FBS[state["fbs"]], ECG[state["ecg"]], state["hr"], ANGINA[state["ang"]],
                      state["old"], SLOPE[state["slope"]], f"{pct:.1f}",
                      "High risk" if label == 1 else "Not high risk"],
        })
        st.markdown("&nbsp;", unsafe_allow_html=True)
        st.download_button("Download summary to show your doctor", report.to_csv(index=False).encode(),
                           file_name="heart_risk_summary.csv", mime="text/csv", width="stretch")

# Advice appears only after Predict has been pressed
if result is not None:
    st.markdown(advice_html(tier, state), unsafe_allow_html=True)
    st.markdown(EMERGENCY_HTML, unsafe_allow_html=True)