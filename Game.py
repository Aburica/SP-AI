import streamlit as st
import time

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Shinra's Adventures - Chapter 1</title>
    <style>
        body {
            margin: 0;
            background-color: #111;
            color: #fff;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            overflow: hidden;
        }
        #game-container {
            width: 800px;
            height: 500px;
            background: #222;
            border: 4px solid #444;
            border-radius: 10px;
            position: relative;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            padding: 20px;
            box-shadow: 0 0 20px rgba(0,0,0,0.8);
        }
        .screen {
            display: none;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100%;
            text-align: center;
        }
        .active {
            display: flex;
        }
        h1 { color: #f39c12; margin-bottom: 10px; }
        p { font-size: 18px; line-height: 1.6; max-width: 700px; }
        button {
            background-color: #e74c3c;
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
            border-radius: 5px;
            margin-top: 20px;
            transition: 0.2s;
        }
        button:hover { background-color: #c0392b; }
        .stats {
            position: absolute;
            top: 10px;
            left: 20px;
            font-size: 14px;
            color: #f1c40f;
        }
        .hud {
            position: absolute;
            bottom: 10px;
            left: 20px;
            font-size: 14px;
            color: #bdc3c7;
        }
    </style>
</head>
<body>

<div id="game-container">
    <!-- شاشة البداية / القصة التمهيدية -->
    <div id="screen-intro" class="screen active">
        <h1>Shinra's Adventures</h1>
        <p>200 years ago, the Balance Crystal shattered. Hikari (Light) and Yami (Darkness) emerged... Now, a new tale begins in the isolated mountains.</p>
        <button onclick="nextScreen('screen-story1')">Start Chapter 1</button>
    </div>

    <!-- المشهد السينمائي الأول والثاني -->
    <div id="screen-story1" class="screen">
        <h3>Scene: The Mountain Home</h3>
        <p>Yora (Father) is sick. Maki and Soho care for him. Shinra returns from selling lotus flowers and earns 30 gold pieces.</p>
        <button onclick="startJourneyToVillage()">Go to Village with Cart (1200m)</button>
    </div>

    <!-- رحلة القرية والبيع -->
    <div id="screen-village" class="screen">
        <h3>The Village Market</h3>
        <p id="village-text">Villagers want goods (Cloth, Potatoes, Coal, Lotus Flowers, Lettuce). You sell everything successfully!</p>
        <button onclick="startReturnJourney()">Return to Mountain House</button>
    </div>

    <!-- طريق العودة ومواجهة الدب -->
    <div id="screen-bear-encounter" class="screen">
        <h3>Forest Path</h3>
        <p>"Oh no! Bears are roaming our forest. I must fight it!"</p>
        <button onclick="startCombat()">Fight the Bear!</button>
    </div>

    <!-- شاشة القتال (Turn-based Combat) -->
    <div id="screen-combat" class="screen">
        <div class="stats">Shinra HP: <span id="shinra-hp">1500</span> | Bear HP: <span id="bear-hp">500</span></div>
        <h3>Combat vs Fierce Bear</h3>
        <p id="combat-log">Choose your action wisely!</p>
        <div>
            <button onclick="combatAction('attack')">Normal Attack</button>
            <button onclick="combatAction('dodge')">Dodge</button>
            <button onclick="combatAction('dash')">Dash Strike</button>
        </div>
    </div>

    <!-- نهاية القتال وما بعده -->
    <div id="screen-after-combat" class="screen">
        <h3>Aftermath</h3>
        <p>Shinra defeats the bear with a slash, cooks the meat, and rushes back home...</p>
        <button onclick="startTragedyScene()">Reach Home</button>
    </div>

    <!-- المشهد الأخير والمأساة -->
    <div id="screen-tragedy" class="screen">
        <h1>Tragedy at Home</h1>
        <p>The house is destroyed. Father, Soho, and Maki are dead on the ground.<br>
        Shinra loads them onto the cart and races to Dr. Yuno at the village (40 km/h).</p>
        <button onclick="endChapter1()">Go to Hospital & Ending</button>
    </div>

    <!-- النهاية -->
    <div id="screen-ending" class="screen">
        <h1>End of Chapter 1</h1>
        <p>Dr. Yuno: "Soho and Maki didn't survive, but your father is alive in a coma."<br>
        Shinra lets out a powerful cry, releasing a dark, heavy aura that terrifies the doctor.<br><br><strong>To be continued...</strong></p>
        <button onclick="location.reload()">Play Again</button>
    </div>
</div>

<script>
    function nextScreen(screenId) {
        document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
        document.getElementById(screenId).classList.add('active');
    }

    function startJourneyToVillage() {
        // محاكاة مسافة 1200 متر والوصول للقرية
        alert("Traveling 1200m down the mountain to the village...");
        nextScreen('screen-village');
    }

    function startReturnJourney() {
        alert("Goods sold out! Returning to the mountain house with 5000 gold in pocket...");
        nextScreen('screen-bear-encounter');
    }

    let shinraHP = 1500;
    let bearHP = 500;

    function startCombat() {
        nextScreen('screen-combat');
        updateHPCard();
    }

    function updateHPCard() {
        document.getElementById('shinra-hp').innerText = shinraHP;
        document.getElementById('bear-hp').innerText = bearHP;
    }

    function combatAction(action) {
        let log = document.getElementById('combat-log');
        let bearDamage = 0;
        let shinraDamage = 0;

        if (action === 'attack') {
            shinraDamage = Math.floor(Math.random() * 16) + 25; // 25-40
            bearDamage = Math.floor(Math.random() * 21) + 30;  // 30-50
            bearHP -= shinraDamage;
            shinraHP -= bearDamage;
            log.innerText = `You attacked for ${shinraDamage}. Bear hit you for ${bearDamage}.`;
        } else if (action === 'dodge') {
            bearDamage = 0; // تفادي كامل
            log.innerText = `You successfully dodged the bear's attack!`;
        } else if (action === 'dash') {
            shinraDamage = Math.floor(Math.random() * 20) + 40;
            bearDamage = Math.floor(Math.random() * 41) + 50; // هجمة سريعة قوية للطرفين
            bearHP -= shinraDamage;
            shinraHP -= bearDamage;
            log.innerText = `Dash attack! You dealt ${shinraDamage}, but took ${bearDamage} damage!`;
        }

        if (bearHP <= 0) {
            updateHPCard();
            alert("You defeated the bear!");
            nextScreen('screen-after-combat');
            return;
        }

        if (shinraHP <= 0) {
            alert("You were defeated by the bear! Try again.");
            shinraHP = 1500;
            bearHP = 500;
        }
        updateHPCard();
    }

    function startTragedyScene() {
        nextScreen('screen-tragedy');
    }

    function endChapter1() {
        nextScreen('screen-ending');
    }
</script>

</body>
</html>
