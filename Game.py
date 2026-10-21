import streamlit as st
import time

# إعدادات صفحة اللعبة
st.set_page_config(
    page_title="Shinra Adventures",
    page_icon="⚔️",
    layout="wide"
)

# تهيئة حالة اللعبة (Game State)
if "scene" not in st.session_state:
    st.session_state.scene = 1  # نبدأ بالمشهد الأول
if "gold" not in st.session_state:
    st.session_state.gold = 5000
if "distance_to_village" not in st.session_state:
    st.session_state.distance_to_village = 1200
if "player_hp" not in st.session_state:
    st.session_state.player_hp = 1500
if "bear_hp" not in st.session_state:
    st.session_state.bear_hp = 500
if "quest_status" not in st.session_state:
    st.session_state.quest_status = "Deliver goods to the village"
if "inventory" not in st.session_state:
    st.session_state.inventory = {"Cloth": 0, "Potatoes": 10, "Coal": 5, "Lotus Flowers": 5}
if "carried_family" not in st.session_state:
    st.session_state.carried_family = False

# تصميم واجهة اللعبة الجذابة (CSS)
st.markdown("""
<style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button {
        width: 100%;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px;
    }
    .stButton>button:hover { background-color: #ff2222; }
    .game-box {
        background-color: #1e2530;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #3a4454;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# العنوان الرئيسي والشريط الجانبي (HUD)
st.title("⚔️ Shinra Adventures (3D World Simulation)")
st.sidebar.title("📊 Game Status (HUD)")
st.sidebar.write(f"💰 Gold: **{st.session_state.gold}**")
st.sidebar.write(f"❤️ Shinra HP: **{st.session_state.player_hp} / 1500**")
st.sidebar.write(f"🎯 Current Quest: **{st.session_state.quest_status}**")

# ==================== المشهد الأول: السينمائي (الكريستالة) ====================
if st.session_state.scene == 1:
    st.markdown('<div class="game-box">', unsafe_allow_html=True)
    st.subheader("Cinematic Scene 1: The Balance Crystal")
    st.write("""
    In a heavily isolated place within a series of towering mountains, stands the colossal Balance Crystal—white on the right side and black on the left.
    200 years ago, the crystal exploded without warning. Two figures emerged: **Hikari** (white hair, white armor, representing Light) and **Yami** (black hair, black armor, representing Darkness). Both stand at 195 cm tall. 
    Rule: Yami tries to destroy the world's balance, while Hikari tries to restore it indirectly without direct interference.
    """)
    if st.button("Next: 200 Years Later ⏩"):
        st.session_state.scene = 2
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== المشهد الثاني والثالث والرابع: البداية والتجارة ====================
elif st.session_state.scene == 2:
    st.markdown('<div class="game-box">', unsafe_allow_html=True)
    st.subheader("Chapter 1: The Journey Begins")
    st.write("""
    **200 Years Later...**
    A small rustic house in the mountains. Shinra lives with his sick father Yura, brother Soho, sister Maki, and the grave of his mother Korn.
    Maki cares for Yura who fell ill. Soho and Shinra return from trading lotus flowers. Shinra manages to sell goods and learns business.
    A week later, Soho is exhausted. Shinra takes the cart and the axe to go sell goods at the village.
    """)
    
    st.markdown("---")
    st.info("🎮 **Active Gameplay: Deliver Goods to the Village**")
    st.write(f"Distance to Village: **{st.session_state.distance_to_village} meters**")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚶‍♂️ Move Forward (Walk 400m)"):
            if st.session_state.distance_to_village > 0:
                st.session_state.distance_to_village -= 400
                st.rerun()
    with col2:
        if st.button("🏃‍♂️ Dash to Village (Fast)"):
            if st.session_state.distance_to_village > 0:
                st.session_state.distance_to_village -= 1200
                st.rerun()
                
    if st.session_state.distance_to_village <= 0:
        st.success("You reached the village! Villagers buy all your goods. You earned 30 + more gold.")
        st.session_state.gold += 200
        st.session_state.quest_status = "Return to Home"
        if st.button("Proceed to Return Journey 🌲"):
            st.session_state.scene = 3
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== المشهد الخامس: مواجهة الدب (القتال) ====================
elif st.session_state.scene == 3:
    st.markdown('<div class="game-box">', unsafe_allow_html=True)
    st.subheader("Chapter 1: Encounter in the Forest - Boss Battle (Bear)")
    st.write("""
    On his way back at night, Shinra encounters a fierce bear roaming the forest near their home!
    * **Shinra HP:** 1500 | **Bear HP:** 500
    * **Shinra Skills:** Normal Attack (25-40 dmg), Dodge, Dash.
    * **Bear Skills:** Normal Attack (30-50 dmg), Fast Attack (50-90 dmg).
    """)
    
    st.metric("🐻 Bear HP", st.session_state.bear_hp)
    st.metric("🧑 Shinra HP", st.session_state.player_hp)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("⚔️ Normal Attack"):
            import random
            s_dmg = random.randint(25, 40)
            b_dmg = random.randint(30, 50)
            st.session_state.bear_hp -= s_dmg
            st.session_state.player_hp -= b_dmg
            st.rerun()
    with col2:
        if st.button("🛡️ Dodge / Dash"):
            import random
            b_dmg = random.randint(10, 20)  # Reduced damage on dodge
            st.session_state.player_hp -= b_dmg
            st.success("Successfully dodged part of the attack!")
            st.rerun()
    with col3:
        if st.button("⚡ Fast Slash"):
            import random
            s_dmg = random.randint(50, 70)
            b_dmg = random.randint(40, 80)
            st.session_state.bear_hp -= s_dmg
            st.session_state.player_hp -= b_dmg
            st.rerun()
            
    if st.session_state.bear_hp <= 0:
        st.success("Shinra defeated the bear with difficulty, cut its head off, roasted the meat, and ate it deliciously! He hurried back home.")
        if st.button("Continue to Home 🏚️"):
            st.session_state.scene = 4
            st.rerun()
    elif st.session_state.player_hp <= 0:
        st.error("You were defeated by the bear! Game Over.")
        if st.button("🔄 Restart Battle"):
            st.session_state.player_hp = 1500
            st.session_state.bear_hp = 500
            st.rerun()
            
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== المشهد السادس: المأساة والعودة للمستشفى ====================
elif st.session_state.scene == 4:
    st.markdown('<div class="game-box">', unsafe_allow_html=True)
    st.subheader("Chapter 1: The Tragedy")
    st.write("""
    **Narrator:** And here the tragedy begins for Shinra...
    He arrives home to find the house destroyed, father Yura unconscious, and Soho and Maki dead.
    Shinra cries in shock: *'Aaah! Soho! Maki! Dad! Anyone alive?! I must take them to the hospital!'*
    """)
    
    if not st.session_state.carried_family:
        if st.button("Press [E] to lift Maki, Soho, and Yura into the cart"):
            st.session_state.carried_family = True
            st.rerun()
    else:
        st.success("Family loaded into the cart! Shinra runs at 40 km/h back to the village hospital.")
        st.write("""
        **At the Hospital:**
        Doctor Yuno: *"I am sorry, young merchant. Your brother and sister are dead, but your old father is alive though in a coma that could last 1 to 3 years."*
        
        Shinra experiences extreme shock, crying and screaming. A powerful, non-destructive black aura surrounds him, terrifying Doctor Yuno!
        """)
        st.markdown("### 🎬 **THE END OF CHAPTER 1**")
        if st.button("🔄 Play Again / Restart Chapter"):
            st.session_state.scene = 1
            st.session_state.player_hp = 1500
            st.session_state.bear_hp = 500
            st.session_state.distance_to_village = 1200
            st.session_state.carried_family = False
            st.rerun()
            
    st.markdown('</div>', unsafe_allow_html=True)
