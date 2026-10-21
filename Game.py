import streamlit as st
import time
import random

# ضبط إعدادات الصفحة
st.set_page_config(page_title="حكاية كريستالة التوازن - الفصل الأول", page_icon="💎", layout="centered")

# CSS لإضفاء مظهر اللعبة المظلم والتفاعلي
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    .scene-box {
        background-color: #1a1c23;
        border: 2px solid #4a4e69;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        font-size: 18px;
        line-height: 1.6;
    }
    .dialogue-box {
        background-color: #2b2d42;
        border-left: 5px solid #8d99ae;
        padding: 15px;
        border-radius: 5px;
        margin-top: 10px;
        font-style: italic;
    }
    .quest-box {
        background-color: #22223b;
        border: 1px solid #c9ada7;
        padding: 10px;
        border-radius: 5px;
        color: #f2e9e4;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# تهيئة حالات اللعبة (Session State)
if 'step' not in st.session_state:
    st.session_state.step = 1  # خطوة القصة الحالية
if 'shinra_pos' not in st.session_state:
    st.session_state.shinra_pos = 0  # المسافة المقطوعة (بالمتر)
if 'gold' not in st.session_state:
    st.session_state.gold = 0
if 'shinra_hp' not in st.session_state:
    st.session_state.shinra_hp = 1500
if 'bear_hp' not in st.session_state:
    st.session_state.bear_hp = 500
if 'combat_log' not in st.session_state:
    st.session_state.combat_log = []
if 'family_loaded' not in st.session_state:
    st.session_state.family_loaded = 0 # عدد الأفراد المحمولين للعربة

# دالة إعادة الضبط للقتال
def reset_combat():
    st.session_state.shinra_hp = 1500
    st.session_state.bear_hp = 500
    st.session_state.combat_log = ["بدأ القتال بين شينرا ودب الغابة المفترس!"]

# ---- الشريط الجانبي (Sidebar) ----
st.sidebar.title("🎮 لوحة التحكم والمهمة")
st.sidebar.write("---")

if st.session_state.step in [5, 7, 9]:
    st.sidebar.markdown(f"💰 **العملات الذهبية:** {st.session_state.gold} قطعة")

# عرض المهمة الحالية في الشريط الجانبي
if st.session_state.step == 5:
    st.sidebar.markdown("🎯 **المهمة الرئيسية:** انزل من الجبل واوصل للقرية لبيع البضائع (المسافة: 1200 متر).")
elif st.session_state.step == 7:
    st.sidebar.markdown("🎯 **المهمة الرئيسية:** عد إلى المنزل في الجبل قبل حلول الظلام.")
elif st.session_state.step == 8:
    st.sidebar.markdown("⚔️ **المهمة الحالية:** اقضِ على الدب المفترس!")
elif st.session_state.step == 9:
    st.sidebar.markdown("🎯 **المهمة الرئيسية:** اركض بسرعة نحو المنزل!")
elif st.session_state.step == 11:
    st.sidebar.markdown("🎯 **المهمة الرئيسية:** احمل عائلتك المصابة ضعهم في العربة لنقلهم للقرية (اضغط E).")

st.sidebar.write("---")
if st.sidebar.button("🔄 إعادة بدء الفصل الأول"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# ==========================================
# المشاهد والقصة واللعب
# ==========================================

st.title("🛡️ أسطورة كريستالة التوازن - الفصل الأول")

# --- المشهد 1: مقدمة الكريستالة ---
if st.session_state.step == 1:
    st.markdown("""
    <div class="scene-box">
    🌌 <b>المشهد السينمائي الأول: أسطورة الكريستالة</b><br><br>
    في مكان شديد العزلة بين سلسلة من الجبال الشاهقة، تعتلي السماء كريستالة عملاقة تُعرف بـ <b>"كريستالة التوازن"</b>. 
    نصفها الأيمن أبيض ناصع ونصفها الأيسر أسود دكن.<br><br>
    قبل 200 عام، انفجرت البلورة فجأة بلا سابق إنذار، وخرج منها كائنان بطول 195 سم وبدروع محارب كاملة:<br>
    ⚪ <b>هيكاري (النور):</b> بشعر أبيض ودرع أبيض، يمثل الجانب الأيمن وسعي الإصلاح.<br>
    ⚫ <b>يامي (الظلام):</b> بشعر أسود ودرع أسود، يمثل الجانب الأيسر وسعي التدمير.<br><br>
    قانون التوازن ينص على أن يامي يسعى لتدمير العالم وهيكاري يسعى لإصلاحه... دون تدخل مباشر منهما!
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("⚪ **Hikari** (النور)")
    with col2:
        st.write("⚫ **Yami** (الظلام)")

    if st.button("التالي ➔"):
        st.session_state.step = 2
        st.rerun()

# --- المشهد 2: بعد 200 سنة والبيت ---
elif st.session_state.step == 2:
    st.markdown("""
    <div class="scene-box">
    <b>[ بعد 200 سنة ]</b><br><br>
    يظهر بيت خشبي صغير على سفح الجبل.<br>
    نرى بطلنا <b>شينرا</b> في منزله مع أبيه المريض <b>يورا</b>، وأخيه <b>سوهو</b>، وأخته <b>ماكي</b>، بجوار قبر أمهم الراحلة <i>كورن</i>.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="dialogue-box">
    👴 <b>يورا:</b> ماكي...<br>
    👧 <b>ماكي:</b> أبي، ماذا حدث؟<br>
    👴 <b>يورا:</b> أحضري لي الدواء حالاً...<br>
    <i>(ظهرت علامات الارتباك على ماكي وتسلمه الدواء)</i><br>
    👧 <b>ماكي:</b> تفضل دواءك يا أبي.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("🛒 *صوت عربة تقترب من المنزل...*")
    
    st.markdown("""
    <div class="dialogue-box">
    👦 <b>سوهو:</b> أهلاً ماكي، أهلاً أبي! ها قد عدت.<br>
    👧 <b>ماكي:</b> أهلاً سوهو... وأين شينرا؟<br>
    🧑 <b>شينرا:</b> أنا هنا!<br>
    <i>(لحظة غضب من ماكي... 👊 **بوكس!**)</i><br>
    🧑 <b>شينرا:</b> لماذا تلكمينني؟!<br>
    👧 <b>ماكي:</b> ظننتك ضائعاً وفي النهاية أنت مع سوهو!
    </div>
    """, unsafe_allow_html=True)

    if st.button("التالي ➔"):
        st.session_state.step = 3
        st.rerun()

# --- المشهد 3: فلاش باك ---
elif st.session_state.step == 3:
    st.markdown("""
    <div class="scene-box">
    💫 <b>[ فلاش باك ]</b><br>
    نعود للماضي لحظة ذهاب سوهو للتجارة...<br>
    👧 <b>ماكي (مرتبكة):</b> شينرا! شينرا أين أنت؟<br><br>
    <i>(سوهو يجر العربة في الطريق...)</i><br>
    🧑 <b>شينرا:</b> أخي دعني أساعدك!<br>
    👦 <b>سوهو:</b> ماذا أيها الاحمق؟ لماذا أنت هنا؟<br>
    🧑 <b>شينرا:</b> كان لدي الفضول لمعرفة ماذا تفعل عند ذهابك.<br>
    👦 <b>سوهو:</b> أذهب للتجارة لبيع البضائع وجني المال من أجل والدك!<br>
    🧑 <b>شينرا:</b> حسناً سأساعدك.<br>
    👦 <b>سوهو (غاضباً):</b> حسناً، لا خيار آخر!
    </div>
    """, unsafe_allow_html=True)

    if st.button("العودة للحاضر ➔"):
        st.session_state.step = 4
        st.rerun()

# --- المشهد 4: الاستعداد للتجارة ---
elif st.session_state.step == 4:
    st.markdown("""
    <div class="dialogue-box">
    🧑 <b>شينرا:</b> حسناً، كان لدي فضول ولقد استطعت بيع زهرات اللوتس!<br>
    👧 <b>ماكي:</b> إذاً كم جنيت من زهرات اللوتس؟<br>
    🧑 <b>شينرا (ببراءة):</b> 30 قطعة ذهبية!<br>
    <i>(يبتسم يورا)</i>
    </div>
    """, unsafe_allow_html=True)

    st.write("---")
    st.markdown("⌛ *مر أسبوع كامل...*")

    st.markdown("""
    <div class="dialogue-box">
    👦 <b>سوهو (مرهق):</b> يكفي... أنا مرهق جداً وأريد راحة.<br>
    👧 <b>ماكي:</b> إذاً يا أحمق، من سيذهب للتجارة؟<br>
    🧑 <b>شينرا:</b> أنا سأذهب! تعلمت الحساب وكيف أقنع الزبائن.<br>
    👧 <b>ماكي:</b> حسناً اذهب، وخذ هذا الفأس معك للحماية.
    </div>
    """, unsafe_allow_html=True)

    if st.button("ابدأ الرحلة للقرية ➔"):
        st.session_state.step = 5
        st.session_state.shinra_pos = 0
        st.rerun()

# --- المشهد 5: تحريك البطل للقرية ---
elif st.session_state.step == 5:
    st.subheader("🏔️ طريق الجبل نحو القرية")
    st.info("الهدف: الوصول للقرية لبيع البضائع (المسافة المطلوبة: 1200 متر).")

    remaining = 1200 - st.session_state.shinra_pos
    st.progress(min(st.session_state.shinra_pos / 1200, 1.0))
    st.write(f"🚶 المسافة المقطوعة: **{st.session_state.shinra_pos}** / 1200 متر (المتبقي: {max(0, remaining)} متر)")

    # الخريطة التفاعلية البسيطة
    grid = ["🏔️"] * 10
    idx = min(int((st.session_state.shinra_pos / 1200) * 9), 9)
    grid[idx] = "🧑🛒"
    grid[-1] = "🏡"
    st.markdown("### الخريطة: " + " ➔ ".join(grid))

    st.write("#### أزرار التحكم بالحركة:")
    col_w, col_s, col_dash = st.columns(3)
    
    with col_w:
        if st.button("⬆️ تقدم (W) [+150م]"):
            st.session_state.shinra_pos += 150
            st.rerun()
    with col_s:
        if st.button("⚡ اندفاع Dash [+300م]"):
            st.session_state.shinra_pos += 300
            st.rerun()

    if st.session_state.shinra_pos >= 1200:
        st.success("🎉 وصلت إلى القرية بنجاح!")
        if st.button("دخول القرية ➔"):
            st.session_state.step = 6
            st.rerun()

# --- المشهد 6: بيع البضائع في القرية ---
elif st.session_state.step == 6:
    st.markdown("""
    <div class="scene-box">
    🏘️ <b>المشهد الخامس: البيع في القرية</b><br><br>
    ينزل شينرا من الجبل ويدخل أزقة القرية المليئة بالأكشاك القروية.<br><br>
    👤 <b>أحد القرويين:</b> انظروا! أتت البضائع! لحظة... هل أنت أخ سوهو؟ أين سوهو؟<br>
    🧑 <b>شينرا:</b> إنه منهك حالياً، لذا سأبيع بدلاً عنه.<br>
    👤 <b>القروي:</b> أرني، كجم من هذا القماش كم قيمته؟<br>
    🧑 <b>شينرا:</b> 15 قطعة ذهبية!<br>
    🤨 <b>رجل متعجرف:</b> هذا غالي جداً!<br>
    🧑 <b>شينرا:</b> أخي يبيع الأرخص بالسوق وسعره الأصلي 20 ذهبية، هل تريد أم أزيد السعر؟ وأيضاً هذا قماش نادِر من جلد الدب!<br>
    🤨 <b>المتعجرف:</b> حسناً سأشتريه! (لم تنطلِ عليه الحيلة ولكن القماش أعجبه).<br><br>
    <i>يتجمهر التجار والقرويون: "أريد بطاطس... أريد فحماً... أريد زهرات اللوتس... أريد خساً!"</i>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="dialogue-box">
    🧑 <b>شينرا:</b> يبدو أنني لن أعود مبكراً اليوم...<br><br>
    <i>(بعد إنهاء كافة البضائع وجني الأرباح)</i><br>
    🧑 <b>شينرا:</b> كان يوماً متعباً جداً... حل الليل بالفعل. جيد أن معي الفأس!
    </div>
    """, unsafe_allow_html=True)

    st.session_state.gold = 5000  # إضافة 5000 عملة ذهبية

    if st.button("بدء رحلة العودة للمنزل ➔"):
        st.session_state.step = 7
        st.session_state.shinra_pos = 1200
        st.rerun()

# --- المشهد 7: العودة ولقاء الدب ---
elif st.session_state.step == 7:
    st.subheader("🌙 طريق العودة عبر الغابة المظلمة")
    st.info("الهدف: العودة للمنزل في أعلى الجبل.")

    st.progress(min(st.session_state.shinra_pos / 1200, 1.0))
    st.write(f"🏠 المسافة المتبقية للمنزل: **{st.session_state.shinra_pos}** متر")

    if st.button("⬅️ صعود الجبل (W/S) [-300م]"):
        st.session_state.shinra_pos -= 300
        st.rerun()

    if st.session_state.shinra_pos <= 600:
        st.warning("⚠️ فجأة! تظهر حركة غريبة بين الأشجار...")
        st.markdown("""
        <div class="scene-box">
        🐻 <b>شينرا:</b> يا إلهي... الدببة تتسكع في غابتنا وقرب منزلنا! لعل ماكي لم تحكم المصيدة... حسناً، سأقاتلك!
        </div>
        """, unsafe_allow_html=True)

        if st.button("⚔️ بد المعركة مع الدب!"):
            st.session_state.step = 8
            reset_combat()
            st.rerun()

# --- المشهد 8: القتال بالدور ضد الدب ---
elif st.session_state.step == 8:
    st.subheader("⚔️ معركة ضد دب الغابة المفترس")

    col_s, col_b = st.columns(2)
    with col_s:
        st.markdown(f"### 🧑 شينرا\n❤️ **HP:** {st.session_state.shinra_hp} / 1500")
    with col_b:
        st.markdown(f"### 🐻 دب الغابة\n❤️ **HP:** {st.session_state.bear_hp} / 500")

    st.write("---")
    st.write("#### اختر حركة شينرا:")

    c1, c2, c3 = st.columns(3)
    
    # هجوم شينرا
    if c1.button("🪓 هجوم بالفأس (25-40)"):
        dmg = random.randint(25, 40)
        st.session_state.bear_hp -= dmg
        st.session_state.combat_log.append(f"🗡️ شينرا هاجم الدب وسبب **{dmg}** ضرر!")
        
        # دور الدب
        if st.session_state.bear_hp > 0:
            attack_type = random.choice(["normal", "fast"])
            if attack_type == "normal":
                b_dmg = random.randint(30, 50)
                st.session_state.shinra_hp -= b_dmg
                st.session_state.combat_log.append(f"🐻 الدب ضرب هجوم عادي وسبب **{b_dmg}** ضرر!")
            else:
                b_dmg = random.randint(50, 90)
                st.session_state.shinra_hp -= b_dmg
                st.session_state.combat_log.append(f"⚡ الدب نفذ **هجمة سريعة** وسبب **{b_dmg}** ضرر!")
        st.rerun()

    # مراغبة Dodge
    if c2.button("💨 تفادي (Dodge)"):
        st.session_state.combat_log.append("💨 شينرا تفادى هجمة الدب ببراعة ولم يصب بأي ضرر!")
        st.rerun()

    # اندفاع Dash
    if c3.button("⚡ اندفاع (Dash)"):
        dmg = random.randint(35, 50)
        st.session_state.bear_hp -= dmg
        st.session_state.combat_log.append(f"⚡ شينرا اندفع بسرعة مباغتة وضرب الدب بـ **{dmg}** ضرر!")
        st.rerun()

    # عرض سجل القتال
    st.write("📜 **سجل المعركة:**")
    for log in reversed(st.session_state.combat_log[-5:]):
        st.write(f"- {log}")

    # تفقد نتيجة القتال
    if st.session_state.bear_hp <= 0:
        st.success("🎉 استطعت هزيمة الدب بصعوبة بسيطة!")
        if st.button("متابعة المشهد ➔"):
            st.session_state.step = 9
            st.rerun()

    elif st.session_state.shinra_hp <= 0:
        st.error("💀 لقد هزمت في المعركة!")
        if st.button("🔄 إعادة القتال"):
            reset_combat()
            st.rerun()

# --- المشهد 9: بعد القتال والشواء ---
elif st.session_state.step == 9:
    st.markdown("""
    <div class="scene-box">
    🩸 <i>القتال كان قوياً وشينرا السريع أصيب بجرح صغير في خده...</i><br><br>
    🧑 <b>شينرا:</b> هذا الدب كان قوياً بالذات... سأقضي عليه وأكل لحمه!<br><br>
    <i>(قطع شينرا رأس الدب بصعوبة بسيطة... ثم أوقد ناراً وسلط الضوء لشواثه)</i><br><br>
    🔥 🧑 <b>شينرا:</b> همممم... لحمه لذيذ جداً! <br>
    صحيح! نسيت، يجب أن أعود للمنزل بأقصى سرعة!
    </div>
    """, unsafe_allow_html=True)

    if st.button("🏃 الاندفاع بأقصى سرعة نحو المنزل ➔"):
        st.session_state.step = 10
        st.rerun()

# --- المشهد 10: المأساة في المنزل ---
elif st.session_state.step == 10:
    st.markdown("""
    <div class="scene-box" style="border-color: #e63946;">
    🎙️ <b>الراوي:</b> وهنا... تبدأ المأساة الحقيقية لشينرا.<br><br>
    💥 المنزل محطم بالكامل...<br>
    👴 والده يورا مغشي عليه على الأرض...<br>
    👦👧 سوهو وماكي طريحان بلا حراك والمكان ملطخ بالدماء...<br><br>
    🧑 <b>شينرا (ببكاء وصدمة صرخية):</b> آااااااااااا! ما هذا؟! سوهو! ماكي! أبي! هل أحدكم حي؟! يجب أن أنقلهم للمستشفى فوراً!
    </div>
    """, unsafe_allow_html=True)

    if st.button("إنقاذ العائلة ➔"):
        st.session_state.step = 11
        st.session_state.family_loaded = 0
        st.rerun()

# --- المشهد 11: تحميل العائلة بالعربة ---
elif st.session_state.step == 11:
    st.subheader("🛒 نقل الجرحى والمصابين إلى العربة")
    st.info("الهدف: حمل أفراد العائلة (يورا، سوهو، ماكي) ووضعهم في العربة لنقلهم للقرية.")

    members = ["👴 الأب يورا", "👦 الأخ سوهو", "👧 الأخت ماكي"]
    
    st.write(f"الأفراد المحمولين في العربة: **{st.session_state.family_loaded} / 3**")

    if st.session_state.family_loaded < 3:
        current_member = members[st.session_state.family_loaded]
        if st.button(f"🖐️ حمل {current_member} ووضعه بالعربة (اضغط E)"):
            st.session_state.family_loaded += 1
            st.rerun()
    else:
        st.success("تم نقل الجميع إلى العربة بنجاح!")
        if st.button("⚡ الانطلاق فوراً بأقصى سرعة إلى القرية ➔"):
            st.session_state.step = 12
            st.rerun()

# --- المشهد 12: الانطلاق والصدمة في المستشفى ---
elif st.session_state.step == 12:
    st.markdown("""
    <div class="scene-box">
    💨 <b>شينرا يجري بأقصى سرعته (40 كم/س) وهو يقود العربة بوجه بارد وعينين دامعتين...</b><br>
    يصل القرية ويصرخ في أزقتها:<br><br>
    🧑 <b>شينرا:</b> أي طبيب هنااااا؟! أخي وأختي وأبي مصابون إصابات خطيرة!!<br><br>
    👨‍⚕️ <b>الطبيب يونو:</b> حسناً! سآخذهم معي للغرفة فوراً!
    </div>
    """, unsafe_allow_html=True)

    st.write("---")
    st.markdown("🏥 **[ داخل المستشفى ]**")

    st.markdown("""
    <div class="dialogue-box">
    👨‍⚕️ <b>الطبيب يونو:</b> أهلاً أيها الفتى التاجر... اسمي يونو. للأسف يأسفني أن أخبرك بأن الفتى طويل القامة (أخوك) وأختك ذات الرقعة... قد ماتا.<br>
    أما الرجل العجوز والدك فهو حي، ولكنه دخل في غيبوبة قد يستفيق منها بعد سنة أو ثلاث...<br><br>
    🧑 <b>شينرا (في صدمة ذهول):</b> ماذا... سوهو وماكي... ماتا؟!<br><br>
    🌌 <b>(صراخ وبكاء شديد... هالة سوداء مرعبة تبدأ بالظهور والتصاعد حول شينرا!)</b><br>
    🧑 <b>شينرا:</b> هـااااااااااااااااااااااااااااااااااااااااااااااااااااا!!<br><br>
    💥 <i>يحدث اهتزاز قوي جداً في المكان دون أن يتدمر المستشفى، هالة مظلمة تصعق الطبيب يونو من الخوف...</i>
    </div>
    """, unsafe_allow_html=True)

    st.error("🔚 **نهاية الفصل الأول**")
    
    st.balloons()
    if st.button("🔄 إعادة لعب الفصل الأول"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
