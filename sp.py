import streamlit as st
from google import genai
import time
import datetime
from hijri_converter import Gregorian

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Personal Academic Planner",
    page_icon="🎓",
    layout="wide"
)

# Initialize Session State for Chat/Schedule History
if "history" not in st.session_state:
    st.session_state.history = []

# ---------------------------------------------------------
# Sidebar Configuration (Settings, Language, Calendar & Date Range)
# ---------------------------------------------------------
st.sidebar.header("⚙️ Settings / الإعدادات")

# Language Selector
language = st.sidebar.radio(
    "Choose Language / اختر اللغة:",
    ("العربية", "English")
)

is_arabic = (language == "العربية")

st.sidebar.markdown("---")

# Calendar Type Selector (الميلادي / الهجري)
if is_arabic:
    calendar_type = st.sidebar.radio(
        "اختر نوع التقويم  :",
        ("ميلادي (Gregorian)", "هجري (Hijri)")
    )
else:
    calendar_type = st.sidebar.radio(
        "Select Calendar Type:",
        ("Gregorian", "Hijri")
    )

is_hijri_selected = "Hijri" in calendar_type or "هجري" in calendar_type

st.sidebar.markdown("---")

# Date Range Pickers for Study Schedule
if is_arabic:
    st.sidebar.subheader("📅 نطاق جدول الدراسة")
    start_date = st.sidebar.date_input("تاريخ البداية:", datetime.date.today())
    end_date = st.sidebar.date_input("تاريخ النهاية:", datetime.date.today() + datetime.timedelta(days=5))
else:
    st.sidebar.subheader("📅 Study Date Range")
    start_date = st.sidebar.date_input("Start Date:", datetime.date.today())
    end_date = st.sidebar.date_input("End Date:", datetime.date.today() + datetime.timedelta(days=5))

# Convert to Hijri if Hijri Calendar is selected
start_hijri_obj = Gregorian(start_date.year, start_date.month, start_date.day).to_hijri()
end_hijri_obj = Gregorian(end_date.year, end_date.month, end_date.day).to_hijri()

start_date_str = f"{start_hijri_obj.year}/{start_hijri_obj.month}/{start_hijri_obj.day} هـ" if is_hijri_selected else str(start_date)
end_date_str = f"{end_hijri_obj.year}/{end_hijri_obj.month}/{end_hijri_obj.day} هـ" if is_hijri_selected else str(end_date)

# Display calculated Hijri dates in sidebar when selected
if is_hijri_selected:
    st.sidebar.info(
        f"🕌 **التاريخ الهجري المحدد:**\n\n"
        f"• **البداية:** {start_date_str}\n\n"
        f"• **النهاية:** {end_date_str}"
        if is_arabic else
        f"🕌 **Selected Hijri Dates:**\n\n"
        f"• **Start:** {start_date_str}\n\n"
        f"• **End:** {end_date_str}"
    )

st.sidebar.markdown("---")

# Time Unit Selector Option
if is_arabic:
    time_mode = st.sidebar.radio(
        "اختر طريقة إدخال وقت الدراسة اليومي:",
        ("بالساعات", "بالدقائق", "ساعات ودقائق معاً")
    )
else:
    time_mode = st.sidebar.radio(
        "Choose daily study time format:",
        ("Hours", "Minutes", "Hours & Minutes")
    )

# Dynamic time inputs based on selected mode
time_description = ""

if time_mode in ("بالساعات", "Hours"):
    h = st.sidebar.number_input(
        "عدد الساعات يومياً:" if is_arabic else "Hours per day:",
        min_value=1, max_value=24, value=4
    )
    time_description = f"{h} ساعات يومياً" if is_arabic else f"{h} hours per day"

elif time_mode in ("بالدقائق", "Minutes"):
    m = st.sidebar.number_input(
        "عدد الدقائق يومياً:" if is_arabic else "Minutes per day:",
        min_value=10, max_value=1440, value=240, step=15
    )
    time_description = f"{m} دقيقة يومياً" if is_arabic else f"{m} minutes per day"

else:
    col_h, col_m = st.sidebar.columns(2)
    with col_h:
        h = st.number_input(
            "الساعات" if is_arabic else "Hours",
            min_value=0, max_value=23, value=3
        )
    with col_m:
        m = st.number_input(
            "الدقائق" if is_arabic else "Minutes",
            min_value=0, max_value=59, value=30, step=5
        )
    if is_arabic:
        time_description = f"{h} ساعات و {m} دقيقة يومياً"
    else:
        time_description = f"{h} hours and {m} minutes per day"

# Clear History Button in Sidebar
st.sidebar.markdown("---")
clear_btn_label = "🗑️ مسح سجل المحادثات" if is_arabic else "🗑️ Clear Chat History"
if st.sidebar.button(clear_btn_label, use_container_width=True):
    st.session_state.history = []
    st.rerun()

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
يرجى إنشاء جدول دراسي زمني مفصل ومحدد بالأولويات بناءً على المعطيات التالية:

- التقويم المستخدم: {calendar_type}
- فترة الدراسة: من تاريخ {start_date_str} إلى تاريخ {end_date_str}
- معدل وقت الدراسة المتاح: {time_description}

- الواجبات والمشاريع:
{assignments if assignments.strip() else 'لا يوجد'}

- الاختبارات القادمة:
{exams if exams.strip() else 'لا يوجد'}

- الدروس والمراجعة:
{lessons if lessons.strip() else 'لا يوجد'}

التعليمات:
1. قم بالرد باللغة العربية بالكامل وبأسلوب مشجع ومنظم.
2. قسّم الجدول يوماً بيوم طوال الفترة المحددة، وعنون الأيام بالتواريخ المحددة ({start_date_str} إلى {end_date_str}).
3. رتب الأولويات حسب الأهمية (الاختبارات > الواجبات القريبة > المراجعة العامة).
4. استخدم نقاطاً واضحة وجداول لكل يوم ليكون الجدول سهل التنفيذ.
"""
        else:
            prompt = f"""
You are an expert academic planner and study strategist.
Please create a detailed, day-by-day optimized study schedule based on the following:

- Calendar Type: {calendar_type}
- Study Period: From {start_date_str} to {end_date_str}
- Available Study Time: {time_description}

- ASSIGNMENTS:
{assignments if assignments.strip() else 'None provided'}

- UPCOMING EXAMS:
{exams if exams.strip() else 'None provided'}

- LESSONS TO REVIEW:
{lessons if lessons.strip() else 'None provided'}

INSTRUCTIONS:
1. Respond fully in English.
2. Provide a structured, day-by-day schedule spanning from {start_date_str} to {end_date_str}.
3. Prioritize tasks based on urgency (Exams > Upcoming Assignments > General Review).
4. Allocate daily time slots realistically within the limit of {time_description}.
5. Use clear headings and tables for each day.
"""

        info_msg = "جاري الاتصال بالذكاء الاصطناعي وبناء خطتك الزمنية..." if is_arabic else "Connecting to AI Models and organizing your plan..."
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
            # Save to Session State History
            st.session_state.history.append({
                "assignments": assignments,
                "exams": exams,
                "lessons": lessons,
                "response": response_text,
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            })
        else:
            fail_msg = "❌ السيرفرات مشغولة حالياً (503). يرجى الانتظار 30 ثانية والمحاولة مرة أخرى." if is_arabic else "❌ Servers are currently under heavy load (503). Please wait 30 seconds and click the button again."
            st.error(fail_msg)

# ---------------------------------------------------------
# Display Chat History / Previous Schedules
# ---------------------------------------------------------
if st.session_state.history:
    st.markdown("---")
    history_title = "📚 سجل الجداول السابقة" if is_arabic else "📚 Schedule History"
    st.subheader(history_title)

    for i, item in enumerate(reversed(st.session_state.history)):
        with st.expander(f"📌 جدول بتاريخ: {item['timestamp']} (إصدار #{len(st.session_state.history) - i})"):
            st.markdown(f"**{ 'المهام المدخلة:' if is_arabic else 'Inputs:' }**")
            if item['assignments']:
                st.write(f"- **{ 'الواجبات:' if is_arabic else 'Assignments:' }** {item['assignments']}")
            if item['exams']:
                st.write(f"- **{ 'الاختبارات:' if is_arabic else 'Exams:' }** {item['exams']}")
            if item['lessons']:
                st.write(f"- **{ 'الدروس:' if is_arabic else 'Lessons:' }** {item['lessons']}")
            
            st.markdown("---")
            st.markdown(item['response'])
