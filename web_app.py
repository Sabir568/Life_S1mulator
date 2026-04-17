import streamlit as st
import time

# Конфигурация страницы
st.set_page_config(page_title="Симулятор Миллионера 3.3", page_icon="💎", layout="wide")

# --- СУПЕР ДИЗАЙН (CSS) ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #020111, #191970);
        color: #ffffff;
    }
    .money-card {
        background: rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(20px);
        border: 2px solid #FFD700;
        border-radius: 25px;
        padding: 25px;
        text-align: center;
        margin-bottom: 35px;
        box-shadow: 0 10px 40px rgba(255, 215, 0, 0.2);
    }
    .money-text {
        font-size: 75px;
        font-weight: bold;
        color: #FFD700;
        text-shadow: 0 0 20px rgba(255, 215, 0, 0.6);
    }
    .shop-item {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 25px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        transition: 0.4s ease;
    }
    .shop-item:hover {
        transform: translateY(-10px);
        border-color: #FFD700;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5);
    }
    .item-img-container img {
        border-radius: 15px;
        height: 200px;
        object-fit: cover;
    }
    .inv-box {
        background: rgba(255, 215, 0, 0.1);
        border-radius: 15px;
        padding: 12px;
        margin-bottom: 10px;
        border-left: 6px solid #FFD700;
        color: #FFD700;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ЛОГИКА ИГРЫ ---
if 'money' not in st.session_state: st.session_state.money = 0
if 'click' not in st.session_state: st.session_state.click = 250
if 'income' not in st.session_state: st.session_state.income = 0
if 'inventory' not in st.session_state: st.session_state.inventory = []
if 'last_tick' not in st.session_state: st.session_state.last_tick = time.time()

# Авто-доход
now = time.time()
diff = int(now - st.session_state.last_tick)
if diff >= 1:
    st.session_state.money += diff * st.session_state.income
    st.session_state.last_tick = now

# --- ВЕРХНЯЯ ПАНЕЛЬ ---
st.markdown(f"""
    <div class='money-card'>
        <div style='font-size: 20px; color: #ccc; letter-spacing: 3px;'>ВАШЕ СОСТОЯНИЕ</div>
        <div class='money-text'>{st.session_state.money:,.0f} $</div>
    </div>
    """, unsafe_allow_html=True)

col_work, col_shop = st.columns([1, 2.5])

with col_work:
    st.header("💼 Работа")
    if st.button("РАБОТАТЬ 👷‍♂️", use_container_width=True):
        st.session_state.money += st.session_state.click
        st.rerun()
    
    st.success(f"Клик: +{st.session_state.click}$")
    st.info(f"Доход: +{st.session_state.income}$/сек")
    
    st.write("---")
    st.header("🏠 Мой Гараж")
    if not st.session_state.inventory:
        st.write("Гараж пока пуст...")
    else:
        for item in st.session_state.inventory:
            st.markdown(f"<div class='inv-box'>✔ {item}</div>", unsafe_allow_html=True)

with col_shop:
    st.header("🏪 Элитный Рынок")
    
    # ПРОВЕРЕННЫЕ ССЫЛКИ НА РЕАЛЬНЫЕ МОДЕЛИ
    items = [
        {"name": "Chevrolet Spark", "price": 10500, "img": "https://raw.githubusercontent.com/a-shox/uzb_cars/main/spark.jpg", "inc": 0},
        {"name": "Chevrolet Gentra", "price": 16500, "img": "https://raw.githubusercontent.com/a-shox/uzb_cars/main/gentra.jpg", "inc": 0},
        {"name": "Chevrolet Malibu 2", "price": 35000, "img": "https://raw.githubusercontent.com/a-shox/uzb_cars/main/malibu.jpg", "inc": 0},
        {"name": "Ресторан 'Milliy'", "price": 90000, "img": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=500", "inc": 350},
        {"name": "Вилла в горах", "price": 300000, "img": "https://images.unsplash.com/photo-1580587771525-78b9dba3b914?w=500", "inc": 1000},
        {"name": "Tashkent City Center", "price": 1500000, "img": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=500", "inc": 5000}
    ]

    cols = st.columns(2)
    for idx, item in enumerate(items):
        with cols[idx % 2]:
            st.markdown("<div class='shop-item'>", unsafe_allow_html=True)
            # Отображаем картинку через st.image для надежности
            st.image(item['img'], use_container_width=True)
            st.markdown(f"<h3 style='color: #FFD700;'>{item['name']}</h3>", unsafe_allow_html=True)
            st.write(f"Цена: **{item['price']:,} $**")
            
            if st.button(f"Купить {item['name']}", key=f"item_{idx}", use_container_width=True):
                if st.session_state.money >= item['price']:
                    st.session_state.money -= item['price']
                    st.session_state.inventory.append(item['name'])
                    st.session_state.income += item['inc']
                    st.balloons()
                    st.rerun()
                else:
                    st.error("Недостаточно денег!")
            st.markdown("</div>", unsafe_allow_html=True)

# Сброс
st.sidebar.markdown("### ⚙️ Настройки")
if st.sidebar.button("Начать заново 🔄"):
    st.session_state.clear()
    st.rerun()
