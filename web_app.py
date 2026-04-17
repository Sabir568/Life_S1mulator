import streamlit as st
import random
import time
import base64
import json

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Brawl Stars ADMIN FIX", page_icon="👑", layout="wide")

# --- 2. SUPREME CSS ---
st.markdown("""
    <style>
    .stApp { background: #00050a; color: #00ffcc; font-family: 'Orbitron', sans-serif; }
    .status-bar { background: rgba(0,0,0,0.9); border: 2px solid #00ffcc; border-radius: 50px; padding: 15px; display: flex; justify-content: space-around; margin-bottom: 25px; }
    .brawler-card { background: #000; border: 1px solid #00ffcc; border-radius: 10px; padding: 10px; text-align: center; margin-bottom: 5px; }
    .admin-card { border: 3px solid gold !important; box-shadow: 0 0 20px gold; color: gold !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if 'gold' not in st.session_state:
    st.session_state.update({
        'gold': 10000, 'gems': 600, 'trophies': 0, 'xp': 0,
        'inv': {"Шелли": "🔫"},
        'claimed': [], 'plus': False
    })

# --- 4. ADMIN RECOVERY FUNCTION ---
def restore_admin():
    st.session_state.inv["ADMIN"] = "👑"
    st.session_state.gold += 100000
    st.session_state.gems += 2000
    st.balloons()
    st.success("✅ ADMIN AKKAUNT TIKLANDI! 👑")

# --- 5. UI ---
st.sidebar.header("⚙️ ADMIN PANEL")
if st.sidebar.button("🛠 VOSSTANOVIT ADMINA"):
    restore_admin()

st.markdown("<h1 style='text-align:center;'>🔱 BRAWL STARS: RECOVERY v19.8 🔱</h1>", unsafe_allow_html=True)

# Status Bar
st.markdown(f"""<div class="status-bar">
    <span style="color:#f1c40f">💰 ЗОЛОТО: {st.session_state.gold:,}</span>
    <span style="color:#00d2ff">💎 ГЕМЫ: {st.session_state.gems}</span>
    <span style="color:#ffffff">🏆 КУБКИ: {st.session_state.trophies}</span>
</div>""", unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 1, 1.3])

with c1:
    st.header("🛒 МАГАЗИН")
    if st.button("МЕГА ЯЩИК (10,000 💰)", use_container_width=True):
        if st.session_state.gold >= 10000:
            st.session_state.gold -= 10000
            if random.random() < 0.1:
                st.session_state.inv["НОВЫЙ"] = "🔥"
                st.balloons()
            else: st.session_state.gold += 12000; st.rerun()

with c2:
    st.header("💾 СОХРАНЕНИЕ")
    if st.button("СОЗДАТЬ КОД"):
        data = {k: v for k, v in st.session_state.items()}
        code = base64.b64encode(json.dumps(data).encode()).decode()
        st.code(code)
    
    in_code = st.text_input("ВСТАВИТЬ КОД:")
    if st.button("ЗАГРУЗИТЬ"):
        try:
            d = json.loads(base64.b64decode(in_code).decode())
            for k, v in d.items(): st.session_state[k] = v
            st.success("OK!"); st.rerun()
        except: st.error("Ошибка в коде!")

with c3:
    st.header("👤 МОИ БОЙЦЫ")
    cols = st.columns(3)
    for i, (name, icon) in enumerate(st.session_state.inv.items()):
        with cols[i % 3]:
            cl = "admin-card" if name == "ADMIN" else ""
            st.markdown(f"<div class='brawler-card {cl}'><h2>{icon}</h2><b>{name}</b></div>", unsafe_allow_html=True)
