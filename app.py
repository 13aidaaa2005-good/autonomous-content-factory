import streamlit as st
from agents.research_agent import run_research_agent
from agents.copywriter_agent import run_content_agent
from agents.validator import validate_fact_sheet
import time

st.set_page_config(page_title="Autonomous Content Factory", page_icon="🤖")

# ---------- CSS ----------
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(to right, #e8f5e9, #f1f8f6);
}

/* Title */
.main-title {
    color: #1b5e20;
    text-align: center;
    font-size: 3rem;
    font-weight: 700;
    margin-top: 60px;
}

/* Subtitle */
.sub-title {
    color: #43a047;
    text-align: center;
    font-size: 1.2rem;
    margin-bottom: 40px;
}

/* Button */
div[data-testid="stButton"] > button {
    background-color: #2e7d32;
    color: white;
    border-radius: 25px;
    padding: 12px 30px;
    font-weight: 600;
}

/* Text Area */
.stTextArea textarea {
    border-radius: 10px !important;
    padding: 12px !important;
}

/* Cards */
.card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    margin-top: 15px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}

/* Section Title */
.section-title {
    font-size: 20px;
    margin-top: 20px;
    font-weight: 600;
    color: #1b5e20;
}

</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("<h1 class='main-title'>🤖 Autonomous Content Factory</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Research → Validate → Generate AI Content</p>", unsafe_allow_html=True)

# ---------- SESSION ----------
if "show_input" not in st.session_state:
    st.session_state.show_input = False

def show_input():
    st.session_state.show_input = True

# ---------- START BUTTON ----------
col1, col2, col3 = st.columns([1,1,1])
with col2:
    if not st.session_state.show_input:
        st.button("Start Creating ✨", on_click=show_input)

# ---------- MAIN SECTION ----------
if st.session_state.show_input:

    col1, col2 = st.columns([1.2, 1])

    # -------- LEFT (INPUT) -------- #
    with col1:
        st.subheader("📥 Enter Content")

        user_input = st.text_area(
            "",
            height=250,
            placeholder="Paste your product/article content here..."
        )

        st.write("")
        generate = st.button("⚡ Generate")


    # ---------- GENERATION ----------
    if generate:

        if not user_input.strip():
            st.error("Please enter content first.")

        else:
            progress = st.progress(0)

            # -------- RESEARCH -------- #
            for i in range(30):
                time.sleep(0.01)
                progress.progress(i + 1)

            fact_data = run_research_agent(user_input)

            if "error" in fact_data:
                st.error(fact_data["error"])
                st.write(fact_data.get("details"))

            else:
                st.success("Fact Sheet Ready ✅")

                with st.expander("📊 View Fact Sheet"):
                    st.json(fact_data)

                # -------- VALIDATION -------- #
                safe_data = validate_fact_sheet(fact_data)

                progress.progress(70)
                st.success("Data Validated 🛡️")

                with st.expander("🧾 Verified Data"):
                    st.json(safe_data)

                # -------- CONTENT -------- #
                content = run_content_agent(safe_data)

                progress.progress(100)
                st.success("Content Generated 🚀")

                st.markdown("---")

                tab1, tab2, tab3 = st.tabs(["Blog", "Thread", "Email"])

                # -------- BLOG -------- #
                with tab1:
                    st.markdown("<div class='section-title'>📝 Blog</div>", unsafe_allow_html=True)
                    blog = content.get("blog", "")

                    st.markdown(f"<div class='card'>{blog}</div>", unsafe_allow_html=True)
                    st.download_button("📋 Copy Blog", blog, file_name="blog.txt")

                # -------- THREAD -------- #
                with tab2:
                    st.markdown("<div class='section-title'>🧵 Thread</div>", unsafe_allow_html=True)
                    thread_list = content.get("thread", [])
                    thread_text = "\n\n".join(thread_list)

                    for post in thread_list:
                        st.markdown(f"<div class='card'>{post}</div>", unsafe_allow_html=True)

                    st.download_button("📋 Copy Thread", thread_text, file_name="thread.txt")

                # -------- EMAIL -------- #
                with tab3:
                    st.markdown("<div class='section-title'>📧 Email</div>", unsafe_allow_html=True)
                    email = content.get("email", "")

                    st.markdown(f"<div class='card'>{email}</div>", unsafe_allow_html=True)
                    st.download_button("📋 Copy Email", email, file_name="email.txt")

                # -------- FILTERED -------- #
                if safe_data.get("filtered_out_claims"):
                    st.warning("⚠️ Filtered Claims Removed")
                    for c in safe_data["filtered_out_claims"]:
                        st.write("•", c)