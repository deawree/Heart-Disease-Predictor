from pathlib import Path

import joblib
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ─────────────────────────────────────────────────────────────
# Page setup
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Heart Risk Screening",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="expanded",
)

INK = "#16222E"
BLUE = "#1B6B93"
CORAL = "#C8433B"
GREEN = "#1F7A5C"
AMBER = "#C98A1B"
MUTED = "#5E6E7C"

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&display=swap');

:root {color-scheme: light only;}

/* ── Force a light surface, whatever the browser or Streamlit theme says ── */
html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: #F4F7F9 !important; color: #16222E !important;
    font-family: 'IBM Plex Sans', system-ui, sans-serif !important;
}
[data-testid="stHeader"] {background: transparent !important;}
#MainMenu, footer {visibility: hidden;}
.block-container {padding-top: 1.6rem; padding-bottom: 3rem; max-width: 1180px;}

/* ── Dark text on every Streamlit element ── */
.stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
.stApp p, .stApp li, .stApp label, .stApp legend,
.stApp [data-testid="stMarkdownContainer"] p,
.stApp [data-testid="stWidgetLabel"], .stApp [data-testid="stWidgetLabel"] p,
.stApp [data-testid="stRadio"] label p,
.stApp [data-testid="stMetricValue"], .stApp [data-testid="stMetricLabel"], 
.stApp [data-testid="stMetricLabel"] p,
.stApp [data-testid="stSliderThumbValue"], .stApp [data-testid="stTickBarMin"],
.stApp [data-testid="stTickBarMax"] {
    color: #16222E !important;
}
.stApp [data-testid="stCaptionContainer"], .stApp [data-testid="stCaptionContainer"] p,
.stApp small {color: #4A5B69 !important;}

/* ── Inputs ── */
.stApp [data-baseweb="input"], .stApp [data-baseweb="base-input"],
.stApp [data-baseweb="select"] > div, .stApp [data-testid="stNumberInput"] > div > div {
    background: #FFFFFF !important; border-color: #B8C5D0 !important;
}
.stApp input, .stApp [data-baseweb="select"] span, .stApp [data-baseweb="select"] div {
    color: #16222E !important; -webkit-text-fill-color: #16222E !important;
}
.stApp [data-testid="stNumberInput"] button {background: #EAF1F5 !important; color: #16222E !important;}
.stApp [data-baseweb="select"] svg, .stApp [data-testid="stNumberInput"] svg {fill: #16222E !important;}

/* Dropdown menus render in a portal outside .stApp */
[data-baseweb="popover"], [data-baseweb="popover"] > div, [data-baseweb="menu"],
ul[role="listbox"] {background: #FFFFFF !important;}
[data-baseweb="popover"] li, [data-baseweb="popover"] li *, ul[role="listbox"] li,
[data-baseweb="menu"] * {color: #16222E !important; background: transparent !important;}
[data-baseweb="popover"] li:hover, ul[role="listbox"] li[aria-selected="true"] {
    background: #EAF1F5 !important;
}

/* ── Tabs ── */
.stApp [data-baseweb="tab"] p {color: #4A5B69 !important; font-weight: 500;}
.stApp [data-baseweb="tab"][aria-selected="true"] p {color: #1B6B93 !important; font-weight: 600;}
.stApp [data-baseweb="tab-border"] {background: #DCE4EA !important;}

/* ── Buttons ── */
.stApp .stButton > button, .stApp .stDownloadButton > button {
    background: #FFFFFF !important; border: 1px solid #B8C5D0 !important;
    border-radius: 8px; font-weight: 500;
}
.stApp .stButton > button p, .stApp .stDownloadButton > button p {color: #16222E !important;}
.stApp .stButton > button:hover, .stApp .stDownloadButton > button:hover {
    border-color: #1B6B93 !important; background: #EAF1F5 !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"], section[data-testid="stSidebar"] > div {
    background: #FFFFFF !important; border-right: 1px solid #DCE4EA;
}

/* ── Bordered containers ── */
.stApp [data-testid="stVerticalBlockBorderWrapper"] {
    background: #FFFFFF !important; border-radius: 12px !important; border-color: #DCE4EA !important;
}
.stApp .group-title {font-weight: 600; font-size: 1.02rem; margin: 0 0 2px 0; color: #16222E !important;}
.stApp .group-note {font-size: 0.86rem; margin: 0 0 10px 0; color: #4A5B69 !important;}

/* ── Header band (stays dark, text stays light) ── */
.stApp .hero {
    background: #16222E !important; border-radius: 14px;
    padding: 28px 32px 0 32px; overflow: hidden; margin-bottom: 22px;
}
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
.stApp .result .pct small {font-size: 1.3rem; font-weight: 500; color: #4A5B69 !important; margin-left: 6px; letter-spacing: 0;}
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
.stApp .ticks {position: relative; height: 18px; margin-top: 10px; font-size: 0.78rem; color: #4A5B69 !important;}
.ticks span {position: absolute; transform: translateX(-50%); color: #4A5B69 !important;}
.ticks span:first-child {transform: none;}
.ticks span:last-child {transform: translateX(-100%);}

/* ── Driver lists ── */
.stApp .driver {display: flex; justify-content: space-between; padding: 7px 0; border-bottom: 1px solid #E3E9ED; font-size: 0.92rem; color: #16222E !important;}
.stApp .driver span {color: #16222E !important;}
.stApp .driver:last-child {border-bottom: none;}
.stApp .driver .v {font-weight: 600;}
.stApp .driver .v.up {color: #B3342C !important;}
.stApp .driver .v.down {color: #17664B !important;}
.stApp .list-title {font-weight: 600; font-size: 0.95rem; margin: 0 0 6px 0; color: #16222E !important;}

/* ── Chips ── */
.chips {display: flex; flex-wrap: wrap; gap: 8px; margin-top: 4px;}
.stApp .chip {background: #E3EEF4; border-radius: 999px; padding: 5px 12px; font-size: 0.84rem; color: #16222E !important;}
.stApp .chip b {font-weight: 600; color: #16222E !important;}

.stApp .disclaimer {
    font-size: 0.84rem; line-height: 1.5; background: #F4F7F9 !important;
    border: 1px solid #DCE4EA; border-radius: 10px; padding: 12px 14px; color: #16222E !important;
}
.stApp .disclaimer b {color: #16222E !important;}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# Load artifacts (works with either file name)
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
# Field definitions
# ─────────────────────────────────────────────────────────────
SEX = {"M": "Male", "F": "Female"}
CHEST = {
    "ATA": "Atypical angina",
    "NAP": "Non-anginal pain",
    "TA": "Typical angina",
    "ASY": "No chest pain symptoms",
}
ECG = {"Normal": "Normal", "ST": "ST-T wave abnormality", "LVH": "Left ventricular hypertrophy"}
ANGINA = {"N": "No", "Y": "Yes"}
SLOPE = {"Up": "Upsloping", "Flat": "Flat", "Down": "Downsloping"}
FBS = {0: "No (120 mg/dL or below)", 1: "Yes (above 120 mg/dL)"}

DEFAULTS = dict(
    age=40, sex="M", cp="ATA", bp=120, chol=200, fbs=0,
    ecg="Normal", hr=150, ang="N", old=1.0, slope="Up",
)
EXAMPLES = {
    "Lower-risk profile": dict(age=34, sex="F", cp="ATA", bp=115, chol=190, fbs=0,
                               ecg="Normal", hr=172, ang="N", old=0.0, slope="Up"),
    "Higher-risk profile": dict(age=62, sex="M", cp="ASY", bp=145, chol=260, fbs=1,
                                ecg="ST", hr=108, ang="Y", old=2.8, slope="Flat"),
}

for k, v in DEFAULTS.items():
    st.session_state.setdefault(k, v)


def apply_values(values):
    for k, v in values.items():
        st.session_state[k] = v


# ─────────────────────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Heart risk screening")
    st.caption("Logistic regression model trained on clinical measurements.")
    st.markdown("**Load an example**")
    for label, vals in EXAMPLES.items():
        st.button(label, on_click=apply_values, args=(vals,), width="stretch")
    st.button("Reset all fields", on_click=apply_values, args=(DEFAULTS,), width="stretch")
    st.markdown("&nbsp;", unsafe_allow_html=True)
    st.markdown(
        '<div class="disclaimer"><b>Not a diagnosis.</b> This tool estimates risk from the values '
        "you enter. It cannot replace an examination or tests by a doctor. If you have chest pain, "
        "shortness of breath, or other worrying symptoms, seek medical care.</div>",
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────────────────────
# Header with ECG trace
# ─────────────────────────────────────────────────────────────
ECG_PATH = (
    "M0 40 L120 40 L150 40 L165 38 L180 40 L260 40 L285 40 L295 12 L308 58 L322 40 L345 40 "
    "L370 34 L395 40 L520 40 L545 40 L555 10 L568 60 L582 40 L605 40 L630 33 L655 40 "
    "L780 40 L805 40 L815 14 L828 58 L842 40 L865 40 L890 35 L915 40 L1040 40 "
    "L1065 40 L1075 12 L1088 58 L1102 40 L1125 40 L1150 34 L1175 40 L1400 40"
)
st.markdown(
    '<div class="hero"><h1>Heart disease risk screening</h1>'
    "<p>Enter a patient's measurements to see the model's estimated risk and which "
    "factors push that estimate up or down.</p>"
    f'<svg viewBox="0 0 1400 64" preserveAspectRatio="none" aria-hidden="true">'
    f'<path class="ecg" d="{ECG_PATH}"/></svg></div>',
    unsafe_allow_html=True,
)

tab_assess, tab_drivers, tab_model = st.tabs(["Assessment", "What drives the result", "About the model"])

# ─────────────────────────────────────────────────────────────
# Prediction helpers
# ─────────────────────────────────────────────────────────────
NUMERIC_LABELS = {
    "Age": "Age", "RestingBP": "Resting blood pressure", "Cholesterol": "Cholesterol",
    "FastingBS": "Fasting blood sugar", "MaxHR": "Max heart rate", "Oldpeak": "ST depression (oldpeak)",
}
PREFIX_LABELS = {
    "Sex_": "Sex", "ChestPainType_": "Chest pain type", "RestingECG_": "Resting ECG",
    "ExerciseAngina_": "Exercise-induced angina", "ST_Slope_": "ST slope",
}


def group_of(col):
    if col in NUMERIC_LABELS:
        return NUMERIC_LABELS[col]
    for p, lbl in PREFIX_LABELS.items():
        if col.startswith(p):
            return lbl
    return col


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


def predict(state):
    row = build_row(state)
    scaled = scaler.transform(row)
    prob = float(model.predict_proba(scaled)[0, 1])
    label = int(model.predict(scaled)[0])
    contrib = pd.Series(scaled[0] * model.coef_[0], index=expected_columns)
    grouped = contrib.groupby(group_of).sum().sort_values()
    return prob, label, grouped


def risk_tier(p):
    if p >= 0.5:
        return "High", CORAL, "High risk of heart disease"
    if p >= 0.3:
        return "Moderate", AMBER, "Moderate risk, below the model's high-risk line"
    return "Low", GREEN, "Low risk of heart disease"


# ─────────────────────────────────────────────────────────────
# TAB 1 — Assessment
# ─────────────────────────────────────────────────────────────
with tab_assess:
    left, right = st.columns([1.15, 1], gap="large")

    with left:
        with st.container(border=True):
            st.markdown('<p class="group-title">Patient</p>'
                        '<p class="group-note">Basic details</p>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                st.slider("Age (years)", 18, 100, key="age")
            with c2:
                st.radio("Sex", list(SEX), format_func=SEX.get, horizontal=True, key="sex")

        with st.container(border=True):
            st.markdown('<p class="group-title">Vitals and blood tests</p>'
                        '<p class="group-note">Values at rest</p>', unsafe_allow_html=True)
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
                st.radio("Exercise-induced angina", list(ANGINA), format_func=ANGINA.get,
                         horizontal=True, key="ang")
            with c2:
                st.selectbox("ST slope", list(SLOPE), format_func=SLOPE.get, key="slope")
                st.slider("Max heart rate (bpm)", 60, 220, key="hr")
                st.slider("ST depression (oldpeak)", 0.0, 6.0, step=0.1, key="old")

    state = {k: st.session_state[k] for k in DEFAULTS}
    prob, label, grouped = predict(state)
    tier, tone, headline = risk_tier(prob)

    with right:
        pct = round(prob * 100, 1)
        marker = min(max(pct, 0.5), 99.5)
        st.markdown(
            f'<div class="result" style="--tone:{tone}">'
            f'<div class="pct">{pct:.0f}<small>% estimated risk</small></div>'
            f'<div class="head">{headline}</div>'
            f'<div class="sub">The model classifies a patient as high risk when this estimate reaches 50%. '
            f'The result updates as you change any field.</div>'
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

        st.markdown("&nbsp;", unsafe_allow_html=True)
        with st.container(border=True):
            ups = grouped[grouped > 0.02].sort_values(ascending=False).head(3)
            downs = grouped[grouped < -0.02].head(3)

            st.markdown('<p class="list-title">Raising the estimate</p>', unsafe_allow_html=True)
            if ups.empty:
                st.caption("No factor is raising the estimate noticeably.")
            for name, v in ups.items():
                st.markdown(f'<div class="driver"><span>{name}</span><span class="v up">+{v:.2f}</span></div>',
                            unsafe_allow_html=True)

            st.markdown('<p class="list-title" style="margin-top:14px">Lowering the estimate</p>',
                        unsafe_allow_html=True)
            if downs.empty:
                st.caption("No factor is lowering the estimate noticeably.")
            for name, v in downs.items():
                st.markdown(f'<div class="driver"><span>{name}</span><span class="v down">{v:.2f}</span></div>',
                            unsafe_allow_html=True)
            st.caption("Numbers are log-odds contributions compared with an average patient in the training data.")

        report = pd.DataFrame({
            "Field": ["Age", "Sex", "Chest pain type", "Resting BP (mm Hg)", "Cholesterol (mg/dL)",
                      "Fasting blood sugar > 120", "Resting ECG", "Max heart rate", "Exercise angina",
                      "Oldpeak", "ST slope", "Estimated risk (%)", "Model classification"],
            "Value": [state["age"], SEX[state["sex"]], CHEST[state["cp"]], state["bp"], state["chol"],
                      FBS[state["fbs"]], ECG[state["ecg"]], state["hr"], ANGINA[state["ang"]],
                      state["old"], SLOPE[state["slope"]], f"{pct:.1f}",
                      "High risk" if label == 1 else "Low risk"],
        })
        st.download_button("Download this assessment (CSV)", report.to_csv(index=False).encode(),
                           file_name="heart_risk_assessment.csv", mime="text/csv",
                           width="stretch")

# ─────────────────────────────────────────────────────────────
# TAB 2 — Drivers
# ─────────────────────────────────────────────────────────────
with tab_drivers:
    st.markdown("#### How each factor moves the estimate")
    st.caption("Bars to the right raise the estimated risk. Bars to the left lower it. "
               "Zero means the factor is no different from an average training patient.")

    g = grouped.sort_values()
    fig = go.Figure(go.Bar(
        x=g.values, y=g.index, orientation="h",
        marker_color=[CORAL if v > 0 else GREEN for v in g.values],
        text=[f"{v:+.2f}" for v in g.values], textposition="outside",
        hovertemplate="%{y}: %{x:+.3f}<extra></extra>",
    ))
    pad = max(0.3, float(g.abs().max()) * 0.25)
    fig.update_layout(
        height=420, margin=dict(l=0, r=20, t=10, b=30),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="IBM Plex Sans", color=INK, size=13),
        xaxis=dict(title="Contribution (log-odds)", zeroline=True, zerolinecolor=INK,
                   gridcolor="#E3E9ED", range=[g.min() - pad, g.max() + pad]),
        yaxis=dict(title=None), showlegend=False,
    )
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

    st.markdown("#### Values entered")
    chips = [
        ("Age", state["age"]), ("Sex", SEX[state["sex"]]), ("Chest pain", CHEST[state["cp"]]),
        ("BP", f"{state['bp']} mm Hg"), ("Cholesterol", f"{state['chol']} mg/dL"),
        ("Fasting sugar", "Above 120" if state["fbs"] else "120 or below"),
        ("ECG", ECG[state["ecg"]]), ("Max HR", f"{state['hr']} bpm"),
        ("Exercise angina", ANGINA[state["ang"]]), ("Oldpeak", state["old"]),
        ("ST slope", SLOPE[state["slope"]]),
    ]
    st.markdown('<div class="chips">' + "".join(f'<span class="chip">{k}: <b>{v}</b></span>' for k, v in chips)
                + "</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# TAB 3 — Model
# ─────────────────────────────────────────────────────────────
with tab_model:
    st.markdown("#### Model summary")
    m1, m2, m3 = st.columns(3)
    m1.metric("Algorithm", "Logistic regression")
    m2.metric("Input features", len(expected_columns))
    m3.metric("High-risk threshold", "50%")

    st.markdown("#### Learned weights")
    st.caption("Each weight shows how strongly a standardized input pushes the prediction toward heart disease (right) "
               "or away from it (left).")
    coefs = pd.Series(model.coef_[0], index=expected_columns).sort_values()
    fig2 = go.Figure(go.Bar(
        x=coefs.values, y=coefs.index, orientation="h",
        marker_color=[CORAL if v > 0 else BLUE for v in coefs.values],
        hovertemplate="%{y}: %{x:+.3f}<extra></extra>",
    ))
    fig2.update_layout(
        height=560, margin=dict(l=0, r=10, t=10, b=30),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="IBM Plex Sans", color=INK, size=12),
        xaxis=dict(title="Weight", zeroline=True, zerolinecolor=INK, gridcolor="#E3E9ED"),
        yaxis=dict(title=None), showlegend=False,
    )
    st.plotly_chart(fig2, width="stretch", config={"displayModeBar": False})
    st.caption("This screening tool supports, and does not replace, clinical judgement.")