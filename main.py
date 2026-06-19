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

# store last result to avoid re-evaluating repeatedly
if "result" not in st.session_state:
    st.session_state.result = None

# =========================
# 각도 모드
# =========================
mode = st.radio("각도", ["DEG", "RAD"], horizontal=True)

def convert(x):
    return math.radians(x) if mode == "DEG" else x

# =========================
# 안전 함수 (계산기)
# =========================
safe_dict = {
    "pi": math.pi,
    "e": math.e,

    # wrap trig to respect DEG/RAD mode
    "sin": lambda x: math.sin(convert(x)),
    "cos": lambda x: math.cos(convert(x)),
    "tan": lambda x: math.tan(convert(x)),
}

# =========================
# 스타일: make buttons larger
# =========================
st.markdown(
    """
    <style>
    /* make Streamlit buttons larger and increase font size */
    button[data-testid="stButton"] > div {
        min-height: 56px;
        font-size: 20px;
        padding: 10px 12px;
    }

    /* input box larger font */
    input[type="text"] {
        font-size: 18px !important;
    }

    /* reduce default padding around columns to make layout denser */
    .stApp .css-1d391kg { padding: 6px 8px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================
# 입력창
# =========================
# show the expression in a disabled text input (bigger font from css above)
st.text_input("계산식", value=st.session_state.expr, disabled=True, key="display")

# =========================
# 액션 콜백
# =========================
def add(x):
    st.session_state.expr += str(x)

def delete():
    st.session_state.expr = st.session_state.expr[:-1]

def clear():
    st.session_state.expr = ""
    st.session_state.result = None

# =========================
# 버튼 레이아웃 (키패드)
# Use on_click callbacks which are slightly more efficient than testing return values.
# =========================
st.write("---")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.button("7", key="b7", on_click=add, args=("7",))
    st.button("4", key="b4", on_click=add, args=("4",))
    st.button("1", key="b1", on_click=add, args=("1",))
    st.button("0", key="b0", on_click=add, args=("0",))

with c2:
    st.button("8", key="b8", on_click=add, args=("8",))
    st.button("5", key="b5", on_click=add, args=("5",))
    st.button("2", key="b2", on_click=add, args=("2",))
    st.button(".", key="bdot", on_click=add, args=(".",))

with c3:
    st.button("9", key="b9", on_click=add, args=("9",))
    st.button("6", key="b6", on_click=add, args=("6",))
    st.button("3", key="b3", on_click=add, args=("3",))
    st.button("pi", key="bpi", on_click=add, args=("pi",))

with c4:
    st.button("+", key="bplus", on_click=add, args=("+",))
    st.button("-", key="bminus", on_click=add, args=("-",))
    st.button("*", key="bmul", on_click=add, args=("*",))
    st.button("/", key="bdiv", on_click=add, args=("/",))

# extra row: trig / constants / delete / clear
st.write("---")

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.button("sin", key="bsin", on_click=add, args=("sin(",))
with c2:
    st.button("cos", key="bcos", on_click=add, args=("cos(",))
with c3:
    st.button("tan", key="btan", on_click=add, args=("tan(",))
with c4:
    st.button("e", key="be", on_click=add, args=("e",))

# delete / clear buttons (large and prominent)
c1, c2, c3 = st.columns([1,1,2])
with c1:
    st.button("DEL", key="bdel", on_click=delete)
with c2:
    st.button("C", key="bclear", on_click=clear)
with c3:
    # evaluate button spans two columns visually
    if st.button("= 계산", key="beval"):
        try:
            result = eval(
                st.session_state.expr,
                {"__builtins__": None},
                safe_dict,
            )
            st.session_state.result = result
            st.success(f"결과: {result}")
        except Exception as e:
            st.error(e)

st.write("---")

# =========================
# 그래프
# =========================
st.subheader("📈 함수 그래프")

func = st.text_input("함수 입력 (예: sin(x), x**2, cos(x))", "sin(x)", key="fexpr")

xmin = st.number_input("x 최소", value=-10.0, key="xmin")
xmax = st.number_input("x 최대", value=10.0, key="xmax")
points = st.slider("샘플 포인트 수", 100, 2000, 1000, step=100)

# cache the heavy computation to reduce lag on unrelated interactions
@st.cache_data
def compute_xy(func_str: str, xmin: float, xmax: float, points: int):
    x = np.linspace(xmin, xmax, points)
    safe_graph = {
        "x": x,
        "pi": np.pi,
        "e": np.e,
        # use numpy trig (works elementwise)
        "sin": np.sin,
        "cos": np.cos,
        "tan": np.tan,
    }
    # evaluate once and return arrays
    y = eval(func_str, {"__builtins__": None}, safe_graph)
    return x, y

if st.button("그래프 그리기", key="bplot"):
    try:
        x, y = compute_xy(func, xmin, xmax, points)

        fig, ax = plt.subplots()
        ax.plot(x, y)
        ax.axhline(0, color="black")
        ax.axvline(0, color="black")
        ax.grid(True)

        st.pyplot(fig)

    except Exception as e:
        st.error(f"그래프 오류: {e}")
