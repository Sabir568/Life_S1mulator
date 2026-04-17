import streamlit as st
import random
import time
import base64
import json

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Brawl Stars GIFT", page_icon="💎", layout="wide")

# --- 2. SUPREME CSS ---
st.markdown("""
    <style>
    .stApp { background: #00050a; color: #00ffcc; font-family: 'Orbitron', sans-serif; }
    .status-bar { background: rgba(0,0,0,0.9); border: 2px solid #00ffcc; border-radius: 50px; padding: 15px; display: flex; justify-content: space-around; margin-bottom: 25px; }
    .event-card { background: linear-gradient(135deg, #ff0055 0, #6200ff 100%); border-radius: 20px; padding: 20px; text-align: center; border: 2px solid white; box-shadow: 0 0 20px rgba(255,0,85,0.4); margin-bottom: 15px; }
    .pass-panel { background: rgba(10, 0, 30, 0.85); border: 2px solid #6200ff; border-radius: 20px; padding: 20px; height: 500px; overflow-y: scroll; }
    .gift-panel { background: rgba(0, 255, 204, 0.1); border: 1px dashed #00ffcc; border-radius: 15px; padding: 15px; margin-top: 10px; }
    .brawler-card { background: #000; border: 1px solid #00ffcc; border-radius: 10px; padding: 10px; text-align: center; margin-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if 'gold' not in st.session_state:
    st.session_state.update({
        'gold': 0, 'gems': 100, 'trophies': 0, 'xp': 0,
        'inv': {"Шелли": {"pwr": 300, "icon": "🔫", "rank": "BRONZE III"}},
        'claimed': [], 'plus': False
    })

BRAWLERS_DB = {
    "Леон": {"icon": "🦎", "rank": "SILVER I"},
    "Ворон": {"icon": "🦅", "rank": "BRONZE II"},
    "Спайк": {"icon": "🌵", "rank": "GOLD I"},
    "Мортис": {"icon": "🦇", "rank": "BRONZE III"}
}

# --- 4. FUNCTIONS ---
def open_box(cost, chance, is_mega=False):
    if st.session_state.gold >= cost:
        st.session_state.gold -= cost
        with st.spinner("📦 ОТКРЫТИЕ..."):
            time.sleep(0.5)
            if random.random() < chance:
                new_b = random.choice([b for b in BRAWLERS_DB.keys() if b not in st.session_state.inv])
                if new_b:
                    st.session_state.inv[new_b] = BRAWLERS_DB[new_b]
                    st.balloons(); st.success(f"🔥 НОВЫЙ БОЕЦ: {new_b}!")
                else:
                    st.session_state.gold += (cost * 2)
            else:
                if is_mega: st.session_state.gold += 12000
                else: st.session_state.gold += random.randint(300, 800)
    else:
        st.error("Недостаточно золота!")

# --- 5. UI ---
st.markdown("<h1 style='text-align:center;'>🔱 BRAWL STARS: GIFT EDITION 🔱</h1>", unsafe_allow_html=True)

st.markdown(f"""<div class="status-bar">
    <span style="color:#f1c40f">💰 ЗОЛОТО: {st.session_state.gold:,}</span>
    <span style="color:#00d2ff">💎 ГЕМЫ: {st.session_state.gems}</span>
    <span style="color:#ffffff">🏆 КУБКИ: {st.session_state.trophies}</span>
</div>""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1.3])

with col1:
    st.header("🛒 МАГАЗИН")
    st.markdown("<div class='event-card'><h3>💎 МЕГА УЛЬТРА ЯЩИК</h3><p>10,000 💰</p></div>", unsafe_allow_html=True)
    if st.button("ОТКРЫТЬ МЕГА", use_container_width=True):
        open_box(10000, 0.5, is_mega=True); st.rerun()
    
    # Kristal ulashish bo'limi
    st.markdown("<div class='gift-panel'>", unsafe_allow_html=True)
    st.subheader("🎁 ПОДАРОК ДРУГУ")
    gift_amount = st.number_input("Сколько Гемов:", min_value=1, max_value=max(1, st.session_state.gems), step=1)
    if st.button("СОЗДАТЬ ПОДАРОК", use_container_width=True):
        if st.session_state.gems >= gift_amount:
            st.session_state.gems -= gift_amount
            # Sovg'a kodi faqat kristalni o'z ichiga oladi
            gift_data = {"gems_gift": gift_amount, "time": str(time.time())}
            gift_code = base64.b64encode(json.dumps(gift_data).encode()).decode()
            st.success(f"Код на {gift_amount} 💎 создан!")
            st.code(gift_code)
            st.info("Отправьте этот код другу!")
            time.sleep(1); st.rerun()
        else:
            st.error("Недостаточно Гемов!")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.header("⚔️ АРЕНА")
    if st.button("🔥 НАЧАТЬ БОЙ (+150 XP)", use_container_width=True, type="primary"):
        st.session_state.gold += 100
        st.session_state.xp += 150
        st.session_state.trophies += 10; st.rerun()
    
    st.write("---")
    st.subheader("💾 ДАННЫЕ & ЗАГРУЗКА")
    if st.button("СОХРАНИТЬ МОЙ ПРОГРЕСС"):
        data = {k: v for k, v in st.session_state.items()}
        st.code(base64.b64encode(json.dumps(data).encode()).decode())
    
    in_code = st.text_input("ВСТАВИТЬ КОД (Прогресс или Подарок):")
    if st.button("ПРИНЯТЬ / ЗАГРУЗИТЬ"):
        try:
            d = json.loads(base64.b64decode(in_code).decode())
            if "gems_gift" in d:
                st.session_state.gems += d["gems_gift"]
                st.balloons()
                st.success(f"🎁 Вы получили подарок: {d['gems_gift']} Гемов!")
                time.sleep(1.5); st.rerun()
            else:
                for k, v in d.items(): st.session_state[k] = v
                st.success("Прогресс загружен!"); st.rerun()
        except: st.error("Неверный код!")

with col3:
    st.header("🎫 БРАВЛ ПАСС (LVL 30)")
    st.progress(min((st.session_state.xp / 150000), 1.0))
    st.markdown("<div class='pass-panel'>", unsafe_allow_html=True)
    for i in range(1, 31):
        req = i * 5000
        st.write(f"Уровень {i}: {'✅' if i in st.session_state.claimed else ('🎁' if st.session_state.xp >= req else '🔒')}")
        if st.session_state.xp >= req and i not in st.session_state.claimed:
            if st.button(f"Забрать {i}", key=f"c_{i}"):
                st.session_state.gold += 3000
                st.session_state.claimed.append(i); st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

st.write("---")
st.header("👤 МОИ БОЙЦЫ")
cols = st.columns(4)
for i, (name, info) in enumerate(st.session_state.inv.items()):
    with cols[i % 4]:
        st.markdown(f"<div class='brawler-card'><h2>{info.get('icon')}</h2><b>{name}</b></div>", unsafe_allow_html=True)
