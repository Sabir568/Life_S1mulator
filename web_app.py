import streamlit as st
import time
import random

# Настройки сайта
st.set_page_config(page_title="Симулятор Магната 🏰", page_icon="💰", layout="wide")

# --- СТИЛИ (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    .money-display {
        font-size: 60px; font-weight: bold; color: #00FF00;
        text-align: center; border: 3px solid #00FF00;
        border-radius: 20px; padding: 10px; margin-bottom: 20px;
        background: rgba(0, 255, 0, 0.1);
    }
    .card {
        background-color: #1E1E1E; padding: 20px;
        border-radius: 15px; border: 1px solid #333;
        margin-bottom: 20px; text-align: center;
    }
    .img-fluid { border-radius: 10px; margin-bottom: 10px; width: 100%; height: 180px; object-fit: cover; }
    </style>
    """, unsafe_allow_html=True)

# --- СОСТОЯНИЕ ИГРЫ ---
if 'money' not in st.session_state: st.session_state.money = 0
if 'click_power' not in st.session_state: st.session_state.click_power = 100
if 'passive' not in st.session_state: st.session_state.passive = 0
if 'inventory' not in st.session_state: st.session_state.inventory = []
if 'last_time' not in st.session_state: st.session_state.last_time = time.time()

# Пассивный доход
now = time.time()
diff = now - st.session_state.last_time
if diff >= 1:
    st.session_state.money += int(diff * st.session_state.passive)
    st.session_state.last_time = now

# --- ВЕРХНЯЯ ПАНЕЛЬ ---
st.markdown(f"<div class='money-display'>{st.session_state.money:,.0f} $</div>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["💼 Работа", "🚗 Автосалон и Недвижимость", "🎰 Казино"])

# --- ВКЛАДКА 1: РАБОТА ---
with tab1:
    col_a, col_b = st.columns(2)
    with col_a:
        st.header("Заработок")
        if st.button("КЛИКАТЬ И ЗАРАБАТЫВАТЬ 💸", use_container_width=True):
            st.session_state.money += st.session_state.click_power
            st.rerun()
    with col_b:
        st.header("Статистика")
        st.write(f"Доход за клик: **{st.session_state.click_power} $**")
        st.write(f"Пассивный доход: **{st.session_state.passive} $/сек**")
        st.subheader("Моё имущество:")
        if not st.session_state.inventory: st.write("Пусто")
        for item in st.session_state.inventory: st.write(f"✅ {item}")

# --- ВКЛАДКА 2: МАГАЗИН ---
with tab2:
    items = [
        {"name": "Chevrolet Spark", "price": 12000, "img": "https://images.unsplash.com/photo-1541899481282-d53bffe3c35d?auto=format&fit=crop&q=80&w=400", "income": 0},
        {"name": "Chevrolet Gentra", "price": 18000, "img": "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?auto=format&fit=crop&q=80&w=400", "income": 0},
        {"name": "Chevrolet Malibu 2", "price": 35000, "img": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&q=80&w=400", "income": 0},
        {"name": "Ресторан в центре", "price": 100000, "img": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&q=80&w=400", "income": 200},
        {"name": "Пентхаус Tashkent City", "price": 250000, "img": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&q=80&w=400", "income": 500},
        {"name": "Частный Остров", "price": 1000000, "img": "https://images.unsplash.com/photo-1505881502353-a1986add3762?auto=format&fit=crop&q=80&w=400", "income": 2000},
    ]
    
    shop_cols = st.columns(3)
    for idx, item in enumerate(items):
        with shop_cols[idx % 3]:
            st.markdown(f"<div class='card'>", unsafe_allow_html=True)
            st.markdown(f"<img src='{item['img']}' class='img-fluid'>", unsafe_allow_html=True)
            st.write(f"### {item['name']}")
            st.write(f"Цена: **{item['price']:,} $**")
            if item['income'] > 0: st.write(f"Доход: +{item['income']}$/сек")
            
            if st.button(f"Купить", key=item['name']):
                if st.session_state.money >= item['price']:
                    st.session_state.money -= item['price']
                    st.session_state.inventory.append(item['name'])
                    st.session_state.passive += item['income']
                    st.balloons()
                    st.rerun()
                else:
                    st.error("Недостаточно денег!")
            st.markdown("</div>", unsafe_allow_html=True)

# --- ВКЛАДКА 3: КАЗИНО ---
with tab3:
    st.header("Удвой свои деньги или потеряй всё! 🎰")
    bet = st.number_input("Ваша ставка:", min_value=10, max_value=int(st.session_state.money) if st.session_state.money > 10 else 10)
    if st.button("КРУТИТЬ РУЛЕТКУ"):
        if st.session_state.money >= bet:
            if random.random() > 0.5:
                st.session_state.money += bet
                st.success(f"ВЫ ВЫИГРАЛИ! +{bet}$")
            else:
                st.session_state.money -= bet
                st.error(f"ВЫ ПРОИГРАЛИ! -{bet}$")
            st.rerun()
        else:
            st.error("У вас нет денег для ставки!")

# Сброс игры
if st.sidebar.button("Начать заново (Reset)"):
    st.session_state.clear()
    st.rerun()
