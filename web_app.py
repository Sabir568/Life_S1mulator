import streamlit as st
import random
import time
import base64
import json

# --- 1. CONFIG ---
st.set_page_config(page_title="RECKAT STARS", page_icon="🔱", layout="wide")

# --- 2. RECKAT CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Black+Ops+One&family=Orbitron:wght@400;700&display=swap');
    .stApp { background: linear-gradient(135deg, #050505 0%, #1a0033 100%); color: #ffffff; font-family: 'Orbitron', sans-serif; }
    .main-title { font-family: 'Black Ops One', cursive; font-size: 60px; text-align: center; color: #00ffcc; text-shadow: 4px 4px #6200ff; margin-bottom: 5px; }
    .status-bar { background: rgba(0, 0, 0, 0.9); border: 2px solid #6200ff; border-radius: 25px; padding: 20px; display: flex; justify-content: space-around; margin-bottom: 25px; box-shadow: 0 0 15px #6200ff; font-weight: bold; }
    .battle-zone { background: url('https://www.transparenttextures.com/patterns/carbon-fibre.png'), #111; border: 4px solid #ff3300; border-radius: 20px; padding: 30px; text-align: center; margin-bottom: 20px; box-shadow: inset 0 0 50px #000; }
    .enemy-box { font-size: 50px; margin: 20px; animation: shake 0.5s infinite; }
    @keyframes shake { 0% { transform: translate(1px, 1px); } 10% { transform: translate(-1px, -2px); } 100% { transform: translate(1px, -2px); } }
    .reckat-card { background: #000; border: 1px solid #444; border-radius: 12px; padding: 10px; text-align: center; margin-bottom: 8px; font-size: 14px; }
    .pass-scroll { background: rgba(10, 0, 20, 0.8); border-radius: 20px; padding: 15px; height: 500px; overflow-y: scroll; border: 2px solid #00ffcc; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATABASE ---
ALL_BRAWLERS = ["Шелли", "Нита", "Кольт", "Булл", "Брок", "Эль Примо", "Барли", "Поко", "Роза", "Рико", "Дэррил", "Пенни", "Карл", "Джекки", "Пайпер", "Пэм", "Фрэнк", "Биби", "Беа", "Нани", "Эдгар", "Грифф", "Гром", "Бонни", "Мортис", "Тара", "Джин", "Макс", "Мистер П.", "Спраут", "Байрон", "Скуик", "Спайк", "Ворон", "Леон", "Сэнди", "Амбер", "Мэг", "Гейл", "Вольт", "Колетт", "Лу", "Гавс", "Белль", "Базз", "Эш", "Лола", "Фэнг", "Ева", "Джанет", "Отис", "Сэм", "Бастер", "Мэнди", "Р-Т", "Мэйси", "Хэнк", "Корделиус", "Даг", "Чак", "Мико", "Кит", "Ларри", "Лоури", "Анджело", "Мелоди", "Лили", "Драко", "Клэнси", "Берри", "Кэндзи", "Мо", "Сириус", "Джуджу", "Шад", "Гас", "Честер", "Грей"]

# --- 4. SESSION STATE ---
if 'gold' not in st.session_state:
    st.session_state.update({
        'gold': 0, 'gems': 0, 'xp': 0, 'trophies': 0,
        'inv': ["Шелли"], 'claimed': [], 'pass_type': 'Free',
        'in_battle': False, 'enemy_hp': 0, 'enemy_max_hp': 0
    })

# --- 5. LOGIC (SAVE/LOAD TEGILMADI) ---
def get_save_code():
    data = {"g": st.session_state.gold, "m": st.session_state.gems, "x": st.session_state.xp, "t": st.session_state.trophies, "i": st.session_state.inv, "c": st.session_state.claimed, "p": st.session_state.pass_type}
    return base64.b64encode(json.dumps(data).encode()).decode()

def load_save_code(code):
    try:
        d = json.loads(base64.b64decode(code).decode())
        st.session_state.update({'gold':d['g'], 'gems':d['m'], 'xp':d['x'], 'trophies':d['t'], 'inv':d['i'], 'claimed':d['c'], 'pass_type':d['p']})
        return True
    except: return False

# --- 6. INTERFACE ---
st.markdown("<div class='main-title'>RECKAT STARS</div>", unsafe_allow_html=True)

st.markdown(f"""
<div class="status-bar">
    <div style="text-align:center; color:#f1c40f">💰 ЗОЛОТО<br>{st.session_state.gold:,}</div>
    <div style="text-align:center; color:#00ffcc">💎 КРИСТАЛЛЫ<br>{st.session_state.gems:,}</div>
    <div style="text-align:center; color:#ffffff">🏆 КУБКИ<br>{st.session_state.trophies:,}</div>
    <div style="text-align:center; color:#6200ff">⭐ ОПЫТ (XP)<br>{st.session_state.xp:,}</div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1.5, 1, 1.2])

with col1:
    st.header("⚔️ БИТВА (BATTLE)")
    
    if not st.session_state.in_battle:
        if st.button("🔥 ИГРАТЬ (В БОЙ)", use_container_width=True, type="primary"):
            st.session_state.in_battle = True
            st.session_state.enemy_max_hp = random.randint(10, 30)
            st.session_state.enemy_hp = st.session_state.enemy_max_hp
            st.rerun()
    else:
        st.markdown("<div class='battle-zone'>", unsafe_allow_html=True)
        st.markdown(f"<div class='enemy-box'>👾</div>", unsafe_allow_html=True)
        st.write(f"HP ПРОТИВНИКА: {st.session_state.enemy_hp} / {st.session_state.enemy_max_hp}")
        st.progress(st.session_state.enemy_hp / st.session_state.enemy_max_hp)
        
        if st.button("👊 УДАР!", use_container_width=True):
            st.session_state.enemy_hp -= 1
            if st.session_state.enemy_hp <= 0:
                st.session_state.in_battle = False
                reward_g = random.randint(100, 200)
                reward_x = 250
                st.session_state.gold += reward_g
                st.session_state.xp += reward_x
                st.session_state.trophies += 10
                st.success(f"ПОБЕДА! +{reward_g} 💰 | +{reward_x} XP")
                time.sleep(1)
            st.rerun()
        
        if st.button("🏃 СБЕЖАТЬ (ESC)", use_container_width=True):
            st.session_state.in_battle = False
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.header("🏪 МАГАЗИН")
    if st.button("РЕККАТ ЯЩИК (5,000 💰)", use_container_width=True):
        if st.session_state.gold >= 5000:
            st.session_state.gold -= 5000
            if random.random() < 0.15:
                new_b = random.choice([b for b in ALL_BRAWLERS if b not in st.session_state.inv])
                st.session_state.inv.append(new_b); st.balloons()
            else: st.toast("Пусто!")
        else: st.error("Мало золота!")

with col2:
    st.header("💾 СОХРАНЕНИЕ")
    if st.button("СОЗДАТЬ КОД", use_container_width=True): st.code(get_save_code())
    load_in = st.text_input("ВСТАВИТЬ КОD:")
    if st.button("ЗАГРУЗИТЬ", use_container_width=True):
        if load_save_code(load_in): st.success("ОК!"); st.rerun()
    
    st.write("---")
    st.header("🎫 ПРОМОКОД")
    promo = st.text_input("Код:").strip()
    if st.button("OK"):
        if promo == "KHIVA90":
            st.session_state.gold += 9000; st.session_state.gems += 90; st.balloons()
        elif promo == "APRIL2026":
            st.session_state.inv.append("Сириус"); st.balloons()
        st.rerun()

with col3:
    st.header("🎫 RECKAT PASS PLUS")
    lvl = st.session_state.xp // 15000
    st.write(f"Уровень: {lvl}")
    if st.session_state.pass_type == 'Free':
        if st.button("💎 КУПИТЬ PLUS (499 💎)", use_container_width=True):
            if st.session_state.gems >= 499:
                st.session_state.gems -= 499; st.session_state.pass_type = 'Plus'; st.rerun()
    
    st.markdown("<div class='pass-scroll'>", unsafe_allow_html=True)
    for i in range(1, 51):
        unlocked = lvl >= i
        claimed = i in st.session_state.claimed
        if unlocked and not claimed:
            if st.button(f"ЗАБРАТЬ {i}", key=f"l_{i}"):
                st.session_state.gold += 500; st.session_state.gems += 2
                if st.session_state.pass_type == 'Plus':
                    st.session_state.gold += 2500; st.session_state.gems += 15
                st.session_state.claimed.append(i); st.rerun()
        st.write(f"Уровень {i} {'✅' if claimed else ('🎁' if unlocked else '🔒')}")
    st.markdown("</div>", unsafe_allow_html=True)

st.header(f"👥 МОИ БОЙЦЫ ({len(st.session_state.inv)}/78)")
c_inv = st.columns(6)
for idx, b in enumerate(st.session_state.inv):
    with c_inv[idx % 6]: st.markdown(f"<div class='reckat-card'>{b}</div>", unsafe_allow_html=True)
