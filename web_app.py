import streamlit as st
import random
import time

# --- KONFIGURATSIYA ---
st.set_page_config(page_title="Brawl Stars Universe", page_icon="🌠", layout="wide")

# --- ULTRA PREMIUM INTERFEYS (CSS) ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #050505 0%, #1a0a2e 100%);
        color: #e0e0e0;
    }
    .main-stat-card {
        background: rgba(255, 255, 255, 0.05);
        border: 2px solid #f1c40f;
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 0 25px rgba(241, 196, 15, 0.2);
    }
    .brawler-card {
        padding: 15px; border-radius: 20px; margin-bottom: 10px;
        border: 2px solid; text-align: center;
        transition: 0.4s ease-in-out;
    }
    .legendary { border-color: #f1c40f; background: rgba(241, 196, 15, 0.15); box-shadow: 0 0 20px #f1c40f; }
    .mythic { border-color: #e74c3c; background: rgba(231, 76, 60, 0.15); }
    .epic { border-color: #9b59b6; background: rgba(155, 89, 182, 0.15); }
    .rare { border-color: #2ecc71; background: rgba(46, 204, 113, 0.15); }
    
    .reward-box {
        background: rgba(0, 210, 255, 0.1);
        border: 1px dashed #00d2ff;
        padding: 10px; border-radius: 10px; margin-top: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- O'YIN MA'LUMOTLAR BAZASI ---
if 'coins' not in st.session_state: st.session_state.coins = 2000
if 'gems' not in st.session_state: st.session_state.gems = 150
if 'trophies' not in st.session_state: st.session_state.trophies = 0
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'inv' not in st.session_state: 
    st.session_state.inv = {"Shelly": {"lvl": 1, "power": 120, "rarity": "rare", "star_power": False}}
if 'battle_log' not in st.session_state: st.session_state.battle_log = []

BRAWLERS_LIB = {
    "Leon": {"rarity": "legendary", "base_pwr": 450},
    "Crow": {"rarity": "legendary", "base_pwr": 430},
    "Spike": {"rarity": "legendary", "base_pwr": 460},
    "Mortis": {"rarity": "mythic", "base_pwr": 350},
    "Tara": {"rarity": "mythic", "base_pwr": 340},
    "Edgar": {"rarity": "epic", "base_pwr": 280},
    "Frank": {"rarity": "epic", "base_pwr": 300},
    "Colt": {"rarity": "rare", "base_pwr": 180},
    "Poco": {"rarity": "rare", "base_pwr": 160}
}

# --- FUNKSIYALAR (LOGIKA) ---
def start_battle():
    # Jang logikasi: Brawlerlar soni va umumiy kuchga asoslangan
    total_pwr = sum(b['power'] for b in st.session_state.inv.values())
    difficulty = random.randint(100, 1000)
    
    if total_pwr + random.randint(0, 500) > difficulty:
        t_win = random.randint(10, 25)
        c_win = random.randint(50, 150)
        st.session_state.trophies += t_win
        st.session_state.coins += c_win
        st.session_state.xp += 40
        msg = f"🏆 POBEDA! +{t_win} kubok, +{c_win} tanga"
        st.balloons()
    else:
        t_loss = random.randint(5, 15)
        st.session_state.trophies = max(0, st.session_state.trophies - t_loss)
        msg = f"❌ MAG'LUBIYAT! -{t_loss} kubok"
    
    st.session_state.battle_log.insert(0, f"[{time.strftime('%H:%M')}] {msg}")

def open_omega_box():
    # Eng kuchli keys logikasi
    st.session_state.gems -= 120
    if random.random() < 0.6: # 60% yangi brawler
        potential = [name for name in BRAWLERS_LIB if name not in st.session_state.inv]
        if potential:
            name = random.choice(potential)
            st.session_state.inv[name] = {
                "lvl": 1, 
                "power": BRAWLERS_LIB[name]['base_pwr'], 
                "rarity": BRAWLERS_LIB[name]['rarity'],
                "star_power": False
            }
            return f"🔥 NEW BRAWLER: {name}!"
    st.session_state.coins += random.randint(1000, 3000)
    return "💰 OMEGA REWARD: 2500+ Coins!"

# --- ASOSIY EKRAN ---
st.markdown(f"""
    <div class='main-stat-card'>
        <h1 style='color: #f1c40f;'>⭐ BRAWL STARS UNIVERSE ⭐</h1>
        <div style='display: flex; justify-content: space-around; font-size: 24px;'>
            <span>💰 {st.session_state.coins}</span>
            <span>💎 {st.session_state.gems}</span>
            <span>🏆 {st.session_state.trophies}</span>
            <span>✨ XP: {st.session_state.xp}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.write("---")

col_left, col_mid, col_right = st.columns([1, 1.2, 1])

# --- CHAP KOLONNA: JANG VA SHOP ---
with col_left:
    st.header("⚔️ BATTLE MODE")
    if st.button("🚀 PLAY SHOWDOWN", use_container_width=True):
        start_battle()
        st.rerun()
    
    st.write("---")
    st.header("🏪 MEGA SHOP")
    if st.button("🔵 OMEGA BOX (120 💎)", use_container_width=True):
        if st.session_state.gems >= 120:
            res = open_omega_box()
            st.success(res)
            time.sleep(1)
            st.rerun()
        else: st.error("Gems yetarli emas!")
    
    if st.button("🎁 DAILY GIFT", use_container_width=True):
        st.session_state.coins += 100
        st.toast("Sizga 100 tanga berildi!")

# --- O'RTA KOLONNA: TROPHY ROAD & LOGS ---
with col_mid:
    st.header("🛣️ TROPHY ROAD")
    progress = min(st.session_state.trophies / 10000, 1.0)
    st.progress(progress)
    st.write(f"Keyingi maqsad: {((st.session_state.trophies // 500) + 1) * 500} 🏆")
    
    st.write("---")
    st.subheader("📝 BATTLE LOGS")
    for log in st.session_state.battle_log[:8]:
        st.markdown(f"<div class='reward-box'>{log}</div>", unsafe_allow_html=True)

# --- O'NG KOLONNA: BRAWLERS & UPGRADES ---
with col_right:
    st.header("👤 MY BRAWLERS")
    for name, data in st.session_state.inv.items():
        st.markdown(f"""
            <div class='brawler-card {data['rarity']}'>
                <h3 style='margin:0;'>{name}</h3>
                <small>{data['rarity'].upper()}</small><br>
                <b>LVL: {data['lvl']}</b> | PWR: {data['power']}
            </div>
        """, unsafe_allow_html=True)
        
        # Upgrade Logikasi
        cost = data['lvl'] * 400
        if st.button(f"⚡ UPGRADE ({cost} 💰)", key=f"up_{name}"):
            if st.session_state.coins >= cost:
                st.session_state.coins -= cost
                st.session_state.inv[name]['lvl'] += 1
                st.session_state.inv[name]['power'] += 60
                st.rerun()
            else: st.error("Tangalar yetarli emas!")

# --- SIDEBAR ---
with st.sidebar:
    st.title("⚙️ SETTINGS")
    if st.button("RESET DATA"):
        st.session_state.clear()
        st.rerun()
    st.write("---")
    st.info("Bu o'yinning 6.0 Universe versiyasi. Jang qilish orqali XP va kubok yig'ing!")
