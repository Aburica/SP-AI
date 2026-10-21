import streamlit as st
import time
import random

# ==========================================
# PAGE CONFIGURATION & CUSTOM CSS (STYLING)
# ==========================================
st.set_page_config(
    page_title="Chronicles of Shinra - Chapter 1",
    page_icon="⚔️",
    layout="centered"
)

# Dark Fantasy Custom Styling with HTML Canvas & Animations
st.markdown("""
<style>
    .stApp {
        background-color: #0d0f12;
        color: #e0e0e0;
        font-family: 'Georgia', serif;
    }
    .story-box {
        background-color: #161a22;
        border: 2px solid #2e3646;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.7);
    }
    .dialogue-speaker {
        color: #e5a93c;
        font-weight: bold;
        font-size: 1.1em;
    }
    .dialogue-text {
        font-style: italic;
        color: #d1d5db;
    }
    .status-bar {
        background-color: #111827;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #374151;
        margin-bottom: 15px;
    }
    .boss-header {
        color: #ef4444;
        text-align: center;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    .combat-log {
        background-color: #050505;
        border: 1px solid #1f2937;
        padding: 10px;
        height: 120px;
        overflow-y: auto;
        font-family: monospace;
        color: #10b981;
        border-radius: 4px;
    }
    div.stButton > button {
        background-color: #1f2937;
        color: #f3f4f6;
        border: 1px solid #4b5563;
        border-radius: 4px;
        padding: 10px 20px;
        transition: all 0.3s ease;
        width: 100%;
    }
    div.stButton > button:hover {
        background-color: #374151;
        border-color: #9ca3af;
        color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# INITIALIZE STATE VARIABLES
# ==========================================
if "stage" not in st.session_state:
    st.session_state.stage = "INTRO_YEAR"

# Movement & Quest Mechanics State
if "pos_mountain" not in st.session_state:
    st.session_state.pos_mountain = 0
if "pos_return" not in st.session_state:
    st.session_state.pos_return = 0
if "carried_bodies" not in st.session_state:
    st.session_state.carried_bodies = []
if "pos_cart" not in st.session_state:
    st.session_state.pos_cart = 0

# Combat State
if "shinra_hp" not in st.session_state:
    st.session_state.shinra_hp = 1500
if "bear_hp" not in st.session_state:
    st.session_state.bear_hp = 500
if "combat_log" not in st.session_state:
    st.session_state.combat_log = []

# Helper Navigation Function
def set_stage(next_stage):
    st.session_state.stage = next_stage
    st.rerun()

# ==========================================
# STAGE 0: INTRO YEAR (792 AD)
# ==========================================
if st.session_state.stage == "INTRO_YEAR":
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #9ca3af; font-size: 80px;'>792 A.D.</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #4b5563;'>The Era of Awakening and Sorrow</p>", unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("Begin Story"):
        set_stage("CUTSCENE_FAMILY")

# ==========================================
# STAGE 1: CUTSCENE - HOME & FAMILY
# ==========================================
elif st.session_state.stage == "CUTSCENE_FAMILY":
    st.title("Chapter 1: The Quiet Before The Storm")
    
    st.markdown("""
    <div class='story-box'>
        <p>High upon the mountain, shrouded in mist, stands a humble house. Near the house lies a solitary grave marked <b>'Koren'</b>—Shinra's late mother.</p>
        <p>Inside, the father <b>Yura (Age 54, 178 cm)</b> lies bedridden, stricken by a sudden severe illness. His eyes are filled with deep sorrow. His daughter <b>Maki (Age 13, 154 cm)</b> tends to him tenderly.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='story-box'>
        <p><span class='dialogue-speaker'>Yura:</span> <span class='dialogue-text'>"Maki..."</span></p>
        <p><span class='dialogue-speaker'>Maki:</span> <span class='dialogue-text'>"Father! What happened? Hold on!"</span></p>
        <p><span class='dialogue-speaker'>Yura:</span> <span class='dialogue-text'>"Bring me my medicine... quickly."</span></p>
        <p><i>[Maki shows a flustered and anxious expression as she hands him the medicine bottle]</i></p>
        <p><span class='dialogue-speaker'>Maki:</span> <span class='dialogue-text'>"Here, Father! Please take it!"</span></p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<i>The sound of wooden wheels echoing from outside... A cart arrives.</i>")
    
    st.markdown("""
    <div class='story-box'>
        <p><span class='dialogue-speaker'>Soho (Age 17, 182 cm):</span> <span class='dialogue-text'>"Hello Maki! Father! I have returned!"</span></p>
        <p><i>[Yura and Maki smile with relief at Soho's return]</i></p>
        <p><span class='dialogue-speaker'>Maki:</span> <span class='dialogue-text'>"Welcome back, Soho! ...Wait, where is Shinra?"</span></p>
        <p><span class='dialogue-speaker'>Shinra (Age 9, 142 cm):</span> <span class='dialogue-text'>"I'm right here!"</span></p>
        <p><i>[A vein pops on Maki's forehead in anger. POW! She punches Shinra on the head!]</i></p>
        <p><span class='dialogue-speaker'>Shinra:</span> <span class='dialogue-text'>"Ouch! Why did you punch me?!"</span></p>
        <p><span class='dialogue-speaker'>Maki:</span> <span class='dialogue-text'>"I thought you were lost! And you were with Soho the whole time?!"</span></p>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("📜 Flashback: How Shinra Sneaked Out"):
        st.markdown("""
        <div class='story-box'>
            <p><span class='dialogue-speaker'>Maki (Panicking):</span> <span class='dialogue-text'>"Shinra! Shinra! Where are you?!"</span></p>
            <p><i>[Meanwhile, down the road, Soho is pulling the merchant cart...]</i></p>
            <p><span class='dialogue-speaker'>Shinra:</span> <span class='dialogue-text'>"Brother! Let me help you!"</span></p>
            <p><span class='dialogue-speaker'>Soho:</span> <span class='dialogue-text'>"What?! You idiot, why are you here?"</span></p>
            <p><span class='dialogue-speaker'>Shinra:</span> <span class='dialogue-text'>"I was curious about what you do when you go trading."</span></p>
            <p><span class='dialogue-speaker'>Soho:</span> <span class='dialogue-text'>"I go to trade, sell goods, and make money for Father's medicine."</span></p>
            <p><span class='dialogue-speaker'>Shinra:</span> <span class='dialogue-text'>"Alright then! I will help you!"</span></p>
            <p><span class='dialogue-speaker'>Soho (Sighs):</span> <span class='dialogue-text'>"Fine... No turning back now."</span></p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class='story-box'>
        <p><span class='dialogue-speaker'>Shinra:</span> <span class='dialogue-text'>"Anyway, I was curious and I even managed to sell the Lotus Flowers!"</span></p>
        <p><span class='dialogue-speaker'>Maki:</span> <span class='dialogue-text'>"Oh? How much did you make from them?"</span></p>
        <p><span class='dialogue-speaker'>Shinra (Innocently):</span> <span class='dialogue-text'>"30 Gold Coins!"</span></p>
        <p><i>[Yura smiles faintly at his young son's achievement.]</i></p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<b>One Week Later...</b>")

    st.markdown("""
    <div class='story-box'>
        <p><span class='dialogue-speaker'>Soho (Exhausted):</span> <span class='dialogue-text'>"Enough... I am completely exhausted. I need rest."</span></p>
        <p><span class='dialogue-speaker'>Maki:</span> <span class='dialogue-text'>"Then who is going to trade in the village, you fool?"</span></p>
        <p><span class='dialogue-speaker'>Shinra:</span> <span class='dialogue-text'>"I will go! I learned arithmetic and how to persuade customers!"</span></p>
        <p><span class='dialogue-speaker'>Maki:</span> <span class='dialogue-text'>"Alright. Take this Woodcutter's Axe with you for safety."</span></p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Proceed to Mountain Path"):
        set_stage("GAMEPLAY_DESCENT")

# ==========================================
# STAGE 2: GAMEPLAY - DESCENT FROM MOUNTAIN
# ==========================================
elif st.session_state.stage == "GAMEPLAY_DESCENT":
    st.title("Descent to the Village")
    st.caption("Target Distance: 1300 meters through the forest.")

    st.markdown(f"""
    <div class='status-bar'>
        🎒 <b>Inventory:</b> Merchant Pack, Trade Goods, Woodcutter's Axe [Rank: Unknown]<br>
        📍 <b>Distance Travelled:</b> {st.session_state.pos_mountain} / 1300 meters
    </div>
    """, unsafe_allow_html=True)

    # HTML Canvas graphic for visualization
    progress_pct = int((st.session_state.pos_mountain / 1300) * 100)
    st.markdown(f"""
    <div style="background-color: #1f2937; border-radius: 10px; padding: 5px; border: 1px solid #4b5563;">
        <div style="background-color: #3b82f6; width: {progress_pct}%; height: 20px; border-radius: 8px; text-align: center; line-height: 20px; font-size: 12px; font-weight: bold; color: white;">
            {progress_pct}%
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Walk Down Mountain (+150m)"):
            st.session_state.pos_mountain += 150
            if st.session_state.pos_mountain >= 1300:
                st.session_state.pos_mountain = 1300
                set_stage("CUTSCENE_VILLAGE_MARKET")
            else:
                st.rerun()

    with col2:
        if st.button("Dash Down Mountain (+350m)"):
            st.session_state.pos_mountain += 350
            if st.session_state.pos_mountain >= 1300:
                st.session_state.pos_mountain = 1300
                set_stage("CUTSCENE_VILLAGE_MARKET")
            else:
                st.rerun()

# ==========================================
# STAGE 3: CUTSCENE - VILLAGE MARKET TRADING
# ==========================================
elif st.session_state.stage == "CUTSCENE_VILLAGE_MARKET":
    st.title("Village Market - Trading")

    st.markdown("""
    <div class='story-box'>
        <p><span class='dialogue-speaker'>Villager:</span> <span class='dialogue-text'>"Look, the goods are here! Wait, you are Soho's younger brother. Where is Soho?"</span></p>
        <p><span class='dialogue-speaker'>Shinra:</span> <span class='dialogue-text'>"He is exhausted today, so I am taking over the sales!"</span></p>
        <p><span class='dialogue-speaker'>Villager:</span> <span class='dialogue-text'>"I see. How much for 1kg of this fabric?"</span></p>
        <p><span class='dialogue-speaker'>Shinra:</span> <span class='dialogue-text'>"15 Gold Coins!"</span></p>
        <p><span class='dialogue-speaker'>Arrogant Customer:</span> <span class='dialogue-text'>"That's way too expensive!"</span></p>
        <p><span class='dialogue-speaker'>Shinra:</span> <span class='dialogue-text'>"No way! My brother sells cheaper than anyone in the market. Original price is 20 gold coins. Do you want it or should I raise the price? Besides, this is genuine Bear-Skin Fabric that we gathered ourselves!"</span></p>
        <p><span class='dialogue-speaker'>Arrogant Customer:</span> <span class='dialogue-text'>"Tch... fine! I'll buy it!" <i>(The trick worked!)</i></span></p>
        <hr>
        <p><span class='dialogue-speaker'>Other Customers:</span> <span class='dialogue-text'>"Give me potatoes!" "I want charcoal!" "Lotus flowers here!" "I'll take lettuce!"</span></p>
        <p><span class='dialogue-speaker'>Shinra (Sweating):</span> <span class='dialogue-text'>"Looks like I won't be returning home early today..."</span></p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='story-box'>
        <p><i>Night falls... All goods are completely sold out.</i></p>
        <p><span class='dialogue-speaker'>Shinra:</span> <span class='dialogue-text'>"What a tiring day... Time to head back home. It's dark, but good thing I brought my axe."</span></p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Head Back Home Into The Night Forest"):
        set_stage("CUTSCENE_BEAR_ENCOUNTER")

# ==========================================
# STAGE 4: ENCOUNTER - THE RED-EYED BEAR
# ==========================================
elif st.session_state.stage == "CUTSCENE_BEAR_ENCOUNTER":
    st.title("Night Forest Encounter")

    st.markdown("""
    <div class='story-box' style='border-color: #ef4444;'>
        <p><i>As Shinra walks up the mountain path, glowing red eyes emerge from the thick darkness of the forest... A massive, wild bear appears!</i></p>
        <p><span class='dialogue-speaker'>Shinra:</span> <span class='dialogue-text'>"My God... Bears are wandering around our forest near home? Maybe Maki didn't secure the trap properly... Fine, I will fight you!"</span></p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Draw Woodcutter's Axe & Fight!"):
        set_stage("GAMEPLAY_BOSS_FIGHT")

# ==========================================
# STAGE 5: GAMEPLAY - BOSS FIGHT (GIANT BEAR)
# ==========================================
elif st.session_state.stage == "GAMEPLAY_BOSS_FIGHT":
    st.markdown("<h2 class='boss-header'>⚠️ BOSS BATTLE: GIANT RED-EYED BEAR ⚠️</h2>", unsafe_allow_html=True)

    col_s, col_b = st.columns(2)
    with col_s:
        st.markdown(f"### 🧑 Shinra\n**HP:** {st.session_state.shinra_hp} / 1500")
        st.progress(max(0, st.session_state.shinra_hp) / 1500)
    with col_b:
        st.markdown(f"### 🐻 Giant Bear\n**HP:** {st.session_state.bear_hp} / 500")
        st.progress(max(0, st.session_state.bear_hp) / 500)

    st.markdown("#### Combat Log")
    log_html = "<br>".join(st.session_state.combat_log[-4:])
    st.markdown(f"<div class='combat-log'>{log_html if log_html else 'Battle starting...'}</div>", unsafe_allow_html=True)

    st.write("")
    
    if st.session_state.shinra_hp > 0 and st.session_state.bear_hp > 0:
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🪓 Axe Slash (30-60 DMG)"):
                # Player attack
                dmg = random.randint(30, 60)
                st.session_state.bear_hp -= dmg
                st.session_state.combat_log.append(f"> Shinra slashes with Axe for {dmg} DMG!")

                # Boss turn if alive
                if st.session_state.bear_hp > 0:
                    # 70% normal attack, 30% heavy attack
                    if random.random() < 0.7:
                        b_dmg = random.randint(50, 70)
                        st.session_state.combat_log.append(f"> Giant Bear claws Shinra for {b_dmg} DMG!")
                    else:
                        b_dmg = random.randint(90, 140)
                        st.session_state.combat_log.append(f"> 💥 GIANT BEAR SWIPE! Shinra takes {b_dmg} DMG!")
                    st.session_state.shinra_hp -= b_dmg

                st.rerun()

        with c2:
            if st.button("🛡️ Dodge & Quick Counter (20-40 DMG)"):
                dmg = random.randint(20, 40)
                st.session_state.bear_hp -= dmg
                b_dmg = random.randint(20, 40) # Reduced damage taken
                st.session_state.shinra_hp -= b_dmg
                st.session_state.combat_log.append(f"> Shinra swiftly dodged and hit for {dmg} DMG, taking only {b_dmg} DMG!")
                st.rerun()

    elif st.session_state.shinra_hp <= 0:
        st.error("💀 You were defeated by the Giant Bear...")
        if st.button("🔄 Retry Battle"):
            st.session_state.shinra_hp = 1500
            st.session_state.bear_hp = 500
            st.session_state.combat_log = []
            st.rerun()

    elif st.session_state.bear_hp <= 0:
        st.success("🎉 Victory! The Giant Bear has been slain!")
        if st.button("Continue Story"):
            set_stage("CUTSCENE_POST_BEAR")

# ==========================================
# STAGE 6: CUTSCENE - AFTER THE FIGHT
# ==========================================
elif st.session_state.stage == "CUTSCENE_POST_BEAR":
    st.title("After the Battle")

    st.markdown("""
    <div class='story-box'>
        <p><i>Shinra, wounded with a fresh scratch on his cheek, stands over the defeated beast. With a powerful final strike, he severs the bear's head.</i></p>
        <p><span class='dialogue-speaker'>Shinra:</span> <span class='dialogue-text'>"Man, this specific bear was tough! I'm going to cook it and eat its meat."</span></p>
        <p><i>[Phew...] Shinra starts a fire and roasts the meat over glowing embers.</i></p>
        <p><span class='dialogue-speaker'>Shinra:</span> <span class='dialogue-text'>"Mmm, delicious meat! ...Wait, I almost forgot! I need to return home as fast as possible!"</span></p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Run Home Quickly"):
        set_stage("GAMEPLAY_RUN_HOME")

# ==========================================
# STAGE 7: GAMEPLAY - RUSH BACK HOME
# ==========================================
elif st.session_state.stage == "GAMEPLAY_RUN_HOME":
    st.title("Rushing Back Home")
    
    st.markdown(f"""
    <div class='status-bar'>
        🏃 <b>Shinra's Movement</b><br>
        📍 <b>Distance to Home:</b> {st.session_state.pos_return} / 1000 meters
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Run (+200m)"):
            st.session_state.pos_return += 200
            if st.session_state.pos_return >= 1000:
                set_stage("CUTSCENE_TRAGEDY")
            else:
                st.rerun()
    with c2:
        if st.button("⚡ DASH (40 km/h) (+400m)"):
            st.session_state.pos_return += 400
            if st.session_state.pos_return >= 1000:
                set_stage("CUTSCENE_TRAGEDY")
            else:
                st.rerun()

# ==========================================
# STAGE 8: CUTSCENE - THE TRAGEDY
# ==========================================
elif st.session_state.stage == "CUTSCENE_TRAGEDY":
    st.title("The Tragedy")

    st.markdown("""
    <div class='story-box' style='border-color: #7f1d1d; background-color: #1a0505;'>
        <h3 style='color: #ef4444; text-align: center;'>[ Narrator ]</h3>
        <p style='text-align: center; font-size: 1.2em; color: #f87171;'><i>"And here... begins the true tragedy for Shinra."</i></p>
        <hr style='border-color: #7f1d1d;'>
        <p>Shinra reaches the top of the mountain. The house is completely destroyed and shattered. His father Yura lies unconscious on the floor. Soho and Maki are lying motionless in pools of blood... all lifeless.</p>
        <p><span class='dialogue-speaker'>Shinra (Tears streaming, in utter shock):</span> <span class='dialogue-text'>"AAAAAAAH! WHAT IS THIS?! Soho! Maki! Father! Is anyone alive?! I must take you to the hospital right now!"</span></p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Load Family into the Cart"):
        set_stage("GAMEPLAY_CARRY_FAMILY")

# ==========================================
# STAGE 9: GAMEPLAY - CARRY FAMILY TO CART
# ==========================================
elif st.session_state.stage == "GAMEPLAY_CARRY_FAMILY":
    st.title("Rescue Operation")
    st.subheader("Carry your family members one by one to the merchant cart!")

    st.markdown(f"""
    <div class='status-bar'>
        🛒 <b>Cart Contents:</b> {', '.join(st.session_state.carried_bodies) if st.session_state.carried_bodies else 'Empty'}
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    
    with c1:
        if "Soho" not in st.session_state.carried_bodies:
            if st.button("Carry Soho"):
                st.session_state.carried_bodies.append("Soho")
                st.rerun()
        else:
            st.write("✅ Soho in cart")

    with c2:
        if "Maki" not in st.session_state.carried_bodies:
            if st.button("Carry Maki"):
                st.session_state.carried_bodies.append("Maki")
                st.rerun()
        else:
            st.write("✅ Maki in cart")

    with c3:
        if "Father (Yura)" not in st.session_state.carried_bodies:
            if st.button("Carry Father Yura"):
                st.session_state.carried_bodies.append("Father (Yura)")
                st.rerun()
        else:
            st.write("✅ Father in cart")

    if len(st.session_state.carried_bodies) == 3:
        st.markdown("---")
        st.success("All family members loaded! Sprint to the village hospital!")
        if st.button("Sprint to Village (40 km/h)"):
            set_stage("GAMEPLAY_CART_SPRINT")

# ==========================================
# STAGE 10: GAMEPLAY - DASH CART TO VILLAGE
# ==========================================
elif st.session_state.stage == "GAMEPLAY_CART_SPRINT":
    st.title("Desperate Sprint to Village")

    st.markdown(f"""
    <div class='status-bar'>
        ⚡ <b>Speed:</b> 40 km/h<br>
        📍 <b>Distance to Hospital:</b> {st.session_state.pos_cart} / 1200 meters
    </div>
    """, unsafe_allow_html=True)

    if st.button("⚡ MAXIMUM DASH (+400m)"):
        st.session_state.pos_cart += 400
        if st.session_state.pos_cart >= 1200:
            set_stage("CUTSCENE_HOSPITAL_ARRIVAL")
        else:
            st.rerun()

# ==========================================
# STAGE 11: CUTSCENE - HOSPITAL ARRIVAL
# ==========================================
elif st.session_state.stage == "CUTSCENE_HOSPITAL_ARRIVAL":
    st.title("Arrival at Village Hospital")

    st.markdown("""
    <div class='story-box'>
        <p><i>Shinra's face is completely cold and emotionless as he pulls the heavy cart at a terrifying speed of 40 km/h, shocking and pushing past terrified villagers!</i></p>
        <p><span class='dialogue-speaker'>Shinra (Scream echoing across town):</span> <span class='dialogue-text'>"IS THERE A DOCTOR HERE?! MY BROTHER, SISTER, AND FATHER ARE CRITICALLY INJURED!!"</span></p>
        <p><i>Villagers stand terrified. A doctor rushes out from the clinic...</i></p>
        <p><span class='dialogue-speaker'>Doctor Yuno (Age 34, 180 cm):</span> <span class='dialogue-text'>"Quickly! Bring them inside for emergency treatment now!"</span></p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Wait for Doctor's Diagnosis"):
        set_stage("CUTSCENE_ENDING")

# ==========================================
# STAGE 12: CUTSCENE - THE TRAGIC ENDING & AWAKENING
# ==========================================
elif st.session_state.stage == "CUTSCENE_ENDING":
    st.title("Hospital Room")

    st.markdown("""
    <div class='story-box'>
        <p><span class='dialogue-speaker'>Doctor Yuno:</span> <span class='dialogue-text'>"Hello, young merchant... My name is Dr. Yuno. I am deeply sorry to inform you... The tall boy, your brother Soho, and your sister Maki wearing the patch... have passed away."</span></p>
        <p><span class='dialogue-speaker'>Doctor Yuno:</span> <span class='dialogue-text'>"Your old father is still alive, but he has fallen into a deep coma. He might awaken in 1 to 3 years..."</span></p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='story-box' style='border-color: #9333ea; background-color: #0d021a;'>
        <p><span class='dialogue-speaker'>Shinra (In profound shock & despair):</span> <span class='dialogue-text'>"What...? Soho... Maki... are DEAD?!"</span></p>
        <h2 style='color: #a855f7; text-align: center;'>HAAAAAAAAAAAAAAA...!!!!!!!</h2>
        <p><i>A massive dark aura bursts forth from Shinra's body. Violent atmospheric tremors shake the hospital ground without causing structural damage—a terrifying pressure that frightens Doctor Yuno to his core!</i></p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Conclusion"):
        set_stage("FINAL_SCREEN")

# ==========================================
# STAGE 13: END SCREEN
# ==========================================
elif st.session_state.stage == "FINAL_SCREEN":
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #dc2626; font-size: 70px;'>THE END</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #9ca3af;'>To Be Continued in Chapter 2...</p>", unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    if st.button("Restart Chapter 1"):
        st.session_state.clear()
        st.rerun()