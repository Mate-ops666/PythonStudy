import json
import random
import string

import streamlit as st
import streamlit.components.v1 as components

st.title("网页版密码生成器")

length = st.slider("密码长度", min_value=8, max_value=32, value=10)
required_chars = st.text_input("必须包含的特定字符")

if "password" not in st.session_state:
    st.session_state.password = ""


def generate_password(password_length: int, required: str) -> str:
    alphabet = string.ascii_letters + string.digits + string.punctuation
    rng = random.SystemRandom()

    required_list = list(required)
    remaining = password_length - len(required_list)
    extra_chars = [rng.choice(alphabet) for _ in range(remaining)]
    password_chars = required_list + extra_chars
    rng.shuffle(password_chars)
    return "".join(password_chars)


def render_copy_button(text: str) -> None:
    payload = json.dumps(text)
    components.html(
        f"""
        <button id="copy-btn" style="
            background-color:#ff4b4b;
            color:white;
            border:none;
            border-radius:0.5rem;
            padding:0.45rem 0.9rem;
            cursor:pointer;
            font-size:0.9rem;
        ">一键复制</button>
        <script>
        const btn = document.getElementById("copy-btn");
        const text = {payload};
        btn.addEventListener("click", () => {{
            const ta = document.createElement("textarea");
            ta.value = text;
            document.body.appendChild(ta);
            ta.select();
            document.execCommand("copy");
            document.body.removeChild(ta);
            btn.innerText = "已复制";
            setTimeout(() => {{ btn.innerText = "一键复制"; }}, 1500);
        }});
        </script>
        """,
        height=48,
    )


if st.button("生成强密码"):
    if len(required_chars) > length:
        st.error(f"必须包含的字符数量（{len(required_chars)}）不能超过密码长度（{length}）。")
    else:
        st.session_state.password = generate_password(length, required_chars)

if st.session_state.password:
    st.success(f"随机强密码：`{st.session_state.password}`")
    render_copy_button(st.session_state.password)
