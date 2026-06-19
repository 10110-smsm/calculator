import streamlit as st
import math
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="간단 공학용 계산기", page_icon="🧮")

st.title("🧮 간단 공학용 계산기 + 그래프")

# =========================
# 상태
# =========================
if "expr" not in st.session_state:
    st.session_state.expr = ""

# =========================
# 각도 모드
# =========================
mode = st.radio("각도", ["DEG", "RAD"], horizontal=True)

def convert(x):
    return math.radians(x) if mode == "DEG" else x

# =========================
# 안전 함수
# =========================
safe_dict = {
    "pi": math.pi,
    "e": math.e,

    "sin": lambda x: math.sin(convert(x)),
    "cos": lambda x: math.cos(convert(x)),
    "tan": lambda x: math.tan(convert(x)),
}

# =========================
# 입력창
# =========================
st.text_input("계산식", value=st.session_state.expr, disabled=True)

def add(x):
    st.session_state.expr += x

st.write("---")

# =========================
# 버튼
# =========================
c1, c2, c3, c4 = st.columns(4)

with c1:
    if st.button("7"): add("7")
    if st.button("4"): add("4")
    if st.button("1"): add("1")
    if st.button("0"): add("0")

with c2:
    if st.button("8"): add("8")
    if st.button("5"): add("5")
    if st.button("2"): add("2")
    if st.button("."): add(".")

with c3:
    if st.button("9"): add("9")
    if st.button("6"): add("6")
    if st.button("3"): add("3")
    if st.button("pi"): add("pi")

with c4:
    if st.button("+"): add("+")
    if st.button("-"): add("-")
    if st.button("*"): add("*")
    if st.button("/"): add("/")

st.write("---")

# 삼각함수 + 상수
c1, c2, c3, c4 = st.columns(4)

with c1:
    if st.button("sin"): add("sin(")
with c2:
    if st.button("cos"): add("cos(")
with c3:
    if st.button("tan"): add("tan(")
with c4:
    if st.button("e"): add("e")

# =========================
# 계산
# =========================
if st.button("= 계산"):

    try:
        result = eval(
            st.session_state.expr,
            {"__builtins__": None},
            safe_dict
        )

        st.success(f"결과: {result}")

    except Exception as e:
        st.error(e)

st.write("---")

# =========================
# 그래프
# =========================
st.subheader("📈 함수 그래프")

func = st.text_input("함수 입력 (예: sin(x), x**2, cos(x))", "sin(x)")

xmin = st.number_input("x 최소", value=-10.0)
xmax = st.number_input("x 최대", value=10.0)

if st.button("그래프 그리기"):

    x = np.linspace(xmin, xmax, 1000)

    safe_graph = {
        "x": x,
        "pi": np.pi,
        "e": np.e,
        "sin": np.sin,
        "cos": np.cos,
        "tan": np.tan,
    }

    try:
        y = eval(func, {"__builtins__": None}, safe_graph)

        fig, ax = plt.subplots()
        ax.plot(x, y)

        ax.axhline(0, color="black")
        ax.axvline(0, color="black")
        ax.grid(True)

        st.pyplot(fig)

    except Exception as e:
        st.error(f"그래프 오류: {e}")
