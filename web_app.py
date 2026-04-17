import streamlit as st
import random
import time

# --- SETUP ---
st.set_page_config(page_title="Brawl Stars 7.0 PRO", page_icon="📦", layout="wide")

# --- ULTRA DESIGN (CSS) ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #111, #001f3f, #1a0a2e);
        color: white;
    }
    .box-container {
        text-align: center;
        padding: 20px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 30px;
        border: 2px solid #333;
        transition: 0.5s;
        cursor: pointer;
    }
    .box-container:hover {
        transform: scale(1.1);
        border-color: #f1c40f;
        background: rgba(241, 196, 15, 0.1);
    }
    .box-img {
        width: 180px;
        filter: drop-shadow(0 0 10px rgba(0, 210, 255, 0.5));
    }
    .resource-card {
        background: rgba(0,0,0,0.6);
        border-radius: 50px;
        padding: 10px 30px;
        border: 2px solid #f1c40f;
        font-size: 22px;
        font-weight: bold;
        display: inline-block;
        margin: 10px;
    }
    .brawler-card {
        padding: 15px; border-radius: 20px; border: 2px solid;
        text-align: center; margin-bottom: 10px;
    }
    .legendary { border-color: #f1c40f; color: #f1c40f; box-shadow: 0 0 15px #f1c40f; }
    .mythic { border-color: #e74c3c; color: #e74c3c; }
    .epic { border-color: #9b59b6; color: #9b59b6; }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALIZATION ---
if 'coins' not in st.session_state: st.session_state.coins = 5000
if 'gems' not in st.session_state: st.session_state.gems = 200
if 'inv' not in st.session_state: st.session_state.inv = {}
if 'msg' not in st.session_state: st.session_state.msg = ""

BRAWLERS = {
    "Leon": "legendary", "Crow": "legendary", "Spike": "legendary",
    "Mortis": "mythic", "Tara": "mythic",
    "Edgar": "epic", "Bibi": "epic"
}

# --- FUNCTIONS ---
def open_box(box_type):
    with st.spinner('Ochilyapti...'):
        time.sleep(1)
    
    if random.random() < 0.3: # 30% yangi brawler
        new_b = random.choice(list(BRAWLERS.keys()))
        if new_b not in st.session_state.inv:
            st.session_state.inv[new_b] = BRAWLERS[new_b]
            st.session_state.msg = f"🔥 YANGI JANGCHI: {new_b.upper()}!"
            st.balloons()
        else:
            st.session_state.coins += 1000
            st.session_state.msg = f"Takroriy {new_b}! +1000 tanga berildi."
    else:
        reward = random.randint(200, 600)
        st.session_state.coins += reward
        st.session_state.msg = f"💰 Faqat tangalar: +{reward}"

# --- UI ---
st.markdown(f"""
    <div style='text-align: center;'>
        <div class='resource-card'>💰 {st.session_state.coins}</div>
        <div class='resource-card'>💎 {st.session_state.gems}</div>
    </div>
    """, unsafe_allow_html=True)

st.write("---")

col_shop, col_inv = st.columns([2, 1])

with col_shop:
    st.header("📦 BOX MARKET (Ustiga bosing!)")
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("<div class='box-container'>", unsafe_allow_html=True)
        # Big Box rasmi
        st.image("https://raw.githubusercontent.com/A-Shox/Brawl_Images/main/big_box.png", width=180)
        if st.button("BIG BOX (500 💰)", use_container_width=True):
            if st.session_state.coins >= 500:
                st.session_state.coins -= 500
                open_box("Big")
                st.rerun()
            else: st.error("Tangalar yetarli emas!")
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("<div class='box-container'>", unsafe_allow_html=True)
        # Mega Box rasmi
        st.image("https://raw.githubusercontent.com/A-Shox/Brawl_Images/main/mega_box.png", width=180)
        if st.button("MEGA BOX (80 💎)", use_container_width=True):
            if st.session_state.gems >= 80:
                st.session_state.gems -= 80
                open_box("Mega")
                st.rerun()
            else: st.error("Gemlar yetarli emas!")
        st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.msg:
        st.info(st.session_state.msg)
    
    st.write("---")
    if st.button("⚡ JANG QILISH (PUL TOPISH)", use_container_width=True):
        st.session_state.coins += 150
        st.rerun()

with col_inv:
    st.header("👤 JANGCHILARIM")
    if not st.session_state.inv:
        st.write("Hozircha hech kim yo'q.")
    else:
        for name, rarity in st.session_state.inv.items():
            st.markdown(f"<div class='brawler-card {rarity}'>{name} ({rarity})</div>", unsafe_allow_html=True)

# Settings
if st.sidebar.button("Reset Game"):
    st.session_state.clear()
    st.rerun()
