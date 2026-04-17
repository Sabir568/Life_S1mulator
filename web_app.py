import streamlit as st
import random
import time
import base64
import json

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Brawl Stars ADMIN EDITION", page_icon="🔱", layout="wide")

# --- 2. SUPREME CSS ---
st.markdown("""
    <style>
    .stApp { background: #00050a; color: #00ffcc; font-family: 'Orbitron', sans-serif; }
    .status-bar { background: rgba(0,0,0,0.9); border: 2px solid #00ffcc; border-radius: 50px; padding: 15px; display: flex; justify-content: space-around; margin-bottom: 25px; }
    .event-card { background: linear-gradient(135deg, #ff0055 0, #6200ff 100%); border-radius: 20px; padding: 20px; text-align: center; border: 2px solid white; box-shadow: 0 0 20px rgba(255,0,85,0.4); margin-bottom: 15px; }
    .pass-panel { background: rgba(10, 0, 30, 0.85); border: 2px solid #6200ff; border-radius: 20px; padding: 20px; height: 550px; overflow-y: scroll; }
    .brawler-card { background: #000; border: 1px solid #00ffcc; border-radius: 10px; padding: 10px; text-align: center; margin-bottom: 5px; min-height: 120px; }
    .admin-brawler { border: 3px solid gold !important; box-shadow: 0 0 20px gold; color: gold !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LARGE BRAWLERS DATABASE (70+) ---
ALL_BRAWLERS = {
    "Шелли": "🔫", "Кольт": "🔫", "Нита": "🐻", "Булл": "🐂", "Брок": "🚀", "Эль Примо": "🥊", "Барли": "🧪", "Поко": "🎸", 
    "Роза": "🌿", "Рико": "🤖", "Дэррил": "🛢️", "Пенни": "🏴‍☠️", "Карл": "⛏️", "Джекки": "🚜", "Пайпер": "☂️", "Пэм": "🔧", 
    "Фрэнк": "🔨", "Биби": "⚾", "Беа": "🐝", "Нани": "👁️", "Эдгар": "🧣", "Грифф": "💰", "Гром": "💣", "Бонни": "🧨", 
    "Мортис": "🦇", "Тара": "🃏", "Джин": "🧞", "Макс": "⚡", "Мистер П.": "🐧", "Спраут": "🌱", "Байрон": "🐍", "Скуик": "💧", 
    "Спайк": "🌵", "Ворон": "🦅", "Леон": "🦎", "Сэнди": "⏳", "Амбер": "🔥", "Мэг": "🤖", "Суперчел": "🦸", "Гейл": "❄️", 
    "Вольт": "🥤", "Колетт": "📔", "Лу": "🍦", "Гавс": "🐶", "Белль": "🔫", "Базз": "🦖", "Эш": "🗑️", "Лола": "🎭", 
    "Фэнг": "👟", "Ева": "🛸", "Джанет": "🚀", "Отис": "🐙", "Сэм": "👊", "Бастер": "📽️", "Мэнди": "🍭", "Р-Т": "📺", 
    "Мэйси": "🦾", "Хэнк": "🦐", "Корделиус": "🍄", "Даг": "🌭", "Чак": "🚂", "Мико": "🐒", "Кит": "🐱", "Ларри": "👮", 
    "Анджело": "🦟", "Мелоди": "🎵", "Лили": "🌸", "Драко": "🎸", "Клэнси": "🦀", "Берри": "🦄", "Кэндзи": "🍣", "Мо": "🐭"
}

# --- 4. SESSION STATE ---
if 'gold' not in st.session_state:
    st.session_state.update({
        'gold': 5000, 'gems': 100, 'trophies': 0, 'xp': 0,
        'inv': {"Шелли": "🔫"},
        'claimed': [], 'plus': False
    })

# --- 5. CORE FUNCTIONS ---
def open_box(cost, chance, is_mega=False):
    if st.session_state.gold >= cost:
        st.session_state.gold -= cost
        with st.spinner("📦 ОТКРЫТИЕ..."):
            time.sleep(0.8)
            
            # ADMIN BRAWLER CHECK (0.1% chance)
            if random.random() < 0.001 and "ADMIN" not in st.session_state.inv:
                st.session_state.inv["ADMIN"] = "👑"
                st.balloons()
                st.success("😱 НЕВЕРОЯТНО!!! ВЫ ВЫБИЛИ ADMIN BRAWLER!!! 👑")
                return

            # NORMAL BRAWLER CHECK
            if random.random() < chance:
                available = [b for b in ALL_BRAWLERS.keys() if b not in st.session_state.inv]
                if available:
                    new_b = random.choice(available)
                    st.session_state.inv[new_b] = ALL_BRAWLERS[new_b]
                    st.balloons()
                    st.success(f"🔥 НОВЫЙ БОЕЦ: {new_b}!")
                else:
                    st.session_state.gold += (cost * 2)
                    st.info("💰 Все бойцы собраны!")
            else:
                if is_mega:
                    st.session_state.gold += 12000
                    st.info("🍀 Боец не выпал, но вы получили 12,000 💰")
                else:
                    gain = random.randint(int(cost*0.5), int(cost*0.9))
                    st.session_state.gold += gain
                    st.toast(f"📦 +{gain} 💰")
    else:
        st.error(f"Недостаточно золота!")

# --- 6. UI ---
st.markdown("<h1 style='text-align:center;'>🔱 BRAWL STARS: ADMIN EDITION v19.7 🔱</h1>", unsafe_allow_html=True)

st.markdown(f"""<div class="status-bar">
    <span style="color:#f1c40f">💰 ЗОЛОТО: {st.session_state.gold:,}</span>
    <span style="color:#00d2ff">💎 ГЕМЫ: {st.session_state.gems}</span>
    <span style="color:#ffffff">🏆 КУБКИ: {st.session_state.trophies}</span>
</div>""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1.3])

with col1:
    st.header("🛒 МАГАЗИН")
    st.markdown("<div class='event-card'><small>ШАНС НА ADMIN: 0.1%</small><h3>💎 МЕГА УЛЬТРА ЯЩИК</h3><p>10,000 💰</p></div>", unsafe_allow_html=True)
    if st.button("ОТКРЫТЬ МЕГА ЯЩИК", use_container_width=True):
        open_box(10000, 0.5, is_mega=True); st.rerun()
    
    for c, n in [(500, "МАЛЫЙ"), (1000, "БОЛЬШОЙ"), (3000, "МЕГА")]:
        if st.button(f"КУПИТЬ {n} ({c} 💰)", key=f"shop_{c}", use_container_width=True):
            open_box(c, 0.1); st.rerun()

with col2:
    st.header("⚔️ АРЕНА")
    if st.button("🔥 НАЧАТЬ БОЙ (+100 💰 | +150 XP)", use_container_width=True, type="primary"):
        st.session_state.gold += 100
        st.session_state.xp += 150
        st.session_state.trophies += 10; st.rerun()
    
    st.write("---")
    st.subheader("💾 СОХРАНЕНИЕ / ВХОД")
    if st.button("СОЗДАТЬ КОД АККАУНТА", use_container_width=True):
        data = {k: v for k, v in st.session_state.items()}
        code = base64.b64encode(json.dumps(data).encode()).decode()
        st.code(code)

    input_code = st.text_input("ВСТАВЬТЕ КОД:")
    if st.button("ВОЙТИ В АККАУНТ", use_container_width=True):
        try:
            decoded = base64.b64decode(input_code).decode()
            data = json.loads(decoded)
            for k, v in data.items(): st.session_state[k] = v
            st.success("✅ Вход выполнен!"); st.rerun()
        except: st.error("❌ Ошибка!")

with col3:
    st.header("🎫 БРАВЛ ПАСС (30 LVL)")
    st.progress(min(st.session_state.xp/150000, 1.0))
    st.markdown("<div class='pass-panel'>", unsafe_allow_html=True)
    for i in range(1, 31):
        unlocked = st.session_state.xp >= i * 5000
        claimed = i in st.session_state.claimed
        status = "✅" if claimed else ("🎁" if unlocked else "🔒")
        st.write(f"Уровень {i}: {status}")
        if unlocked and not claimed:
            if st.button(f"Забрать {i}", key=f"c_{i}"):
                st.session_state.gold += 3000; st.session_state.claimed.append(i); st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

st.write("---")
st.header(f"👤 МОИ БОЙЦЫ ({len(st.session_state.inv)} / {len(ALL_BRAWLERS)+1})")
cols = st.columns(6)
for i, (name, icon) in enumerate(st.session_state.inv.items()):
    with cols[i % 6]:
        is_admin = "admin-brawler" if name == "ADMIN" else ""
        st.markdown(f"<div class='brawler-card {is_admin}'><h2>{icon}</h2><b>{name}</b></div>", unsafe_allow_html=True)
