import streamlit as st
import random
import time
import base64

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Brawl Stars OMNI RU", page_icon="💣", layout="wide")

# --- 2. SUPREME NEON CSS ---
st.markdown("""
    <style>
    .stApp { background: #020617; color: #f8fafc; font-family: 'Orbitron', sans-serif; }
    .status-bar {
        background: rgba(30, 41, 59, 0.8);
        border: 2px solid #00ffcc; border-radius: 15px; padding: 15px;
        display: flex; justify-content: space-around; margin-bottom: 25px;
    }
    .box-card {
        background: #1e293b; border: 2px solid #334155;
        border-radius: 15px; padding: 15px; text-align: center;
        transition: 0.3s; margin-bottom: 10px;
    }
    .box-card:hover { border-color: #ff0055; transform: scale(1.02); }
    .pass-container {
        background: rgba(15, 23, 42, 0.9);
        border: 2px solid #6200ff; border-radius: 20px; padding: 20px;
    }
    .tier-card {
        background: #0f172a; border-radius: 10px; padding: 10px;
        margin-bottom: 10px; border-left: 5px solid #6200ff;
    }
    .brawler-card {
        background: #0f172a; border: 1px solid #1e293b;
        border-radius: 12px; padding: 10px; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. INITIAL STATE ---
if 'gold' not in st.session_state:
    st.session_state.update({
        'gold': 0, 'gems': 0, 'trophies': 0, 'xp': 0,
        'inv': {"Шелли": {"lvl": 1, "pwr": 300, "icon": "🔫", "rarity": "Начальный"}},
        'claimed': [], 'plus': False
    })

BRAWLERS_DB = {
    "Леон": {"rarity": "Легендарный", "pwr": 600, "icon": "🦎"},
    "Ворон": {"rarity": "Легендарный", "pwr": 580, "icon": "🦅"},
    "Спайк": {"rarity": "Легендарный", "pwr": 620, "icon": "🌵"},
    "Мортис": {"rarity": "Мифический", "pwr": 500, "icon": "🦇"}
}

PASS_TIERS = {
    1: {"xp": 500, "reward": "1,000 Золота", "val": 1000, "type": "gold"},
    2: {"xp": 2000, "reward": "50 Гемов", "val": 50, "type": "gems"},
    3: {"xp": 5000, "reward": "2,500 Золота", "val": 2500, "type": "gold"},
    5: {"xp": 15000, "reward": "100 Гемов", "val": 100, "type": "gems"},
    7: {"xp": 40000, "reward": "5,000 Золота", "val": 5000, "type": "gold"},
    10: {"xp": 100000, "reward": "PLUS: 20,000 Золота", "val": 20000, "type": "gold"},
    12: {"xp": 200000, "reward": "PLUS: 50,000 Золота", "val": 50000, "type": "gold"},
    15: {"xp": 400000, "reward": "ФИНАЛ PLUS: 400,000 ЗОЛОТА", "val": 400000, "type": "gold"}
}

# --- 4. FUNCTIONS ---
def open_box(cost, brawler_chance):
    if st.session_state.gold >= cost:
        st.session_state.gold -= cost
        with st.spinner("📦 Открытие..."):
            time.sleep(0.7)
            if random.random() < brawler_chance:
                name = random.choice(list(BRAWLERS_DB.keys()))
                if name not in st.session_state.inv:
                    st.session_state.inv[name] = BRAWLERS_DB[name]
                    st.session_state.inv[name]['lvl'] = 1
                    st.balloons()
                    st.success(f"🔥 НОВЫЙ БОЕЦ: {name}!")
                else:
                    st.session_state.gold += (cost * 2)
                    st.info(f"💰 Дубликат! Получено {cost*2} золота.")
            else:
                gain = random.randint(int(cost*0.3), int(cost*0.9))
                st.session_state.gold += gain
                st.toast(f"📦 Золото: +{gain}")
    else:
        st.error("Недостаточно золота!")

def save_game():
    data = {
        "gold": st.session_state.gold, "gems": st.session_state.gems,
        "trophies": st.session_state.trophies, "xp": st.session_state.xp,
        "inv": st.session_state.inv, "claimed": st.session_state.claimed,
        "plus": st.session_state.plus
    }
    return base64.b64encode(str(data).encode()).decode()

def load_game(code):
    try:
        decoded = eval(base64.b64decode(code).decode())
        st.session_state.update(decoded)
        st.success("✅ Прогресс успешно загружен!")
        time.sleep(1)
        st.rerun()
    except:
        st.error("❌ Неверный код сохранения!")

# --- 5. UI ---
st.markdown("<h1 style='text-align: center; color: #00ffcc;'>💣 BRAWL STARS OMNI: RU v18.4</h1>", unsafe_allow_html=True)

# Status Bar
st.markdown(f"""
    <div class="status-bar">
        <span style="color: #fbbf24; font-size: 20px;">💰 {st.session_state.gold:,}</span>
        <span style="color: #38bdf8; font-size: 20px;">💎 {st.session_state.gems}</span>
        <span style="color: #f8fafc; font-size: 20px;">🏆 {st.session_state.trophies}</span>
    </div>
    """, unsafe_allow_html=True)

col_shop, col_arena, col_pass = st.columns([1, 1, 1.4])

with col_shop:
    st.header("🛒 Магазин")
    st.markdown("<div class='box-card'><h3>📦 Малый ящик</h3><p>500 Золота</p></div>", unsafe_allow_html=True)
    if st.button("ОТКРЫТЬ (500)", key="b500", use_container_width=True):
        open_box(500, 0.05); st.rerun()

    st.markdown("<div class='box-card'><h3>🔵 Большой ящик</h3><p>1,000 Золота</p></div>", unsafe_allow_html=True)
    if st.button("ОТКРЫТЬ (1,000)", key="b1000", use_container_width=True):
        open_box(1000, 0.12); st.rerun()

    st.markdown("<div class='box-card' style='border-color: #ff0055;'><h3>🔥 Ультра ящик</h3><p>3,000 Золота</p></div>", unsafe_allow_html=True)
    if st.button("ОТКРЫТЬ (3,000)", key="b3000", use_container_width=True):
        open_box(3000, 0.30); st.rerun()

with col_arena:
    st.header("⚔️ Арена")
    if st.button("🔥 НАЧАТЬ БОЙ (PLAY)", use_container_width=True, type="primary"):
        with st.spinner("Бой..."):
            time.sleep(0.5)
            st.session_state.gold += 250
            st.session_state.xp += 1000 
            st.session_state.trophies += 20
            st.rerun()
    
    st.write("---")
    st.subheader("💾 Сохранение & Загрузка")
    
    # Save
    if st.button("СОХРАНИТЬ ПРОГРЕСС", use_container_width=True):
        code = save_game()
        st.code(code)
        st.caption("Скопируйте этот код и сохраните его!")

    # Load (Siz so'ragan narsa)
    st.write("---")
    input_code = st.text_input("Введите код для загрузки:", placeholder="Вставьте код сюда...")
    if st.button("ЗАГРУЗИТЬ ИГРУ", use_container_width=True):
        if input_code:
            load_game(input_code)
        else:
            st.warning("Сначала введите код!")

with col_pass:
    st.header("🎫 Бравл Пасс")
    st.write(f"XP: **{st.session_state.xp:,}**")
    st.progress(min(st.session_state.xp / 400000, 1.0))
    
    if not st.session_state.plus:
        if st.button("КУПИТЬ PLUS (200 💎)", use_container_width=True):
            if st.session_state.gems >= 200:
                st.session_state.gems -= 200
                st.session_state.plus = True
                st.rerun()
    else:
        st.success("BRAWL PASS PLUS АКТИВЕН ✅")

    st.markdown("<div class='pass-container'>", unsafe_allow_html=True)
    for t, d in PASS_TIERS.items():
        is_plus = t >= 10
        claimed = t in st.session_state.claimed
        unlocked = st.session_state.xp >= d['xp']
        
        status = "✅" if claimed else ("🎁" if unlocked else "🔒")
        color = "#fbbf24" if is_plus else "#f8fafc"
        
        st.markdown(f"""
            <div class="tier-card" style="border-left-color: {'#ff0055' if is_plus else '#6200ff'};">
                <div style="display: flex; justify-content: space-between; color: {color};">
                    <span>Tier {t}: {d['reward']}</span>
                    <span>{status}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        if unlocked and not claimed:
            if is_plus and not st.session_state.plus:
                st.button(f"Нужен Plus", key=f"l_{t}", disabled=True, use_container_width=True)
            else:
                if st.button(f"Забрать {d['reward']}", key=f"btn_{t}", use_container_width=True):
                    if d['type'] == 'gold': st.session_state.gold += d['val']
                    elif d['type'] == 'gems': st.session_state.gems += d['val']
                    st.session_state.claimed.append(t)
                    st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# Collection
st.write("---")
st.header("👤 Мои Бойцы")
cols = st.columns(5)
for i, (name, data) in enumerate(st.session_state.inv.items()):
    with cols[i % 5]:
        st.markdown(f"<div class='brawler-card'><h3>{data['icon']}</h3><b>{name}</b><br><small>Сила: {data['pwr']}</small></div>", unsafe_allow_html=True)

if st.sidebar.button("♻️ СБРОСИТЬ ВСЁ (0)"):
    st.session_state.clear()
    st.rerun()
