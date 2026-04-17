import streamlit as st
import random
import time
import base64

# --- 1. ENGINE CONFIGURATION ---
st.set_page_config(page_title="Brawl Stars OMNI", page_icon="💣", layout="wide")

# --- 2. THE ULTIMATE NEON CSS ---
st.markdown("""
    <style>
    .stApp { background: #010101; color: #00ffcc; font-family: 'Orbitron', sans-serif; }
    .main-card {
        background: rgba(0, 20, 40, 0.9);
        border: 2px solid #00ffcc; border-radius: 25px;
        padding: 25px; box-shadow: 0 0 30px rgba(0, 255, 204, 0.3);
    }
    .resource-bar {
        display: flex; justify-content: space-around;
        background: #000; border: 1px solid #00ffcc;
        border-radius: 50px; padding: 15px; margin-bottom: 20px;
    }
    .brawl-pass-plus {
        background: linear-gradient(135deg, #6200ff, #ff0055);
        color: white; border-radius: 20px; padding: 25px;
        border: 3px solid #fff; text-shadow: 2px 2px 5px #000;
    }
    .battle-btn {
        background: linear-gradient(90deg, #ff0055, #6200ff);
        color: white; font-weight: 900; border-radius: 15px;
        height: 60px; border: none; box-shadow: 0 0 20px #ff0055;
    }
    .brawler-box {
        background: #050505; border: 1px solid #333;
        border-radius: 15px; padding: 15px; transition: 0.3s;
    }
    .brawler-box:hover { border-color: #00ffcc; transform: scale(1.05); }
    </style>
    """, unsafe_allow_html=True)

# --- 3. PERSISTENCE LOGIC (SAVE/LOAD) ---
def init_state():
    if 'gold' not in st.session_state:
        st.session_state.update({
            'gold': 0, 'gems': 0, 'trophies': 0, 'xp': 0,
            'inv': {"Shelly": {"lvl": 1, "pwr": 300, "icon": "🔫", "rank": "Bronza"}},
            'claimed': [], 'plus': False, 'league': "Bronza I"
        })

init_state()

# --- 4. GAME DATA ---
PASS_Tiers = {
    1: {"xp": 500, "reward": "1,000 Gold", "val": 1000, "type": "gold"},
    3: {"xp": 5000, "reward": "100 Gems", "val": 100, "type": "gems"},
    5: {"xp": 20000, "reward": "Mega Box", "type": "box"},
    10: {"xp": 100000, "reward": "PLUS: 50,000 Gold", "val": 50000, "type": "gold"},
    15: {"xp": 400000, "reward": "ULTRA FINAL: 400,000 GOLD", "val": 400000, "type": "gold"}
}

# --- 5. FUNCTIONS ---
def save_game():
    save_obj = {
        "gold": st.session_state.gold, "gems": st.session_state.gems,
        "trophies": st.session_state.trophies, "xp": st.session_state.xp,
        "inv": st.session_state.inv, "claimed": st.session_state.claimed,
        "plus": st.session_state.plus
    }
    st.session_state.save_code = base64.b64encode(str(save_obj).encode()).decode()

def load_game(code):
    try:
        decoded = eval(base64.b64decode(code).decode())
        st.session_state.update(decoded)
        st.success("Ma'lumotlar tiklandi!")
    except: st.error("Xato kod!")

def start_battle():
    with st.spinner("🚀 JANG KETMOQDA..."): time.sleep(1)
    if random.random() > 0.5:
        st.session_state.trophies += 15
        st.session_state.gold += 200
        st.session_state.xp += 800
        st.balloons()
    else:
        st.session_state.trophies = max(0, st.session_state.trophies - 10)
        st.session_state.xp += 200

# --- 6. UI LAYOUT ---
st.markdown("<h1 style='text-align: center;'>💣 BRAWL STARS: OMNI v18 💣</h1>", unsafe_allow_html=True)

# Resources Panel
st.markdown(f"""
    <div class="resource-bar">
        <span>💰 {st.session_state.gold:,}</span>
        <span>💎 {st.session_state.gems}</span>
        <span>🏆 {st.session_state.trophies}</span>
        <span>⚔️ {st.session_state.league}</span>
    </div>
    """, unsafe_allow_html=True)

col_main, col_pass = st.columns([1, 1.2])

with col_main:
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    st.header("🎮 O'YIN MAYDONI")
    if st.button("🔥 START SUPREME BATTLE", use_container_width=True):
        start_battle()
        st.rerun()
    
    st.write("---")
    st.subheader("🎰 DAILY LUCKY SPIN")
    if st.button("SPIN (TEKIN)"):
        win = random.randint(10, 1000)
        st.session_state.gold += win
        st.toast(f"Yutuq: {win} Oltin!")
        st.rerun()

    st.write("---")
    st.subheader("💾 SAVE / LOAD")
    if st.button("O'YINNI SAQLASH (Save)"):
        save_game()
        st.code(st.session_state.save_code)
        st.info("Yuqoridagi kodni nusxalab oling! Keyingi safar shu bilan tiklaysiz.")
    
    load_code = st.text_input("Save kodni kiriting:")
    if st.button("YUKLASH (Load)"):
        load_game(load_code)
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

with col_pass:
    st.markdown("<div class='brawl-pass-plus'>", unsafe_allow_html=True)
    st.header("🎫 BRAWL PASS ULTRA PLUS")
    st.write(f"PROGRES: **{st.session_state.xp:,} / 400,000 XP**")
    st.progress(min(st.session_state.xp / 400000, 1.0))
    
    if not st.session_state.plus:
        if st.button("BUY PASS PLUS (500 💎)", use_container_width=True):
            if st.session_state.gems >= 500:
                st.session_state.plus = True
                st.session_state.gems -= 500
                st.rerun()

    for t, d in PASS_Tiers.items():
        is_plus = t >= 10
        claimed = t in st.session_state.claimed
        unlocked = st.session_state.xp >= d['xp']
        
        c1, c2 = st.columns([3, 1])
        with c1:
            st.write(f"**Tier {t}:** {d['reward']} ({d['xp']:,} XP)")
        with c2:
            if claimed: st.write("✅")
            elif unlocked:
                if is_plus and not st.session_state.plus: st.write("🔒 Plus")
                elif st.button("GET", key=f"t_{t}"):
                    if d['type'] == 'gold': st.session_state.gold += d['val']
                    elif d['type'] == 'gems': st.session_state.gems += d['val']
                    st.session_state.claimed.append(t)
                    st.rerun()
            else: st.write("❌")
    st.markdown("</div>", unsafe_allow_html=True)

# --- 7. COLLECTION ---
st.write("---")
st.header("👤 MY BRAWLERS")
cols = st.columns(4)
for i, (name, data) in enumerate(st.session_state.inv.items()):
    with cols[i % 4]:
        st.markdown(f"""
            <div class='brawler-box'>
                <h3>{data['icon']} {name}</h3>
                <p>PWR: {data['pwr']} | LVL: {data['lvl']}</p>
            </div>
            """, unsafe_allow_html=True)

if st.sidebar.button("♻️ FULL REBOOT"):
    st.session_state.clear()
    st.rerun()
