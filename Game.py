<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Chronicles of Shinra - Chapter 1 (3D World)</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Three.js Library -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <!-- FontAwesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@700;900&family=Tajawal:wght@400;700;900&display=swap" rel="stylesheet">

    <style>
        * {
            user-select: none;
            -webkit-user-select: none;
            touch-action: manipulation;
        }
        body, html {
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
            font-family: 'Tajawal', sans-serif;
            background-color: #05070a;
            color: #f3f4f6;
        }
        .font-cinzel { font-family: 'Cinzel', serif; }
        
        #game-canvas {
            width: 100%;
            height: 100%;
            display: block;
        }

        .glass-panel {
            background: rgba(15, 23, 42, 0.85);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.15);
            box-shadow: 0 20px 50px rgba(0,0,0,0.8);
        }

        .dialogue-box {
            background: rgba(10, 14, 23, 0.95);
            backdrop-filter: blur(16px);
            border: 2px solid rgba(229, 169, 60, 0.5);
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.9);
        }

        .shake-screen {
            animation: shake 0.4s cubic-bezier(.36,.07,.19,.97) both infinite;
        }

        @keyframes shake {
            10%, 90% { transform: translate3d(-3px, 0, 0); }
            20%, 80% { transform: translate3d(5px, 0, 0); }
            30%, 50%, 70% { transform: translate3d(-8px, 0, 0); }
            40%, 60% { transform: translate3d(8px, 0, 0); }
        }
    </style>
</head>
<body class="relative">

    <canvas id="game-canvas"></canvas>

    <div id="ui-layer" class="absolute inset-0 pointer-events-none flex flex-col justify-between p-3 md:p-6 z-10">
        
        <!-- Top Navigation HUD -->
        <div id="top-hud" class="flex justify-between items-start w-full">
            <!-- Player Status Panel -->
            <div class="glass-panel p-3 rounded-xl flex items-center space-x-3 space-x-reverse min-w-[240px]">
                <div class="w-10 h-10 rounded-full bg-amber-600/30 border-2 border-amber-500 flex items-center justify-center font-bold text-amber-400 text-lg">
                    ⚔️
                </div>
                <div class="flex-1">
                    <div class="flex justify-between text-xs font-semibold mb-1">
                        <span class="text-amber-400">شينرا (9 سنوات)</span>
                        <span id="player-hp-text" class="text-emerald-400">1500 / 1500 HP</span>
                    </div>
                    <div class="w-full h-2.5 bg-slate-800 rounded-full overflow-hidden border border-slate-700">
                        <div id="player-hp-bar" class="h-full bg-gradient-to-r from-emerald-600 to-emerald-400 transition-all duration-200" style="width: 100%;"></div>
                    </div>
                    <div class="text-[10px] text-slate-400 mt-1 flex justify-between">
                        <span>الذهب: <strong id="gold-text" class="text-amber-300">0 قطعة</strong></span>
                        <span>السلاح: <strong class="text-amber-300">فأس الحطاب</strong></span>
                    </div>
                </div>
            </div>

            <!-- Current Objective Tracker -->
            <div id="objective-panel" class="glass-panel px-5 py-2.5 rounded-xl text-center">
                <div class="text-[11px] uppercase font-bold text-amber-500 tracking-widest mb-0.5" id="stage-title">الفصل الأول - سنة 792 م</div>
                <div id="objective-text" class="text-xs md:text-sm font-medium text-slate-200">تحدث مع عائلتك أمام بيت الجبل [E]</div>
            </div>
        </div>

        <!-- Bear RPG Battle HUD Overlay -->
        <div id="boss-hud" class="w-full max-w-xl mx-auto glass-panel p-4 rounded-xl text-center hidden border-red-500/50 pointer-events-auto">
            <div class="flex justify-between items-center mb-1">
                <span class="text-red-500 font-bold uppercase tracking-widest text-xs md:text-sm flex items-center gap-2">
                    <i class="fa-solid fa-skull"></i> الدب العملاق ذو العينين الحمراوين
                </span>
                <span id="boss-hp-text" class="text-red-400 text-xs font-bold">500 / 500 HP</span>
            </div>
            <div class="w-full h-3.5 bg-slate-900 rounded-full overflow-hidden border border-red-900 mb-3">
                <div id="boss-hp-bar" class="h-full bg-gradient-to-r from-red-700 to-rose-500 transition-all duration-200" style="width: 100%;"></div>
            </div>
            <div class="flex justify-center gap-2">
                <button id="attack-btn" onclick="attackBear()" class="bg-red-600 hover:bg-red-500 text-white font-bold px-6 py-2 rounded-lg text-xs md:text-sm shadow-lg border border-red-400 active:scale-95 transition">
                    ⚔️ هجوم بالفأس (Space / اضغط هنا)
                </button>
            </div>
        </div>

        <!-- Interactive Action Hint (Mobile & PC) -->
        <div id="action-prompt" class="hidden pointer-events-auto mx-auto bg-amber-500 text-slate-950 font-black px-6 py-2 rounded-full shadow-2xl text-xs md:text-sm animate-bounce cursor-pointer" onclick="triggerAction()">
            <span id="action-prompt-text">اضغط [E] للتفاعل</span>
        </div>

        <!-- Cart Attachment Status Display -->
        <div id="cart-status-bar" class="glass-panel px-4 py-2 rounded-lg mx-auto text-xs text-amber-400 font-bold flex items-center gap-3 border border-amber-500/40">
            <i class="fa-solid fa-truck-ramp-box text-base"></i>
            <span id="cart-status-text">العربة مفصولة | اقترب من العربة واضغط [G] لإمساكها / تركها</span>
        </div>

        <!-- Dialogue Box -->
        <div id="dialogue-container" class="dialogue-box w-full max-w-3xl mx-auto p-4 rounded-2xl pointer-events-auto hidden transition-all duration-300 mb-2">
            <div class="flex items-start gap-3">
                <div id="speaker-avatar" class="w-12 h-12 rounded-full bg-amber-600/30 border-2 border-amber-500 flex-shrink-0 flex items-center justify-center text-2xl font-bold text-amber-400 shadow-inner">
                    👤
                </div>
                <div class="flex-1">
                    <div class="flex justify-between items-center mb-1">
                        <span id="speaker-name" class="font-bold text-amber-400 text-base">اسم الشخصية</span>
                        <span id="speaker-role" class="text-[10px] text-slate-400 font-mono">معلومات</span>
                    </div>
                    <p id="dialogue-text" class="text-slate-200 text-xs md:text-sm leading-relaxed">
                        نص الحوار...
                    </p>
                </div>
            </div>
            <div class="mt-3 flex justify-end">
                <button id="dialogue-next-btn" onclick="nextDialogue()" class="bg-amber-600 hover:bg-amber-500 text-slate-950 font-bold px-5 py-1.5 rounded-lg text-xs transition-all transform active:scale-95 flex items-center gap-2 shadow-lg">
                    <span>التالي</span> <i class="fa-solid fa-chevron-left text-xs"></i>
                </button>
            </div>
        </div>
    </div>

    <!-- Title Screen & End Overlay -->
    <div id="full-screen-overlay" class="absolute inset-0 bg-black z-30 flex flex-col items-center justify-center p-6 text-center transition-opacity duration-1000">
        <div id="title-screen-content" class="max-w-xl space-y-6">
            <div class="text-amber-500/80 font-mono tracking-widest text-xs uppercase">سنة 792 م - جبل شينرا (3D)</div>
            <h1 class="text-4xl md:text-6xl font-extrabold font-cinzel tracking-wider text-transparent bg-clip-text bg-gradient-to-b from-amber-200 via-amber-400 to-amber-700 drop-shadow-2xl">
                CHRONICLES OF SHINRA
            </h1>
            <p class="text-slate-400 text-xs md:text-sm max-w-md mx-auto leading-relaxed">
                الفصل الأول: الجبل مرتفع والنزول إلى القرية التجارية الضخمة والتفاعل الإمساك بالعربة.
            </p>
            <div class="pt-4">
                <button onclick="startGame()" class="pointer-events-auto bg-gradient-to-r from-amber-600 to-amber-500 hover:from-amber-500 hover:to-amber-400 text-slate-950 font-black px-8 py-3 rounded-xl text-sm shadow-2xl uppercase transition-all transform hover:scale-105 active:scale-95 border border-amber-300/40">
                    بدء اللعب بالـ 3D
                </button>
            </div>
        </div>
    </div>

    <script>
        const GameStage = {
            TITLE: 0,
            INTRO_HOUSE: 1,
            DESCENT_TO_VILLAGE: 2,
            VILLAGE_TRADE: 3,
            FOREST_RETURN: 4,
            BEAR_BATTLE: 5,
            COOK_MEAT: 6,
            RETURN_DESTROYED_HOME: 7,
            TRAGEDY_DISCOVERY: 8,
            LOAD_FAMILY_CART: 9,
            CART_RUSH_HOSPITAL: 10,
            HOSPITAL_DOCTOR: 11,
            DARK_MAGIC_END: 12
        };

        let currentStage = GameStage.TITLE;
        let goldCount = 0;
        let playerHP = 1500, maxPlayerHP = 1500;
        let bearHP = 500, maxBearHP = 500;

        // 3D Engine References
        let scene, camera, renderer, clock = new THREE.Clock();
        let playerMesh, cartMesh, bearMesh;
        let houseGroup, destroyedHouseGroup, villageGroup, hospitalGroup;
        let isCartAttached = false;
        let familyLoaded = { yura: false, soho: false, maki: false };
        let dialogueIndex = 0, currentDialogueList = [], dialogueCallback = null;

        // Input Controls
        const keys = { w: false, a: false, s: false, d: false, ArrowUp: false, ArrowLeft: false, ArrowDown: false, ArrowRight: false, Shift: false };

        function init3D() {
            const container = document.getElementById('game-canvas');
            scene = new THREE.Scene();
            scene.background = new THREE.Color(0x0c1322);
            scene.fog = new THREE.FogExp2(0x0c1322, 0.005);

            camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
            renderer = new THREE.WebGLRenderer({ canvas: container, antialias: true });
            renderer.setSize(window.innerWidth, window.innerHeight);
            renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
            renderer.shadowMap.enabled = true;

            // Lights
            const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
            scene.add(ambientLight);

            const sunLight = new THREE.DirectionalLight(0xfff5ea, 0.9);
            sunLight.position.set(100, 150, 50);
            sunLight.castShadow = true;
            scene.add(sunLight);

            // Terrain with Mountain Elevation
            buildTerrainAndMountain();
            buildMountainHouse();
            buildVillage3D();
            buildForest3D();
            buildHospital3D();

            // Dynamic Interactive Meshes
            buildPlayer3D();
            buildCart3D();
            buildBear3D();

            window.addEventListener('resize', onWindowResize);
            setupInputListeners();
        }

        function buildTerrainAndMountain() {
            // Expanded 3D Ground
            const terrainGeo = new THREE.PlaneGeometry(600, 600, 80, 80);
            terrainGeo.rotateX(-Math.PI / 2);

            const pos = terrainGeo.attributes.position;
            for (let i = 0; i < pos.count; i++) {
                const x = pos.getX(i);
                const z = pos.getZ(i);
                
                // Real High Mountain Peak on the North-West (-150, -150)
                const distToPeak = Math.hypot(x + 150, z + 150);
                if (distToPeak < 140) {
                    pos.setY(i, Math.cos(distToPeak / 140 * Math.PI) * 45 + 45);
                }
            }
            terrainGeo.computeVertexNormals();

            const terrainMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.9 });
            const terrain = new THREE.Mesh(terrainGeo, terrainMat);
            terrain.receiveShadow = true;
            scene.add(terrain);

            // Road curving down from Mountain top to Village
            const pathPoints = [
                new THREE.Vector3(-150, 85, -150),
                new THREE.Vector3(-100, 50, -90),
                new THREE.Vector3(-40, 25, -30),
                new THREE.Vector3(20, 5, 20),
                new THREE.Vector3(120, 0, 120)
            ];
            const curve = new THREE.CatmullRomCurve3(pathPoints);
            const tubeGeo = new THREE.TubeGeometry(curve, 64, 5, 8, false);
            const pathMat = new THREE.MeshStandardMaterial({ color: 0x78350f, roughness: 1 });
            const pathMesh = new THREE.Mesh(tubeGeo, pathMat);
            pathMesh.position.y = -4;
            scene.add(pathMesh);
        }

        function buildMountainHouse() {
            houseGroup = new THREE.Group();
            houseGroup.position.set(-150, 88, -150);

            // House Walls
            const houseGeo = new THREE.BoxGeometry(16, 10, 14);
            const houseMat = new THREE.MeshStandardMaterial({ color: 0x542d12 });
            const houseBody = new THREE.Mesh(houseGeo, houseMat);
            houseBody.position.y = 5;
            houseGroup.add(houseBody);

            // Roof
            const roofGeo = new THREE.ConeGeometry(13, 7, 4);
            roofGeo.rotateY(Math.PI / 4);
            const roofMat = new THREE.MeshStandardMaterial({ color: 0x991b1b });
            const roof = new THREE.Mesh(roofGeo, roofMat);
            roof.position.y = 13.5;
            houseGroup.add(roof);

            scene.add(houseGroup);

            // Destroyed House Variant (Burnt Ruin)
            destroyedHouseGroup = new THREE.Group();
            destroyedHouseGroup.position.set(-150, 88, -150);
            destroyedHouseGroup.visible = false;

            for (let i = 0; i < 15; i++) {
                const plankGeo = new THREE.BoxGeometry(2 + Math.random()*4, 1, 6 + Math.random()*4);
                const plankMat = new THREE.MeshStandardMaterial({ color: 0x1c1917 });
                const plank = new THREE.Mesh(plankGeo, plankMat);
                plank.position.set((Math.random() - 0.5)*16, 0.5, (Math.random() - 0.5)*16);
                plank.rotation.set(Math.random(), Math.random(), Math.random());
                destroyedHouseGroup.add(plank);
            }
            scene.add(destroyedHouseGroup);
        }

        function buildVillage3D() {
            villageGroup = new THREE.Group();
            villageGroup.position.set(120, 0, 120);

            // Large Village Layout
            for (let x = -2; x <= 2; x++) {
                for (let z = -2; z <= 2; z++) {
                    if (x === 0 && z === 0) continue; // Central Plaza

                    const buildingGroup = new THREE.Group();
                    buildingGroup.position.set(x * 30, 0, z * 30);

                    // Randomize House / Store Type
                    const width = 12 + Math.random() * 4;
                    const height = 8 + Math.random() * 6;
                    const depth = 12 + Math.random() * 4;

                    const bodyMat = new THREE.MeshStandardMaterial({ 
                        color: (x + z) % 2 === 0 ? 0x854d0e : 0x334155 
                    });
                    const body = new THREE.Mesh(new THREE.BoxGeometry(width, height, depth), bodyMat);
                    body.position.y = height / 2;

                    const roofMat = new THREE.MeshStandardMaterial({ color: 0x0284c7 });
                    const roof = new THREE.Mesh(new THREE.ConeGeometry(width * 0.8, 6, 4), roofMat);
                    roof.rotateY(Math.PI / 4);
                    roof.position.y = height + 3;

                    buildingGroup.add(body, roof);
                    villageGroup.add(buildingGroup);
                }
            }
            scene.add(villageGroup);
        }

        function buildForest3D() {
            const forestGroup = new THREE.Group();
            for (let i = 0; i < 60; i++) {
                const treeGroup = new THREE.Group();
                const trunk = new THREE.Mesh(
                    new THREE.CylinderGeometry(0.8, 1.2, 8),
                    new THREE.MeshStandardMaterial({ color: 0x451a03 })
                );
                trunk.position.y = 4;

                const foliage = new THREE.Mesh(
                    new THREE.ConeGeometry(6, 14, 5),
                    new THREE.MeshStandardMaterial({ color: 0x064e3b })
                );
                foliage.position.y = 12;

                treeGroup.add(trunk, foliage);
                
                // Spread along the mountain slope
                const x = -80 + (Math.random() - 0.5) * 160;
                const z = -60 + (Math.random() - 0.5) * 160;
                const distToPeak = Math.hypot(x + 150, z + 150);
                const y = distToPeak < 140 ? Math.cos(distToPeak / 140 * Math.PI) * 45 + 45 : 0;

                treeGroup.position.set(x, y, z);
                forestGroup.add(treeGroup);
            }
            scene.add(forestGroup);
        }

        function buildHospital3D() {
            hospitalGroup = new THREE.Group();
            hospitalGroup.position.set(-120, 0, 100);

            const building = new THREE.Mesh(
                new THREE.BoxGeometry(24, 14, 20),
                new THREE.MeshStandardMaterial({ color: 0x0f766e })
            );
            building.position.y = 7;

            const crossHorizontal = new THREE.Mesh(
                new THREE.BoxGeometry(8, 2, 0.5),
                new THREE.MeshStandardMaterial({ color: 0xef4444 })
            );
            crossHorizontal.position.set(0, 10, 10.3);

            hospitalGroup.add(building, crossHorizontal);
            scene.add(hospitalGroup);
        }

        function buildPlayer3D() {
            playerMesh = new THREE.Group();
            
            // Body
            const body = new THREE.Mesh(
                new THREE.CylinderGeometry(1, 1, 3.5),
                new THREE.MeshStandardMaterial({ color: 0x0284c7 })
            );
            body.position.y = 1.75;

            // Head
            const head = new THREE.Mesh(
                new THREE.SphereGeometry(1.2, 16, 16),
                new THREE.MeshStandardMaterial({ color: 0xfca5a5 })
            );
            head.position.y = 4;

            playerMesh.add(body, head);
            playerMesh.position.set(-150, 88, -135); // Mountain Top Home
            scene.add(playerMesh);
        }

        function buildCart3D() {
            cartMesh = new THREE.Group();
            
            const frame = new THREE.Mesh(
                new THREE.BoxGeometry(4.5, 1.5, 6.5),
                new THREE.MeshStandardMaterial({ color: 0x78350f })
            );
            frame.position.y = 1.5;

            const wheelGeo = new THREE.CylinderGeometry(1.2, 1.2, 0.4, 12);
            wheelGeo.rotateZ(Math.PI / 2);
            const wheelMat = new THREE.MeshStandardMaterial({ color: 0x1c1917 });

            const w1 = new THREE.Mesh(wheelGeo, wheelMat); w1.position.set(-2.4, 1.2, -2);
            const w2 = new THREE.Mesh(wheelGeo, wheelMat); w2.position.set(2.4, 1.2, -2);
            const w3 = new THREE.Mesh(wheelGeo, wheelMat); w3.position.set(-2.4, 1.2, 2);
            const w4 = new THREE.Mesh(wheelGeo, wheelMat); w4.position.set(2.4, 1.2, 2);

            cartMesh.add(frame, w1, w2, w3, w4);
            cartMesh.position.set(-142, 88, -135);
            scene.add(cartMesh);
        }

        function buildBear3D() {
            bearMesh = new THREE.Group();
            
            const body = new THREE.Mesh(
                new THREE.BoxGeometry(7, 7, 10),
                new THREE.MeshStandardMaterial({ color: 0x1c1311 })
            );
            body.position.y = 3.5;

            const head = new THREE.Mesh(
                new THREE.SphereGeometry(3, 12, 12),
                new THREE.MeshStandardMaterial({ color: 0x271c19 })
            );
            head.position.set(0, 5, 5);

            const eyeMat = new THREE.MeshBasicMaterial({ color: 0xef4444 });
            const eye1 = new THREE.Mesh(new THREE.SphereGeometry(0.5, 8, 8), eyeMat);
            eye1.position.set(-1.2, 5.5, 7.5);
            const eye2 = new THREE.Mesh(new THREE.SphereGeometry(0.5, 8, 8), eyeMat);
            eye2.position.set(1.2, 5.5, 7.5);

            bearMesh.add(body, head, eye1, eye2);
            bearMesh.position.set(-20, 15, -10);
            bearMesh.visible = false;
            scene.add(bearMesh);
        }

        function setupInputListeners() {
            window.addEventListener('keydown', (e) => {
                if (e.key === 'w' || e.key === 'W' || e.key === 'ArrowUp') keys.w = true;
                if (e.key === 's' || e.key === 'S' || e.key === 'ArrowDown') keys.s = true;
                if (e.key === 'a' || e.key === 'A' || e.key === 'ArrowLeft') keys.a = true;
                if (e.key === 'd' || e.key === 'D' || e.key === 'ArrowRight') keys.d = true;
                if (e.key === 'Shift') keys.Shift = true;
                if (e.key === 'e' || e.key === 'E' || e.key === ' ') triggerAction();
                if (e.key === 'g' || e.key === 'G') toggleCartAttachment();
            });

            window.addEventListener('keyup', (e) => {
                if (e.key === 'w' || e.key === 'W' || e.key === 'ArrowUp') keys.w = false;
                if (e.key === 's' || e.key === 'S' || e.key === 'ArrowDown') keys.s = false;
                if (e.key === 'a' || e.key === 'A' || e.key === 'ArrowLeft') keys.a = false;
                if (e.key === 'd' || e.key === 'D' || e.key === 'ArrowRight') keys.d = false;
                if (e.key === 'Shift') keys.Shift = false;
            });
        }

        const DIALOGUES = {
            INTRO: [
                { speaker: "يورا (الأب)", role: "العمر 54 | مريض", text: "ماكي... أحضري دواء الحمى بسرعة..." },
                { speaker: "ماكي (الأخت)", role: "العمر 13", text: "تفضل يا أبي! اشربه الآن فوراً!" },
                { speaker: "سوهو (الأخ)", role: "العمر 18", text: "لقد عدتُ من السوق! ومعي شينرا الصغير الذي تسلل في عربتي!" },
                { speaker: "شينرا", role: "العمر 9", text: "ساعدت سوهو في تجارة اللوتس وجنينا 30 قطعة ذهب!" },
                { speaker: "سوهو", role: "العمر 18", text: "اليوم أنا تعبان جداً، هل يمكنك النزول للقرية للتداول يا شينرا؟" },
                { speaker: "شينرا", role: "العمر 9", text: "بالتأكيد! سأنزل الآن عبر طريق الجبل إلى سوق القرية!" }
            ],
            VILLAGE: [
                { speaker: "تاجر القرية", role: "سوق القرية التجارية", text: "أهلاً بك يا صغيري! سأشتري منك كل البضائع بـ 30 قطعة ذهب!" },
                { speaker: "شينرا", role: "العمر 9", text: "صفقة ممتازة! حل الليل الآن، حان وقت العودة عبر الغابة والجبل." }
            ],
            TRAGEDY: [
                { speaker: "شينرا", role: "العمر 9", text: "مـ... ما هذا؟! البيت مدمر ومحترق بالكامل!!" },
                { speaker: "شينرا", role: "العمر 9", text: "سوهو وماكي لا يتنفسان... وأبي في غيبوبة! امسك العربة بحرف [G] وانقلهم لمستشفى القرية!" }
            ],
            HOSPITAL: [
                { speaker: "الطبيب يونو", role: "طبيب القرية", text: "يؤسفني جداً... سوهو وماكي قد فارقا الحياة، ووالدك دخل غيبوبة عميقة." },
                { speaker: "شينرا", role: "العمر 9", text: "سـ... سوهو... ماكي... لاااااااااااااااا!!" }
            ]
        };

        function startDialogueSequence(key, onComplete) {
            currentDialogueList = DIALOGUES[key];
            dialogueIndex = 0;
            dialogueCallback = onComplete;
            document.getElementById('dialogue-container').classList.remove('hidden');
            renderDialogue();
        }

        function renderDialogue() {
            if (dialogueIndex >= currentDialogueList.length) {
                document.getElementById('dialogue-container').classList.add('hidden');
                if (dialogueCallback) dialogueCallback();
                return;
            }
            const item = currentDialogueList[dialogueIndex];
            document.getElementById('speaker-name').innerText = item.speaker;
            document.getElementById('speaker-role').innerText = item.role;
            document.getElementById('dialogue-text').innerText = item.text;
        }

        function nextDialogue() {
            dialogueIndex++;
            renderDialogue();
        }

        function toggleCartAttachment() {
            const distToCart = playerMesh.position.distanceTo(cartMesh.position);
            if (distToCart < 12) {
                isCartAttached = !isCartAttached;
                document.getElementById('cart-status-text').innerText = isCartAttached ? 
                    "العربة متصلة وممسوكة! | اضغط [G] لترك العربة" : 
                    "العربة مفصولة | اقترب واضغط [G] لإمساك العربة";
            }
        }

        function triggerAction() {
            if (!document.getElementById('dialogue-container').classList.contains('hidden')) {
                nextDialogue();
                return;
            }

            // Mountain House Intro Interaction
            if (currentStage === GameStage.INTRO_HOUSE && playerMesh.position.distanceTo(houseGroup.position) < 25) {
                startDialogueSequence('INTRO', () => {
                    currentStage = GameStage.DESCENT_TO_VILLAGE;
                    document.getElementById('objective-text').innerText = "انزل عبر الطريق الجبلي نحو القرية التجارية الضخمة";
                });
            }

            // Village Market Trading
            if (currentStage === GameStage.DESCENT_TO_VILLAGE && playerMesh.position.distanceTo(villageGroup.position) < 40) {
                currentStage = GameStage.VILLAGE_TRADE;
                startDialogueSequence('VILLAGE', () => {
                    goldCount = 30;
                    document.getElementById('gold-text').innerText = `${goldCount} قطعة`;
                    currentStage = GameStage.FOREST_RETURN;
                    document.getElementById('objective-text').innerText = "اصعد الجبل راجعاً للبيت عبر الطريق المظلم";
                });
            }
        }

        function startBearBattle() {
            currentStage = GameStage.BEAR_BATTLE;
            bearMesh.visible = true;
            document.getElementById('boss-hud').classList.remove('hidden');
            document.getElementById('objective-text').innerText = "اهزم الدب المفترس بالفأس!";
        }

        function attackBear() {
            if (bearHP <= 0) return;

            const dmg = Math.floor(Math.random() * 35) + 40;
            bearHP = Math.max(0, bearHP - dmg);
            
            document.getElementById('boss-hp-text').innerText = `${bearHP} / ${maxBearHP} HP`;
            document.getElementById('boss-hp-bar').style.width = `${(bearHP / maxBearHP) * 100}%`;

            if (bearHP <= 0) {
                bearMesh.visible = false;
                document.getElementById('boss-hud').classList.add('hidden');
                currentStage = GameStage.RETURN_DESTROYED_HOME;

                // Burn House Ruin
                houseGroup.visible = false;
                destroyedHouseGroup.visible = true;

                document.getElementById('objective-text').innerText = "تفقد البيت المدمر في القمة واسحب العائلة بالعربة!";
            }
        }

        function updatePlayerLogic(delta) {
            let speed = keys.Shift ? 28 : 15;
            let moveVector = new THREE.Vector3();

            if (keys.w || keys.ArrowUp) moveVector.z -= 1;
            if (keys.s || keys.ArrowDown) moveVector.z += 1;
            if (keys.a || keys.ArrowLeft) moveVector.x -= 1;
            if (keys.d || keys.ArrowRight) moveVector.x += 1;

            if (moveVector.length() > 0) {
                moveVector.normalize().multiplyScalar(speed * delta);
                playerMesh.position.add(moveVector);

                // Calculate Mountain Height Elevation for Player
                const distToPeak = Math.hypot(playerMesh.position.x + 150, playerMesh.position.z + 150);
                if (distToPeak < 140) {
                    playerMesh.position.y = Math.cos(distToPeak / 140 * Math.PI) * 45 + 45;
                } else {
                    playerMesh.position.y = 0;
                }

                // If Cart is Attached, Drag Cart Behind Player
                if (isCartAttached) {
                    const targetCartPos = playerMesh.position.clone().sub(moveVector.clone().normalize().multiplyScalar(6));
                    cartMesh.position.lerp(targetCartPos, 0.2);
                    cartMesh.position.y = playerMesh.position.y;
                }
            }

            // Camera Follows Player
            camera.position.set(playerMesh.position.x, playerMesh.position.y + 22, playerMesh.position.z + 32);
            camera.lookAt(playerMesh.position);

            // Trigger Bear Attack Encounter on Mountain Path Return
            if (currentStage === GameStage.FOREST_RETURN && playerMesh.position.distanceTo(bearMesh.position) < 30) {
                startBearBattle();
            }

            // Trigger Tragedy Discovery at Ruined House
            if (currentStage === GameStage.RETURN_DESTROYED_HOME && playerMesh.position.distanceTo(destroyedHouseGroup.position) < 25) {
                currentStage = GameStage.TRAGEDY_DISCOVERY;
                startDialogueSequence('TRAGEDY', () => {
                    currentStage = GameStage.CART_RUSH_HOSPITAL;
                    document.getElementById('objective-text').innerText = "امسك العربة [G] وانزل بها سريعاً لمستشفى القرية!";
                });
            }

            // Hospital Arrival Transition
            if (currentStage === GameStage.CART_RUSH_HOSPITAL && playerMesh.position.distanceTo(hospitalGroup.position) < 30) {
                currentStage = GameStage.HOSPITAL_DOCTOR;
                startDialogueSequence('HOSPITAL', () => {
                    currentStage = GameStage.DARK_MAGIC_END;
                    document.getElementById('objective-text').innerText = "اكتمل الفصل الأول - استيقاظ القوة المظلمة لشينرا";
                });
            }
        }

        function startGame() {
            document.getElementById('full-screen-overlay').classList.add('opacity-0', 'pointer-events-none');
            currentStage = GameStage.INTRO_HOUSE;
        }

        function onWindowResize() {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        }

        function animate() {
            requestAnimationFrame(animate);
            const delta = clock.getDelta();

            if (currentStage !== GameStage.TITLE && currentStage !== GameStage.DARK_MAGIC_END) {
                updatePlayerLogic(delta);
            }

            renderer.render(scene, camera);
        }

        window.onload = function() {
            init3D();
            animate();
        };
    </script>
</body>
</html>
