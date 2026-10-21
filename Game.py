import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_page_title="Chronicles of Shinra - Chapter 1",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

game_html = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Shinra RPG - Chapter 1: The Tragedy of 792 AD</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- FontAwesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@700;900&family=Press+Start+2P&family=Tajawal:wght@400;700;900&display=swap" rel="stylesheet">

    <style>
        * {
            user-select: none;
            -webkit-user-select: none;
            touch-action: manipulation;
        }
        body {
            background-color: #05070d;
            color: #f1f5f9;
            font-family: 'Tajawal', sans-serif;
            overflow: hidden;
            margin: 0;
            padding: 0;
        }
        .font-cinzel { font-family: 'Cinzel', serif; }
        .font-pixel { font-family: 'Press Start 2P', monospace; }

        #game-container {
            position: relative;
            box-shadow: 0 0 40px rgba(0, 0, 0, 0.95), 0 0 20px rgba(239, 68, 68, 0.25);
        }

        canvas {
            display: block;
            image-rendering: pixelated;
            background: #000;
        }

        /* Screen Shake Effect */
        .shake {
            animation: shake 0.4s cubic-bezier(.36,.07,.19,.97) both infinite;
        }

        @keyframes shake {
            10%, 90% { transform: translate3d(-3px, 0, 0); }
            20%, 80% { transform: translate3d(5px, 0, 0); }
            30%, 50%, 70% { transform: translate3d(-7px, 0, 0); }
            40%, 60% { transform: translate3d(7px, 0, 0); }
        }

        /* Dark Aura Particle Glow */
        .dark-aura-active {
            box-shadow: inset 0 0 80px #000, 0 0 50px #991b1b;
            animation: pulse-aura 1.2s ease-in-out infinite alternate;
        }

        @keyframes pulse-aura {
            from { filter: drop-shadow(0 0 15px #dc2626); }
            to { filter: drop-shadow(0 0 35px #000000); }
        }
    </style>
</head>
<body class="h-screen w-screen flex flex-col justify-between items-center p-2 md:p-4 select-none">

    <!-- Top Navigation Header -->
    <header class="w-full max-w-5xl flex justify-between items-center bg-slate-900/90 border border-slate-800 px-4 py-2 rounded-xl shadow-lg z-20">
        <div class="flex items-center space-x-3 space-x-reverse">
            <span class="text-red-500 font-extrabold text-xl font-cinzel tracking-wider"><i class="fa-solid fa-dragon ml-2"></i>SHINRA RPG</span>
            <span class="text-xs bg-red-950 text-red-400 px-2.5 py-1 rounded-md border border-red-800 font-bold">الفصل 1: سنة 792 م</span>
        </div>
        <div class="flex items-center space-x-3 space-x-reverse">
            <div id="scene-tag" class="text-xs bg-slate-800 text-amber-400 px-3 py-1 rounded-lg border border-slate-700 font-bold flex items-center gap-2">
                <i class="fa-solid fa-location-dot"></i> <span id="current-location-text">بيت الجبل</span>
            </div>
            <button onclick="toggleAudio()" id="btn-audio" class="text-xs bg-slate-800 hover:bg-slate-700 text-slate-300 p-2 rounded-lg border border-slate-700 transition">
                <i class="fa-solid fa-volume-high text-emerald-400" id="audio-icon"></i>
            </button>
        </div>
    </header>

    <!-- Main Game Frame -->
    <main class="relative w-full max-w-5xl my-auto flex flex-col items-center justify-center">
        <div id="game-container" class="w-full aspect-[16/9] max-h-[72vh] bg-black rounded-2xl overflow-hidden border-2 border-slate-800 relative">
            
            <!-- Game Canvas -->
            <canvas id="gameCanvas" class="w-full h-full"></canvas>

            <!-- Visual Novel Story Overlay Dialog Box -->
            <div id="vn-overlay" class="absolute bottom-3 left-3 right-3 bg-slate-950/95 border-2 border-slate-700/80 rounded-xl p-3 md:p-4 text-white shadow-2xl flex flex-col md:flex-row items-center gap-4 hidden z-30 transition-all duration-300">
                <div id="vn-avatar-box" class="w-20 h-20 md:w-24 md:h-24 rounded-lg border-2 border-amber-600/60 bg-slate-900 flex-shrink-0 flex items-center justify-center overflow-hidden shadow-inner">
                    <div id="vn-avatar-sprite" class="w-full h-full"></div>
                </div>
                <div class="flex-1 w-full flex flex-col justify-between h-full">
                    <div>
                        <div class="flex justify-between items-center mb-1">
                            <span id="vn-speaker-name" class="font-bold text-amber-400 text-base md:text-lg tracking-wide">شينرا</span>
                            <span id="vn-speaker-info" class="text-xs text-slate-400 font-mono">العمر 9 | 142 سم</span>
                        </div>
                        <p id="vn-dialog-text" class="text-sm md:text-base text-slate-200 leading-relaxed min-h-[48px]">جاري تحميل الأحداث...</p>
                    </div>
                    <div class="flex justify-end mt-2">
                        <button id="vn-next-btn" onclick="advanceStory()" class="px-5 py-1.5 bg-amber-600 hover:bg-amber-500 active:scale-95 text-slate-950 text-xs font-black rounded-lg shadow-md transition flex items-center gap-2">
                            <span>متابعة</span>
                            <i class="fa-solid fa-chevron-left text-xs"></i>
                        </button>
                    </div>
                </div>
            </div>

            <!-- RPG Bear Battle Interface -->
            <div id="battle-overlay" class="absolute inset-0 bg-slate-950/95 p-4 flex flex-col justify-between hidden z-30">
                <div class="flex justify-between items-center bg-slate-900/90 p-3 rounded-xl border border-slate-800">
                    <div class="w-5/12">
                        <div class="flex justify-between text-xs font-bold mb-1">
                            <span class="text-cyan-400">شينرا (9 سنوات)</span>
                            <span id="shinra-hp-text" class="text-slate-300">1500 / 1500 HP</span>
                        </div>
                        <div class="w-full bg-slate-800 h-3 rounded-full overflow-hidden border border-slate-700">
                            <div id="shinra-hp-bar" class="bg-gradient-to-r from-emerald-500 to-teal-400 h-full w-full transition-all duration-300"></div>
                        </div>
                        <div class="text-[10px] text-slate-400 mt-1"><i class="fa-solid fa-axe text-amber-500 ml-1"></i> السلاح: فأس الحطاب الغامض</div>
                    </div>

                    <div class="text-red-500 font-pixel text-xs md:text-sm animate-pulse">VS</div>

                    <div class="w-5/12 text-left">
                        <div class="flex justify-between text-xs font-bold mb-1">
                            <span class="text-red-500">الدب الأحيائي الأحمر</span>
                            <span id="bear-hp-text" class="text-slate-300">500 / 500 HP</span>
                        </div>
                        <div class="w-full bg-slate-800 h-3 rounded-full overflow-hidden border border-slate-700">
                            <div id="bear-hp-bar" class="bg-gradient-to-r from-red-600 to-rose-400 h-full w-full transition-all duration-300 float-left"></div>
                        </div>
                        <div class="text-[10px] text-red-400 mt-1">مستوى التهديد: خطير جداً</div>
                    </div>
                </div>

                <!-- Central Arena Visual -->
                <div class="flex-1 my-2 relative flex items-center justify-around border border-slate-800/60 rounded-xl bg-slate-900/50 overflow-hidden">
                    <div id="battle-shinra" class="relative transition-transform duration-200">
                        <div class="w-28 h-28 bg-cyan-950/40 border-2 border-cyan-500/50 rounded-2xl flex items-center justify-center shadow-lg relative">
                            <svg class="w-20 h-20" viewBox="0 0 100 100">
                                <circle cx="50" cy="30" r="18" fill="#fca5a5"/>
                                <path d="M50 12 C 40 10, 35 25, 30 30 C 45 20, 55 20, 70 30 C 65 25, 60 10, 50 12 Z" fill="#334155"/>
                                <circle cx="43" cy="28" r="3" fill="#0284c7"/>
                                <circle cx="57" cy="28" r="3" fill="#0284c7"/>
                                <path d="M 30 48 L 70 48 L 65 90 L 35 90 Z" fill="#0284c7"/>
                                <line x1="70" y1="50" x2="85" y2="25" stroke="#78350f" stroke-width="4"/>
                                <path d="M 80 20 C 95 15, 95 35, 80 35 Z" fill="#94a3b8"/>
                            </svg>
                            <span class="absolute -top-3 bg-cyan-900 text-cyan-300 text-[10px] px-2 py-0.5 rounded border border-cyan-500">شينرا</span>
                        </div>
                    </div>

                    <div id="battle-bear" class="relative transition-transform duration-200">
                        <div class="w-32 h-32 bg-red-950/40 border-2 border-red-600/60 rounded-2xl flex items-center justify-center shadow-lg relative">
                            <svg class="w-24 h-24" viewBox="0 0 100 100">
                                <circle cx="50" cy="50" r="38" fill="#271c19"/>
                                <circle cx="25" cy="20" r="12" fill="#1c1311"/>
                                <circle cx="75" cy="20" r="12" fill="#1c1311"/>
                                <circle cx="38" cy="42" r="5" fill="#ef4444" class="animate-pulse"/>
                                <circle cx="62" cy="42" r="5" fill="#ef4444" class="animate-pulse"/>
                                <circle cx="39" cy="42" r="2" fill="#ffffff"/>
                                <circle cx="63" cy="42" r="2" fill="#ffffff"/>
                                <polygon points="40,65 44,75 48,65" fill="#ffffff"/>
                                <polygon points="52,65 56,75 60,65" fill="#ffffff"/>
                            </svg>
                            <span class="absolute -top-3 bg-red-950 text-red-400 text-[10px] px-2 py-0.5 rounded border border-red-700">الدب العملاق</span>
                        </div>
                    </div>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
                    <div id="battle-log" class="md:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-3 text-xs md:text-sm text-slate-300 h-24 overflow-y-auto leading-relaxed">
                        <p class="text-amber-400 font-bold">ظهر الدب المفترس ذو العينين الحمراوين! استعد للقتال بالفأس!</p>
                    </div>
                    <div class="flex flex-col gap-2">
                        <button onclick="executeBattleAction('attack')" class="w-full h-full py-3 bg-gradient-to-r from-red-600 to-rose-700 hover:from-red-500 hover:to-rose-600 active:scale-95 text-white font-bold rounded-xl border border-red-500 shadow-md transition flex items-center justify-center gap-2">
                            <i class="fa-solid fa-hand-fist text-lg"></i>
                            <span>ضربة الفأس (30-60 ضرر)</span>
                        </button>
                    </div>
                </div>
            </div>

            <!-- Mobile Controls Layer -->
            <div id="mobile-controls" class="absolute bottom-4 left-4 right-4 flex justify-between items-end pointer-events-none z-20 md:hidden">
                <div class="pointer-events-auto grid grid-cols-3 gap-1 w-32 h-32 bg-slate-950/70 p-1.5 rounded-2xl backdrop-blur-sm border border-slate-800">
                    <div></div>
                    <button id="btn-up" class="bg-slate-800/90 active:bg-amber-600 rounded-lg flex items-center justify-center text-white text-lg"><i class="fa-solid fa-chevron-up"></i></button>
                    <div></div>
                    <button id="btn-left" class="bg-slate-800/90 active:bg-amber-600 rounded-lg flex items-center justify-center text-white text-lg"><i class="fa-solid fa-chevron-left"></i></button>
                    <div class="bg-slate-900/50 rounded-lg flex items-center justify-center text-slate-600 text-xs font-mono">PAD</div>
                    <button id="btn-right" class="bg-slate-800/90 active:bg-amber-600 rounded-lg flex items-center justify-center text-white text-lg"><i class="fa-solid fa-chevron-right"></i></button>
                    <div></div>
                    <button id="btn-down" class="bg-slate-800/90 active:bg-amber-600 rounded-lg flex items-center justify-center text-white text-lg"><i class="fa-solid fa-chevron-down"></i></button>
                    <div></div>
                </div>

                <div class="pointer-events-auto flex flex-col gap-2">
                    <button id="btn-dash" class="w-14 h-14 bg-amber-600/90 active:bg-amber-500 text-slate-950 rounded-full flex flex-col items-center justify-center border-2 border-amber-400 shadow-lg text-xs font-black">
                        <i class="fa-solid fa-bolt text-sm"></i>
                        <span>ركض</span>
                    </button>
                    <button id="btn-action" class="w-16 h-16 bg-red-600/95 active:bg-red-500 text-white rounded-full flex flex-col items-center justify-center border-2 border-red-400 shadow-xl text-xs font-bold">
                        <i class="fa-solid fa-hand text-base"></i>
                        <span>تفاعل (E)</span>
                    </button>
                </div>
            </div>

            <!-- Objective Status & Gold Bar -->
            <div id="objective-banner" class="absolute top-3 right-3 bg-slate-950/85 border border-slate-800 px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-300 flex items-center gap-2 z-20 backdrop-blur-sm">
                <i class="fa-solid fa-compass text-amber-400"></i>
                <span id="objective-text">اقترب من المنزل للحديث مع العائلة.</span>
            </div>

            <div id="gold-banner" class="absolute top-3 left-3 bg-slate-950/85 border border-amber-800/80 px-3 py-1.5 rounded-lg text-xs font-bold text-amber-400 flex items-center gap-2 z-20 backdrop-blur-sm">
                <i class="fa-solid fa-coins text-amber-400"></i>
                <span id="gold-amount">0 قطعة ذهب</span>
            </div>

        </div>
    </main>

    <!-- Desktop Controls Instructions Bar -->
    <footer class="w-full max-w-5xl bg-slate-900/90 border border-slate-800 rounded-xl p-2.5 text-xs text-slate-400 flex flex-wrap justify-between items-center gap-2 z-20">
        <div class="flex items-center gap-4">
            <span><strong class="text-slate-200">التحكم:</strong> أسهم الاتجاهات / WASD للتحرك</span>
            <span><strong class="text-slate-200">Shift:</strong> الجري بسرعة 40 كم/س</span>
            <span><strong class="text-slate-200">Space / E:</strong> التفاعل / التجارة / نقل العائلة</span>
        </div>
        <div class="text-slate-500 font-mono text-[11px]">
            HTML5 Visual Scene Engine • Shinra Chapter 1
        </div>
    </footer>

    <!-- MAIN GAME ENGINE JAVASCRIPT LOGIC -->
    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');

        const CANVAS_WIDTH = 960;
        const CANVAS_HEIGHT = 540;
        canvas.width = CANVAS_WIDTH;
        canvas.height = CANVAS_HEIGHT;

        let audioCtx = null;
        let soundEnabled = true;

        function initAudio() {
            if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        }

        function playTone(freq, duration = 0.1, type = 'sine') {
            if (!soundEnabled) return;
            try {
                initAudio();
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.type = type;
                osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
                gain.gain.setValueAtTime(0.1, audioCtx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + duration);
                osc.connect(gain);
                gain.connect(audioCtx.destination);
                osc.start();
                osc.stop(audioCtx.currentTime + duration);
            } catch(e){}
        }

        function toggleAudio() {
            soundEnabled = !soundEnabled;
            document.getElementById('audio-icon').className = soundEnabled ? 
                "fa-solid fa-volume-high text-emerald-400" : "fa-solid fa-volume-xmark text-red-400";
        }

        const SCENARIOS = {
            TITLE_792: 0,
            MOUNTAIN_HOME_INTRO: 1,
            WALK_TO_MARKET_PATH: 2,
            VILLAGE_MARKET_TRADE: 3,
            FOREST_NIGHT_RETURN: 4,
            BEAR_BATTLE: 5,
            COOKING_BEAR_MEAT: 6,
            RUSH_HOME_DESTROYED: 7,
            TRAGEDY_DISCOVERY: 8,
            LOADING_FAMILY_CART: 9,
            RUSH_TO_HOSPITAL_SPEED: 10,
            DOCTOR_HOSPITAL_SCENE: 11,
            DARK_MAGIC_AWAKENING: 12
        };

        let gameState = {
            step: SCENARIOS.TITLE_792,
            gold: 0,
            shinraHP: 1500,
            maxShinraHP: 1500,
            bearHP: 500,
            maxBearHP: 500,
            isDashing: false,
            carriedCount: 0,
            familyLoaded: { yura: false, soho: false, maki: false },
            titleTimer: 0,
            currentLocation: "بيت الجبل"
        };

        const player = {
            x: 180,
            y: 320,
            width: 28,
            height: 28,
            speed: 3.2,
            dashMultiplier: 2.2,
            isMoving: false
        };

        const keys = { up: false, down: false, left: false, right: false, dash: false };

        const CHARACTERS = {
            shinra: { name: "شينرا", info: "العمر 9 سنوات | 142 سم", color: "#38bdf8" },
            yura: { name: "يورا (الأب)", info: "العمر 54 سنة | 178 سم", color: "#f59e0b" },
            soho: { name: "سوهو (الأخ)", info: "العمر 18 سنة | 182 سم", color: "#22c55e" },
            maki: { name: "ماكي (الأخت)", info: "العمر 13 سنة | 154 سم", color: "#ef4444" },
            merchant: { name: "تاجر القرية", info: "سوق جبل شينرا", color: "#fbbf24" },
            yuno: { name: "الطبيب يونو", info: "طبيب القرية (34 سنة)", color: "#14b8a6" },
            narrator: { name: "الراوي", info: "حقبة 792 م", color: "#a855f7" }
        };

        const DIALOGUES = {
            INTRO: [
                { speaker: 'yura', text: "ماكي..." },
                { speaker: 'maki', text: "أبي! ما الذي يحدث لك؟!" },
                { speaker: 'yura', text: "أحضري لي دواء الحمي... بسرعة." },
                { speaker: 'maki', text: "تفضل يا أبي، اشربه الآن فوراً!" },
                { speaker: 'narrator', text: "تصل عربة خيول إلى أعلى الجبل أمام منزل العائلة..." },
                { speaker: 'soho', text: "أهلاً ماكي! أهلاً أبي! لقد عدتُ أخيراً من رحلة التداول!" },
                { speaker: 'maki', text: "أهلاً بعودتك يا سوهو! ولكن... أين شينرا الصغير؟!" },
                { speaker: 'shinra', text: "أنا هنا بالأسفل!" },
                { speaker: 'narrator', text: "*ماكي تضرب شينرا بغضب على رأسه!*" },
                { speaker: 'shinra', text: "آخ! لماذا ضربتيني؟!" },
                { speaker: 'maki', text: "ظننتك ضعت في الغابة! ماذا كنت تفعل مع سوهو؟" },
                { speaker: 'soho', text: "لقد تسلل داخل عربتي البارحة لأنه كان فضولياً!" },
                { speaker: 'shinra', text: "ولكني ساعدته! باعت زهور اللوتس بـ 30 قطعة ذهبية كاملة!" },
                { speaker: 'yura', text: "*يبتسم بحنان رغم مرضه الشديد*" },
                { speaker: 'narrator', text: "بعد مرور أسبوع كامل..." },
                { speaker: 'soho', text: "أنا مرهق جداً اليوم... لا أستطيع الذهاب للسوق." },
                { speaker: 'maki', text: "ومن سينزل لقرية السوق لتداول البضائع اليوم إذن؟!" },
                { speaker: 'shinra', text: "أنا سأذهب! تعلمت كيف أحسب الأسعار وأقنع التجار. أعطني البضائع والفأس للحماية!" }
            ],
            TRADING: [
                { speaker: 'merchant', text: "أهلاً بالبضائع! انتظر... أنت أخو سوهو الصغير! أين سوهو اليوم؟" },
                { speaker: 'shinra', text: "سوهو متعب اليوم، لذا جئت أنا لأبيع البضائع للقرية!" },
                { speaker: 'merchant', text: "ممتاز! كم سعر 1 كيلو من هذا القماش الفاخر؟" },
                { speaker: 'shinra', text: "15 قطعة ذهبية!" },
                { speaker: 'merchant', text: "هذا غالي جداً يا صغيري!" },
                { speaker: 'shinra', text: "مستحيل! أخي يبيع بأرخص سعر في السوق. السعر الأصلي 20 قطعة! كما أننا أحضرنا جلود الدببة واللوتس النادرة!" },
                { speaker: 'merchant', text: "ههههه! أنت تاجر ذكي ومقنع مثل أخيك! اتبعني وسآخذ كل البضائع بـ 30 قطعة ذهب!" },
                { speaker: 'shinra', text: "رائع! حصلت على 30 قطعة ذهب! حل الليل... يجب أن أسرع بالعودة للبيت عبر الغابة." }
            ],
            BEAR_COOK: [
                { speaker: 'shinra', text: "هذا الدب كان قوي للغاية! ولكني قطعت رأسه بالفأس. حان وقت شواء لحمه على النار!" },
                { speaker: 'narrator', text: "*شينرا يشعل النار ويشوي لحم الدب اللذيذ ويستعيد كامل طاقته...*" },
                { speaker: 'shinra', text: "ممم! طعمه أسطوري! ولكن الوقت تأخر... يجب أن أركض للبيت الآن!" }
            ],
            TRAGEDY_ARRIVE: [
                { speaker: 'narrator', text: "وهنا تبدأ الفاجعة الكبرى في حياة شينرا..." },
                { speaker: 'shinra', text: "مـ... ما هذا الذي أراه؟! المنزل مدمر ومحترق بالكامل!!" },
                { speaker: 'shinra', text: "سوهو؟! ماكي؟! أبتي؟! أرجوكم ردوا علي!!" },
                { speaker: 'shinra', text: "سوهو وماكي لا يتنفسان... وأبي في حالة غيبوبة خطيرة! يجب أن أحملهم على العربة فوراً وأركض بسرعة 40 كم/س للمستشفى!" }
            ],
            HOSPITAL: [
                { speaker: 'yuno', text: "أهلاً بك يا بني... أنا الطبيب يونو. يؤسفني جداً أن أخبرك بهذه الفاجعة." },
                { speaker: 'yuno', text: "أخوك سوهو وأختك ماكي... قد فارقا الحياة فوراً. أما والدك يورا فهو على قيد الحياة ولكنه دخل في غيبوبة عميقة قد يستيقظ منها بعد 1 إلى 3 سنوات..." },
                { speaker: 'shinra', text: "ماذا... سوهو وماكي... ماتوا؟!!" },
                { speaker: 'narrator', text: "*شينرا يصرخ بصرخة حزن مأساوية تهز الأركان! وهالة سحرية سوداء مرعبة تتصاعد منه بغضب...*" }
            ]
        };

        let currentDialogList = [];
        let currentDialogStep = 0;
        let onDialogCompleteCallback = null;

        function startDialogue(dialogKey, onComplete) {
            currentDialogList = DIALOGUES[dialogKey];
            currentDialogStep = 0;
            onDialogCompleteCallback = onComplete;
            document.getElementById('vn-overlay').classList.remove('hidden');
            renderDialogStep();
        }

        function renderDialogStep() {
            if (currentDialogStep >= currentDialogList.length) {
                document.getElementById('vn-overlay').classList.add('hidden');
                if (onDialogCompleteCallback) onDialogCompleteCallback();
                return;
            }

            const item = currentDialogList[currentDialogStep];
            const charData = CHARACTERS[item.speaker] || { name: item.speaker, info: "", color: "#ffffff" };

            document.getElementById('vn-speaker-name').innerText = charData.name;
            document.getElementById('vn-speaker-name').style.color = charData.color;
            document.getElementById('vn-speaker-info').innerText = charData.info;
            document.getElementById('vn-dialog-text').innerText = item.text;

            document.getElementById('vn-avatar-sprite').innerHTML = generateAvatarSVG(item.speaker);
            playTone(450, 0.04, 'triangle');
        }

        function advanceStory() {
            currentDialogStep++;
            renderDialogStep();
        }

        function generateAvatarSVG(speaker) {
            switch(speaker) {
                case 'shinra':
                    return `<svg viewBox="0 0 100 100" class="w-full h-full"><rect width="100" height="100" fill="#0f172a"/><circle cx="50" cy="45" r="25" fill="#fca5a5"/><path d="M50 15 C 30 15, 25 35, 20 45 C 40 30, 60 30, 80 45 C 75 35, 70 15, 50 15 Z" fill="#334155"/><circle cx="40" cy="42" r="3.5" fill="#0284c7"/><circle cx="60" cy="42" r="3.5" fill="#0284c7"/></svg>`;
                case 'soho':
                    return `<svg viewBox="0 0 100 100" class="w-full h-full"><rect width="100" height="100" fill="#064e3b"/><circle cx="50" cy="40" r="28" fill="#fde047"/><path d="M50 10 C 25 10, 20 35, 15 45 C 40 25, 60 25, 85 45 Z" fill="#854d0e"/><circle cx="38" cy="38" r="4" fill="#15803d"/><circle cx="62" cy="38" r="4" fill="#15803d"/></svg>`;
                case 'maki':
                    return `<svg viewBox="0 0 100 100" class="w-full h-full"><rect width="100" height="100" fill="#450a0a"/><circle cx="50" cy="45" r="24" fill="#fca5a5"/><path d="M 20 20 L 80 20 L 85 80 L 15 80 Z" fill="#991b1b"/><circle cx="40" cy="42" r="3.5" fill="#dc2626"/></svg>`;
                case 'yura':
                    return `<svg viewBox="0 0 100 100" class="w-full h-full"><rect width="100" height="100" fill="#451a03"/><circle cx="50" cy="45" r="25" fill="#fef08a"/><path d="M25 45 C 25 75, 75 75, 75 45 Z" fill="#d1d5db"/><circle cx="40" cy="40" r="3" fill="#78350f"/><circle cx="60" cy="40" r="3" fill="#78350f"/></svg>`;
                case 'merchant':
                    return `<svg viewBox="0 0 100 100" class="w-full h-full"><rect width="100" height="100" fill="#78350f"/><circle cx="50" cy="45" r="25" fill="#fdba74"/><rect x="25" y="15" width="50" height="15" fill="#d97706"/></svg>`;
                case 'yuno':
                    return `<svg viewBox="0 0 100 100" class="w-full h-full"><rect width="100" height="100" fill="#042f2e"/><circle cx="50" cy="45" r="25" fill="#fed7aa"/><rect x="20" y="15" width="60" height="20" fill="#0f766e"/></svg>`;
                default:
                    return `<svg viewBox="0 0 100 100" class="w-full h-full"><rect width="100" height="100" fill="#1e293b"/><circle cx="50" cy="50" r="25" fill="#64748b"/></svg>`;
            }
        }

        window.addEventListener('keydown', (e) => {
            initAudio();
            if (e.key === 'ArrowUp' || e.key === 'w' || e.key === 'W') keys.up = true;
            if (e.key === 'ArrowDown' || e.key === 's' || e.key === 'S') keys.down = true;
            if (e.key === 'ArrowLeft' || e.key === 'a' || e.key === 'A') keys.left = true;
            if (e.key === 'ArrowRight' || e.key === 'd' || e.key === 'D') keys.right = true;
            if (e.key === 'Shift') keys.dash = true;
            if (e.key === ' ' || e.key === 'e' || e.key === 'E') triggerInteraction();
        });

        window.addEventListener('keyup', (e) => {
            if (e.key === 'ArrowUp' || e.key === 'w' || e.key === 'W') keys.up = false;
            if (e.key === 'ArrowDown' || e.key === 's' || e.key === 'S') keys.down = false;
            if (e.key === 'ArrowLeft' || e.key === 'a' || e.key === 'A') keys.left = false;
            if (e.key === 'ArrowRight' || e.key === 'd' || e.key === 'D') keys.right = false;
            if (e.key === 'Shift') keys.dash = false;
        });

        function setupTouchControls() {
            const bindTouch = (id, keyName) => {
                const el = document.getElementById(id);
                if (!el) return;
                el.addEventListener('touchstart', (e) => { e.preventDefault(); initAudio(); keys[keyName] = true; });
                el.addEventListener('touchend', (e) => { e.preventDefault(); keys[keyName] = false; });
            };
            bindTouch('btn-up', 'up');
            bindTouch('btn-down', 'down');
            bindTouch('btn-left', 'left');
            bindTouch('btn-right', 'right');
            bindTouch('btn-dash', 'dash');

            document.getElementById('btn-action').addEventListener('touchstart', (e) => {
                e.preventDefault();
                initAudio();
                triggerInteraction();
            });
        }

        function triggerInteraction() {
            if (!document.getElementById('vn-overlay').classList.contains('hidden')) {
                advanceStory();
                return;
            }

            if (gameState.step === SCENARIOS.MOUNTAIN_HOME_INTRO && Math.hypot(player.x - 240, player.y - 200) < 70) {
                startDialogue('INTRO', () => {
                    gameState.step = SCENARIOS.WALK_TO_MARKET_PATH;
                    document.getElementById('objective-text').innerText = "انزل عبر الطريق نحو سوق القرية للتداول!";
                });
            }

            if (gameState.step === SCENARIOS.LOADING_FAMILY_CART) {
                if (!gameState.familyLoaded.yura && Math.hypot(player.x - 220, player.y - 240) < 55) {
                    gameState.familyLoaded.yura = true;
                    gameState.carriedCount++;
                    playTone(650, 0.12);
                } else if (!gameState.familyLoaded.soho && Math.hypot(player.x - 280, player.y - 280) < 55) {
                    gameState.familyLoaded.soho = true;
                    gameState.carriedCount++;
                    playTone(650, 0.12);
                } else if (!gameState.familyLoaded.maki && Math.hypot(player.x - 170, player.y - 300) < 55) {
                    gameState.familyLoaded.maki = true;
                    gameState.carriedCount++;
                    playTone(650, 0.12);
                }

                if (gameState.carriedCount >= 3) {
                    gameState.step = SCENARIOS.RUSH_TO_HOSPITAL_SPEED;
                    document.getElementById('objective-text').innerText = "اركض بسرعة 40 كم/س للمستشفى! اضغط Shift للجري!";
                }
            }
        }

        function startBearBattle() {
            gameState.step = SCENARIOS.BEAR_BATTLE;
            gameState.bearHP = 500;
            document.getElementById('battle-overlay').classList.remove('hidden');
            updateBattleUI();
        }

        function updateBattleUI() {
            document.getElementById('shinra-hp-text').innerText = `${gameState.shinraHP} / ${gameState.maxShinraHP} HP`;
            document.getElementById('shinra-hp-bar').style.width = `${(gameState.shinraHP / gameState.maxShinraHP) * 100}%`;

            document.getElementById('bear-hp-text').innerText = `${gameState.bearHP} / ${gameState.maxBearHP} HP`;
            document.getElementById('bear-hp-bar').style.width = `${(gameState.bearHP / gameState.maxBearHP) * 100}%`;
        }

        function appendBattleLog(msg, colorClass = "text-slate-300") {
            const log = document.getElementById('battle-log');
            log.innerHTML += `<p class="${colorClass} my-0.5">${msg}</p>`;
            log.scrollTop = log.scrollHeight;
        }

        function executeBattleAction(action) {
            if (gameState.bearHP <= 0 || gameState.shinraHP <= 0) return;

            if (action === 'attack') {
                const dmg = Math.floor(Math.random() * 31) + 35;
                gameState.bearHP = Math.max(0, gameState.bearHP - dmg);
                
                playTone(280, 0.15, 'sawtooth');
                animateHit('battle-bear');
                appendBattleLog(` يضرب شينرا بفأسه بقوة مسبباً <strong class="text-amber-400">${dmg} ضرر</strong>!`);
                updateBattleUI();

                if (gameState.bearHP <= 0) {
                    appendBattleLog(` تم القضاء على الدب العملاق بنجاح!`, "text-emerald-400 font-bold");
                    setTimeout(() => {
                        document.getElementById('battle-overlay').classList.add('hidden');
                        gameState.step = SCENARIOS.COOKING_BEAR_MEAT;
                        startDialogue('BEAR_COOK', () => {
                            gameState.shinraHP = gameState.maxShinraHP;
                            gameState.step = SCENARIOS.RUSH_HOME_DESTROYED;
                            document.getElementById('objective-text').innerText = "عد مسرعاً إلى بيت العائلة أعلى الجبل!";
                        });
                    }, 1200);
                    return;
                }

                setTimeout(() => {
                    const bearDmg = Math.floor(Math.random() * 35) + 40;
                    gameState.shinraHP = Math.max(0, gameState.shinraHP - bearDmg);
                    playTone(130, 0.2, 'square');
                    animateHit('battle-shinra');
                    appendBattleLog(` يهاجم الدب بمخالبه ويسبب لشينرا <strong class="text-red-400">${bearDmg} ضرر</strong>!`);
                    updateBattleUI();
                }, 500);
            }
        }

        function animateHit(id) {
            const el = document.getElementById(id);
            el.classList.add('shake');
            setTimeout(() => el.classList.remove('shake'), 350);
        }

        function drawMountainHomeScene(isDestroyed = false) {
            gameState.currentLocation = isDestroyed ? "البيت المحترق (الفاجعة)" : "بيت العائلة (الجبل)";

            ctx.fillStyle = isDestroyed ? '#1c0a0a' : '#0f172a';
            ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);

            ctx.fillStyle = isDestroyed ? '#291d18' : '#334155';
            ctx.beginPath();
            ctx.moveTo(0, 260); ctx.lineTo(CANVAS_WIDTH, 360); ctx.lineTo(CANVAS_WIDTH, 540); ctx.lineTo(0, 540);
            ctx.fill();

            ctx.fillStyle = isDestroyed ? '#1c1310' : '#78350f';
            ctx.beginPath();
            ctx.moveTo(100, 540); ctx.lineTo(240, 260); ctx.lineTo(340, 260); ctx.lineTo(220, 540);
            ctx.fill();

            ctx.fillStyle = isDestroyed ? '#1c1917' : '#542d12';
            ctx.fillRect(180, 140, 160, 120);

            ctx.fillStyle = isDestroyed ? '#0c0a09' : '#991b1b';
            ctx.beginPath();
            ctx.moveTo(160, 140); ctx.lineTo(260, 70); ctx.lineTo(360, 140);
            ctx.fill();

            ctx.fillStyle = isDestroyed ? '#000000' : '#78350f';
            ctx.fillRect(240, 200, 35, 60);

            if (!isDestroyed) {
                ctx.fillStyle = 'rgba(203, 213, 225, 0.3)';
                ctx.beginPath(); ctx.arc(320, 50, 12, 0, Math.PI*2); ctx.fill();
                ctx.beginPath(); ctx.arc(330, 35, 18, 0, Math.PI*2); ctx.fill();

                ctx.fillStyle = '#f59e0b'; ctx.beginPath(); ctx.arc(220, 240, 10, 0, Math.PI*2); ctx.fill();
                ctx.fillStyle = '#22c55e'; ctx.beginPath(); ctx.arc(280, 235, 12, 0, Math.PI*2); ctx.fill();
                ctx.fillStyle = '#ef4444'; ctx.beginPath(); ctx.arc(170, 245, 9, 0, Math.PI*2); ctx.fill();

                ctx.fillStyle = '#fbbf24'; ctx.font = 'bold 12px Tajawal';
                ctx.fillText("اضغط E للحديث مع العائلة", 200, 120);
            } else {
                ctx.fillStyle = '#ef4444';
                ctx.fillRect(200, 180, 15, 25); ctx.fillRect(280, 160, 20, 30);

                if (!gameState.familyLoaded.yura) {
                    ctx.fillStyle = '#f59e0b'; ctx.fillRect(220, 240, 22, 10);
                    ctx.fillStyle = '#fff'; ctx.font = '10px Tajawal'; ctx.fillText("يورا", 220, 235);
                }
                if (!gameState.familyLoaded.soho) {
                    ctx.fillStyle = '#22c55e'; ctx.fillRect(280, 280, 26, 10);
                    ctx.fillStyle = '#fff'; ctx.font = '10px Tajawal'; ctx.fillText("سوهو", 280, 275);
                }
                if (!gameState.familyLoaded.maki) {
                    ctx.fillStyle = '#ef4444'; ctx.fillRect(170, 300, 20, 10);
                    ctx.fillStyle = '#fff'; ctx.font = '10px Tajawal'; ctx.fillText("ماكي", 170, 295);
                }

                ctx.fillStyle = '#b45309'; ctx.fillRect(360, 280, 50, 35);
                ctx.fillStyle = '#f59e0b'; ctx.font = 'bold 11px Tajawal';
                ctx.fillText(`العربة (${gameState.carriedCount}/3)`, 355, 270);
            }
        }

        function drawVillageMarketScene() {
            gameState.currentLocation = "قرية التداول والأسواق";

            ctx.fillStyle = '#14532d';
            ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);

            ctx.fillStyle = '#a16207';
            ctx.fillRect(0, 220, CANVAS_WIDTH, 120);

            for(let i=60; i<CANVAS_WIDTH; i+=220) {
                ctx.fillStyle = '#78350f';
                ctx.fillRect(i, 100, 120, 90);
                ctx.fillStyle = i % 400 === 0 ? '#dc2626' : '#0284c7';
                ctx.beginPath();
                ctx.moveTo(i-10, 100); ctx.lineTo(i+60, 50); ctx.lineTo(i+130, 100); ctx.fill();

                ctx.fillStyle = '#fbbf24';
                ctx.beginPath(); ctx.arc(i+60, 200, 11, 0, Math.PI*2); ctx.fill();
            }

            ctx.fillStyle = '#f59e0b';
            ctx.font = 'bold 14px Tajawal';
            ctx.fillText("← البوابة للعودة للغابة", 40, 380);
        }

        function drawDarkForestScene() {
            gameState.currentLocation = "الغابة المظلمة ليلاً";

            ctx.fillStyle = '#022c22';
            ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);

            ctx.fillStyle = '#1c1917';
            ctx.fillRect(0, 230, CANVAS_WIDTH, 100);

            for(let i=20; i<CANVAS_WIDTH; i+=90) {
                ctx.fillStyle = '#064e3b';
                ctx.beginPath(); ctx.arc(i+30, 110, 45, 0, Math.PI*2); ctx.fill();
                ctx.beginPath(); ctx.arc(i+30, 430, 45, 0, Math.PI*2); ctx.fill();

                ctx.fillStyle = '#451a03';
                ctx.fillRect(i+22, 140, 16, 50);
                ctx.fillRect(i+22, 360, 16, 50);
            }
        }

        function drawHospitalScene() {
            gameState.currentLocation = "مستشفى قرية شينرا";

            ctx.fillStyle = '#0f766e';
            ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);

            ctx.fillStyle = '#134e4a';
            ctx.fillRect(0, 0, CANVAS_WIDTH, 140);

            ctx.fillStyle = '#f8fafc';
            ctx.fillRect(150, 200, 100, 60);
            ctx.fillRect(350, 200, 100, 60);

            ctx.fillStyle = '#14b8a6';
            ctx.beginPath(); ctx.arc(500, 280, 14, 0, Math.PI*2); ctx.fill();
            ctx.fillStyle = '#fff'; ctx.font = 'bold 12px Tajawal'; ctx.fillText("الطبيب يونو", 475, 255);
        }

        function updatePlayerLogic() {
            let moveSpeed = player.speed;
            if (keys.dash) {
                moveSpeed *= player.dashMultiplier;
                gameState.isDashing = true;
            } else {
                gameState.isDashing = false;
            }

            let dx = 0, dy = 0;
            if (keys.up) dy -= moveSpeed;
            if (keys.down) dy += moveSpeed;
            if (keys.left) dx -= moveSpeed;
            if (keys.right) dx += moveSpeed;

            if (dx !== 0 || dy !== 0) {
                player.x += dx; player.y += dy;
                player.isMoving = true;
                player.x = Math.max(30, Math.min(CANVAS_WIDTH - 40, player.x));
                player.y = Math.max(30, Math.min(CANVAS_HEIGHT - 40, player.y));
            } else {
                player.isMoving = false;
            }

            if (gameState.step === SCENARIOS.WALK_TO_MARKET_PATH && player.x > CANVAS_WIDTH - 60) {
                player.x = 80;
                gameState.step = SCENARIOS.VILLAGE_MARKET_TRADE;
                startDialogue('TRADING', () => {
                    gameState.gold = 30;
                    document.getElementById('gold-amount').innerText = `${gameState.gold} قطعة ذهب`;
                    gameState.step = SCENARIOS.FOREST_NIGHT_RETURN;
                    document.getElementById('objective-text').innerText = "عد للبيت عبر الغابة المظلمة ليلاً!";
                });
            } else if (gameState.step === SCENARIOS.FOREST_NIGHT_RETURN && player.x > 450) {
                startBearBattle();
            } else if (gameState.step === SCENARIOS.RUSH_HOME_DESTROYED && player.x < 100) {
                gameState.step = SCENARIOS.TRAGEDY_DISCOVERY;
                startDialogue('TRAGEDY_ARRIVE', () => {
                    gameState.step = SCENARIOS.LOADING_FAMILY_CART;
                    document.getElementById('objective-text').innerText = "اقترب من جثث العائلة واضغط E لنقلهم للعربة!";
                });
            } else if (gameState.step === SCENARIOS.RUSH_TO_HOSPITAL_SPEED && player.x > CANVAS_WIDTH - 70) {
                player.x = 100;
                gameState.step = SCENARIOS.DOCTOR_HOSPITAL_SCENE;
                startDialogue('HOSPITAL', () => {
                    gameState.step = SCENARIOS.DARK_MAGIC_AWAKENING;
                    document.getElementById('game-container').classList.add('shake', 'dark-aura-active');
                });
            }

            document.getElementById('current-location-text').innerText = gameState.currentLocation;
        }

        function renderScene() {
            ctx.clearRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);

            if (gameState.step === SCENARIOS.TITLE_792) {
                ctx.fillStyle = '#000000'; ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
                ctx.fillStyle = '#ef4444'; ctx.font = 'bold 58px Cinzel'; ctx.textAlign = 'center';
                ctx.fillText('792 AD', CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2 - 10);
                ctx.fillStyle = '#94a3b8'; ctx.font = '18px Tajawal';
                ctx.fillText('عصر الفرسان، السحر، والفاجعة المأساوية', CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2 + 40);

                gameState.titleTimer++;
                if (gameState.titleTimer > 120) {
                    gameState.step = SCENARIOS.MOUNTAIN_HOME_INTRO;
                }
                return;
            }

            if (gameState.step === SCENARIOS.DARK_MAGIC_AWAKENING) {
                ctx.fillStyle = '#000000'; ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
                ctx.fillStyle = '#dc2626'; ctx.font = 'bold 50px Cinzel'; ctx.textAlign = 'center';
                ctx.fillText('THE END', CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2 - 20);
                ctx.fillStyle = '#f59e0b'; ctx.font = '20px Tajawal';
                ctx.fillText('اكتمل الفصل الأول • استيقاظ السحر الأسود لشينرا', CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2 + 35);
                return;
            }

            switch(gameState.step) {
                case SCENARIOS.MOUNTAIN_HOME_INTRO:
                case SCENARIOS.WALK_TO_MARKET_PATH:
                    drawMountainHomeScene(false);
                    break;
                case SCENARIOS.VILLAGE_MARKET_TRADE:
                    drawVillageMarketScene();
                    break;
                case SCENARIOS.FOREST_NIGHT_RETURN:
                case SCENARIOS.COOKING_BEAR_MEAT:
                    drawDarkForestScene();
                    break;
                case SCENARIOS.RUSH_HOME_DESTROYED:
                case SCENARIOS.TRAGEDY_DISCOVERY:
                case SCENARIOS.LOADING_FAMILY_CART:
                case SCENARIOS.RUSH_TO_HOSPITAL_SPEED:
                    drawMountainHomeScene(true);
                    break;
                case SCENARIOS.DOCTOR_HOSPITAL_SCENE:
                    drawHospitalScene();
                    break;
            }

            ctx.fillStyle = '#38bdf8';
            ctx.beginPath(); ctx.arc(player.x, player.y, 14, 0, Math.PI * 2); ctx.fill();

            ctx.fillStyle = '#334155';
            ctx.beginPath(); ctx.arc(player.x, player.y - 4, 12, Math.PI, 0); ctx.fill();

            if (gameState.isDashing) {
                ctx.fillStyle = 'rgba(56, 189, 248, 0.4)';
                ctx.beginPath(); ctx.arc(player.x - 16, player.y, 11, 0, Math.PI * 2); ctx.fill();
            }

            if (gameState.carriedCount > 0 && gameState.step < SCENARIOS.DOCTOR_HOSPITAL_SCENE) {
                ctx.fillStyle = '#f59e0b'; ctx.font = 'bold 12px Tajawal';
                ctx.fillText(`[عربة العائلة: ${gameState.carriedCount}/3]`, player.x - 30, player.y - 22);
            }
        }

        function gameLoop() {
            updatePlayerLogic();
            renderScene();
            requestAnimationFrame(gameLoop);
        }

        window.onload = function() {
            setupTouchControls();
            requestAnimationFrame(gameLoop);
        };
    </script>
</body>
</html>
"""

st.title("⚔️ Chronicles of Shinra - Chapter 1")
st.write("لعبة RPG تفاعلية كاملة مدمجة داخل تطبيق Streamlit.")

# Render game html inside streamlit iframe
components.html(game_html, height=750, scrolling=False)
