import streamlit as st
import random
import time
import base64
import json

# --- 1. GLOBAL STYLING ---
st.set_page_config(page_title="RECKAT STARS: EVOLUTION", page_icon="🛸", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Syncopate:wght@700&display=swap');
    .stApp { background: #000205; color: #00ffcc; font-family: 'Orbitron', sans-serif; }
    .main-header { font-family: 'Syncopate', sans-serif; font-size: 55px; text-align: center; color: #00ffcc; text-shadow: 0 0 30px #00ffcc; padding: 20px; border-bottom: 2px solid #00ffcc; }
    .stat-box { background: rgba(0, 255, 204, 0.05); border: 1px solid #00ffcc; border-radius: 10px; padding: 15px; text-align: center; box-shadow: 0 0 10px rgba(0, 255, 204, 0.2); }
    .forge-card { background: #050505; border-left: 5px solid #6200ff; padding: 15px; margin-bottom: 10px; border-radius: 5px; }
    .battle-screen { background: black; border: 3px solid #ff0055; border-radius: 20px; padding: 40px; text-align: center; box-shadow: inset 0 0 100px #330011; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ENGINE & PERSISTENCE ---
# Brawlerlar o'rniga endi 'Ship Modules' (Kema modullari)
if 'gold' not in st.session_state:
    st.session_state.update({
        'gold': 0, 'gems': 0, 'xp': 0, 'level': 1,
        'modules': ["Engine v1"], 'claimed_milestones': [],
        'used_promos': [], 'in_warp': False, 'target_hp': 0
    })

def get_save_string():
    data = {
        "g": st.session_state.gold, "m": st.session_state.gems, 
        "x": st.session_state.xp, "l": st.session_state.level,
        "mod": st.session_state.modules, "cl": st.session_state.claimed_milestones,
        "up": st.session_state.used_promos
    }
    return base64.b64encode(json.dumps(data).encode()).decode()

def load_from_string(code):
    try:
        d = json.loads(base64.b64decode(code).decode())
        st.session_state.update({
            'gold':d['g'], 'gems':d['m'], 'xp':d['x'], 'level':d.get('l', 1),
            'modules':d['mod'], 'claimed_milestones':d['cl'], 'used_promos':d.get('up', [])
        })
        return True
    except: return False

# --- 3. MAIN UI ---
st.markdown("<div class='main-header'>RECKAT STARS: EVOLUTION</div>", unsafe_allow_html=True)

# Status Dashboard
c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f"<div class='stat-box'>💰 КРЕДИТЫ<br>{st.session_state.gold:,}</div>", unsafe_allow_html=True)
with c2: st.markdown(f"<div class='stat-box'>💎 КРИСТАЛЛЫ<br>{st.session_state.gems:,}</div>", unsafe_allow_html=True)
with c3: st.markdown(f"<div class='stat-box'>⭐ ОПЫТ (XP)<br>{st.session_state.xp:,}</div>", unsafe_allow_html=True)
with c4: st.markdown(f"<div class='stat-box'>🛸 МОДУЛИ<br>{len(st.session_state.modules)}/50</div>", unsafe_allow_html=True)

st.write("---")

col_main, col_side = st.columns([2, 1])

with col_main:
    st.header("🌌 КОСМИЧЕСКАЯ БИТВА")
    if not st.session_state.in_warp:
        st.info("Обнаружена вражеская станция в секторе RECKAT.")
        if st.button("🚀 АТАКОВАТЬ СТАНЦИЮ", use_container_width=True, type="primary"):
            st.session_state.in_warp = True
            st.session_state.target_hp = random.randint(50, 100)
            st.rerun()
    else:
        st.markdown("<div class='battle-screen'>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='font-size:80px;'>🛰️</h1>", unsafe_allow_html=True)
        st.write(f"ПРОЧНОСТЬ ЦЕЛИ: {st.session_state.target_hp}%")
        st.progress(st.session_state.target_hp / 100)
        
        if st.button("📡 ВЫСТРЕЛ ЛАЗЕРОМ", use_container_width=True):
            dmg = random.randint(5, 15)
            st.session_state.target_hp -= dmg
            if st.session_state.target_hp <= 0:
                st.session_state.in_warp = False
                reward = random.randint(500, 1200)
                st.session_state.gold += reward
                st.session_state.xp += 600
                st.balloons(); st.success(f"ЦЕЛЬ УНИЧТОЖЕНА! ПОЛУЧЕНО: {reward} КРЕДИТОВ")
                time.sleep(1.5)
            st.rerun()
        if st.button("🛑 ОТСТУПЛЕНИЕ", use_container_width=True):
            st.session_state.in_warp = False; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.write("---")
    st.header("🛠️ RECKAT FORGE (ПРОГРЕСС)")
    # Pass o'rniga darajali rivojlanish
    current_tier = st.session_state.xp // 10000
    st.write(f"ТЕКУЩИЙ ТЕХНО-УРОВЕНЬ: **{current_tier}**")
    
    for i in range(1, 21):
        unlocked = current_tier >= i
        claimed = i in st.session_state.claimed_milestones
        with st.container():
            col_f1, col_f2 = st.columns([3, 1])
            col_f1.markdown(f"<div class='forge-card'><b>УРОВЕНЬ {i}:</b> {'Доступно к улучшению' if unlocked else 'Заблокировано'}</div>", unsafe_allow_html=True)
            if unlocked and not claimed:
                if col_f2.button("УЛУЧШИТЬ", key=f"forge_{i}"):
                    st.session_state.gold += 2000
                    st.session_state.gems += 5
                    st.session_state.claimed_milestones.append(i)
                    st.session_state.modules.append(f"Module XP-{i}")
                    st.rerun()

with col_side:
    st.header("📡 КОМАНДНЫЙ ЦЕНТР")
    if st.button("📝 СОЗДАТЬ BACKUP-КОД", use_container_width=True):
        st.code(get_save_string())
    
    load_code = st.text_input("ВВОД КОДА ВОССТАНОВЛЕНИЯ:")
    if st.button("📥 ЗАГРУЗИТЬ ДАННЫЕ", use_container_width=True):
        if load_from_string(load_code): st.success("СИСТЕМА ВОССТАНОВЛЕНА"); st.rerun()
        else: st.error("ОШИБКА КОДА")

    st.write("---")
    st.header("🔄 ТРАНСФЕР")
    trans_amt = st.number_input("Кол-во:", min_value=1)
    trans_type = st.selectbox("Ресурс:", ["Кредиты", "Кристаллы"])
    if st.button("ГЕНЕРИРОВАТЬ 4-ЗНАЧНЫЙ КОД"):
        if (trans_type == "Кредиты" and st.session_state.gold >= trans_amt) or (trans_type == "Кристаллы" and st.session_state.gems >= trans_amt):
            if trans_type == "Кредиты": st.session_state.gold -= trans_amt
            else: st.session_state.gems -= trans_amt
            t_code = base64.b64encode(str(random.random()).encode()).decode()[:4].upper()
            st.success(f"КОД ПЕРЕДАЧИ: {t_code}")
        else: st.error("НЕДОСТАТОЧНО СРЕДСТВ")

    st.write("---")
    st.header("🔑 ТЕРМИНАЛ")
    promo = st.text_input("ПРОМОКОД:").strip()
    if st.button("ВВОД"):
        if promo == "REKCATv22" and "REKCATv22" not in st.session_state.used_promos:
            st.session_state.gold += 250; st.session_state.gems += 30
            st.session_state.used_promos.append("REKCATv22"); st.balloons()
        elif promo == "KHIVA90":
            st.session_state.gold += 9000; st.session_state.gems += 90; st.balloons()
        st.rerun()

st.write("---")
st.header(f"📦 АРСЕНАЛ МОДУЛЕЙ ({len(st.session_state.modules)})")
m_cols = st.columns(5)
for idx, m in enumerate(st.session_state.modules):
    with m_cols[idx % 5]:
        st.markdown(f"<div style='background:#111; border:1px solid #00ffcc; padding:10px; border-radius:5px; text-align:center;'>{m}</div>", unsafe_allow_html=True)
