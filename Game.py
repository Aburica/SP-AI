import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Chronicles of Shinra - 3D Chapter 1", layout="wide")

html_code = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Chronicles of Shinra - 3D Chapter 1</title>
    <style>
        body { margin: 0; overflow: hidden; background-color: #000; font-family: 'Arial', sans-serif; user-select: none; }
        #canvas-container { width: 100vw; height: 100vh; display: block; }
        
        /* UI Overlay */
        #ui-layer {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            pointer-events: none;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            box-sizing: border-box;
            padding: 20px;
        }

        .hud {
            color: #fff;
            font-size: 18px;
            text-shadow: 2px 2px 4px #000;
            background: rgba(0, 0, 0, 0.6);
            padding: 15px;
            border-radius: 8px;
            width: fit-content;
        }

        .health-bar-container {
            width: 250px; height: 20px; background: #444; border-radius: 10px; overflow: hidden; margin-top: 5px; border: 1px solid #777;
        }
        .health-bar-fill {
            height: 100%; background: #22c55e; width: 100%; transition: width 0.2s;
        }
        .boss-health-fill {
            height: 100%; background: #ef4444; width: 100%; transition: width 0.2s;
        }

        /* Dialogue Box */
        #dialogue-box {
            background: rgba(10, 10, 15, 0.85);
            border: 2px solid #4a5568;
            border-radius: 10px;
            padding: 20px;
            color: #fff;
            max-width: 800px;
            margin: 0 auto 30px auto;
            pointer-events: auto;
            display: none;
        }
        #speaker-name { font-weight: bold; color: #f6ad55; font-size: 20px; margin-bottom: 8px; }
        #dialogue-text { font-size: 16px; line-height: 1.5; color: #e2e8f0; }
        #dialogue-btn {
            margin-top: 15px; background: #3182ce; color: white; border: none; padding: 8px 16px;
            border-radius: 5px; cursor: pointer; font-weight: bold; float: right;
        }
        #dialogue-btn:hover { background: #2b6cb0; }

        /* Controls Prompt */
        #controls-info {
            position: absolute; bottom: 20px; left: 20px;
            background: rgba(0,0,0,0.5); color: #aaa; padding: 10px; border-radius: 5px; font-size: 12px;
        }

        /* Intro Screen */
        #screen-overlay {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background: #000; color: #fff; display: flex; flex-direction: column;
            justify-content: center; align-items: center; z-index: 100;
            pointer-events: auto;
        }
        #screen-overlay h1 { font-size: 80px; margin: 0; color: #d1d5db; letter-spacing: 5px; }
        #screen-overlay button {
            margin-top: 30px; padding: 12px 30px; font-size: 20px; background: #dc2626; color: #fff;
            border: none; border-radius: 5px; cursor: pointer; font-weight: bold;
        }
        #screen-overlay button:hover { background: #b91c1c; }
    </style>
    <!-- Three.js Library -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>

    <div id="screen-overlay">
        <h1 id="overlay-title">792 A.D.</h1>
        <p id="overlay-sub">Chronicles of Shinra - Chapter 1</p>
        <button id="start-btn" onclick="startGame()">START GAME</button>
    </div>

    <div id="ui-layer">
        <div class="hud" id="hud-stats" style="display:none;">
            <div><b>Shinra</b> (Age 9 | 142cm)</div>
            <div>HP: <span id="player-hp-num">1500</span> / 1500</div>
            <div class="health-bar-container"><div id="player-hp-bar" class="health-bar-fill"></div></div>
            <div id="boss-hud" style="display:none; margin-top: 10px;">
                <div style="color:#ef4444;"><b>Giant Red-Eyed Bear</b></div>
                <div class="health-bar-container"><div id="boss-hp-bar" class="boss-health-fill"></div></div>
            </div>
        </div>

        <div id="controls-info">
            <b>Controls:</b> W, A, S, D = Move | Shift = Dash (40km/h) | Space = Attack / Interact | E = Pick Up Body
        </div>

        <div id="dialogue-box">
            <div id="speaker-name">Speaker</div>
            <div id="dialogue-text">Dialogue Text Goes Here...</div>
            <button id="dialogue-btn" onclick="nextDialogue()">Next ►</button>
        </div>
    </div>

    <div id="canvas-container"></div>

    <script>
        // Game Engine Variables
        let scene, camera, renderer;
        let player, playerAxe, bear, cart, house, hospital;
        let family = [];
        let keys = {};
        
        // Game State
        let currentStage = "INTRO"; // INTRO, HOME_CUTSCENE, MOUNTAIN_DESCENT, MARKET_CUTSCENE, BEAR_FIGHT, POST_BEAR, RETURN_HOME, TRAGEDY_CUTSCENE, CARRY_FAMILY, SPRINT_HOSPITAL, ENDING
        let playerHP = 1500;
        let bearHP = 500;
        let dialogueIndex = 0;
        let currentDialogues = [];
        let carriedCount = 0;

        function init3D() {
            const container = document.getElementById('canvas-container');
            scene = new THREE.Scene();
            scene.background = new THREE.Color(0x0a0d12);
            scene.fog = new THREE.FogExp2(0x0a0d12, 0.015);

            camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
            
            renderer = new THREE.WebGLRenderer({ antialias: true });
            renderer.setSize(window.innerWidth, window.innerHeight);
            renderer.shadowMap.enabled = true;
            container.appendChild(renderer.domElement);

            // Lighting
            const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
            scene.add(ambientLight);

            const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
            dirLight.position.set(20, 40, 20);
            dirLight.castShadow = true;
            scene.add(dirLight);

            // Environment: Ground
            const groundGeo = new THREE.PlaneGeometry(300, 300);
            const groundMat = new THREE.MeshLambertMaterial({ color: 0x1c2518 });
            const ground = new THREE.Mesh(groundGeo, groundMat);
            ground.rotation.x = -Math.PI / 2;
            ground.receiveShadow = true;
            scene.add(ground);

            // Create Characters & Objects
            createPlayer();
            createHouseAndFamily();
            createBear();
            createCart();
            createTrees();

            // Camera Setup
            camera.position.set(0, 5, 10);
            
            // Event Listeners
            window.addEventListener('resize', onWindowResize);
            window.addEventListener('keydown', e => keys[e.code] = true);
            window.addEventListener('keyup', e => keys[e.code] = false);

            animate();
        }

        function createPlayer() {
            // Shinra Player Mesh (Stylized 142cm representation)
            player = new THREE.Group();
            
            const bodyGeo = new THREE.CylinderGeometry(0.3, 0.3, 1.4);
            const bodyMat = new THREE.MeshLambertMaterial({ color: 0x3b82f6 });
            const body = new THREE.Mesh(bodyGeo, bodyMat);
            body.position.y = 0.7;
            player.add(body);

            const headGeo = new THREE.SphereGeometry(0.25);
            const headMat = new THREE.MeshLambertMaterial({ color: 0xffdbac });
            const head = new THREE.Mesh(headGeo, headMat);
            head.position.y = 1.5;
            player.add(head);

            // Axe (Unknown Rank)
            playerAxe = new THREE.Group();
            const handleGeo = new THREE.CylinderGeometry(0.03, 0.03, 0.8);
            const handleMat = new THREE.MeshLambertMaterial({ color: 0x78350f });
            const handle = new THREE.Mesh(handleGeo, handleMat);
            
            const bladeGeo = new THREE.BoxGeometry(0.3, 0.2, 0.05);
            const bladeMat = new THREE.MeshLambertMaterial({ color: 0x9ca3af });
            const blade = new THREE.Mesh(bladeGeo, bladeMat);
            blade.position.set(0.1, 0.3, 0);

            playerAxe.add(handle);
            playerAxe.add(blade);
            playerAxe.position.set(0.4, 0.8, 0.2);
            player.add(playerAxe);

            player.position.set(0, 0, 0);
            scene.add(player);
        }

        function createHouseAndFamily() {
            // Mountain House
            house = new THREE.Group();
            const wallMat = new THREE.MeshLambertMaterial({ color: 0x451a03 });
            const walls = new THREE.Mesh(new THREE.BoxGeometry(6, 4, 6), wallMat);
            walls.position.y = 2;
            
            const roofMat = new THREE.MeshLambertMaterial({ color: 0x27272a });
            const roof = new THREE.Mesh(new THREE.ConeGeometry(5, 2, 4), roofMat);
            roof.position.y = 5;
            roof.rotation.y = Math.PI / 4;

            house.add(walls);
            house.add(roof);
            house.position.set(0, 0, -15);
            scene.add(house);

            // Family Members (Yura, Soho, Maki, Koren's Grave)
            const graveGeo = new THREE.BoxGeometry(0.5, 1, 0.2);
            const graveMat = new THREE.MeshLambertMaterial({ color: 0x6b7280 });
            const grave = new THREE.Mesh(graveGeo, graveMat);
            grave.position.set(-6, 0.5, -15);
            scene.add(grave);

            // Family Meshes inside/near house
            const createMember = (color, height, x, z, name) => {
                const m = new THREE.Mesh(new THREE.CylinderGeometry(0.3, 0.3, height), new THREE.MeshLambertMaterial({ color: color }));
                m.position.set(x, height/2, z);
                m.userData = { name: name, isCarried: false };
                scene.add(m);
                return m;
            };

            family.push(createMember(0xef4444, 1.78, -2, -13, "Father Yura"));
            family.push(createMember(0x10b981, 1.82, 2, -13, "Soho"));
            family.push(createMember(0xec4899, 1.54, 3, -14, "Maki"));
        }

        function createBear() {
            bear = new THREE.Group();
            const body = new THREE.Mesh(new THREE.BoxGeometry(2, 2, 3), new THREE.MeshLambertMaterial({ color: 0x1f1917 }));
            body.position.y = 1;
            
            // Glowing Red Eyes
            const eyeGeo = new THREE.SphereGeometry(0.1);
            const eyeMat = new THREE.MeshBasicMaterial({ color: 0xff0000 });
            const eye1 = new THREE.Mesh(eyeGeo, eyeMat);
            const eye2 = new THREE.Mesh(eyeGeo, eyeMat);
            eye1.position.set(-0.4, 1.5, 1.5);
            eye2.position.set(0.4, 1.5, 1.5);

            bear.add(body);
            bear.add(eye1);
            bear.add(eye2);
            bear.position.set(0, 0, -60);
            scene.add(bear);
        }

        function createCart() {
            cart = new THREE.Group();
            const boxMat = new THREE.MeshLambertMaterial({ color: 0x78350f });
            const box = new THREE.Mesh(new THREE.BoxGeometry(2, 1, 3), boxMat);
            box.position.y = 0.8;
            cart.add(box);
            cart.position.set(5, 0, -10);
            scene.add(cart);
        }

        function createTrees() {
            const treeMat = new THREE.MeshLambertMaterial({ color: 0x064e3b });
            const trunkMat = new THREE.MeshLambertMaterial({ color: 0x451a03 });

            for(let i = 0; i < 60; i++) {
                const tree = new THREE.Group();
                const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.4, 2), trunkMat);
                trunk.position.y = 1;
                const leaves = new THREE.Mesh(new THREE.ConeGeometry(2, 6, 5), treeMat);
                leaves.position.y = 4;
                tree.add(trunk);
                tree.add(leaves);

                let x = (Math.random() - 0.5) * 200;
                let z = (Math.random() - 0.5) * 200;
                if(Math.abs(x) < 8 && Math.abs(z) < 80) continue; // Keep path clear
                tree.position.set(x, 0, z);
                scene.add(tree);
            }
        }

        function startGame() {
            document.getElementById('screen-overlay').style.display = 'none';
            document.getElementById('hud-stats').style.display = 'block';
            startCutscene("HOME_CUTSCENE");
        }

        // Dialogue System
        function startCutscene(stage) {
            currentStage = stage;
            dialogueIndex = 0;

            if (stage === "HOME_CUTSCENE") {
                currentDialogues = [
                    { speaker: "Yura", text: "Maki... bring me my medicine... quickly." },
                    { speaker: "Maki", text: "Here Father! Please take it!" },
                    { speaker: "Soho", text: "Hello Maki! Father! I have returned with the cart!" },
                    { speaker: "Maki", text: "Welcome back Soho! ...Wait, where is Shinra?" },
                    { speaker: "Shinra", text: "I'm right here!" },
                    { speaker: "Maki", text: "*PUNCHES SHINRA* I thought you were lost!" },
                    { speaker: "Shinra", text: "Ouch! I helped Soho sell Lotus Flowers for 30 Gold Coins!" },
                    { speaker: "Soho", text: "A week later... I am completely exhausted. I need rest." },
                    { speaker: "Shinra", text: "I will go sell the goods in the village! I learned arithmetic!" },
                    { speaker: "Maki", text: "Alright, take this Woodcutter's Axe with you for safety." }
                ];
            } else if (stage === "MARKET_CUTSCENE") {
                currentDialogues = [
                    { speaker: "Villager", text: "Look, goods are here! Are you Soho's brother?" },
                    { speaker: "Shinra", text: "Yes! Selling Bear-Skin Fabric for 15 Gold Coins!" },
                    { speaker: "Arrogant Customer", text: "Too expensive! ...Fine, I'll buy it!" },
                    { speaker: "Shinra", text: "Phew, sold out everything! It's dark now. Time to walk back home." }
                ];
            } else if (stage === "POST_BEAR") {
                currentDialogues = [
                    { speaker: "Shinra", text: "Phew! This bear was tough... I sliced off its head and roasted the meat. Delicious!" },
                    { speaker: "Shinra", text: "Wait! I need to rush back home right now!" }
                ];
            } else if (stage === "TRAGEDY_CUTSCENE") {
                currentDialogues = [
                    { speaker: "Narrator", text: "And here... begins the tragedy for Shinra." },
                    { speaker: "Shinra", text: "NOOO! The house is destroyed! Father is unconscious! Soho and Maki are dead?!" },
                    { speaker: "Shinra", text: "I must load them onto the cart and run to the hospital! [Press E near family members to pick them up]" }
                ];
            } else if (stage === "ENDING") {
                currentDialogues = [
                    { speaker: "Doctor Yuno", text: "Young boy... I am Dr. Yuno. Your brother Soho and sister Maki have passed away." },
                    { speaker: "Doctor Yuno", text: "Your father Yura is alive, but in a deep coma for 1-3 years..." },
                    { speaker: "Shinra", text: "SOHO... MAKI... ARE DEAD?! HAAAAAAAAAAAAAAA...!!!!!" },
                    { speaker: "Narrator", text: "A terrifying dark aura erupts from Shinra, shaking the hospital grounds..." }
                ];
            }

            showDialogue();
        }

        function showDialogue() {
            if (dialogueIndex < currentDialogues.length) {
                const d = currentDialogues[dialogueIndex];
                document.getElementById('speaker-name').innerText = d.speaker;
                document.getElementById('dialogue-text').innerText = d.text;
                document.getElementById('dialogue-box').style.display = 'block';
            } else {
                document.getElementById('dialogue-box').style.display = 'none';
                endCutsceneStage();
            }
        }

        function nextDialogue() {
            dialogueIndex++;
            showDialogue();
        }

        function endCutsceneStage() {
            if (currentStage === "HOME_CUTSCENE") {
                currentStage = "MOUNTAIN_DESCENT";
            } else if (currentStage === "MARKET_CUTSCENE") {
                currentStage = "BEAR_FIGHT";
                document.getElementById('boss-hud').style.display = 'block';
            } else if (currentStage === "POST_BEAR") {
                currentStage = "RETURN_HOME";
            } else if (currentStage === "TRAGEDY_CUTSCENE") {
                currentStage = "CARRY_FAMILY";
            } else if (currentStage === "ENDING") {
                document.getElementById('screen-overlay').style.display = 'flex';
                document.getElementById('overlay-title').innerText = "THE END";
                document.getElementById('overlay-title').style.color = "#ef4444";
                document.getElementById('overlay-sub').innerText = "To Be Continued in Chapter 2...";
                document.getElementById('start-btn').innerText = "RESTART CHAPTER 1";
                document.getElementById('start-btn').onclick = () => location.reload();
            }
        }

        // Gameplay Loop Mechanics
        function updatePlayerMovement() {
            let speed = (keys['ShiftLeft'] || keys['ShiftRight']) ? 0.3 : 0.12; // Dash speed option
            
            if (currentStage === "MOUNTAIN_DESCENT" || currentStage === "RETURN_HOME" || currentStage === "CARRY_FAMILY" || currentStage === "SPRINT_HOSPITAL" || currentStage === "BEAR_FIGHT") {
                if (keys['KeyW']) player.position.z -= speed;
                if (keys['KeyS']) player.position.z += speed;
                if (keys['KeyA']) player.position.x -= speed;
                if (keys['KeyD']) player.position.x += speed;

                // Stage Trigger Progression Checks
                if (currentStage === "MOUNTAIN_DESCENT" && player.position.z < -40) {
                    startCutscene("MARKET_CUTSCENE");
                }
                if (currentStage === "RETURN_HOME" && player.position.z > -10) {
                    startCutscene("TRAGEDY_CUTSCENE");
                }
                if (currentStage === "SPRINT_HOSPITAL" && player.position.z < -100) {
                    startCutscene("ENDING");
                }
            }

            // Attack & Interact Logic
            if (keys['Space']) {
                playerAxe.rotation.x = Math.PI / 2; // Axe Swing Animation
                if (currentStage === "BEAR_FIGHT") {
                    let dist = player.position.distanceTo(bear.position);
                    if (dist < 4) {
                        let dmg = Math.floor(Math.random() * 30) + 30; // 30-60 DMG
                        bearHP = Math.max(0, bearHP - dmg);
                        document.getElementById('boss-hp-bar').style.width = (bearHP / 500 * 100) + '%';
                        
                        if (bearHP <= 0) {
                            scene.remove(bear);
                            document.getElementById('boss-hud').style.display = 'none';
                            startCutscene("POST_BEAR");
                        }
                    }
                }
            } else {
                playerAxe.rotation.x = 0;
            }

            // Carry Family Action
            if (currentStage === "CARRY_FAMILY" && keys['KeyE']) {
                family.forEach(m => {
                    if (!m.userData.isCarried && player.position.distanceTo(m.position) < 3) {
                        m.userData.isCarried = true;
                        m.position.set(0, 1 + carriedCount * 0.4, 0);
                        cart.add(m);
                        carriedCount++;
                        if (carriedCount >= 3) {
                            currentStage = "SPRINT_HOSPITAL";
                        }
                    }
                });
            }

            // Camera follow player
            camera.position.set(player.position.x, player.position.y + 6, player.position.z + 12);
            camera.lookAt(player.position);
        }

        // Bear AI Fight Attack Logic
        let lastBearAttack = Date.now();
        function updateBearAI() {
            if (currentStage === "BEAR_FIGHT" && bearHP > 0) {
                bear.lookAt(player.position);
                let dist = bear.position.distanceTo(player.position);
                if (dist > 2) {
                    bear.translateZ(0.04);
                } else if (Date.now() - lastBearAttack > 1500) {
                    // Bear Attacks Shinra (50-70 DMG)
                    let dmg = Math.floor(Math.random() * 20) + 50;
                    playerHP = Math.max(0, playerHP - dmg);
                    document.getElementById('player-hp-num').innerText = playerHP;
                    document.getElementById('player-hp-bar').style.width = (playerHP / 1500 * 100) + '%';
                    lastBearAttack = Date.now();

                    if (playerHP <= 0) {
                        alert("You were slain by the Bear! Restarting battle...");
                        playerHP = 1500;
                        bearHP = 500;
                        document.getElementById('player-hp-bar').style.width = '100%';
                        document.getElementById('boss-hp-bar').style.width = '100%';
                        player.position.set(0,0,-40);
                    }
                }
            }
        }

        function animate() {
            requestAnimationFrame(animate);
            updatePlayerMovement();
            updateBearAI();
            renderer.render(scene, camera);
        }

        function onWindowResize() {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        }

        window.onload = init3D;
    </script>
</body>
</html>
"""

components.html(html_code, height=800, scrolling=False)
