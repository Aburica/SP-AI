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

# ---------------------------------------------------------
# Sidebar Configuration (Settings & Language Selection)
# ---------------------------------------------------------
st.sidebar.header("⚙️ Settings / الإعدادات")

# Language Selector
language = st.sidebar.radio(
    "Choose Language / اختر اللغة:",
    ("العربية", "English")
)

is_arabic = (language == "العربية")

# Dynamic Sidebar Inputs (API Key input removed from UI)
if is_arabic:
    daily_hours = st.sidebar.number_input("ساعات الدراسة اليومية المتاحة:", min_value=1, max_value=16, value=4)
else:
    daily_hours = st.sidebar.number_input("Available Daily Study Hours:", min_value=1, max_value=16, value=4)

# Retrieve API Key securely from Streamlit Secrets
api_key = st.secrets.get("GEMINI_API_KEY", "")

# ---------------------------------------------------------
# Main Page Titles & Description
# ---------------------------------------------------------
if is_arabic:
    st.title("🎓 مخطط المهام والأولويات الأكاديمية")
    st.write("نظم جدول دراستك اليومي، واجباتك، واختباراتك باستخدام الذكاء الاصطناعي.")
else:
    st.title("🎓 Personal Academic Task & Priority Planner")
    st.write("Organize your daily study sessions, assignments, and exams using AI.")

# ---------------------------------------------------------
# Main Input Form (Dynamic Labels & Placeholders)
# ---------------------------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    if is_arabic:
        st.subheader("📝 الواجبات والمشاريع")
        assignments = st.text_area(
            "اكتب الواجبات والمواعيد النهائية:",
            placeholder="مثال:\n- مشروع بايثون النهائي (تسليم بعد 5 أيام)\n- واجب الرياضيات (تسليم غداً)",
            height=180
        )
    else:
        st.subheader("📝 Assignments")
        assignments = st.text_area(
            "List your homework/projects & deadlines:",
            placeholder="Example:\n- Python Final Project (Due in 5 days)\n- Math Homework 3 (Due tomorrow)",
            height=180
        )

with col2:
    if is_arabic:
        st.subheader("📚 الاختبارات")
        exams = st.text_area(
            "اكتب الاختبارات القادمة والمواضيع المطلوبة:",
            placeholder="مثال:\n- اختبار رياضيات الفصل الأول (هذا الخميس)\n- اختبار منتصف الفصل في الفيزياء (الأسبوع القادم)",
            height=180
        )
    else:
        st.subheader("📚 Exams")
        exams = st.text_area(
            "List upcoming exams & topics:",
            placeholder="Example:\n- Mathematics Ch 1 Exam (This Thursday)\n- Physics Midterm (Next Week)",
            height=180
        )

with col3:
    if is_arabic:
        st.subheader("📖 الدروس والمراجعة")
        lessons = st.text_area(
            "اكتب الدروس المطلوبة للمراجعة اليوم:",
            placeholder="مثال:\n- قراءة فصل الفيزياء 1-3\n- مراجعة ملاحظات محاضرة هياكل البيانات",
            height=180
        )
    else:
        st.subheader("📖 Daily Lessons")
        lessons = st.text_area(
            "List lessons/topics to review:",
            placeholder="Example:\n- Read Physics Ch 1-3\n- Review Data Structures lecture notes",
            height=180
        )

# ---------------------------------------------------------
# Button & Logic
# ---------------------------------------------------------
button_label = "🚀 إنشاء الجدول الدراسي" if is_arabic else "🚀 Generate My Study Schedule"

if st.button(button_label, type="primary", use_container_width=True):
    if not api_key:
        err_msg = "مفتاح API غير متوفر في إعدادات Streamlit Secrets!" if is_arabic else "API Key is missing in Streamlit Secrets!"
        st.error(err_msg)
    elif not (assignments.strip() or exams.strip() or lessons.strip()):
        warn_msg = "يرجى تعبئة قسم واحد على الأقل (الواجبات، الاختبارات، أو الدروس) قبل البدء." if is_arabic else "Please fill in at least one section before generating."
        st.warning(warn_msg)
    else:
        if is_arabic:
            prompt = f"""
أنت مخطط أكاديمي وخبير في تنظيم الوقت والدراسة.
يرجى إنشاء جدول دراسي منظم ومحدد بالأولويات بناءً على المهام التالية:

- ساعات الدراسة المتاحة يومياً: {daily_hours} ساعات

- الواجبات والمشاريع:
{assignments if assignments.strip() else 'لا يوجد'}

- الاختبارات القادمة:
{exams if exams.strip() else 'لا يوجد'}

- الدروس والمراجعة اليومية:
{lessons if lessons.strip() else 'لا يوجد'}

التعليمات:
1. قم بالرد باللغة العربية بالكامل وبأسلوب مشجع ومنظم.
2. رتب الأولويات حسب الأهمية (الاختبارات > الواجبات القريبة > المراجعة العامة).
3. وزّع المهام بمرونة ضمن حدود الـ {daily_hours} ساعات المتاحة.
4. استخدم نقاطاً واضحة وجداول إن أمكن ليكون الجدول سهلاً للقراءة والتنفيذ.
"""
        else:
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
1. Respond fully in English.
2. Prioritize tasks based on urgency (Exams > Upcoming Assignments > General Review).
3. Allocate daily time slots realistically within the {daily_hours}-hour daily limit.
4. Provide actionable step-by-step breakdown using clean formatting.
"""

        info_msg = "جاري الاتصال بالذكاء الاصطناعي وبناء جدولك..." if is_arabic else "Connecting to AI Models and organizing your plan..."
        st.info(info_msg)

        models_to_try = ["gemini-3.8-flash", "gemini-2.5-flash", "gemini-1.5-flash"]
        client = genai.Client(api_key=api_key)

        success = False
        response_text = ""

        spin_msg = "جاري تحضير الجدول... يرجى الانتظار..." if is_arabic else "Processing schedule... Please wait..."
        with st.spinner(spin_msg):
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
            succ_msg = "✅ تم إنشاء الجدول بنجاح!" if is_arabic else "✅ Schedule Generated Successfully!"
            st.success(succ_msg)
            st.markdown("---")
            st.markdown(response_text)
        else:
            fail_msg = "❌ السيرفرات مشغولة حالياً (503). يرجى الانتظار 30 ثانية والمحاولة مرة أخرى." if is_arabic else "❌ Servers are currently under heavy load (503). Please wait 30 seconds and click the button again."
            st.error(fail_msg)
