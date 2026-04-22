import streamlit as st
import PyPDF2
import plotly.express as px

from ml_utils import calculate_score, missing_skills, recommend_jobs
from gpt_utils import get_feedback
from auth import login_signup, check_login
from report import generate_pdf

st.set_page_config(page_title="AI Career Assistant PRO", layout="wide")

# ---------- LOGIN ----------
login_signup()

if not check_login():
    st.warning("Please login to continue")
    st.stop()

# ---------- UI ----------
st.markdown("""
<style>
.big-title {
    font-size: 40px;
    font-weight: bold;
    color: #00ff88;
}
.card {
    padding: 18px;
    border-radius: 14px;
    background: linear-gradient(145deg, #1e1e2f, #2a2a40);
    box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    transition: 0.3s;
}
.card:hover {
    transform: translateY(-5px);
}
.title {
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-title">🚀 AI Career Assistant PRO</div>', unsafe_allow_html=True)

# ---------- INPUT ----------
col1, col2 = st.columns(2)

with col1:
    file = st.file_uploader("📄 Upload Resume", type=["pdf"])

with col2:
    jd = st.text_area("💼 Job Description")

def extract_text(file):
    pdf = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf.pages:
        text += page.extract_text()
    return text

# ---------- MAIN ----------
if file and jd:
    resume = extract_text(file)

    score = calculate_score(resume, jd)

    # ---------- DASHBOARD ----------
    st.markdown("## 📊 Dashboard")

    c1, c2, c3 = st.columns(3)
    c1.metric("Match", f"{score}%")
    c2.metric("Gap", f"{100-score}%")
    c3.metric("Level", "High" if score > 70 else "Medium")

    st.progress(int(score))

    fig = px.pie(
        names=["Match", "Gap"],
        values=[score, 100-score],
        color_discrete_sequence=["#00ff88", "#ff4b4b"]
    )
    st.plotly_chart(fig, use_container_width=True)

    # ---------- SKILLS ----------
    st.markdown("### 📉 Missing Skills")
    st.write(missing_skills(resume, jd))

    # ---------- ROLES ----------
    st.markdown("### 🎯 Recommended Roles")
    st.write(recommend_jobs(resume))

    # ---------- AI SUGGESTIONS ----------
    st.markdown("## 🤖 AI Career Insights")

    with st.spinner("Generating smart suggestions..."):
        feedback = get_feedback(resume, jd)

    # -------- PARSE --------
    missing, improvements, suggestions = [], [], []
    current = None

    for line in feedback.split("\n"):
        line = line.strip()

        if "Missing Skills" in line:
            current = "missing"
        elif "Improvements" in line:
            current = "improvements"
        elif "Suggestions" in line:
            current = "suggestions"
        elif line.startswith("-"):
            if current == "missing":
                missing.append(line)
            elif current == "improvements":
                improvements.append(line)
            elif current == "suggestions":
                suggestions.append(line)

    # ---------- DISPLAY ----------
    col1, col2, col3 = st.columns(3)

    def render(title, items, color):
        html = "<br>".join(items) if items else "No data"
        return f"""
        <div class="card">
            <div class="title" style="color:{color}">{title}</div>
            {html}
        </div>
        """

    with col1:
        st.markdown(render("🔴 Missing Skills", missing, "#ff4b4b"), unsafe_allow_html=True)

    with col2:
        st.markdown(render("🟡 Improvements", improvements, "#ffc107"), unsafe_allow_html=True)

    with col3:
        st.markdown(render("🟢 Suggestions", suggestions, "#00ff88"), unsafe_allow_html=True)

    st.success("💡 Tip: Add measurable achievements (e.g., improved accuracy by 20%)")

    # ---------- PDF ----------
    if st.button("📄 Download Report"):
        file_path = generate_pdf(
    feedback,
    st.session_state.get("user", "Guest"),
    score
)
        with open(file_path, "rb") as f:
            st.download_button("Download PDF", f, file_name="report.pdf")

else:
    st.info("Upload resume and enter job description")