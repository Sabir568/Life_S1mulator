import streamlit as st
import random
import time
import base64
import json

# --- 1. GLOBAL STYLING (DARK LUXURY) ---
st.set_page_config(page_title="RECKAT LUXURY", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syncopate:wght@700&family=Inter:wght@400;700&display=swap');
    .stApp { background: #080808; color: #ffffff; font-family: 'Inter', sans-serif; }
    .main-header { font-family: 'Syncopate', sans-serif; font-size: 50px; text-align: center; color: #fff; text-shadow: 0 0 20px #6200ff; padding: 30px; border-bottom: 1px solid #333; }
    .luxury-card { background: #111; border: 1px solid #222; border-radius: 15px; padding: 0px; overflow: hidden; margin-bottom: 25px; transition: 0.4s; }
    .luxury-card:hover { border-color: #6200ff; transform: scale(1.02); }
    .price-tag { color: #00ffcc; font-weight: bold; font-size: 20px; padding: 10px; }
    .stat-box { background: rgba(255, 255, 255, 0.03); border: 1px solid #333; border-radius: 10px; padding: 15px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ASSETS DATA ---
CARS = [
    {"name": "BMW M3 G80", "price": 95000, "img": "https://images.unsplash.com/photo-1617531653332-bd46c24f2068?q=80&w=1000&auto=format&fit=crop"},
    {"name": "Porsche 911 GT3 RS", "price": 240000, "img": "https://images.unsplash.com/photo-1614162692292-7ac56d7f7f1e?q=80&w=1000&auto=format&fit=crop"},
    {"name": "Lamborghini Revuelto", "price": 600000, "img": "https://images.unsplash.com/photo-1691436442656-7883391d848f?q=80&w=1000&auto=format&fit=crop"},
    {"name": "Ferrari SF90", "price": 520000, "img": "https://images.unsplash.com/photo-1592198084033-aade902d1aae?q=80&w=1000&auto=format&fit=crop"}
]

HOUSES = [
    {"name": "Bel Air Mansion, LA", "price": 2500000, "img": "https://images.unsplash.com/photo-1613490493576-7fde63acd811?q=80&w=1000&auto=format&fit=crop"},
    {"name": "Beverly Hills Villa", "price": 4800000, "img": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?q=80&w=1000&auto=format&fit=crop"},
    {"name": "Malibu Oceanfront", "price": 7500000, "img": "https://images.unsplash.com/photo-1580587771525-78b9dba3b914?q=80&w=1000&auto=format&fit=crop"}
]

# --- 3. ENGINE (SAVE/LOAD TEGILMADI) ---
if 'gold' not in st.session_state:
    st.session_state.update({
        'gold': 0, 'gems': 0, 'xp': 0, 'used_promos': [],
        'inventory': []
    })

def get_save_code():
    data = {"g": st.session_state.gold, "m": st.session_state.gems, "x": st.session_state.xp, "up": st.session_state.used_promos, "inv": st.session_state.inventory}
    return base64.b64encode(json.dumps(data).encode()).decode()

def load_save_code(code):
    try:
        d = json.loads(base64.b64decode(code).decode())
        st.session_state.update({'gold':d['g'], 'gems':d['m'], 'xp':d['x'], 'used_promos':d['up'], 'inventory':d['inv']})
        return True
    except: return False

# --- 4. UI ---
st.markdown("<div class='main-header'>RECKAT LUXURY MARKET</div>", unsafe_allow_html=True)

# Dash
c1, c2, c3 = st.columns(3)
with c1: st.markdown(f"<div class='stat-box'>💵 BANK BALANCE<br>${st.session_state.gold:,}</div>", unsafe_allow_html=True)
with c2: st.markdown(f"<div class='stat-box'>💎 CRYSTALS<br>{st.session_state.gems:,}</div>", unsafe_allow_html=True)
with c3: st.markdown(f"<div class='stat-box'>⭐ TOTAL XP<br>{st.session_state.xp:,}</div>", unsafe_allow_html=True)

st.write("---")

tab1, tab2, tab3, tab4 = st.tabs(["🏎️ CAR SHOWROOM", "🏡 REAL ESTATE", "⚔️ MISSIONS", "⚙️ SYSTEM"])

with tab1:
    st.subheader("Exclusive Vehicles")
    cols = st.columns(2)
    for idx, car in enumerate(CARS):
        with cols[idx % 2]:
            st.markdown(f"""
            <div class='luxury-card'>
                <img src='{car['img']}' style='width:100%; height:250px; object-fit:cover;'>
                <div style='padding:15px;'>
                    <h3>{car['name']}</h3>
                    <p class='price-tag'>Price: ${car['price']:,}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"BUY {car['name']}", key=f"car_{idx}"):
                if st.session_state.gold >= car['price']:
                    st.session_state.gold -= car['price']
                    st.session_state.inventory.append(car['name'])
                    st.balloons(); st.success(f"Success! {car['name']} added to garage.")
                else: st.error("Insufficient funds!")

with tab2:
    st.subheader("Los Angeles Estates")
    for idx, house in enumerate(HOUSES):
        st.markdown(f"""
        <div class='luxury-card'>
            <img src='{house['img']}' style='width:100%; height:400px; object-fit:cover;'>
            <div style='padding:20px;'>
                <h2>{house['name']}</h2>
                <p class='price-tag'>Market Price: ${house['price']:,}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"PURCHASE {house['name']}", key=f"house_{idx}"):
            if st.session_state.gold >= house['price']:
                st.session_state.gold -= house['price']
                st.session_state.inventory.append(house['name'])
                st.balloons(); st.success(f"Welcome home! {house['name']} is yours.")
            else: st.error("Bank rejected the transaction. Not enough money.")

with tab3:
    st.subheader("Earn Money & XP")
    if st.button("💰 EXECUTE HIGH-STAKES MISSION (+$100| +25 XP)", use_container_width=True):
        st.session_state.gold += 100
        st.session_state.xp += 25
        st.toast("Mission Accomplished!"); time.sleep(0.5); st.rerun()

with tab4:
    st.subheader("Terminal & Recovery")
    sc1, sc2 = st.columns(2)
    with sc1:
        if st.button("📝 GENERATE SAVE CODE"): st.code(get_save_code())
        l_code = st.text_input("ENTER LOAD CODE:")
        if st.button("📥 RESTORE DATA"):
            if load_save_code(l_code): st.success("Data restored!"); st.rerun()
    with sc2:
        promo = st.text_input("PROMO CODE:").strip()
        if st.button("ACTIVATE"):
            if promo == "REKCATv22" and "REKCATv22" not in st.session_state.used_promos:
                st.session_state.gold += 250; st.session_state.gems += 30; st.session_state.used_promos.append("REKCATv22"); st.balloons()
            elif promo == "KHIVA90":
                st.session_state.gold += 9000; st.session_state.gems += 90; st.success("Bonus Activated!")
            elif promo == "APRIL2026":
                st.session_state.inventory.append("Sirius Edition"); st.success("Special Item Unlocked!")
            else: st.error("Invalid or already used code.")
            st.rerun()

st.write("---")
st.subheader(f"💼 MY ASSETS ({len(st.session_state.inventory)})")
if st.session_state.inventory:
    for item in st.session_state.inventory:
        st.write(f"• {item}")
else:
    st.info("Your asset list is empty. Start shopping!")
