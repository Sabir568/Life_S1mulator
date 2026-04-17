import streamlit as st
import random
import time
import base64
import json

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Brawl Stars OMNI", page_icon="🔱", layout="wide")

# --- 2. CSS ---
st.markdown("""
    <style>
    .stApp { background: #00050a; color: #00ffcc; font-family: 'Orbitron', sans-serif; }
    .status-bar { background: rgba(0,0,0,0.9); border: 2px solid #00ffcc; border-radius: 50px; padding: 15px; display: flex; justify-content: space-around; margin-bottom: 25px; }
    .event-card { background: linear-gradient(135deg, #ff0055 0%, #6200ff 100%); border-radius: 20px; padding: 20px; text-align: center; border: 2px solid white; box-shadow: 0 0 20px rgba(255,0,85,0.4); }
    .box-card { background: #0a0a0a; border: 1px solid #333; border-radius: 15px; padding: 15px; text-align: center; }
    .brawler-card { background: #000; border: 1px solid #00ffcc; border-radius: 10px; padding: 10px; text-align: center; margin-bottom: 5px; }
    .rank-badge { background: #cd7f32; color: white; padding: 2px 5px; border-radius: 4px; font-size: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE INITIALIZATION ---
# Xavfsiz ishga tushirish (Initialization)
def init_state():
    defaults = {
        'gold': 0, 'gems': 0, 'trophies': 0, 'xp': 0,
        'inv': {"Шелли": {"lvl": 1, "pwr": 300, "icon": "🔫", "rank": "BRONZE III"}},
        'claimed': [], 'plus': False
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_state()

# --- 4. CORE LOGIC ---
def open_box(cost, chance):
    if st.session_state.gold >= cost:
        st.session_state.gold -= cost
        with st.spinner("📦 ОТКРЫТИЕ..."):
            time.sleep(0.5)
            if random.random() < chance:
                st.balloons()
                st.success("🔥 НОВЫЙ БОЕЦ!")
                st.session_state.gold += 500
            else:
                gain = random.randint(int(cost*0.4), int(cost*0.8))
                st.session_state.gold += gain
                st.toast(f"📦 +{gain} 💰")
    else:
        st.error(f"Недостаточно золота! Нужно {cost}")

# --- 5. UI LAYOUT ---
st.markdown("<h1 style='text-align:center;'>🔱 BRAWL STARS v19.1 🔱</h1>", unsafe_allow_html=True)

# Status Bar
st.markdown(f"""<div class="status-bar">
    <span>💰 {st.session_state.gold:,}</span>
    <span>💎 {st.session_state.gems}</span>
    <span>🏆 {st.session_state.trophies}</span>
</div>""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1.3])

with col1:
    st.header("🛒 SHOP")
    # Mega Box
    st.markdown("<div class='event-card'><h3>MEGA ULTRA</h3><p>10,000 💰</p><small>24 ЧАСА</small></div>", unsafe_allow_html=True)
    if st.button("OPEN MEGA BOX", use_container_width=True, key="m_btn"):
        open_box(10000, 0.6)
        st.rerun()
    
    st.write("---")
    for cost in [500, 1000, 3000]:
        st.markdown(f"<div class='box-card'><h4>BOX {cost}</h4></div>", unsafe_allow_html=True)
        if st.button(f"OPEN {cost}", key=f"shop_{cost}", use_container_width=True):
            open_box(cost, 0.1)
            st.rerun()

with col2:
    st.header("⚔️ ARENA")
    if st.button("🔥 START BATTLE (+100 💰)", use_container_width=True, type="primary"):
        st.session_state.gold += 100
        st.session_state.xp += 600
        st.session_state.trophies += 10
        st.rerun()
    
    st.write("---")
    st.subheader("💾 SAVE/LOAD")
    
    if st.button("GENERATE CODE"):
        try:
            data = {
                "gold": st.session_state.gold, "gems": st.session_state.gems,
                "xp": st.session_state.xp, "inv": st.session_state.inv,
                "plus": st.session_state.plus, "claimed": st.session_state.claimed,
                "trophies": st.session_state.trophies
            }
            code = base64.b64encode(json.dumps(data).encode()).decode()
            st.code(code)
        except Exception as e:
            st.error("Ошибка при создании кода!")

    input_code = st.text_input("PASTE CODE:", placeholder="Вставьте код...")
    if st.button("LOAD DATA"):
        if input_code:
            try:
                raw_data = base64.b64decode(input_code).decode()
                data = json.loads(raw_data)
                
                # Xavfsiz yuklash (har bir kalitni tekshirib)
                st.session_state.gold = data.get("gold", 0)
                st.session_state.gems = data.get("gems", 0)
                st.session_state.xp = data.get("xp", 0)
                st.session_state.inv = data.get("inv", {})
                st.session_state.plus = data.get("plus", False)
                st.session_state.claimed = data.get("claimed", [])
                st.session_state.trophies = data.get("trophies", 0)
                
                st.success("✅ Загружено!")
                time.sleep(0.5)
                st.rerun()
            except Exception:
                st.error("Неверный формат кода!")
        else:
            st.warning("Введите код!")

with col3:
    st.header("🎫 PASS")
    st.write(f"XP: {st.session_state.xp}/400k")
    st.progress(min(st.session_state.xp/400000, 1.0))
    
    st.write("---")
    st.header("👤 BRAWLERS")
    if st.session_state.inv:
        for b_name, b_info in st.session_state.inv.items():
            r = b_info.get('rank', 'BRONZE I')
            st.markdown(f"<div class='brawler-card'><span class='rank-badge'>{r}</span> <b>{b_name}</b></div>", unsafe_allow_html=True)

if st.sidebar.button("♻️ FULL RESET"):
    st.session_state.clear()
    st.rerun()
