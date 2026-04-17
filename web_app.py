import streamlit as st
import random
import time
import base64
import json

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Brawl Stars HARDCORE", page_icon="⏳", layout="wide")

# --- 2. ELITE CYBER CSS ---
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at center, #001220 0%, #000000 100%);
        background-attachment: fixed; color: #00ffcc; font-family: 'Orbitron', sans-serif;
    }
    .status-bar {
        background: rgba(0, 0, 0, 0.8); border: 2px solid #00ffcc;
        border-radius: 50px; padding: 15px; display: flex; justify-content: space-around;
        box-shadow: 0 0 20px rgba(0, 255, 204, 0.4); margin-bottom: 30px;
    }
    .box-card {
        background: rgba(10, 10, 10, 0.9); border: 2px solid #333;
        border-radius: 20px; padding: 20px; text-align: center;
        transition: 0.4s; margin-bottom: 15px;
    }
    .event-card {
        background: linear-gradient(135deg, #ff0055 0%, #6200ff 100%);
        border: 3px solid #fff; border-radius: 20px; padding: 20px;
        text-align: center; box-shadow: 0 0 30px rgba(255, 0, 85, 0.6);
    }
    .small-timer { font-size: 11px; color: #fff; font-weight: bold; background: rgba(0,0,0,0.5); padding: 2px 6px; border-radius: 5px; }
    .brawler-card {
        background: #050505; border: 1px solid #00ffcc;
        border-radius: 15px; padding: 15px; text-align: center;
    }
    .rank-badge {
        background: #cd7f32; color: white; padding: 2px 8px; border-radius: 5px; font-size: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. INITIAL STATE ---
if 'gold' not in st.session_state:
    st.session_state.update({
        'gold': 0, 'gems': 0, 'trophies': 0, 'xp': 0,
        'inv': {"Шелли": {"lvl": 1, "pwr": 300, "icon": "🔫", "rank": "BRONZE III"}},
        'claimed': [], 'plus': False
    })

BRAWLERS_DB = {
    "Леон": {"pwr": 600, "icon": "🦎", "rank": "SILVER I"},
    "Ворон": {"pwr": 580, "icon": "🦅", "rank": "BRONZE II"},
    "Спайк": {"pwr": 620, "icon": "🌵", "rank": "GOLD I"},
    "Мортис": {"pwr": 500, "icon": "🦇", "rank": "BRONZE III"}
}

# --- 4. SECURE DATA FUNCTIONS ---
def get_save_code():
    data = {k: v for k, v in st.session_state.items() if k != 'save_code'}
    return base64.b64encode(json.dumps(data).encode()).decode()

def load_from_code(code):
    try:
        data = json.loads(base64.b64decode(code).decode())
        for k, v in data.items(): st.session_state[k] = v
        st.success("✅ ДАННЫЕ ЗАГРУЖЕНЫ!"); time.sleep(0.5); st.rerun()
    except: st.error("❌ ОШИБКА КОДА!")

def open_box(cost, chance, is_mega=False):
    # Xatolikni oldini olish uchun cost son ekanligini tekshiramiz
    cost = int(cost)
    if st.session_state.gold >= cost:
        st.session_state.gold -= cost
        with st.spinner("⏳ СИНХРОНИЗАЦИЯ..."):
            time.sleep(1)
            if random.random() < chance:
                name = random.choice(list(BRAWLERS_DB.keys()))
                if name not in st.session_state.inv:
                    st.session_state.inv[name] = BRAWLERS_DB[name]
                    st.balloons(); st.success(f"🔥 УЛЬТРА РЕДКИЙ: {name}!")
                else:
                    refund = cost * 1.5 if is_mega else cost * 2
                    st.session_state.gold += int(refund)
                    st.info(f"💰 ДУБЛИКАТ! Возвращено: {int(refund)}")
            else:
                gain = random.randint(int(cost*0.3), int(cost*0.6))
                st.session_state.gold += gain
                st.toast(f"📦 +{gain} ЗОЛОТА")
    else:
        st.error(f"Недостаточно золота! Нужно {cost:,}")

# --- 5. UI LAYOUT ---
st.markdown("<h1 style='text-align: center; color: #00ffcc;'>🔱 BRAWL STARS: HARDCORE v18.8 🔱</h1>", unsafe_allow_html=True)

st.markdown(f"""
    <div class="status-bar">
        <span style="color: #f1c40f;">💰 ЗОЛОТО: {st.session_state.gold:,}</span>
        <span style="color: #00d2ff;">💎 ГЕМЫ: {st.session_state.gems}</span>
        <span style="color: #ffffff;">🏆 КУБКИ: {st.session_state.trophies}</span>
    </div>
    """, unsafe_allow_html=True)

col_shop, col_arena, col_pass = st.columns([1, 1, 1.4])

with col_shop:
    st.header("🛒 SHOP")
    
    # MEGA ULTRA EVENT BOX - TypeError FIXED (10000 vergulsiz yozildi)
    st.markdown("""
        <div class='event-card'>
            <span class='small-timer'>ОСТАЛОСЬ: 24 ЧАСА</span>
            <h3>💎 MEGA ULTRA BOX</h3>
            <p>10,000 ЗОЛОТА</p>
            <small>Шанс на бойца: 60%</small>
        </div>
        """, unsafe_allow_html=True)
    if st.button("ОТКРЫТЬ MEGA BOX (10,000)", key="mega_btn", use_container_width=True):
        open_box(10000, 0.60, is_mega=True)
        st.rerun()
    
    st.write("---")
    # Boshqa qutilar
    for cost, name, color in [(500, "SMALL", "#333"), (1000, "BIG", "#00d2ff"), (3000, "ULTRA", "#ff0055")]:
        st.markdown(f"<div class='box-card' style='border-color: {color};'><h3>{name} BOX</h3><p>{cost}</p></div>", unsafe_allow_html=True)
        if st.button(f"ОТКРЫТЬ {name}", key=f"b_{cost}", use_container_width=True):
            open_box(cost, 0.04 if cost == 500 else (0.12 if cost == 1000 else 0.25))
            st.rerun()

with col_arena:
    st.header("⚔️ ARENA")
    st.warning("Сложность: ВЫСОКАЯ (Награда снижена)")
    if st.button("🔥 START HARD BATTLE", use_container_width=True, type="primary"):
        st.session_state.gold += 100
        st.session_state.xp += 600
        st.session_state.trophies += 12
        st.toast("Тяжелая победа! +100 Золота")
        st.rerun()
    
    st.write("---")
    st.subheader("💾 DATA CENTER")
    if st.button("GENERATE SAVE CODE"): st.code(get_save_code())
    input_code = st.text_input("PASTE LOAD CODE:")
    if st.button("LOAD PROGRESS"): load_from_code(input_code)

with col_pass:
    st.header("🎫 BRAWL PASS")
    st.write(f"XP: **{st.session_state.xp:,} / 400,000**")
    st.progress(min(st.session_state.xp / 400000, 1.0))
    
    if not st.session_state.plus:
        if st.button("BUY PLUS (200 💎)", use_container_width=True):
            if st.session_state.gems >= 200:
                st.session_state.gems -= 200
                st.session_state.plus = True; st.rerun()

    for t in [1, 5, 10, 15]:
        d = {1: "1,000 Зол", 5: "100 Гем", 10: "50k Зол", 15: "400k ЗОЛОТА"}[t]
        unlocked = st.session_state.xp >= {1:500, 5:15000, 10:100000, 15:400000}[t]
        claimed = t in st.session_state.claimed
        st.write(f"Tier {t}: {d} {'✅' if claimed else ('🔓' if unlocked else '🔒')}")
        if unlocked and not claimed:
            if t >= 10 and not st.session_state.plus: st.button("NEED PLUS", key=f"l_{t}", disabled=True)
            elif st.button(f"GET TIER {t}", key=f"c_{t}"):
                vals = {1:1000, 5:100, 10:50000, 15:400000}
                if t == 5: st.session_state.gems += vals[t]
                else: st.session_state.gold += vals[t]
                st.session_state.claimed.append(t); st.rerun()

st.write("---")
st.header("👤 MY BRAWLERS")
b_cols = st.columns(5)
for i, (name, data) in enumerate(st.session_state.inv.items()):
    with b_cols[i % 5]:
        st.markdown(f"<div class='brawler-card'><div class='rank-badge'>{data.get('rank','BRONZE I')}</div><h2>{data['icon']}</h2><b>{name}</b></div>", unsafe_allow_html=True)
