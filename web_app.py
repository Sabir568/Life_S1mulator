import streamlit as st
import random
import time
import base64
import json

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Brawl Stars: 50 LVL Pass", page_icon="⚔️", layout="wide")

# --- 2. CSS ---
st.markdown("""
    <style>
    .stApp { background: #000814; color: #ffffff; font-family: 'Arial'; }
    .status-bar { background: rgba(0,0,0,0.9); border: 2px solid #00ffcc; border-radius: 15px; padding: 15px; display: flex; justify-content: space-around; margin-bottom: 20px; font-weight: bold; }
    .pass-panel { background: #050505; border: 2px solid #6200ff; border-radius: 15px; padding: 15px; height: 600px; overflow-y: scroll; }
    .tier-box { background: #111; border: 1px solid #333; border-radius: 10px; padding: 10px; margin-bottom: 10px; }
    .plus-label { color: #ff00ff; font-weight: bold; font-size: 12px; }
    .brawler-item { background: #111; border: 1px solid #333; border-radius: 8px; padding: 5px; text-align: center; font-size: 11px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BRAWLERS DATABASE ---
B_DB = [
    "Шелли", "Нита", "Кольт", "Булл", "Брок", "Эль Примо", "Барли", "Поко", "Роза", "Рико", "Дэррил", "Пенни", "Карл", "Джекки", 
    "Пайпер", "Пэм", "Фрэнк", "Биби", "Беа", "Нани", "Эдгар", "Грифф", "Гром", "Бонни", "Мортис", "Тара", "Джин", "Макс", 
    "Мистер П.", "Спраут", "Байрон", "Скуик", "Спайк", "Ворон", "Леон", "Сэнди", "Амбер", "Мэг", "Гейл", "Вольт", "Колетт", 
    "Лу", "Гавс", "Белль", "Базз", "Эш", "Лола", "Фэнг", "Ева", "Джанет", "Отис", "Сэм", "Бастер", "Мэнди", "Р-Т", "Мэйси", 
    "Хэнк", "Корделиус", "Даг", "Чак", "Мико", "Кит", "Ларри", "Лоури", "Анджело", "Мелоди", "Лили", "Драко", "Клэнси", 
    "Берри", "Кэндзи", "Мо", "Сириус", "Джуджу", "Шад", "Гас", "Честер", "Грей"
]

# --- 4. SESSION STATE ---
if 'gold' not in st.session_state:
    st.session_state.update({
        'gold': 0, 'gems': 0, 'xp': 0,
        'inv': ["Шелли"],
        'claimed': [], 'pass_type': 'Free'
    })

# --- 5. LOGIC ---
def open_box(cost):
    if st.session_state.gold >= cost:
        st.session_state.gold -= cost
        rand = random.random()
        if cost == 1000:
            if rand < 0.05:
                new = random.choice([b for b in B_DB if b not in st.session_state.inv])
                if new: st.session_state.inv.append(new); st.balloons()
            elif rand < 0.15: st.session_state.xp += 300
            else: st.session_state.gold += 250
        elif cost == 5000:
            if rand < 0.15:
                new = random.choice([b for b in B_DB if b not in st.session_state.inv])
                if new: st.session_state.inv.append(new); st.balloons()
            elif rand < 0.30: st.session_state.xp += 1000
            else: st.session_state.gold += 2000
    else: st.error("Недостаточно золота!")

# --- 6. UI ---
st.markdown("<h1 style='text-align:center;'>🔱 BRAWL STARS: 50 LVL EVOLUTION</h1>", unsafe_allow_html=True)

st.markdown(f"""<div class="status-bar">
    <span style="color:#f1c40f">💰 ЗОЛОТО: {st.session_state.gold:,}</span>
    <span style="color:#00d2ff">💎 ГЕМЫ: {st.session_state.gems:,}</span>
    <span style="color:#ffffff">🏆 XP: {st.session_state.xp:,}</span>
</div>""", unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 1, 1.2])

with c1:
    st.header("🛒 МАГАЗИН")
    if st.button("МАЛЫЙ ЯЩИК (1,000 💰)", use_container_width=True):
        open_box(1000); st.rerun()
    if st.button("БОЛЬШОЙ ЯЩИК (5,000 💰)", use_container_width=True):
        open_box(5000); st.rerun()
    
    st.write("---")
    if st.button("⚔️ В БОЙ (+80 💰 | +150 XP)", use_container_width=True, type="primary"):
        st.session_state.gold += 80
        st.session_state.xp += 150; st.rerun()
    
    # PROMO
    promo = st.text_input("Промокод:")
    if st.button("OK"):
        if promo == "APRIL2026":
            if "Сириус" not in st.session_state.inv:
                st.session_state.inv.append("Сириус"); st.balloons()
        st.rerun()

with c2:
    st.header("💾 АККАУНТ")
    if st.button("ПОЛУЧИТЬ КОД"):
        save_data = {'gold': st.session_state.gold, 'gems': st.session_state.gems, 'xp': st.session_state.xp, 'inv': st.session_state.inv, 'claimed': st.session_state.claimed, 'pass': st.session_state.pass_type}
        st.code(base64.b64encode(json.dumps(save_data).encode()).decode())

    in_code = st.text_input("ВСТАВИТЬ КОД:")
    if st.button("ЗАГРУЗИТЬ"):
        try:
            d = json.loads(base64.b64decode(in_code).decode())
            st.session_state.update({'gold':d['gold'], 'gems':d['gems'], 'xp':d['xp'], 'inv':d['inv'], 'claimed':d['claimed'], 'pass_type':d['pass']})
            st.success("OK!"); st.rerun()
        except: st.error("Error")

    st.write("---")
    st.header("👤 КОЛЛЕКЦИЯ")
    st.write(f"Бойцы: {len(st.session_state.inv)} / 78")
    cols = st.columns(3)
    for i, name in enumerate(st.session_state.inv[-6:]): # Oxirgi 6 tasini ko'rsatish
        with cols[i % 3]: st.markdown(f"<div class='brawler-item'>{name}</div>", unsafe_allow_html=True)

with c3:
    st.header("🎫 BRAWL PASS (50 LVL)")
    current_lvl = st.session_state.xp // 15000
    st.write(f"Ваш уровень: **{current_lvl} / 50**")
    st.progress(min(current_lvl/50, 1.0))
    
    if st.session_state.pass_type == 'Free':
        if st.button("💎 КУПИТЬ PLUS (499 ГЕМОВ)", use_container_width=True):
            if st.session_state.gems >= 499:
                st.session_state.gems -= 499; st.session_state.pass_type = 'Plus'; st.rerun()
    else:
        st.success("🎫 BRAWL PASS PLUS АКТИВИРОВАН")

    st.markdown("<div class='pass-panel'>", unsafe_allow_html=True)
    for i in range(1, 51):
        unlocked = current_lvl >= i
        claimed = i in st.session_state.claimed
        status = "✅" if claimed else ("🎁" if unlocked else "🔒")
        
        with st.container():
            st.markdown(f"**Уровень {i}** {status}")
            if unlocked and not claimed:
                if st.button(f"Забрать {i}", key=f"get_{i}"):
                    # Tekin mukofot
                    st.session_state.gold += 800
                    st.session_state.gems += 5
                    
                    # Plus mukofot (Agar Plus bo'lsa)
                    if st.session_state.pass_type == 'Plus':
                        st.session_state.gold += 2000 # Qo'shimcha oltin
                        st.session_state.gems += 25   # Qo'shimcha gems
                        if i % 10 == 0: # Har 10-levelda tasodifiy brawler
                            new_b = random.choice(B_DB)
                            if new_b not in st.session_state.inv:
                                st.session_state.inv.append(new_b)
                    
                    st.session_state.claimed.append(i); st.rerun()
            st.markdown("---")
    st.markdown("</div>", unsafe_allow_html=True)
