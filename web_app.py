import streamlit as st
import random
import time

# Sayt sozlamalari
st.set_page_config(page_title="Matematik Duel ⚡", page_icon="🧮", layout="centered")

# --- STYLING (Saytni chiroyli qilish) ---
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
    }
    .score-box {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #FF4B4B;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- O'YIN MANTIQI ---
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'num1' not in st.session_state:
    st.session_state.num1 = random.randint(1, 10)
    st.session_state.num2 = random.randint(1, 10)
    st.session_state.op = random.choice(['+', '-', '*'])

def generate_new_question():
    st.session_state.num1 = random.randint(1, 15)
    st.session_state.num2 = random.randint(1, 15)
    st.session_state.op = random.choice(['+', '-', '*'])

# --- INTERFEYS ---
st.title("⚡ Tezkor Matematik Duel")
st.write(f"Sizning joriy balingiz: **{st.session_state.score}**")

# Savolni ko'rsatish
misol = f"{st.session_state.num1} {st.session_state.op} {st.session_state.num2}"
st.markdown(f"<div class='score-box'><h1>{misol} = ?</h1></div>", unsafe_allow_html=True)

# To'g'ri javobni hisoblash
if st.session_state.op == '+': correct_ans = st.session_state.num1 + st.session_state.num2
elif st.session_state.op == '-': correct_ans = st.session_state.num1 - st.session_state.num2
else: correct_ans = st.session_state.num1 * st.session_state.num2

# Javob kiritish
user_ans = st.number_input("Javobingizni yozing:", value=None, placeholder="Son kiriting...", step=1)

if st.button("Javobni tekshirish"):
    if user_ans == correct_ans:
        st.balloons()
        st.success("BARAKALLA! 🔥 +1 ball")
        st.session_state.score += 1
        generate_new_question()
        time.sleep(1) # Foydalanuvchi xursand bo'lishi uchun 1 soniya kutamiz
        st.rerun()
    else:
        st.error(f"Xato! To'g'ri javob {correct_ans} edi. ❌")
        st.session_state.score = 0 # Xato qilsa ball nolga tushadi
        st.info("O'yin qaytadan boshlanadi!")
        generate_new_question()
        time.sleep(2)
        st.rerun()

# Sidebar (Yon panel)
st.sidebar.title("O'yin haqida")
st.sidebar.write("Bu o'yin Python-da yaratildi.")
if st.sidebar.button("Ballarni nolga tushirish"):
    st.session_state.score = 0
    st.rerun()
