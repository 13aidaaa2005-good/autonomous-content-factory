import streamlit as st
from agents.research_agent import run_research_agent
from agents.copywriter_agent import run_copywriter_agent

st.set_page_config(page_title="Autonomous Content Factory", layout="wide")

st.title("🏭 Autonomous Content Factory")

st.subheader("📥 Input Source Document")

user_input = st.text_area("Paste your content here:", height=300)

if st.button("🚀 Generate Campaign"):
    if user_input.strip() == "":
        st.warning("Please enter some content!")
    else:
        # -------- Research Agent --------
        st.info("🔍 Research Agent is analyzing...")

        fact_sheet = run_research_agent(user_input)

        st.success("✅ Research Completed!")

        st.subheader("📊 Fact Sheet (Source of Truth)")
        st.json(fact_sheet)

        # -------- Copywriter Agent --------
        st.info("✍️ Copywriter Agent is generating content...")

        content = run_copywriter_agent(fact_sheet)

        # DEBUG (keep for now)
        st.write("DEBUG OUTPUT:", content)

        if "error" in content:
            st.error("❌ Failed to generate content")
            st.code(content["raw_output"])
        else:
            st.success("✅ Content Generated!")

            st.subheader("📝 Blog")
            st.write(content["blog"])

            st.subheader("🧵 Social Media Thread")
            for post in content["thread"]:
                st.write(f"- {post}")

            st.subheader("📧 Email Teaser")
            st.write(content["email"])