import streamlit as st
import time

# Конфигурация
st.set_page_config(page_title="Luxury Magnat", page_icon="🏎️", layout="wide")

# --- СТИЛЬ И ФОН ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #000000, #1a1a1a, #001f3f);
        color: #ffffff;
    }
    .money-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid #00d2ff;
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 0 15px rgba(0, 210, 255, 0.3);
    }
    .money-text {
        font-size: 50px;
        font-weight: bold;
        color: #00d2ff;
    }
    .shop-card {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 15px;
        padding: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        transition: 0.3s;
    }
    .shop-card:hover {
        border-color: #00d2ff;
        transform: translateY(-5px);
    }
    .inv-item {
        background: rgba(0, 210, 255, 0.1);
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 5px;
        border-left: 4px solid #00d2ff;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ЛОГИКА ---
if 'money' not in st.session_state: st.session_state.money = 0
if 'click' not in st.session_state: st.session_state.click = 10 # Pul topish qiyinroq (10$)
if 'income' not in st.session_state: st.session_state.income = 0
if 'inv' not in st.session_state: st.session_state.inv = []
if 'last_t' not in st.session_state: st.session_state.last_t = time.time()

# Пассивный доход
now = time.time()
diff = int(now - st.session_state.last_t)
if diff >= 1:
    st.session_state.money += diff * st.session_state.income
    st.session_state.last_t = now

# --- ИНТЕРФЕЙС ---
st.markdown(f"""
    <div class='money-card'>
        <div style='color: #888;'>ТЕКУЩИЙ БАЛАНС</div>
        <div class='money-text'>{st.session_state.money:,.0f} $</div>
    </div>
    """, unsafe_allow_html=True)

c1, c2 = st.columns([1, 2.5])

with c1:
    st.header("💼 Работа")
    if st.button("ЗАРАБОТАТЬ 💵", use_container_width=True):
        st.session_state.money += st.session_state.click
        st.rerun()
    
    st.write(f"За клик: **{st.session_state.click}$**")
    st.write(f"В секунду: **{st.session_state.income}$**")
    
    st.write("---")
    st.header("📦 Гараж")
    if not st.session_state.inv:
        st.write("У вас нет имущества")
    else:
        for item in st.session_state.inv:
            st.markdown(f"<div class='inv-item'>✅ {item}</div>", unsafe_allow_html=True)

with c2:
    st.header("🏁 Автосалон и Бизнес")
    
    # Список крутых машин и недвижимости
    store = [
        {"name": "BMW 3 G20", "price": 45000, "img": "https://images.unsplash.com/photo-1555215695-3004980ad54e?w=500", "inc": 50},
        {"name": "BMW M5 CS", "price": 140000, "img": "https://images.unsplash.com/photo-1619362227493-270bb3f07a7c?w=500", "inc": 200},
        {"name": "Mercedes G-Class", "price": 250000, "img": "https://images.unsplash.com/photo-1520031441872-265e4ff70366?w=500", "inc": 500},
        {"name": "Mercedes GT63 S", "price": 180000, "img": "https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?w=500", "inc": 350},
        {"name": "Автосервис Tuning", "price": 500000, "img": "https://images.unsplash.com/photo-1486006920555-c77dcf18193c?w=500", "inc": 1500},
        {"name": "Небоскреб Офис", "price": 2000000, "img": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=500", "inc": 10000}
    ]

    scols = st.columns(2)
    for idx, item in enumerate(store):
        with scols[idx % 2]:
            st.markdown("<div class='shop-card'>", unsafe_allow_html=True)
            st.image(item['img'], use_container_width=True)
            st.markdown(f"<h3>{item['name']}</h3>", unsafe_allow_html=True)
            st.write(f"Цена: **{item['price']:,} $**")
            st.write(f"Доход: **+{item['inc']}$/сек**")
            
            if st.button(f"Купить {item['name']}", key=f"b_{idx}", use_container_width=True):
                if st.session_state.money >= item['price']:
                    st.session_state.money -= item['price']
                    st.session_state.inv.append(item['name'])
                    st.session_state.income += item['inc']
                    st.balloons()
                    st.rerun()
                else:
                    st.error("Недостаточно средств!")
            st.markdown("</div>", unsafe_allow_html=True)

# Очистка
if st.sidebar.button("Сбросить игру"):
    st.session_state.clear()
    st.rerun()
