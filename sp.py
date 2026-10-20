import streamlit as st
from google import genai
import time

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Personal Academic Planner",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Personal Academic Task & Priority Planner")
st.write("Organize your daily study sessions, assignments, and exams using AI.")

# ---------------------------------------------------------
# Sidebar Configuration
# ---------------------------------------------------------
st.sidebar.header("🔑 Settings")
api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")
daily_hours = st.sidebar.number_input("Available Daily Study Hours:", min_value=1, max_value=16, value=4)

# ---------------------------------------------------------
# Main Input Form
# ---------------------------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("📝 Assignments")
    assignments = st.text_area(
        "List your homework/projects & deadlines:",
        placeholder="Example:\n- Python Final Project (Due in 5 days)\n- Math Homework 3 (Due tomorrow)",
        height=180
    )

with col2:
    st.subheader("📚 Exams")
    exams = st.text_area(
        "List upcoming exams & topics:",
        placeholder="Example:\n- Mathematics Ch 1 Exam (This Thursday)\n- Physics Midterm (Next Week)",
        height=180
    )

with col3:
    st.subheader("📖 Daily Lessons")
    lessons = st.text_area(
        "List lessons/topics to review:",
        placeholder="Example:\n- Read Physics Ch 1-3\n- Review Data Structures lecture notes",
        height=180
    )

# ---------------------------------------------------------
# AI Generation Logic with Failover Handling
# ---------------------------------------------------------
if st.button("🚀 Generate My Study Schedule", type="primary", use_container_width=True):
    if not api_key:
        st.error("Please enter your Gemini API Key in the sidebar on the left!")
    elif not (assignments.strip() or exams.strip() or lessons.strip()):
        st.warning("Please fill in at least one section (Assignments, Exams, or Lessons) before generating.")
    else:
        # Construct structured prompt
        prompt = f"""
You are an expert academic planner and study strategist.
Please create an optimized, prioritized study schedule based on the following student workload:

- Available Daily Study Time: {daily_hours} hours/day

- ASSIGNMENTS:
{assignments if assignments.strip() else 'None provided'}

- UPCOMING EXAMS:
{exams if exams.strip() else 'None provided'}

- LESSONS TO REVIEW:
{lessons if lessons.strip() else 'None provided'}

INSTRUCTIONS:
1. Prioritize tasks based on urgency (Exams > Upcoming Assignments > General Review).
2. Allocate daily time slots realistically within the {daily_hours}-hour daily limit.
3. Provide actionable step-by-step breakdown for studying each item.
4. Keep the output clean, structured, and easy to read.
"""
        
        st.info("Connecting to AI Models and organizing your plan...")
        
        models_to_try = ["gemini-3.8-flash", "gemini-2.5-flash", "gemini-1.5-flash"]
        client = genai.Client(api_key=api_key)
        
        success = False
        response_text = ""
        
        with st.spinner("Processing schedule... Please wait..."):
            for model_name in models_to_try:
                for attempt in range(1, 4):
                    try:
                        res = client.models.generate_content(
                            model=model_name,
                            contents=prompt
                        )
                        response_text = res.text
                        success = True
                        break
                    except Exception as e:
                        err_str = str(e)
                        if "503" in err_str or "UNAVAILABLE" in err_str or "404" in err_str:
                            time.sleep(2)
                        else:
                            break
                if success:
                    break
        
        if success:
            st.success("✅ Schedule Generated Successfully!")
            st.markdown("---")
            st.markdown(response_text)
        else:
            st.error("❌ Servers are currently under heavy load (503). Please wait 30 seconds and click the button again.")