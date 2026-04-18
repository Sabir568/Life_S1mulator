import streamlit as st
import random
import time
import base64
import json

# --- 1. CONFIG ---
st.set_page_config(page_title="RECKAT STARS: ULTIMATE", page_icon="🔱", layout="wide")

# --- 2. ADVANCED RECKAT CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Black+Ops+One&family=Orbitron:wght@400;900&display=swap');
    
    .stApp { background: #050505; color: #ffffff; font-family: 'Orbitron', sans-serif; }
    
    .main-title { 
        font-family: 'Black Ops One', cursive; font-size: 70px; text-align: center; 
        background: linear-gradient(to bottom, #00ffcc, #6200ff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 0 10px #6200ff); margin-bottom: 5px;
    }
    
    .status-bar { 
        background: rgba(20, 20, 20, 0.95); border: 3px solid #00ffcc; border-radius: 20px; 
        padding: 20px; display: flex; justify-content: space-around; margin-bottom: 25px; 
        box-shadow: 0 0 20px rgba(0, 255, 204, 0.3);
    }

    .battle-arena {
        background: radial-gradient(circle, #1a1a1a 0%, #000000 100%);
        border: 4px solid #ff0055; border-radius: 25px; padding: 40px;
        text-align: center; position: relative; overflow: hidden;
        box-shadow: inset 0 0 100px #ff0055; min-height: 400px;
    }

    .enemy-sprite {
        font-size: 80px; text-shadow: 0 0 30px red;
        animation: enemy-move 2s infinite ease-in-out;
    }

    @keyframes enemy-move {
        0% { transform: scale(1) translateY(0px); }
        50% { transform: scale(1.2) translateY(-20px); }
        100% { transform: scale(1) translateY(0px); }
    }

    .reckat-btn {
        background: linear-gradient(45deg, #6200ff, #00ffcc);
        border: none; color: white; padding: 15px 30px;
        border-radius: 10px; font-weight: bold; cursor: pointer;
    }

    .pass-container {
        background: #0a0a0a; border: 2px solid #6200ff;
        border-radius: 20px; padding: 15px; height: 600px; overflow-y: scroll;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATA ---
BRAWLERS = ["Шелли", "Нита", "Кольт", "Булл", "Брок", "Эль Примо", "Барли", "Поко", "Роза", "Рико", "Дэррил", "Пенни", "Карл", "Джекки", "Пайпер", "Пэм", "Фрэнк", "Биби", "Беа", "Нани", "Эдгар", "Грифф", "Гром", "Бонни", "Мортис", "Тара", "Джин", "Макс", "Мистер П.", "Спраут", "Байрон", "Скуик", "Спайк", "Ворон", "Леон", "Сэнди", "Амбер", "Мэг", "Гейл", "Вольт", "Колетт", "Лу", "Гавс", "Белль", "Базз", "Эш", "Лола", "Фэнг", "Ева", "Джанет", "Отис", "Сэм", "Бастер", "Мэнди", "Р-Т", "Мэйси", "Хэнк", "Корделиус", "Даг", "Чак", "Мико", "Кит", "Ларри", "Лоури", "Анджело", "Мелоди", "Лили", "Драко", "Клэнси", "Берри", "Кэндзи", "Мо", "Сириус", "Джуджу", "Шад", "Гас", "Честер", "Грей"]

# --- 4. ENGINE ---
if 'gold' not in st.session_state:
    st.session_state.update({
        'gold': 0, 'gems': 0, 'xp': 0, 'trophies': 0,
        'inv': ["Шелли"], 'claimed': [], 'pass_type': 'Free',
        'battle_mode': False, 'enemy_hp': 0, 'enemy_type': ""
    })

def save():
    data = {"g":st.session_state.gold, "m":st.session_state.gems, "x":st.session_state.xp, "t":st.session_state.trophies, "i":st.session_state.inv, "c":st.session_state.claimed, "p":st.session_state.pass_type}
    return base64.b64encode(json.dumps(data).encode()).decode()

def load(code):
    try:
        d = json.loads(base64.b64decode(code).decode())
        st.session_state.update({'gold':d['g'], 'gems':d['m'], 'xp':d['x'], 'trophies':d['t'], 'inv':d['i'], 'claimed':d['c'], 'pass_type':d['p']})
        return True
    except: return False

# --- 5. UI ---
st.markdown("<div class='main-title'>RECKAT STARS</div>", unsafe_allow_html=True)

st.markdown(f"""
<div class="status-bar">
    <div style="color:#f1c40f">💰 ЗОЛОТО: {st.session_state.gold:,}</div>
    <div style="color:#00ffcc">💎 КРИСТАЛЛЫ: {st.session_state.gems:,}</div>
    <div style="color:#ffffff">🏆 КУБКИ: {st.session_state.trophies:,}</div>
    <div style="color:#6200ff">⭐ XP: {st.session_state.xp:,}</div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1.6, 1, 1.4])

with col1:
    if not st.session_state.battle_mode:
        st.markdown("""
        <div style='text-align:center; padding:50px; background:rgba(255,255,255,0.05); border-radius:20px;'>
            <h2>ГОТОВ К БИТВЕ?</h2>
            <p>Нажми кнопку ниже, чтобы войти на арену!</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚀 ИГРАТЬ (В БОЙ!)", use_container_width=True, type="primary"):
            st.session_state.battle_mode = True
            st.session_state.enemy_type = random.choice(["👾", "🤖", "👹", "👽"])
            st.session_state.enemy_hp = random.randint(15, 40)
            st.rerun()
    else:
        st.markdown("<div class='battle-arena'>", unsafe_allow_html=True)
        st.markdown(f"<div class='enemy-sprite'>{st.session_state.enemy_type}</div>", unsafe_allow_html=True)
        st.write(f"### HP ВРАГА: {st.session_state.enemy_hp}")
        st.progress(max(st.session_state.enemy_hp / 40, 0.0))
        
        if st.button("💥 УДАРИТЬ (ATTACK!)", use_container_width=True):
            st.session_state.enemy_hp -= random.randint(1, 5)
            if st.session_state.enemy_hp <= 0:
                st.session_state.battle_mode = False
                win_gold = random.randint(200, 500)
                win_xp = 400
                st.session_state.gold += win_gold
                st.session_state.xp += win_xp
                st.session_state.trophies += 15
                st.balloons()
                st.success(f"🔥 ПОБЕДА! +{win_gold} 💰 | +{win_xp} XP")
                time.sleep(1)
            st.rerun()
        
        if st.button("🏳️ СБЕЖАТЬ", use_container_width=True):
            st.session_state.battle_mode = False
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.write("---")
    st.header("🏪 МАГАЗИН")
    if st.button("🎁 РЕККАТ ЯЩИК (5,000 💰)", use_container_width=True):
        if st.session_state.gold >= 5000:
            st.session_state.gold -= 5000
            if random.random() < 0.20:
                new = random.choice([b for b in BRAWLERS if b not in st.session_state.inv])
                st.session_state.inv.append(new)
                st.success(f"НОВЫЙ БОЕЦ: {new}!"); st.balloons()
            else: st.info("Пусто! Повезет в следующий раз.")
        else: st.error("Недостаточно золота!")

with col2:
    st.header("💾 DATA CENTER")
    if st.button("📝 СОЗДАТЬ SAVE-КОД", use_container_width=True):
        st.code(save())
    
    code_in = st.text_input("ВСТАВИТЬ LOAD-КОД:")
    if st.button("📥 ЗАГРУЗИТЬ", use_container_width=True):
        if load(code_in): st.success("Данные восстановлены!"); st.rerun()
        else: st.error("Ошибка кода!")
    
    st.write("---")
    st.header("🔑 ПРОМО")
    p_code = st.text_input("Введите код:").strip()
    if st.button("АКТИВИРОВАТЬ"):
        if p_code == "KHIVA90":
            st.session_state.gold += 9000; st.session_state.gems += 90; st.balloons()
        elif p_code == "APRIL2026":
            if "Сириус" not in st.session_state.inv: st.session_state.inv.append("Сириус"); st.balloons()
        st.rerun()

with col3:
    st.header("🎫 RECKAT PASS")
    lvl = st.session_state.xp // 15000
    st.write(f"**УРОВЕНЬ: {lvl} / 50**")
    
    if st.session_state.pass_type == 'Free':
        if st.button("💎 КУПИТЬ PLUS (499 💎)", use_container_width=True):
            if st.session_state.gems >= 499:
                st.session_state.gems -= 499; st.session_state.pass_type = 'Plus'; st.rerun()
    else: st.success("👑 PLUS STATUS")

    st.markdown("<div class='pass-container'>", unsafe_allow_html=True)
    for i in range(1, 51):
        is_ok = lvl >= i
        is_got = i in st.session_state.claimed
        status = "✅" if is_got else ("🎁" if is_ok else "🔒")
        
        col_p1, col_p2 = st.columns([2, 1])
        col_p1.write(f"Level {i}: {status}")
        if is_ok and not is_got:
            if col_p2.button("GET", key=f"btn_{i}"):
                st.session_state.gold += 500; st.session_state.gems += 2
                if st.session_state.pass_type == 'Plus':
                    st.session_state.gold += 3000; st.session_state.gems += 20
                st.session_state.claimed.append(i); st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

st.write("---")
st.header(f"👥 КОЛЛЕКЦИЯ ({len(st.session_state.inv)}/78)")
inv_cols = st.columns(6)
for idx, b_name in enumerate(st.session_state.inv):
    with inv_cols[idx % 6]:
        st.markdown(f"<div style='background:black; border:1px solid #6200ff; border-radius:10px; padding:10px; text-align:center; margin-bottom:10px;'>{b_name}</div>", unsafe_allow_html=True)
