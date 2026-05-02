import streamlit as st
from pipeline import run_research_pipeline

# Page config
st.set_page_config(page_title="AI Research Agent", layout="wide")

# ---------- CUSTOM CSS ----------
st.markdown(
    """
<style>
/* Background */
body {
    background: linear-gradient(135deg, #0f172a, #020617);
    color: white;
}

/* Title */
.main-title {
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(90deg, #38bdf8, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
}

/* Card */
.card {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(10px);
    padding: 20px;
    border-radius: 20px;
    margin-bottom: 20px;
    box-shadow: 0 0 20px rgba(0,0,0,0.3);
}

/* Button */
.stButton>button {
    background: linear-gradient(90deg, #6366f1, #a855f7);
    color: white;
    border-radius: 12px;
    height: 50px;
    width: 100%;
    font-size: 18px;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 15px #a855f7;
}

/* Input */
.stTextInput>div>div>input {
    border-radius: 10px;
    padding: 10px;
    background: #020617;
    color: white;
}

/* Section Title */
.section-title {
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 10px;
    color: #38bdf8;
}
</style>
""",
    unsafe_allow_html=True,
)

# ---------- HEADER ----------
st.markdown(
    '<div class="main-title">🚀 AI Multi-Agent Research System</div>',
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align:center;color:gray;'>Search → Scrape → Write → Critique</p>",
    unsafe_allow_html=True,
)

st.write("")

# ---------- INPUT ----------
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    topic = st.text_input(
        "Enter your research topic:", placeholder="e.g. Future of AI in Healthcare"
    )

    run_btn = st.button("⚡ Run Research")

# ---------- RUN ----------
if run_btn:
    if topic.strip() == "":
        st.warning("⚠️ Please enter a topic.")
    else:
        with st.spinner("🤖 Agents are thinking..."):
            result = run_research_pipeline(topic)

        st.success("✅ Research Completed!")

        st.write("")

        # ---------- OUTPUT ----------
        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(
                '<div class="section-title">🔎 Search Results</div>',
                unsafe_allow_html=True,
            )
            st.write(result["search_result"])
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(
                '<div class="section-title">📄 Scraped Content</div>',
                unsafe_allow_html=True,
            )
            st.write(result["scraped_content"])
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(
                '<div class="section-title">� Final Report</div>',
                unsafe_allow_html=True,
            )
            st.write(result["report"])
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(
                '<div class="section-title">🧠 Critic Feedback</div>',
                unsafe_allow_html=True,
            )
            st.write(result["feedback"])
            st.markdown("</div>", unsafe_allow_html=True)
