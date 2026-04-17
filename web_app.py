import streamlit as st
import random
import time

# --- KONFIGURATSIYA ---
st.set_page_config(page_title="Brawl Stars 8.0", page_icon="⭐", layout="wide")

# --- ULTRA MODERN CSS ---
st.markdown("""
    <style>
    /* Fon va umumiy uslub */
    .stApp {
        background: radial-gradient(circle, #1a1a2e 0%, #16213e 100%);
        color: white;
    }
    
    /* Resurslar paneli */
    .stat-bar {
        background: rgba(0, 0, 0, 0.6);
        border: 2px solid #f1c40f;
        border-radius: 50px;
        padding: 10px 25px;
        display: inline-block;
        margin: 10px;
        font-weight: bold;
        font-size: 22px;
        box-shadow: 0 0 15px rgba(241, 196, 15, 0.3);
    }

    /* Box interfeysi */
    .box-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 30px;
        padding: 30px;
        text-align: center;
        border: 2px solid transparent;
        transition: 0.4s;
    }
    .box-card:hover {
        border-color: #00d2ff;
        transform: translateY(-10px);
        background: rgba(255, 255, 255, 0.1);
    }
    
    /* Brawler kartochkalari */
    .brawler-unit {
        background: rgba(0, 0, 0, 0.4);
        border-radius: 15px;
        padding: 10px;
        margin: 5px;
        border-left: 5px solid #f1c40f;
        text-align: left;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIKA ---
if 'coins' not in st.session_state: st.session_state.coins = 3000
if 'gems' not in st.session_state: st.session_state.gems = 150
if 'inv' not in st.session_state: st.session_state.inv = []
if 'last_reward' not in st.session_state: st.session_state.last_reward = ""

# Yangi brawlerlar bazasi
BRAWLERS_DATA = {
    "Leon": "Legendary", "Crow": "Legendary", "Spike": "Legendary",
    "Mortis": "Mythic", "Tara": "Mythic", "Gene": "Mythic",
    "Edgar": "Epic", "Frank": "Epic", "Bibi": "Epic"
}

def open_logic(box_name):
    st.session_state.last_reward = "Ochilyapti..."
    # Haqiqiy ochilish effekti uchun animatsiya kutish
    time.sleep(0.8)
    
    chance = 0.4 if box_name == "Mega" else 0.2
    if random.random() < chance:
        new_b = random.choice(list(BRAWLERS_DATA.keys()))
        if new_b not in st.session_state.inv:
            st.session_state.inv.append(new_b)
            st.session_state.last_reward = f"🔥 YANGI JANGCHI: {new_b.upper()}!"
            st.balloons()
        else:
            bonus = random.randint(500, 1000)
            st.session_state.coins += bonus
            st.session_state.last_reward = f"Takroriy {new_b}! +{bonus} tanga."
    else:
        reward = random.randint(150, 450)
        st.session_state.coins += reward
        st.session_state.last_reward = f"💰 Faqat tangalar: +{reward}"

# --- ASOSIY UI ---
st.markdown(f"""
    <div style='text-align: center;'>
        <div class='stat-bar'>💰 {st.session_state.coins:,}</div>
        <div class='stat-bar'>💎 {st.session_state.gems}</div>
    </div>
    """, unsafe_allow_html=True)

col_shop, col_inv = st.columns([2, 1])

with col_shop:
    st.header("🛒 BOX MARKET")
    
    s1, s2 = st.columns(2)
    
    with s1:
        st.markdown("<div class='box-card'>", unsafe_allow_html=True)
        # Big Box uchun barqaror havola
        st.image("https://img.icons8.com/color/160/gift-box.png", caption="BIG BOX")
        if st.button("OCHISH (400 💰)", use_container_width=True, key="big"):
            if st.session_state.coins >= 400:
                st.session_state.coins -= 400
                open_logic("Big")
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with s2:
        st.markdown("<div class='box-card'>", unsafe_allow_html=True)
        # Mega Box uchun barqaror havola
        st.image("https://img.icons8.com/color/160/treasure-chest.png", caption="MEGA BOX")
        if st.button("OCHISH (60 💎)", use_container_width=True, key="mega"):
            if st.session_state.gems >= 60:
                st.session_state.gems -= 60
                open_logic("Mega")
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.last_reward:
        st.info(st.session_state.last_reward)
    
    st.write("---")
    if st.button("⚔️ JANG QILIB PUL TOPISH", use_container_width=True):
        st.session_state.coins += random.randint(50, 150)
        st.rerun()

with col_inv:
    st.header("👤 JANGCHILARIM")
    if not st.session_state.inv:
        st.write("Hozircha bo'sh...")
    else:
        for b in st.session_state.inv:
            rarity = BRAWLERS_DATA.get(b, "Common")
            st.markdown(f"""
                <div class='brawler-unit'>
                    <b>{b}</b><br>
                    <small style='color: #f1c40f;'>{rarity}</small>
                </div>
            """, unsafe_allow_html=True)

# Reset
if st.sidebar.button("Tozalash (Reset)"):
    st.session_state.clear()
    st.rerun()
