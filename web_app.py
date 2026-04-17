import streamlit as st
import random
import time

# --- KONFIGURATSIYA ---
st.set_page_config(page_title="Brawl Stars PRO", page_icon="🔥", layout="wide")

# --- PREMIUM DESIGN (CSS) ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #000428, #004e92);
        color: white; font-family: 'Arial Black', sans-serif;
    }
    .main-box {
        background: rgba(0, 0, 0, 0.6);
        border: 4px solid #FFD700;
        border-radius: 30px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 0 30px rgba(255, 215, 0, 0.3);
    }
    .brawler-card {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 15px;
        margin: 10px 0;
        border-bottom: 5px solid #00ff00;
    }
    .status-bar {
        background: #222; border-radius: 50px; padding: 5px 20px;
        border: 2px solid #FFD700; display: inline-block; margin: 5px;
    }
    .upgrade-btn { color: #00ff00; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- O'YINNING ASOSIY MANTIQIY QISMI ---
if 'coins' not in st.session_state: st.session_state.coins = 500
if 'gems' not in st.session_state: st.session_state.gems = 50
if 'trophies' not in st.session_state: st.session_state.trophies = 0
if 'inv' not in st.session_state: 
    st.session_state.inv = {"Shelly": {"level": 1, "power": 100, "rarity": "Начальный"}}
if 'last_win' not in st.session_state: st.session_state.last_win = ""

# --- BRAWLERLAR MA'LUMOTI ---
ALL_BRAWLERS = {
    "El Primo": {"rarity": "Редкий", "power": 150},
    "Colt": {"rarity": "Редкий", "power": 120},
    "Mortis": {"rarity": "Мифический", "power": 200},
    "Leon": {"rarity": "Легендарный", "power": 300},
    "Crow": {"rarity": "Легендарный", "power": 280},
    "Spike": {"rarity": "Легендарный", "power": 310},
    "Edgar": {"rarity": "Эпический", "power": 180}
}

# --- FUNKSIYALAR ---
def open_box(cost, cost_type, is_mega=False):
    if cost_type == "coins": st.session_state.coins -= cost
    else: st.session_state.gems -= cost
    
    chance = 0.6 if is_mega else 0.2
    if random.random() < chance:
        name = random.choice(list(ALL_BRAWLERS.keys()))
        if name not in st.session_state.inv:
            st.session_state.inv[name] = {"level": 1, "power": ALL_BRAWLERS[name]['power'], "rarity": ALL_BRAWLERS[name]['rarity']}
            st.session_state.last_win = f"✨ НОВЫЙ БОЕЦ: {name.upper()}!"
            st.balloons()
        else:
            st.session_state.coins += 200
            st.session_state.last_win = f"Повторка {name}! Получено +200 монет."
    else:
        st.session_state.coins += random.randint(50, 150)
        st.session_state.last_win = "Выпали только монеты 💰"

# --- INTERFEYS ---
st.title("🏆 BRAWL STARS ULTIMATE SIMULATOR")

# Yuqori panel (Resources)
st.markdown(f"""
    <div class='status-bar'>💰 {st.session_state.coins}</div>
    <div class='status-bar'>💎 {st.session_state.gems}</div>
    <div class='status-bar'>🏆 {st.session_state.trophies}</div>
    """, unsafe_allow_html=True)

col_lobby, col_inv = st.columns([2, 1])

with col_lobby:
    st.markdown("<div class='main-box'>", unsafe_allow_html=True)
    st.header("🎮 ГЛАВНОЕ ЛОББИ")
    
    # O'ynash tugmasi (Trophy yig'ish)
    if st.button("⚔️ В БОЙ! (ИГРАТЬ)", use_container_width=True):
        win_trophies = random.randint(5, 12)
        st.session_state.trophies += win_trophies
        st.session_state.coins += random.randint(10, 30)
        st.toast(f"+{win_trophies} кубков!")
        st.rerun()

    st.write("---")
    st.subheader("🛍️ МАГАЗИН")
    shop1, shop2 = st.columns(2)
    with shop1:
        st.write("🎁 **BIG BOX**")
        if st.button("Открыть (200 💰)"):
            if st.session_state.coins >= 200: open_box(200, "coins")
            else: st.error("Недостаточно монет!")
            st.rerun()
            
    with shop2:
        st.write("🔵 **MEGA BOX**")
        if st.button("Открыть (80 💎)"):
            if st.session_state.gems >= 80: open_box(80, "gems", True)
            else: st.error("Недостаточно гемов!")
            st.rerun()

    if st.session_state.last_win:
        st.info(st.session_state.last_win)
    st.markdown("</div>", unsafe_allow_html=True)

    # Brawl Pass Progress
    st.write("---")
    st.subheader("📋 BRAWL PASS PROGRESS")
    progress = (st.session_state.trophies % 100) / 100
    st.progress(progress)
    st.write(f"До следующей награды: {100 - (st.session_state.trophies % 100)}🏆")

with col_inv:
    st.header("👤 БОЙЦЫ")
    for name, data in st.session_state.inv.items():
        with st.container():
            st.markdown(f"""
                <div class='brawler-card'>
                    <h3 style='margin:0;'>{name}</h3>
                    <small>{data['rarity']}</small><br>
                    <b>Level: {data['level']}</b> | Power: {data['power']}
                </div>
            """, unsafe_allow_html=True)
            
            # Upgrade tizimi
            upgrade_cost = data['level'] * 300
            if st.button(f"UPGRADE ({upgrade_cost} 💰)", key=f"up_{name}"):
                if st.session_state.coins >= upgrade_cost:
                    st.session_state.coins -= upgrade_cost
                    st.session_state.inv[name]['level'] += 1
                    st.session_state.inv[name]['power'] += 25
                    st.rerun()
                else:
                    st.error("Нет монет!")

# Sidebar sozlamalari
if st.sidebar.button("СБРОСИТЬ ВСЁ 🔄"):
    st.session_state.clear()
    st.rerun()
